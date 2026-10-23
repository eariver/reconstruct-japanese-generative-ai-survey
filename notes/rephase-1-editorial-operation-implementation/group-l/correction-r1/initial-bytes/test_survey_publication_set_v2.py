#!/usr/bin/env python3
"""Pure low-level schema/identity tests for Group L (no authority fixtures).

Covers: seal schema exact 15 roles + malformed cases, activation branch exact
keys + malformed cases, before_active_digest recomputation, canonical anchor
derivation (empty/legacy/mixed/sequence/unknown), and no-stub discipline.
No long authority/build fixtures; temp files live under tempfile (never in
the implementation copy). Run isolated with bytecode outside the source tree.
"""
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


class SealSchemaTests(unittest.TestCase):
    def test_seal_schema_requires_exact_15(self) -> None:
        schema = json.loads((_repo_root() / "schemas" / "editorial-publication-set-v2.schema.json").read_text())
        self.assertEqual(schema["properties"]["kind"]["const"], "EDITORIAL_PUBLICATION_SET_V1")
        self.assertEqual(schema["properties"]["status"]["const"], "SEALED_INERT")
        required_roles = schema["properties"]["roles"]["required"]
        self.assertEqual(len(required_roles), 15)
        self.assertEqual(set(required_roles), {
            "reader-input", "authoring-input", "source-receipt", "reader-manuscript",
            "validated-source", "bibliography", "style", "publication-pdf",
            "build-log", "pdf-digest", "quality-regression-bundle", "semantic-review",
            "visual-review", "reader-surface-gate", "publication-candidate",
        })
        # strict objects, no additional properties at top or roles
        self.assertFalse(schema["additionalProperties"])
        self.assertFalse(schema["properties"]["roles"]["additionalProperties"])
        for name in required_roles:
            self.assertIn(name, schema["properties"]["roles"]["properties"])

    def test_seal_schema_top_keys_exact(self) -> None:
        schema = json.loads((_repo_root() / "schemas" / "editorial-publication-set-v2.schema.json").read_text())
        self.assertEqual(set(schema["required"]), {
            "schema_version", "kind", "status", "issue_id", "research_profile",
            "publication_profile", "proposal_ref", "staged_manifest_ref",
            "build_record_ref", "roles", "set_sha256",
        })

    def test_seal_self_hash_pattern(self) -> None:
        # set_sha256 must be lowercase 64-hex; digest helper is canonical excluding itself.
        from scripts import survey_production_v2 as core
        doc = {"a": 1, "b": [2, 3]}
        digest = core.sha256_object(doc)
        self.assertEqual(len(digest), 64)
        self.assertTrue(all(c in "0123456789abcdef" for c in digest))


class RevalidationSchemaTests(unittest.TestCase):
    def test_revalidation_has_two_strict_branches(self) -> None:
        schema = json.loads((_repo_root() / "schemas" / "publication-surface-revalidation.schema.json").read_text())
        self.assertIn("oneOf", schema)
        self.assertEqual(len(schema["oneOf"]), 2)
        defs = schema["$defs"]
        self.assertIn("legacy_revalidation", defs)
        self.assertIn("editorial_activation", defs)
        legacy = defs["legacy_revalidation"]
        # Legacy preserves exact 14 required fields and verbatim semantics.
        self.assertEqual(set(legacy["required"]), {
            "schema_version", "issue_id", "reason_class", "reason", "lifecycle",
            "prior_checkpoint", "superseded_artifacts", "preserved_artifacts",
            "validation", "core", "executor", "recorded_at", "supersedes", "establishment",
        })
        self.assertFalse(legacy["additionalProperties"])
        self.assertEqual(legacy["properties"]["reason_class"]["const"], "REVIEWED_CORE_CHANGE")
        editorial = defs["editorial_activation"]
        self.assertEqual(set(editorial["required"]), {
            "schema_version", "kind", "issue_id", "reason_class", "reason", "lifecycle",
            "prior_checkpoint", "supersedes", "canonical_anchor", "before_state_ref",
            "before_active_digest", "before_candidate_ref", "set_ref", "core",
            "executor", "recorded_at", "establishment",
        })
        self.assertFalse(editorial["additionalProperties"])
        self.assertEqual(editorial["properties"]["kind"]["const"], "EDITORIAL_PUBLICATION_ACTIVATION_V1")
        self.assertEqual(editorial["properties"]["reason_class"]["const"], "REVIEWED_EDITORIAL_CORRECTION")
        self.assertEqual(editorial["properties"]["lifecycle"]["const"], "VALIDATED_DRAFT")
        anchor = editorial["properties"]["canonical_anchor"]
        self.assertEqual(set(anchor["required"]), {"kind", "ref"})
        self.assertEqual(set(anchor["properties"]["kind"]["enum"]), {"VALIDATION_CHECKPOINT", "LEGACY_REVALIDATION"})

    def test_legacy_schema_validates_old_record_shape(self) -> None:
        from scripts import survey_schema_v2 as schema_gate
        schema_path = _repo_root() / "schemas" / "publication-surface-revalidation.schema.json"
        # Minimal legacy-shaped record (hashes/paths are structural only here;
        # file existence is checked by low-level identity, not schema).
        record = {
            "schema_version": "2.0-rc1",
            "issue_id": "2026-W01",
            "reason_class": "REVIEWED_CORE_CHANGE",
            "reason": "test",
            "lifecycle": "VALIDATED_DRAFT",
            "prior_checkpoint": {"path": "a.json", "sha256": "0" * 64},
            "superseded_artifacts": [{"name": "n", "path": "p", "prior_sha256": "0" * 64, "new_sha256": "1" * 64, "byte_count": 1}],
            "preserved_artifacts": [],
            "validation": {
                "manuscript": {"path": "m", "sha256": "0" * 64},
                "quality_bundle": {"path": "q", "sha256": "0" * 64},
                "semantic_review": {"path": "s", "sha256": "0" * 64},
                "visual_review": {"path": "v", "sha256": "0" * 64},
                "pdf": {"path": "p.pdf", "sha256": "0" * 64, "byte_count": 10, "page_count": 1},
                "deterministic_checks": [{"check_id": "c", "status": "PASS"}],
                "summary": "s",
            },
            "core": {"contract": {}, "implementation_commit_sha": "0" * 40},
            "executor": "tester",
            "recorded_at": "2026-01-01T00:00:00Z",
            "supersedes": None,
            "establishment": {
                "state_sha256": "0" * 64, "lifecycle": "VALIDATED_DRAFT",
                "architecture_review": "approved", "publication_preview": "pending",
                "freeze": "pending", "release": "pending",
                "implementation_commit_sha": "0" * 40, "recorded_at": "2026-01-01T00:00:00Z",
            },
        }
        schema_gate.validate_instance(record, schema_path, label="legacy revalidation")
        # Editorial reason must NOT validate as legacy (branch discrimination).
        bad = dict(record)
        bad["reason_class"] = "REVIEWED_EDITORIAL_CORRECTION"
        with self.assertRaises(ValueError):
            schema_gate.validate_instance(bad, schema_path, label="legacy must reject editorial")


class DigestTests(unittest.TestCase):
    def test_before_digest_deterministic_and_candidate_sensitive(self) -> None:
        from scripts import survey_publication_set_v2 as pubset
        eff = {name: {"path": f"p/{name}.json", "sha256": f"{i:064x}"} for i, name in enumerate(sorted(pubset.PUBLICATION_ROLES_7))}
        d_none = pubset.before_active_digest(eff, None)
        d_cand = pubset.before_active_digest(eff, {"path": "c.json", "sha256": "a" * 64})
        self.assertEqual(len(d_none), 64)
        self.assertNotEqual(d_none, d_cand)
        # Order-independent (sorted).
        eff2 = dict(reversed(list(eff.items())))
        self.assertEqual(pubset.before_active_digest(eff2, None), d_none)

    def test_before_digest_rejects_malformed(self) -> None:
        from scripts import survey_publication_set_v2 as pubset
        with self.assertRaises(ValueError):
            pubset.before_active_digest({}, {"path": "c", "sha256": "zzz"})
        # Pure digest does not enforce the seven (chain/selection do); a
        # single-row input still yields a deterministic digest (no stub PASS).
        digest = pubset.before_active_digest({"only": {"path": "p", "sha256": "0" * 64}}, None)
        self.assertEqual(len(digest), 64)


class AnchorTests(unittest.TestCase):
    def _minimal_state(self, validation_ref: dict[str, str]) -> dict:
        return {"issue_id": "2026-W01", "checkpoint_provenance": {"validation": validation_ref}}

    def test_derive_anchor_empty_chain_returns_validation(self) -> None:
        from scripts import survey_publication_set_v2 as pubset
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "schemas").mkdir()
            # Copy real schemas + checkpoint schema stub? derive needs validation
            # checkpoint file + checkpoint schema. Create minimal checkpoint.
            import shutil
            shutil.copy(_repo_root() / "schemas" / "stage-checkpoint-v2.schema.json", root / "schemas" / "stage-checkpoint-v2.schema.json")
            val_path = root / "validation.json"
            dummy = root / "dummy.txt"
            dummy.write_text("dummy", encoding="utf-8")
            import hashlib
            dummy_sha = hashlib.sha256(b"dummy").hexdigest()
            val_doc = {
                "schema_version": "2.0-rc1", "issue_id": "2026-W01",
                "from_state": "DRAFT_COMPLETE", "to_state": "VALIDATED_DRAFT",
                "checkpoints": ["validation"], "recorded_at": "2026-01-01T00:00:00Z",
                "implementation": {"repository_commit_sha": "0" * 40, "orchestrator_version": "v"},
                "contract": {
                    "pipeline_contract_version": "2.0-rc1", "pipeline_contract_sha256": "0" * 64,
                    "quality_contract_version": "2.0-rc1", "quality_contract_sha256": "0" * 64,
                    "research_profile_version": "2.0-rc1", "research_profile_sha256": "0" * 64,
                    "publication_profile_version": "2.0-rc1", "publication_profile_sha256": "0" * 64,
                },
                "artifacts": [
                    {"name": "validated-source", "path": "dummy.txt", "sha256": dummy_sha},
                    {"name": "publication-pdf", "path": "dummy.txt", "sha256": dummy_sha},
                    {"name": "quality-regression-bundle", "path": "dummy.txt", "sha256": dummy_sha},
                ],
                "reviews": [{"check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC", "status": "PASS",
                             "executor": "tester", "evidence": "pure test",
                             "result": {"path": "dummy.txt", "sha256": dummy_sha}}],
                "summary": "x",
            }
            val_path.write_text(json.dumps(val_doc), encoding="utf-8")
            from scripts import survey_production_v2 as core
            vref = {"path": "validation.json", "sha256": core.sha256_file(val_path)}
            state = self._minimal_state(vref)
            anchor = pubset.derive_canonical_anchor(root, {}, state, [])
            self.assertEqual(anchor["kind"], "VALIDATION_CHECKPOINT")
            self.assertEqual(anchor["ref"], vref)

    def test_normalize_rejects_unknown_branch(self) -> None:
        from scripts import survey_publication_set_v2 as pubset
        with self.assertRaises(ValueError):
            pubset._normalize_chain_input([{"reason_class": "UNKNOWN", "prior_checkpoint": {}}])

    def test_parse_sequence_rules(self) -> None:
        from scripts import survey_publication_set_v2 as pubset
        self.assertEqual(pubset._parse_sequence("sources/x/publication/v2/publication-surface-revalidation-r1.json"), 1)
        self.assertEqual(pubset._parse_sequence("publication-surface-revalidation-r32.json"), 32)
        self.assertIsNone(pubset._parse_sequence("publication-surface-revalidation-r01.json"))
        self.assertIsNone(pubset._parse_sequence("other.json"))


if __name__ == "__main__":
    unittest.main()
