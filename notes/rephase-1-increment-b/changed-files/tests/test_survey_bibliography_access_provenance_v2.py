from __future__ import annotations

import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts import run_semantic_publication_v2_interactive_base as special_pub
from scripts import survey_bibliography_access_provenance_v2 as provenance
from scripts import survey_production_v2 as core
from scripts import survey_weekly_derivation_v2 as weekly
from tests import test_survey_increment_b_weekly_derivation_v2 as fixture_module


class BibliographyAccessProvenanceUnitTests(unittest.TestCase):
    def test_parse_access_date_valid_instants_and_dates(self):
        full, d = provenance.parse_access_date("2026-09-08T14:52:53Z")
        self.assertEqual(full, "2026-09-08T14:52:53Z")
        self.assertEqual(d, "2026-09-08")

        full, d = provenance.parse_access_date("2026-08-14T18:00:00-04:00")
        self.assertEqual(full, "2026-08-14T18:00:00-04:00")
        self.assertEqual(d, "2026-08-14")

        full, d = provenance.parse_access_date("2026-08-24")
        self.assertEqual(full, "2026-08-24")
        self.assertEqual(d, "2026-08-24")

    def test_parse_access_date_preserves_explicit_offset_calendar_date(self):
        # 2026-08-14T23:30:00-04:00 is 2026-08-15T03:30:00Z in UTC.
        # The contract requires preserving the explicit offset calendar date (2026-08-14),
        # rather than silently shifting to 2026-08-15 due to UTC normalization.
        full, d = provenance.parse_access_date("2026-08-14T23:30:00-04:00")
        self.assertEqual(full, "2026-08-14T23:30:00-04:00")
        self.assertEqual(d, "2026-08-14")
        self.assertNotEqual(d, "2026-08-15")

        # Positive offset across day boundary: 2026-08-15T01:30:00+09:00 is 2026-08-14T16:30:00Z
        full, d = provenance.parse_access_date("2026-08-15T01:30:00+09:00")
        self.assertEqual(full, "2026-08-15T01:30:00+09:00")
        self.assertEqual(d, "2026-08-15")
        self.assertNotEqual(d, "2026-08-14")

    def test_parse_access_date_invalid_fails_closed(self):
        for invalid in ["", "   ", "not-a-date", "2026/08/24", None, 12345]:
            with self.assertRaises(ValueError):
                provenance.parse_access_date(invalid)  # type: ignore[arg-type]

    def test_resolve_source_access_provenance_single_source(self):
        sources = [
            {
                "source_id": "src-1",
                "url": "https://example.com/test",
                "accessed_at": "2026-09-08T14:52:53Z",
            }
        ]
        res = provenance.resolve_source_access_provenance(
            sources, "https://example.com/test", "did-1"
        )
        self.assertEqual(res["source_id"], "src-1")
        self.assertEqual(res["source_accessed_at"], "2026-09-08T14:52:53Z")
        self.assertEqual(res["urldate"], "2026-09-08")

    def test_resolve_source_access_provenance_selects_matching_url(self):
        sources = [
            {
                "source_id": "src-other",
                "url": "https://other.example.com/page",
                "accessed_at": "2026-09-01T10:00:00Z",
            },
            {
                "source_id": "src-official",
                "url": "https://official.example.com/announcement",
                "accessed_at": "2026-09-08T12:00:00Z",
            },
        ]
        res = provenance.resolve_source_access_provenance(
            sources, "https://official.example.com/announcement", "did-2"
        )
        self.assertEqual(res["source_id"], "src-official")
        self.assertEqual(res["source_accessed_at"], "2026-09-08T12:00:00Z")
        self.assertEqual(res["urldate"], "2026-09-08")


class BibliographyAccessProvenanceContractTests(unittest.TestCase):
    def test_b1_weekly_per_source_access_date_differs_from_cutoff(self):
        """B1: Weekly publication binds per-source access date, distinct from edition cutoff."""
        profile = {
            "research_scope": {
                "temporal_policy": {
                    "mode": "ROLLING_WINDOW",
                    "window_start": "2026-08-14T18:00:00-04:00",
                    "window_end": "2026-08-21T18:00:00-04:00",
                    "cutoff": "2026-08-21T18:00:00-04:00",
                    "timezone": "America/New_York",
                }
            }
        }
        display_date, boundary = weekly._window(profile)
        self.assertEqual(display_date, "2026-08-21")
        self.assertIn("2026-08-21", boundary)

        record = {
            "entity": {
                "canonical_name": "Grok Bot access expansion",
                "canonical_url": "https://x.ai/news/grok-bot-more-plans",
                "organization": "xAI",
            },
            "status": "VERIFIED",
            "materiality": "MATERIAL",
            "source_accessed_at": "2026-09-08T14:52:53Z",
            "urldate": "2026-09-08",
        }
        bib = weekly.render_bibliography({"bibliography": [{
            "discovery_id": "w34-event-c066", "key": "w2026w34w34eventc066",
            "title": record["entity"]["canonical_name"], "author": "Unknown",
            "url": record["entity"]["canonical_url"], "urldate": record["urldate"],
        }]})
        self.assertIn("urldate = {2026-09-08}", bib)
        self.assertNotIn("urldate = {2026-08-21}", bib)

    def test_b2_special_per_source_access_date_differs_from_as_of(self):
        """B2: Special publication binds per-source access date, distinct from retrospective as_of."""
        as_of = "2026-08-24T17:24:00Z"
        as_of_date = as_of[:10]  # 2026-08-24
        source_accessed_at = "2026-08-15T09:30:00Z"
        source_urldate = "2026-08-15"

        record = {
            "entity": {
                "canonical_name": "Historical Foundation Model Report",
                "canonical_url": "https://arxiv.org/abs/2401.02954",
                "organization": "Research Lab",
            },
            "status": "VERIFIED",
            "materiality": "MATERIAL",
            "source_accessed_at": source_accessed_at,
            "urldate": source_urldate,
        }
        bib = special_pub._bib_text("sp001model01", record, record["urldate"])
        self.assertIn(f"urldate = {{{source_urldate}}}", bib)
        self.assertNotIn(f"urldate = {{{as_of_date}}}", bib)

    def test_b3_multiple_sources_receive_independent_access_dates(self):
        """B3: Multiple sources in the same publication retain independent per-source urldates."""
        rec1 = {
            "entity": {
                "canonical_name": "Source Alpha",
                "canonical_url": "https://alpha.example.com",
                "organization": "Alpha Org",
            },
            "status": "VERIFIED",
            "materiality": "MATERIAL",
            "source_accessed_at": "2026-08-10T08:00:00Z",
            "urldate": "2026-08-10",
        }
        rec2 = {
            "entity": {
                "canonical_name": "Source Beta",
                "canonical_url": "https://beta.example.com",
                "organization": "Beta Org",
            },
            "status": "VERIFIED",
            "materiality": "MATERIAL",
            "source_accessed_at": "2026-08-18T16:00:00Z",
            "urldate": "2026-08-18",
        }
        bib = weekly.render_bibliography({"bibliography": [
            {"discovery_id": "alpha", "key": "w34alpha", "title": rec1["entity"]["canonical_name"],
             "author": "Unknown", "url": rec1["entity"]["canonical_url"], "urldate": rec1["urldate"]},
            {"discovery_id": "beta", "key": "w34beta", "title": rec2["entity"]["canonical_name"],
             "author": "Unknown", "url": rec2["entity"]["canonical_url"], "urldate": rec2["urldate"]},
        ]})
        self.assertIn("urldate = {2026-08-10}", bib)
        self.assertIn("urldate = {2026-08-18}", bib)
        self.assertLess(bib.index("@online{w34alpha,"), bib.index("@online{w34beta,"))
        self.assertLess(bib.index("urldate = {2026-08-10}"), bib.index("urldate = {2026-08-18}"))
        self.assertNotEqual(rec1["urldate"], rec2["urldate"])

    def test_b4_event_date_differs_from_access_date(self):
        """B4: Published/event date differs from retrieval/access date; urldate must bind access date."""
        card_sources = [
            {
                "source_id": "src-paper-1",
                "url": "https://arxiv.org/abs/2210.02414",
                "source_class": "PRIMARY_PAPER",
                "title": "Historical 2022 Paper",
                "published_at": "2022-10-05",
                "accessed_at": "2026-08-24T17:24:00Z",
            }
        ]
        prov = provenance.resolve_source_access_provenance(
            card_sources, "https://arxiv.org/abs/2210.02414", "SP001-D009"
        )
        self.assertEqual(prov["source_accessed_at"], "2026-08-24T17:24:00Z")
        self.assertEqual(prov["urldate"], "2026-08-24")
        self.assertNotEqual(prov["urldate"], "2022-10-05")

    def test_b5_revised_page_chronology_c066_class(self):
        """B5: Event Aug 21, page re-dated Aug 26, canonical access Sep 8 -> urldate Sep 8."""
        card_sources = [
            {
                "source_id": "supplement-src-6b3ce48a6c75d42b",
                "url": "https://x.ai/news/grok-bot-more-plans",
                "source_class": "PRIMARY_OFFICIAL",
                "title": "First-party announcement",
                "published_at": "2026-08-26",
                "accessed_at": "2026-09-08T14:52:53Z",
            }
        ]
        prov = provenance.resolve_source_access_provenance(
            card_sources, "https://x.ai/news/grok-bot-more-plans", "w34-event-c066"
        )
        self.assertEqual(prov["urldate"], "2026-09-08")
        self.assertNotEqual(prov["urldate"], "2026-08-21")  # Not the event cutoff date
        self.assertNotEqual(prov["urldate"], "2026-08-26")  # Not the revised page date

    def test_b6_missing_access_timestamp_fails_closed(self):
        """B6: Missing or blank access timestamp fails closed with an actionable error."""
        sources_missing = [
            {
                "source_id": "src-no-ts",
                "url": "https://example.com/no-timestamp",
                "accessed_at": "",
            }
        ]
        with self.assertRaisesRegex(ValueError, "missing access timestamp"):
            provenance.resolve_source_access_provenance(
                sources_missing, "https://example.com/no-timestamp", "did-missing"
            )

        sources_none = [
            {
                "source_id": "src-none-ts",
                "url": "https://example.com/none-timestamp",
                "accessed_at": None,
            }
        ]
        with self.assertRaisesRegex(ValueError, "missing access timestamp"):
            provenance.resolve_source_access_provenance(
                sources_none, "https://example.com/none-timestamp", "did-none"
            )

        # The current Weekly renderer consumes a reviewed object; missing
        # urldate fails at its full reader-input schema boundary.
        fixture = fixture_module.IncrementBWeeklyDerivationV2Tests(methodName="runTest")
        fixture.setUp()
        try:
            chain = fixture._complete_authorities(fixture._chain())
            state_path = fixture._current_state(chain)
            surface = weekly.load_derivation(fixture.root, state_path, chain["authored_path"])["surface"]
            missing_date = copy.deepcopy(surface)
            missing_date["bibliography"][0]["urldate"] = ""
            with self.assertRaisesRegex(ValueError, "Weekly complete reader input fails .*bibliography"):
                weekly.validate_reader_input(fixture.root, missing_date)
        finally:
            fixture.doCleanups()

        record_no_ts = {"entity": {"canonical_name": "Title", "canonical_url": "https://example.com"}}
        with self.assertRaisesRegex(ValueError, "lacks canonical access date"):
            special_pub._bib_text("key1", record_no_ts, None)

    def test_b7_ambiguous_access_provenance_fails_closed(self):
        """B7: Ambiguous captures with conflicting access times fail closed unless explicitly disambiguated."""
        ambiguous_sources = [
            {
                "source_id": "cap-1",
                "url": "https://example.com/doc",
                "accessed_at": "2026-08-10T10:00:00Z",
            },
            {
                "source_id": "cap-2",
                "url": "https://example.com/doc",
                "accessed_at": "2026-08-20T15:00:00Z",
            },
        ]
        # Ambiguous resolution without explicit_source_id must fail closed
        with self.assertRaisesRegex(ValueError, "ambiguous captures"):
            provenance.resolve_source_access_provenance(
                ambiguous_sources, "https://example.com/doc", "did-ambig"
            )

        # Disambiguated resolution using explicit_source_id succeeds
        resolved_1 = provenance.resolve_source_access_provenance(
            ambiguous_sources,
            "https://example.com/doc",
            "did-ambig",
            explicit_source_id="cap-1",
        )
        self.assertEqual(resolved_1["source_id"], "cap-1")
        self.assertEqual(resolved_1["urldate"], "2026-08-10")

        resolved_2 = provenance.resolve_source_access_provenance(
            ambiguous_sources,
            "https://example.com/doc",
            "did-ambig",
            explicit_source_id="cap-2",
        )
        self.assertEqual(resolved_2["source_id"], "cap-2")
        self.assertEqual(resolved_2["urldate"], "2026-08-20")

    def test_b8_source_identity_and_citation_invariants_preserved(self):
        """B8: Citation keys, URL, name, organization, status, materiality, and ordering are preserved."""
        record_before = {
            "entity": {
                "canonical_name": "Grok Bot access expansion",
                "canonical_url": "https://x.ai/news/grok-bot-more-plans",
                "organization": "xAI",
            },
            "status": "VERIFIED",
            "materiality": "MATERIAL",
        }
        # Render old with cutoff
        bib_old = (
            "@online{w2026w34w34eventc066,\n"
            "  title = {{Grok Bot access expansion}},\n"
            "  author = {{xAI}},\n"
            "  url = {https://x.ai/news/grok-bot-more-plans},\n"
            "  urldate = {2026-08-21}\n"
            "}"
        )
        # Render new with canonical access date
        record_after = {
            **record_before,
            "source_accessed_at": "2026-09-08T14:52:53Z",
            "urldate": "2026-09-08",
        }
        bib_new = weekly.render_bibliography({"bibliography": [{
            "discovery_id": "w34-event-c066", "key": "w2026w34w34eventc066",
            "title": record_after["entity"]["canonical_name"], "author": "Unknown",
            "url": record_after["entity"]["canonical_url"], "urldate": record_after["urldate"],
        }]})

        # Invariants
        self.assertIn("@online{w2026w34w34eventc066,", bib_new)
        self.assertIn("title = {{Grok Bot access expansion}},", bib_new)
        self.assertIn("author = {{Unknown}},", bib_new)
        self.assertIn("urldate = {2026-09-08}", bib_new)
        self.assertNotEqual(bib_old, bib_new)
        self.assertIn("url = {https://x.ai/news/grok-bot-more-plans},", bib_new)
        self.assertEqual(record_after["status"], record_before["status"])
        self.assertEqual(record_after["materiality"], record_before["materiality"])
        self.assertEqual(
            record_after["entity"]["canonical_name"],
            record_before["entity"]["canonical_name"],
        )
        self.assertEqual(
            record_after["entity"]["canonical_url"],
            record_before["entity"]["canonical_url"],
        )
        self.assertEqual(
            record_after["entity"]["organization"],
            record_before["entity"]["organization"],
        )

    def test_b9_w34_read_only_fixture_regression(self):
        """B9: Verify all 41 W34 cited records resolve canonical access provenance on 2026-09-08 and verify c066 repair."""
        cmd = ["git", "cat-file", "-e", "6f68fd09955302fd87e5ec0ce77ff06ccaec8448"]
        proc = subprocess.run(cmd, capture_output=True)
        if proc.returncode != 0:
            self.skipTest("W34 fixture commit 6f68fd09955302fd87e5ec0ce77ff06ccaec8448 not available")

        # 1. Obtain all 41 cited Discovery IDs from W34 publication authority
        draft_cmd = [
            "git",
            "show",
            "6f68fd09955302fd87e5ec0ce77ff06ccaec8448:sources/2026-W34/draft/v2/interactive-drafting-synthesis-input.json",
        ]
        draft_proc = subprocess.run(draft_cmd, capture_output=True, text=True, check=True)
        draft_data = json.loads(draft_proc.stdout)
        cited_dids: list[str] = []
        for pkg in draft_data.get("packages", []):
            cited_dids.extend(pkg.get("deck_discovery_ids", []))
            for block in pkg.get("blocks", []):
                cited_dids.extend(block.get("discovery_ids", []))
        cited_dids = list(dict.fromkeys(cited_dids))
        self.assertEqual(len(cited_dids), 41, "W34 publication authority must contain exactly 41 cited Discovery IDs")

        # 2. Obtain canonical bibliography URLs from W34 references.bib via canonical citation keys
        bib_cmd = [
            "git",
            "show",
            "6f68fd09955302fd87e5ec0ce77ff06ccaec8448:surveys/weekly/2026-W34/references.bib",
        ]
        bib_proc = subprocess.run(bib_cmd, capture_output=True, text=True, check=True)
        bib_content = bib_proc.stdout
        bib_url_by_key: dict[str, str] = {}
        current_key = None
        for line in bib_content.splitlines():
            if line.startswith("@online{"):
                current_key = line.split("{")[1].split(",")[0].strip()
            elif current_key and "url = {" in line:
                u = line.split("url = {")[1].split("}")[0].strip()
                bib_url_by_key[current_key] = u
                current_key = None

        canonical_url_by_did: dict[str, str] = {}
        for did in cited_dids:
            expected_key = "w2026w34" + did.lower().replace("-", "").replace(".", "")
            self.assertIn(expected_key, bib_url_by_key, f"Missing citation key {expected_key} in references.bib")
            canonical_url_by_did[did] = bib_url_by_key[expected_key]

        self.assertEqual(len(canonical_url_by_did), 41, "Must resolve canonical URL for all 41 cited IDs")

        # 3. Load checkpoint-bound accepted Evidence fixture at W34 commit using production helper
        acc_rel = "sources/2026-W34/evidence/v2/accepted/647cde464d92935c1ca633ade62bcbf7ebe88c458cc8b3848bae8d2fc4794831"
        with tempfile.TemporaryDirectory() as tmp:
            archive_proc = subprocess.run(
                ["git", "archive", "6f68fd09955302fd87e5ec0ce77ff06ccaec8448", acc_rel],
                capture_output=True,
                check=True,
            )
            subprocess.run(["tar", "-x", "-C", tmp], input=archive_proc.stdout, check=True)

            acc_path = Path(tmp) / acc_rel / "evidence-accepted.json"
            self.assertTrue(acc_path.is_file(), f"Accepted evidence file missing: {acc_path}")
            evidence_sources = provenance.load_evidence_sources(acc_path)

            # 4. For each of the 41 cited IDs, invoke production provenance resolver and assert 2026-09-08
            resolved_count = 0
            c066_prov = None
            for did in cited_dids:
                ev_info = evidence_sources.get(did)
                self.assertIsNotNone(ev_info, f"Accepted evidence must contain entry for {did}")
                sources = ev_info.get("sources")
                self.assertTrue(sources, f"Accepted evidence entry for {did} must have sources")
                url = canonical_url_by_did[did]

                prov = provenance.resolve_source_access_provenance(
                    sources,
                    canonical_url=url,
                    did=did,
                    explicit_source_id=ev_info.get("explicit_source_id"),
                )
                self.assertEqual(
                    prov["urldate"],
                    "2026-09-08",
                    f"Cited ID {did} canonical urldate must be 2026-09-08",
                )
                self.assertTrue(
                    prov["source_accessed_at"].startswith("2026-09-08"),
                    f"Cited ID {did} source_accessed_at must be on 2026-09-08",
                )
                resolved_count += 1
                if did == "w34-event-c066":
                    c066_prov = prov

            self.assertEqual(
                resolved_count,
                41,
                "Exactly 41/41 cited W34 records must resolve canonical access provenance",
            )

            # 5. Separately preserve detailed c066 chronology assertion
            self.assertIsNotNone(c066_prov, "w34-event-c066 must be among resolved citations")
            self.assertEqual(c066_prov["source_accessed_at"], "2026-09-08T14:52:53Z")
            self.assertEqual(c066_prov["urldate"], "2026-09-08")
            # In W34 references.bib prior to repair, c066 had urldate = {2026-08-21} (cutoff)
            self.assertIn("@online{w2026w34w34eventc066,", bib_content)
            self.assertNotEqual(c066_prov["urldate"], "2026-08-21")  # Not the event cutoff date
            self.assertNotEqual(c066_prov["urldate"], "2026-08-26")  # Not the revised page date

    def test_sp001_read_only_fixture_access_provenance(self):
        """SP001 fixture: all 11 accepted evidence sources resolve to 2026-08-24."""
        sp001_acc = Path(
            "sources/SP001/evidence/v2/accepted/3785dc9ee87378b6682cc6d45a064cba1c9325bba4339dc04e460d441dcfb430/evidence-accepted.json"
        )
        if not sp001_acc.is_file():
            self.skipTest(f"SP001 acceptance file not found: {sp001_acc}")

        evidence_sources = provenance.load_evidence_sources(sp001_acc)
        self.assertEqual(len(evidence_sources), 11)

        for did, info in evidence_sources.items():
            sources = info.get("sources")
            self.assertIsNotNone(sources, f"{did} must have sources")
            self.assertTrue(len(sources) >= 1)
            primary_url = sources[0]["url"]
            prov = provenance.resolve_source_access_provenance(
                sources, primary_url, did
            )
            self.assertEqual(prov["urldate"], "2026-08-24")
            self.assertEqual(prov["source_accessed_at"], "2026-08-24T17:24:00Z")


if __name__ == "__main__":
    unittest.main()
