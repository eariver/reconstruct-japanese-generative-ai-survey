#!/usr/bin/env python3
"""DM021-P1 read-only editorial-correction proposal validator (preparatory).

No writes, no approval, no reason enum, no State adoption, no CLI, no PASS
generation. Two entry points:

  prepare_proposal(root, state_path, authoring_path, proposal_id)
      Read-only current-before validation plus real proposed derivation from a
      new publication-authored input. Returns the prospective proposal, the
      independently derived canonical proposed-reader bytes and mechanical
      binding data in memory. The proposed reader FILE need not exist yet.

  validate_proposal(root, state_path, proposal_path, scope_review_path=None)
      Re-derives before/proposal from actual named FILE bytes, compares exact
      canonical proposed-reader bytes and all bindings/plan rows, and
      optionally binds the existing independent scope review. Returns a typed
      deterministic result (REVIEW_REQUIRED or REVIEW_BOUND_PROPOSAL) plus
      input hashes. Never a Reader-Surface PASS, Gate or revalidation record.

All refusals raise ProposalError (a ValueError) with a machine-readable code
prefix. Entry snapshots (consumed-file bytes, full source/survey trees, HEAD,
config) are rechecked before return; any mid-call drift refuses.
"""
from __future__ import annotations

import json
import os
import re
import stat as _stat
from pathlib import Path
from typing import Any

from scripts import survey_agent_control_v2 as agent
from scripts import survey_longform_derivation_v2 as longform_derivation
from scripts import survey_longform_generated_v2 as longform_generated
from scripts import survey_production_v2 as core
from scripts import survey_publication_v2 as publication
from scripts import survey_quality_v2 as quality
from scripts import survey_reader_publication_v2 as reader
from scripts import survey_reader_surface_gate_v2 as surface_gate
from scripts import survey_schema_v2 as schema_gate
from scripts import survey_weekly_derivation_v2 as weekly

PROPOSAL_SCHEMA = Path("schemas/editorial-correction-proposal-v2.schema.json")
PROPOSAL_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
PROPOSAL_FILES = ("authoring-input.json", "reader-surface-input-v2.json", "proposal.json")
SCOPE_VERSION = "EDITORIAL_CORRECTION_SCOPE_V1"
SCOPE_CHECK_ID = "EDITORIAL_CORRECTION_SCOPE"
RESULT_REQUIRED = "REVIEW_REQUIRED"
RESULT_BOUND = "REVIEW_BOUND_PROPOSAL"

LONGFORM_ROUTE = "LONGFORM_SPECIAL"
WEEKLY_ROUTE = "WEEKLY_MAGAZINE"

# Accepted/authored ref names constituting frozen research/Architecture authority.
FROZEN_REF_PREFIXES = (
    "production-profile",
    "issue-architecture",
    "synthesis-",
    "draft-",
    "drafting-authored-archive",
    "drafting-archive",
    "publication-semantic-input",
    "publication-authored-input",
    "evidence-",
    "edition-views-",
    "discovery-",
    "screening-",
    "candidate-",
    "selection",
    "materiality-",
    "profile-completeness",
)


class ProposalError(ValueError):
    """Typed read-only refusal. Message starts with a CODE: prefix."""


def _fail(code: str, detail: str) -> ProposalError:
    return ProposalError(f"{code}: {detail}")


class _Collector:
    """Pins every directly consumed file's bytes; reverify() proves stability."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.files: dict[str, bytes] = {}
        self.head = core.repository_commit_sha(root)
        self.config_sha = core.sha256_file(root / core.DEFAULT_CONFIG)

    def rel(self, path: Path) -> str:
        return path.resolve().relative_to(self.root).as_posix()

    def safe(self, value: str | Path, label: str) -> Path:
        """Repo-local regular non-symlink file; pins bytes on read."""
        raw = value.as_posix() if isinstance(value, Path) else str(value)
        lexical = value if (isinstance(value, Path) and value.is_absolute()) else (self.root / raw)
        if lexical.is_symlink():
            raise _fail("PATH_ALIAS", f"{label} is a symlink: {raw}")
        candidate = lexical.resolve()
        try:
            rel = candidate.relative_to(self.root).as_posix()
        except ValueError:
            raise _fail("PATH_NOT_REPO_LOCAL", f"{label} escapes repository: {raw}") from None
        if ".." in Path(rel).parts:
            raise _fail("PATH_TRAVERSAL", f"{label} contains dotdot: {raw}")
        if candidate.is_symlink():
            raise _fail("PATH_ALIAS", f"{label} resolves through a symlink: {rel}")
        if not candidate.is_file():
            raise _fail("PATH_MISSING", f"{label} missing: {rel}")
        if not _stat.S_ISREG(candidate.lstat().st_mode):
            raise _fail("PATH_NOT_REGULAR", f"{label} not a regular file: {rel}")
        data = candidate.read_bytes()
        previous = self.files.get(rel)
        if previous is not None and previous != data:
            raise _fail("STABILITY_VIOLATION", f"{label} changed mid-inspection: {rel}")
        self.files[rel] = data
        return candidate

    def pinned(self, ref: dict[str, Any], label: str) -> str:
        """Pin a {path,sha256} record against live bytes; return repo rel path."""
        if not isinstance(ref, dict) or set(ref) != {"path", "sha256"}:
            raise _fail("REF_SHAPE", f"{label} is not an exact {{path,sha256}} record")
        live = self.safe(ref["path"], label)
        rel = self.rel(live)
        if core.sha256_bytes(self.files[rel]) != ref["sha256"]:
            raise _fail("REF_DRIFT", f"{label} bytes differ from recorded sha256: {rel}")
        return rel

    def reverify(self) -> None:
        for rel, data in self.files.items():
            if (self.root / rel).read_bytes() != data:
                raise _fail("STABILITY_VIOLATION", f"consumed file changed: {rel}")
        if core.repository_commit_sha(self.root) != self.head:
            raise _fail("HEAD_MOVED", "repository HEAD changed during inspection")
        if core.sha256_file(self.root / core.DEFAULT_CONFIG) != self.config_sha:
            raise _fail("CONFIG_DRIFT", "implementation config changed during inspection")


def _tree_map(root: Path, source_root: Path, survey_root: Path) -> dict[str, str]:
    """Full byte map of the two edition trees (regular files only, .git excluded)."""
    result: dict[str, str] = {}
    for base in (source_root.resolve(), survey_root.resolve()):
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d != ".git"]
            for name in filenames:
                full = Path(dirpath) / name
                rel = full.resolve().relative_to(root.resolve()).as_posix()
                if full.is_symlink():
                    raise _fail("TREE_ALIAS", f"symlink inside edition tree: {rel}")
                result[rel] = core.sha256_file(full)
    return result


def _check_proposal_id(proposal_id: str) -> None:
    if not isinstance(proposal_id, str) or not PROPOSAL_ID_RE.match(proposal_id):
        raise _fail("BAD_PROPOSAL_ID", f"proposal_id must match {PROPOSAL_ID_RE.pattern}")


def _eligibility(state: dict[str, Any]) -> None:
    problems: list[str] = []
    if state.get("lifecycle_state") != "VALIDATED_DRAFT":
        problems.append("requires healthy VALIDATED_DRAFT")
    if state.get("human_gates", {}).get("architecture_review") != "approved":
        problems.append("requires approved Architecture Review")
    if state.get("human_gates", {}).get("publication_preview") != "pending" or \
            state.get("human_gate_provenance", {}).get("publication_preview") is not None:
        problems.append("forbids Publication Preview decision/provenance")
    if any(state.get("machine_checkpoints", {}).get(n) != "pending"
           for n in ("publication_preview", "freeze", "release")):
        problems.append("forbids resolved downstream checkpoint")
    if state.get("exception_gate", {}).get("status") != "inactive":
        problems.append("forbids active Exception Gate")
    if problems:
        raise _fail("INELIGIBLE_STATE", "; ".join(problems))


def _route_of(profile: dict[str, Any]) -> str:
    if profile.get("research_profile") == "THEMATIC" and \
            profile.get("publication_profile") == "LONGFORM_SPECIAL":
        return LONGFORM_ROUTE
    if profile.get("research_profile") == "WEEKLY" and \
            profile.get("publication_profile") == WEEKLY_ROUTE:
        return WEEKLY_ROUTE
    raise _fail("UNSUPPORTED_ROUTE", "P1 supports THEMATIC/LONGFORM_SPECIAL and WEEKLY/WEEKLY_MAGAZINE only")


def _original_checkpoint(col: _Collector, root: Path,
                         state: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, str]]]:
    ref = (state.get("checkpoint_provenance") or {}).get("validation")
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256"}:
        raise _fail("ORIGINAL_REF_INVALID", "State lacks exact validation checkpoint reference")
    record_path = col.safe(ref["path"], "original validation checkpoint")
    if core.sha256_bytes(col.files[col.rel(record_path)]) != ref["sha256"]:
        raise _fail("ORIGINAL_CHECKPOINT_DRIFT", "original checkpoint bytes differ from State pin")
    record = schema_gate.load_and_validate_json(record_path, root / agent.CHECKPOINT_SCHEMA,
                                                label="original validation checkpoint")
    if record.get("issue_id") != state.get("issue_id") or \
            record.get("from_state") != "DRAFT_COMPLETE" or \
            record.get("to_state") != "VALIDATED_DRAFT" or \
            "validation" not in record.get("checkpoints", []):
        raise _fail("ORIGINAL_IDENTITY_MISMATCH", "original checkpoint identity/producer mismatch")
    rows = record.get("artifacts", [])
    names = [row.get("name") for row in rows]
    if len(set(names)) != len(names):
        raise _fail("ORIGINAL_DUPLICATE_ROLE", "original checkpoint has duplicate artifact roles")
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"name", "path", "sha256"}:
            raise _fail("ORIGINAL_ROW_SHAPE", f"original row fields invalid: {row.get('name')}")
    return record, rows


def _active_effective(col: _Collector, root: Path, cfg: dict[str, Any], state: dict[str, Any],
                      original_rows: list[dict[str, str]]) -> tuple[dict[str, Any], dict[str, Any] | None]:
    record, errors = agent.resolve_active_publication_revalidation(root, cfg, state)
    if errors:
        raise _fail("ACTIVE_RECORD_INVALID", "; ".join(errors))
    if record is None:
        effective: dict[str, Any] = {}
        for row in original_rows:
            rel = col.pinned({"path": row["path"], "sha256": row["sha256"]},
                             f"active-before artifact {row['name']}")
            effective[row["name"]] = {"path": rel, "sha256": row["sha256"], "origin": "ORIGINAL"}
        return effective, None
    superseded = {row["name"]: row for row in record.get("superseded_artifacts", [])}
    preserved = {row["name"]: row for row in record.get("preserved_artifacts", [])}
    prior_names = {row["name"] for row in original_rows}
    if set(superseded) | set(preserved) != prior_names or set(superseded) & set(preserved):
        raise _fail("ACTIVE_ROW_MISMATCH", "active record rows do not cover original roles exactly once")
    effective = {}
    for row in original_rows:
        name = row["name"]
        other = superseded.get(name) or preserved.get(name)
        if row["path"] != other["path"]:
            raise _fail("ACTIVE_PATH_REBIND", f"{name} path rebound by active record")
        live = col.safe(row["path"], f"active-before artifact {name}")
        current = core.sha256_bytes(col.files[col.rel(live)])
        if name in superseded:
            if current != superseded[name]["new_sha256"]:
                raise _fail("ACTIVE_SUPERSEDED_DRIFT", f"{name} differs from active record adoption")
        elif current != preserved[name]["sha256"]:
            raise _fail("ACTIVE_PRESERVED_DRIFT", f"{name} differs from active record pin")
        effective[name] = {"path": col.rel(live), "sha256": current, "origin": "ACTIVE"}
    return effective, record


def _load_profile(col: _Collector, state: dict[str, Any]) -> dict[str, Any]:
    profile_path = col.safe(state["profile"]["path"], "Production Profile")
    profile = core.load_json(profile_path)
    if profile.get("issue_id") != state.get("issue_id"):
        raise _fail("PROFILE_ISSUE_MISMATCH", "Production Profile/State issue identity mismatch")
    return profile


def _derive(col: _Collector, root: Path, route: str, state_path: Path,
            authored_value: str | Path) -> dict[str, Any]:
    authored = col.safe(authored_value, "publication-authored input")
    try:
        if route == LONGFORM_ROUTE:
            context = longform_derivation.load_derivation_for_readback(root, state_path, authored)
        else:
            context = weekly.load_derivation(root, state_path, authored)
    except ValueError as exc:
        raise _fail("DERIVATION_REFUSED", str(exc)) from exc
    for key in ("surface", "accepted_refs", "archive_path", "authored_path", "profile", "state"):
        if key not in context:
            raise _fail("DERIVATION_CONTEXT_SHAPE", f"route loader omitted context key: {key}")
    col.safe(context["archive_path"], "bound drafting archive")
    return context


def _canonical(route: str, surface: dict[str, Any]) -> bytes:
    if route == LONGFORM_ROUTE:
        return longform_derivation.canonical_reader_bytes(surface)
    return core.json_bytes(surface)


class _Graph:
    def __init__(self) -> None:
        self.nodes: dict[str, dict[str, Any]] = {}
        self.edges: set[tuple[str, str, str, str]] = set()

    def node(self, path: str, sha256: str, byte_count: int, role: str, policy: str) -> None:
        node = self.nodes.get(path)
        if node is None:
            self.nodes[path] = {"path": path, "sha256": sha256, "byte_count": byte_count,
                                "roles": [role], "policy": policy}
            return
        if node["sha256"] != sha256 or node["byte_count"] != byte_count:
            raise _fail("HASH_CONFLICT", f"contradictory bytes for one path: {path}")
        if node["policy"] != policy:
            raise _fail("POLICY_CONFLICT", f"KEEP vs COPY classification for one path: {path}")
        if role not in node["roles"]:
            node["roles"].append(role)

    def edge(self, from_path: str, edge_type: str, to_path: str, to_sha256: str) -> None:
        self.edges.add((from_path, edge_type, to_path, to_sha256))

    def canonical(self) -> dict[str, Any]:
        nodes = [{"path": p, "sha256": n["sha256"], "byte_count": n["byte_count"],
                  "roles": sorted(n["roles"]), "policy": n["policy"]}
                 for p, n in sorted(self.nodes.items())]
        edges = [{"from_path": f, "edge_type": t, "to_path": p, "to_sha256": s}
                 for f, t, p, s in sorted(self.edges)]
        return {"nodes": nodes, "edges": edges}


def _frozen_kind(name: str) -> str | None:
    for prefix in FROZEN_REF_PREFIXES:
        if name == prefix or name.startswith(prefix):
            return name
    return None


def _frozen_member_kind(roles: list[str]) -> str | None:
    """Frozen-upstream membership: exact selection-mandated authority only.

    Frozen: receipt accepted/authored refs, upstream approval dependencies,
    manuscript profile/architecture/approval. Never mutable outputs
    (manuscript primary-source, supports, tool closures, QA results).
    """
    for role in roles:
        head, _, tail = role.partition(":")
        if head in ("receipt:accepted", "receipt:authored", "upstream"):
            return tail
        if role == "manuscript:profile":
            return "production-profile"
        if role == "manuscript:architecture":
            return "issue-architecture"
        if role == "manuscript:approval":
            return "architecture-approval"
    return None


def _build_graph(col: _Collector, root: Path, state: dict[str, Any],
                 original_rows: list[dict[str, str]], effective: dict[str, Any],
                 active_record: dict[str, Any] | None, receipt: dict[str, Any],
                 receipt_rel: str, gate_record: dict[str, Any], manuscript: dict[str, Any],
                 bundle: dict[str, Any], pretex: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, str]]]:
    graph = _Graph()

    mutable = {info["path"] for name, info in effective.items()
               if name not in ("semantic-review", "visual-review")}
    mutable |= {output["path"] for output in (receipt.get("outputs") or {}).values()
                if isinstance(output, dict) and "path" in output}
    mutable.add(receipt_rel)
    mutable.add(receipt["reviewed_reader_input"]["path"])
    for check in bundle.get("checks", []):
        result = (check or {}).get("result") or {}
        if isinstance(result, dict) and "path" in result:
            mutable.add(result["path"])

    def _pol(rel: str) -> str:
        """Single deterministic policy: mutable publication bytes COPY, else KEEP."""
        return "COPY_BEFORE_REPLACEMENT" if rel in mutable else "KEEP_IMMUTABLE"

    def _add_file(ref: dict[str, Any], role: str, label: str) -> str:
        if not isinstance(ref, dict) or "path" not in ref or "sha256" not in ref:
            raise _fail("REF_SHAPE", f"{label} lacks path/sha256 binding")
        rel = col.pinned({"path": ref["path"], "sha256": ref["sha256"]}, label)
        graph.node(rel, ref["sha256"], len(col.files[rel]), role, _pol(rel))
        return rel

    for row in original_rows:
        info = effective[row["name"]]
        graph.node(info["path"], info["sha256"], len(col.files[info["path"]]),
                   f"checkpoint-row:{row['name']}", _pol(info["path"]))
    checkpoint_ref = (state.get("checkpoint_provenance") or {})["validation"]
    checkpoint_rel = col.pinned(checkpoint_ref, "original checkpoint file")
    graph.node(checkpoint_rel, checkpoint_ref["sha256"], len(col.files[checkpoint_rel]),
               "checkpoint:original-record", _pol(checkpoint_rel))
    for row in original_rows:
        graph.edge(checkpoint_rel, f"CHECKPOINT_ROW {row['name']}",
                   effective[row["name"]]["path"], effective[row["name"]]["sha256"])
    if active_record is not None:
        pointer = state.get("publication_revalidation_provenance") or {}
        active_rel = col.pinned(pointer, "active revalidation record")
        graph.node(active_rel, pointer["sha256"], len(col.files[active_rel]),
                   "revalidation:active-record", _pol(active_rel))
        graph.edge(checkpoint_rel, "PREDECESSOR_CHAIN active", active_rel, pointer["sha256"])

    manuscript_path = effective["reader-manuscript"]["path"]
    for key, role in (("production_profile", "manuscript:profile"),
                      ("architecture", "manuscript:architecture"),
                      ("architecture_approval", "manuscript:approval"),
                      ("primary_source", "manuscript:primary-source")):
        ref = manuscript.get(key)
        rel = _add_file(ref, role, f"manuscript {key}")
        graph.edge(manuscript_path, f"MANUSCRIPT_SUPPORT {key}", rel, ref["sha256"])
    for support in manuscript.get("supporting_files", []):
        rel = _add_file(support, f"manuscript:support:{support.get('role')}",
                        f"manuscript support {support.get('role')}")
        graph.edge(manuscript_path, f"MANUSCRIPT_SUPPORT {support['role']}", rel, support["sha256"])

    approval = core.load_json(col.safe(manuscript["architecture_approval"]["path"], "typed approval"))
    arch_dir = str(Path(manuscript["architecture"]["path"]).parent)
    for filename, field in (("architecture-review-summary-v2.json", "architecture_review_summary_sha256"),
                            ("architecture-review-attention-v2.json", "architecture_review_attention_sha256")):
        candidate = (Path(arch_dir) / filename).as_posix()
        rel = _add_file({"path": candidate, "sha256": approval.get(field, "")},
                        f"upstream:{filename}", f"architecture {filename}")
        graph.edge(manuscript["architecture_approval"]["path"], f"APPROVAL_DEPENDENCY {filename}",
                   rel, approval[field])

    gate_path = effective["reader-surface-gate"]["path"]
    derivation = gate_record.get("derivation") or {}
    receipt_ref = derivation.get("receipt") or {}
    if receipt_ref.get("path") != receipt_rel or \
            receipt_ref.get("sha256") != core.sha256_bytes(col.files[receipt_rel]):
        raise _fail("GATE_RECEIPT_BINDING", "gate derivation receipt does not match validated receipt")
    graph.node(receipt_rel, receipt_ref["sha256"], len(col.files[receipt_rel]),
               "receipt:record", _pol(receipt_rel))
    graph.edge(gate_path, "GATE_BINDING receipt", receipt_rel, receipt_ref["sha256"])
    reader_ref = receipt.get("reviewed_reader_input") or {}
    reader_node_rel = col.pinned(reader_ref, "active-before reader input file")
    graph.node(reader_node_rel, reader_ref["sha256"], len(col.files[reader_node_rel]),
               "reader:before-input", _pol(reader_node_rel))
    graph.edge(receipt_rel, "RECEIPT_CLOSURE reviewed-input", reader_node_rel,
               reader_ref["sha256"])
    sem_auth = gate_record.get("semantic_authority") or {}
    review_path = sem_auth.get("review_path") or (receipt.get("semantic_review") or {}).get("path")
    if not review_path:
        raise _fail("GATE_REVIEW_SHAPE", "gate carries no semantic review binding")
    if receipt.get("semantic_review", {}).get("path") != review_path:
        raise _fail("GATE_REVIEW_BINDING", "gate review binding differs from validated receipt")
    review_rel = col.pinned(receipt["semantic_review"], "gate-bound pre-TeX review")
    review_raw = json.loads(col.files[review_rel].decode("utf-8"))
    if review_raw.get("review_sha256") != pretex["review_sha256"]:
        raise _fail("REVIEW_DIGEST_UNBOUND", "pinned pre-TeX review digest differs from loader authority")
    if review_raw.get("review_sha256") != pretex["review_sha256"]:
        raise _fail("REVIEW_DIGEST_UNBOUND", "pinned pre-TeX review digest differs from loader authority")
    graph.node(review_rel, core.sha256_bytes(col.files[review_rel]), len(col.files[review_rel]),
               "review:pre-tex-target", _pol(review_rel))
    graph.edge(gate_path, "GATE_BINDING pre-tex-review", review_rel,
               core.sha256_bytes(col.files[review_rel]))

    for group, prefix in (("accepted_refs", "receipt:accepted"), ("authored_refs", "receipt:authored")):
        seen: set[str] = set()
        for row in receipt.get(group, []):
            if not isinstance(row, dict) or set(row) != {"name", "path", "sha256"}:
                raise _fail("RECEIPT_REF_SHAPE", f"receipt {group} row fields invalid")
            if row["name"] in seen:
                raise _fail("RECEIPT_DUP_ROLE", f"receipt {group} duplicate name: {row['name']}")
            seen.add(row["name"])
            if _frozen_kind(row["name"]) is None:
                raise _fail("UNCLASSIFIED_DEPENDENCY",
                            f"receipt {group} row has no frozen/operational class: {row['name']}")
            rel = _add_file(row, f"{prefix}:{row['name']}", f"receipt {group} {row['name']}")
            graph.edge(receipt_rel, f"RECEIPT_CLOSURE {row['name']}", rel, row["sha256"])
    for row in receipt.get("current_tools", {}).get("closure", []):
        rel = _add_file(row, f"receipt:tool-closure:{row.get('name')}",
                        f"receipt tool closure {row.get('name')}")
        graph.edge(receipt_rel, f"RECEIPT_TOOL_CLOSURE {row['name']}", rel, row["sha256"])
    for role, output in (receipt.get("outputs") or {}).items():
        rel = _add_file(output, f"receipt:output:{role}", f"receipt output {role}")
        graph.edge(receipt_rel, f"RECEIPT_CLOSURE output:{role}", rel, output["sha256"])

    for check in bundle.get("checks", []):
        result = (check or {}).get("result") or {}
        rel = _add_file(result, f"quality:result:{(check or {}).get('check_id')}",
                        f"quality result {(check or {}).get('check_id')}")
        graph.edge(effective["quality-regression-bundle"]["path"],
                   f"QUALITY_OUTPUT {(check or {}).get('check_id')}", rel, result["sha256"])

    for row_name, kind in (("semantic-review", "SEMANTIC_EDITORIAL"), ("visual-review", "VISUAL")):
        info = effective[row_name]
        record = reader.validate_review_record(
            root, root / info["path"], issue_id=state.get("issue_id"), expected_kind=kind)
        graph.edge(info["path"], "REVIEW_TARGET manuscript",
                   record["reader_manuscript"]["path"], record["reader_manuscript"]["sha256"])
        graph.edge(info["path"], "REVIEW_TARGET source",
                   record["source"]["path"], record["source"]["sha256"])
        graph.edge(info["path"], "REVIEW_TARGET pdf",
                   record["pdf"]["path"], record["pdf"]["sha256"])
        for refkey in ("reader_manuscript", "source", "pdf"):
            ref = record[refkey]
            live = col.safe(ref["path"], f"later review {kind} {refkey}")
            if core.sha256_bytes(col.files[col.rel(live)]) != ref["sha256"]:
                raise _fail("LATER_REVIEW_BINDING_DRIFT", f"later {kind} {refkey} drifted")

    candidate_rel = (Path(state["profile"]["path"]).parent.parent /
                     "publication" / "v2" / "publication-candidate-v2.json").as_posix()
    candidate_full = root / candidate_rel
    if candidate_full.is_symlink():
        raise _fail("CANDIDATE_ALIAS", "observed candidate is a symlink")
    if candidate_full.is_file():
        col.safe(candidate_rel, "observed candidate")
        candidate = publication.validate_candidate(root, candidate_full, issue_id=state.get("issue_id"))
        for field, row_name in (("reader_manuscript", "reader-manuscript"),
                                ("source", "validated-source"), ("pdf", "publication-pdf")):
            if candidate.get(field, {}).get("sha256") != effective[row_name]["sha256"]:
                raise _fail("CANDIDATE_DIVERGED", f"observed candidate {field} differs from active publication")
        graph.node(candidate_rel, core.sha256_bytes(col.files[candidate_rel]),
                   len(col.files[candidate_rel]), "candidate:observed", _pol(candidate_rel))
        graph.edge(checkpoint_rel, "CANDIDATE_OBSERVED unadopted", candidate_rel,
                   core.sha256_bytes(col.files[candidate_rel]))

    frozen: list[dict[str, str]] = []
    for path, node in graph.nodes.items():
        kind = _frozen_member_kind(node["roles"])
        if kind is not None:
            frozen.append({"kind": kind, "path": path, "sha256": node["sha256"]})
    frozen.sort(key=lambda row: (row["kind"], row["path"]))
    preserved_digest = core.sha256_object(frozen)
    return graph.canonical(), frozen, preserved_digest

def _retention_plan(col: _Collector, graph: dict[str, Any], proposal_dir: str) -> list[dict[str, Any]]:
    seen_dest: set[str] = set()
    inputs = set(col.files)
    rows = []
    for node in graph["nodes"]:
        entry: dict[str, Any] = {"role": node["roles"][0], "roles": node["roles"],
                                 "path": node["path"], "sha256": node["sha256"],
                                 "byte_count": node["byte_count"], "policy": node["policy"]}
        if node["policy"] == "KEEP_IMMUTABLE":
            entry["retained_ref"] = {"path": node["path"], "sha256": node["sha256"]}
        else:
            dest = (proposal_dir + "/retained/before/" + node["path"]).replace("//", "/")
            if dest in inputs:
                raise _fail("RETENTION_OVERLAP", f"retention destination overlaps live input: {dest}")
            if dest in seen_dest:
                raise _fail("RETENTION_DEST_CONFLICT", f"duplicate retention destination: {dest}")
            seen_dest.add(dest)
            if (col.root / dest).is_symlink() or (col.root / dest).exists():
                raise _fail("RETENTION_DEST_CONFLICT",
                            f"retention destination already present (no overwrite): {dest}")
            entry["retained_dest"] = dest
        rows.append(entry)
    rows.sort(key=lambda row: row["path"])
    return rows


def _pipeline(col: _Collector, root: Path, state_path: Path, new_authored_value: str | Path,
              proposal_id: str, tree_entry: dict[str, str]) -> dict[str, Any]:
    _check_proposal_id(proposal_id)
    state_file = col.safe(state_path, "Production State")
    state = core.load_json(state_file)
    cfg = core.load_json(root / core.DEFAULT_CONFIG)
    if agent.validate_agent_state(root, cfg, state):
        raise _fail("STATE_INVALID", "Production State fails strict validation")
    _eligibility(state)
    profile = _load_profile(col, state)
    route = _route_of(profile)
    original_record, original_rows = _original_checkpoint(col, root, state)
    effective, active_record = _active_effective(col, root, cfg, state, original_rows)
    allowed = agent._publication_revalidation_roles(root, cfg, state)
    for row in original_rows:
        if allowed.get(row["name"]) != row["path"]:
            raise _fail("ROW_NOT_CANONICAL", f"original row outside configured roles: {row['name']}")

    manuscript_doc = reader.validate_manuscript_manifest(
        root, root / effective["reader-manuscript"]["path"], issue_id=state.get("issue_id"))
    gate_hint = core.load_json(col.safe(
        effective["reader-surface-gate"]["path"], "active Gate record"))
    receipt_rel = ((gate_hint.get("derivation") or {}).get("receipt") or {}).get("path")
    if not receipt_rel:
        raise _fail("GATE_RECEIPT_SHAPE", "gate record carries no receipt binding")
    receipt_file = col.safe(receipt_rel, "generated receipt")
    try:
        envelope = core.load_json(receipt_file)
    except ValueError as exc:
        raise _fail("RECEIPT_UNREADABLE", f"generated receipt is not JSON: {exc}") from exc
    if not isinstance(envelope, dict):
        raise _fail("RECEIPT_UNREADABLE", "generated receipt is not a JSON object")
    try:
        before_authored_rel = next(
            row["path"] for row in envelope.get("authored_refs", [])
            if isinstance(row, dict) and row.get("name") == "publication-semantic-input")
        envelope_reader_rel = (envelope.get("reviewed_reader_input") or {}).get("path")
    except (AttributeError, TypeError, StopIteration) as exc:
        raise _fail("RECEIPT_REF_SHAPE", f"generated receipt routing refs unreadable: {exc}") from exc
    if not before_authored_rel or not envelope_reader_rel:
        raise _fail("RECEIPT_REF_SHAPE", "generated receipt lacks routing refs")
    before_context = _derive(col, root, route, state_file, before_authored_rel)
    reader_file = col.safe(envelope_reader_rel, "active-before reader input")
    before_canonical = _canonical(route, before_context["surface"])
    if reader_file.read_bytes() != before_canonical:
        raise _fail("NONCANONICAL_BEFORE", "active-before reader file is not canonical derivation bytes")

    proposed_context = _derive(col, root, route, state_file, new_authored_value)
    proposed_canonical = _canonical(route, proposed_context["surface"])
    if proposed_canonical == before_canonical:
        raise _fail("NO_EDITORIAL_CHANGE", "proposed reader bytes identical to active-before bytes")

    if route == LONGFORM_ROUTE:
        receipt = longform_generated.validate_receipt(root, receipt_file, state_file)
    else:
        receipt = weekly.validate_receipt(root, receipt_file, state_file)
    renderer_commit = receipt["current_tools"]["repository_commit_sha"]
    if receipt["current_tools"]["contract"] != core.contract_identity(
            root, cfg, profile["research_profile"], profile["publication_profile"]):
        raise _fail("RECEIPT_CONTRACT_DRIFT", "validated receipt contract differs from current contract")
    if receipt["reviewed_reader_input"].get("path") != envelope_reader_rel:
        raise _fail("RECEIPT_BINDING_CHANGED", "validated receipt reader binding differs from routing read")

    gate_record = surface_gate.validate_reader_surface_gate(
        root, root / effective["reader-surface-gate"]["path"], issue_id=state.get("issue_id"),
        publication_profile=profile.get("publication_profile"),
        expected_manuscript_path=root / effective["reader-manuscript"]["path"],
        state_path=state_file)
    if gate_record.get("status") != "PASSED":
        raise _fail("GATE_NOT_PASSED", "active Gate record is not PASSED")
    _frozen_names_check(receipt, before_context)
    pretex = surface_gate.load_and_validate_reader_surface_semantic_review(
        root, receipt["semantic_review"]["path"], expected_issue_id=state.get("issue_id"),
        expected_publication_profile=profile.get("publication_profile"),
        expected_surface_path=envelope_reader_rel,
        expected_surface_sha256=core.sha256_bytes(before_canonical), require_pass=True)
    bundle = quality.validate_bundle(
        root, root / effective["quality-regression-bundle"]["path"], issue_id=state.get("issue_id"))
    graph, frozen, preserved_digest = _build_graph(
        col, root, state, original_rows, effective, active_record,
        receipt, col.rel(receipt_file), gate_record, manuscript_doc, bundle, pretex)
    graph_digest = core.sha256_object(graph)
    proposal_dir = (Path(profile["paths"]["source_root"]) / "publication" / "v2" /
                    "editorial-corrections" / proposal_id).as_posix()
    retention = _retention_plan(col, graph, proposal_dir)
    col.reverify()
    if _tree_map(root, Path(profile["paths"]["source_root"]),
                 Path(profile["paths"]["survey_root"])) != tree_entry:
        raise _fail("TREE_MOVED", "edition tree changed during inspection")
    new_authored_rel = col.rel(col.safe(new_authored_value, "new publication-authored input"))
    proposal = {
        "schema_version": "2.0-rc1",
        "proposal_id": proposal_id,
        "issue_id": state.get("issue_id"),
        "research_profile": profile.get("research_profile"),
        "publication_profile": profile.get("publication_profile"),
        "route": "EDITORIAL_CORRECTION_PROPOSAL_V1",
        "status": "PROPOSED",
        "basis": {
            "state_ref": {"path": col.rel(state_file),
                           "sha256": core.sha256_bytes(col.files[col.rel(state_file)])},
            "validation_checkpoint_ref": dict((state.get("checkpoint_provenance") or {})["validation"]),
            "active_revalidation_ref": dict(state.get("publication_revalidation_provenance"))
            if state.get("publication_revalidation_provenance") else None,
            "active_reader_input_ref": {"path": envelope_reader_rel,
                                        "sha256": core.sha256_bytes(before_canonical)},
            "before_graph_digest": graph_digest,
            "preserved_upstream_digest": preserved_digest,
            "generated_receipt_ref": {"path": col.rel(receipt_file),
                                      "sha256": core.sha256_bytes(col.files[col.rel(receipt_file)])},
            "renderer_commit": renderer_commit,
            "contract_identity": receipt["current_tools"]["contract"],
        },
        "proposed": {
            "authoring_input_ref": {"path": new_authored_rel,
                                    "sha256": core.sha256_bytes(col.files[new_authored_rel])},
            "proposed_reader_canonical_sha256": core.sha256_bytes(proposed_canonical),
            "change_description": f"editorial correction proposal {proposal_id}",
        },
        "retention_plan": retention,
    }
    return {"proposal": proposal, "proposed_canonical": proposed_canonical,
            "before_canonical": before_canonical, "graph": graph, "frozen": frozen,
            "effective": effective, "original_rows": original_rows,
            "active_record": active_record, "route": route,
            "before_authored_rel": before_authored_rel,
            "new_authored_rel": new_authored_rel, "reader_rel": envelope_reader_rel}


def _frozen_names_check(receipt: dict[str, Any], context: dict[str, Any]) -> None:
    receipt_names = {row["name"] for row in receipt.get("accepted_refs", [])}
    context_names = {row["name"] for row in context.get("accepted_refs", [])}
    if receipt_names != context_names:
        raise _fail("UPSTREAM_SET_DRIFT", "receipt accepted authority differs from rederived authority")
    for row in receipt.get("accepted_refs", []):
        match = next(item for item in context["accepted_refs"] if item["name"] == row["name"])
        if match["sha256"] != row["sha256"]:
            raise _fail("UPSTREAM_REF_DRIFT", f"accepted authority drifted: {row['name']}")


def prepare_proposal(root: str | Path, state_path: str | Path,
                     authoring_path: str | Path, proposal_id: str) -> dict[str, Any]:
    """Read-only before validation plus real proposed derivation (in memory)."""
    root_path = Path(root)
    col = _Collector(root_path)
    cfg = core.load_json(root_path / core.DEFAULT_CONFIG)
    state_preview = core.load_json(col.safe(state_path, "Production State"))
    profile_preview = core.load_json(col.safe(state_preview["profile"]["path"], "Production Profile"))
    tree_entry = _tree_map(root_path, Path(profile_preview["paths"]["source_root"]),
                            Path(profile_preview["paths"]["survey_root"]))
    result = _pipeline(col, root_path, Path(state_path), authoring_path, proposal_id, tree_entry)
    schema_gate.validate_instance(result["proposal"], root_path / PROPOSAL_SCHEMA,
                                  label="editorial correction proposal")
    return result


def _validate_scope(col: _Collector, root: Path, scope_review_value: str | Path,
                    proposal: dict[str, Any], state: dict[str, Any],
                    profile: dict[str, Any]) -> str:
    raw_path = col.safe(scope_review_value, "scope review record")
    captured = raw_path.read_bytes()
    captured_sha = core.sha256_bytes(captured)
    try:
        raw = json.loads(captured.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise _fail("SCOPE_UNREADABLE", f"scope review bytes are not JSON: {exc}") from exc
    if not isinstance(raw, dict):
        raise _fail("SCOPE_UNREADABLE", "scope review is not a JSON object")
    after_ref = {"path": proposal["proposed"].get("proposed_reader_ref", {}).get("path", ""),
                 "sha256": proposal["proposed"].get("proposed_reader_sha256", "")}
    try:
        authority = surface_gate.load_and_validate_reader_surface_semantic_review(
            root, raw_path, expected_issue_id=state.get("issue_id"),
            expected_publication_profile=profile.get("publication_profile"),
            expected_surface_path=after_ref["path"],
            expected_surface_sha256=after_ref["sha256"], require_pass=True)
    except ValueError as exc:
        raise _fail("SCOPE_ORDINARY_INVALID", str(exc)) from exc
    if raw_path.read_bytes() != captured:
        raise _fail("SCOPE_BYTES_SWITCHED", "scope review file changed around loader call")
    if core.sha256_object({k: v for k, v in raw.items() if k != "review_sha256"}) != raw.get("review_sha256"):
        raise _fail("SCOPE_DIGEST_MISMATCH", "scope review object digest does not bind captured JSON")
    if authority.get("review_sha256") != raw.get("review_sha256"):
        raise _fail("SCOPE_DIGEST_MISMATCH", "loader digest does not bind captured review bytes")
    block = raw.get("editorial_correction_scope")
    if block is None:
        return RESULT_REQUIRED
    if not isinstance(block, dict) or block.get("version") != SCOPE_VERSION:
        raise _fail("SCOPE_BLOCK_SHAPE", "scope block version invalid")
    if block.get("decision") != "WITHIN_APPROVED_AUTHORITY":
        raise _fail("SCOPE_NOT_WITHIN_AUTHORITY",
                    f"scope decision cannot bind a correction: {block.get('decision')}")
    if block.get("before_reader_input") != proposal["basis"]["active_reader_input_ref"]:
        raise _fail("SCOPE_WRONG_BEFORE", "scope block before-reader does not match proposal basis")
    after_binding = {"path": after_ref["path"], "sha256": after_ref["sha256"]}
    if authority.get("surface_path") != after_binding["path"] or \
            authority.get("surface_sha256") != after_binding["sha256"]:
        raise _fail("SCOPE_WRONG_AFTER", "scope review does not target the proposed reader")
    if block.get("preserved_upstream_sha256") != proposal["basis"]["preserved_upstream_digest"]:
        raise _fail("SCOPE_STALE_UPSTREAM", "scope block upstream digest does not match proposal")
    if not isinstance(block.get("change_summary"), str) or not block["change_summary"].strip():
        raise _fail("SCOPE_BLOCK_SHAPE", "scope block change_summary empty")
    if not isinstance(block.get("evidence_locations"), list) or \
            not all(isinstance(item, str) and item.strip() for item in block["evidence_locations"]):
        raise _fail("SCOPE_BLOCK_SHAPE", "scope block evidence_locations empty")
    scope_checks = [c for c in authority.get("checks", []) if c.get("check_id") == SCOPE_CHECK_ID]
    if not scope_checks or any(c.get("status") != "PASS" for c in scope_checks):
        raise _fail("SCOPE_CHECK_NOT_PASS", "substantive scope check missing or not PASS")
    for check in scope_checks:
        if not check.get("detail", "").strip() or not check.get("evidence_locations"):
            raise _fail("SCOPE_CHECK_NOT_PASS", "scope check lacks substantive detail/evidence")
    return RESULT_BOUND


def validate_proposal(root: str | Path, state_path: str | Path, proposal_path: str | Path,
                      scope_review_path: str | Path | None = None) -> dict[str, Any]:
    """Re-derive from named FILE bytes; return typed result plus input hashes."""
    root_path = Path(root)
    col = _Collector(root_path)
    cfg = core.load_json(root_path / core.DEFAULT_CONFIG)
    proposal_file = col.safe(proposal_path, "editorial correction proposal")
    if Path(proposal_file).name != "proposal.json":
        raise _fail("PROPOSAL_FILENAME", "proposal file must be named proposal.json")
    proposal = core.load_json(proposal_file)
    schema_gate.validate_instance(proposal, root_path / PROPOSAL_SCHEMA,
                                  label="editorial correction proposal")
    proposal_id = proposal["proposal_id"]
    proposal_dir = proposal_file.parent
    if proposal_dir.name != proposal_id or proposal_dir.parent.name != "editorial-corrections":
        raise _fail("PROPOSAL_LAYOUT", "proposal file outside canonical proposal directory")
    for name in PROPOSAL_FILES:
        candidate = proposal_dir / name
        if candidate.is_symlink() or not candidate.is_file():
            raise _fail("PROPOSAL_LAYOUT", f"proposal directory entry invalid: {name}")
    staged_authored = col.safe(proposal_dir / "authoring-input.json", "staged authoring input")
    staged_reader = col.safe(proposal_dir / "reader-surface-input-v2.json", "staged proposed reader")
    if core.sha256_bytes(col.files[col.rel(staged_authored)]) != \
            proposal["proposed"]["authoring_input_ref"]["sha256"]:
        raise _fail("PROPOSED_AUTHORING_MISMATCH", "staged authoring bytes differ from proposal ref")
    state_preview = core.load_json(col.safe(state_path, "Production State"))
    profile_preview = core.load_json(col.safe(state_preview["profile"]["path"], "Production Profile"))
    tree_entry = _tree_map(root_path, Path(profile_preview["paths"]["source_root"]),
                            Path(profile_preview["paths"]["survey_root"]))
    result = _pipeline(col, root_path, Path(state_path), staged_authored, proposal_id, tree_entry)
    if result["proposal"]["basis"] != proposal["basis"]:
        raise _fail("BASIS_MISMATCH", "rederived basis differs from supplied proposal")
    if result["proposal"]["retention_plan"] != proposal["retention_plan"]:
        raise _fail("RETENTION_MISMATCH", "rederived retention plan differs from supplied proposal")
    if staged_reader.read_bytes() != result["proposed_canonical"]:
        raise _fail("PROPOSED_BYTES_MISMATCH", "staged proposed reader differs from rederived canonical bytes")
    proposed = dict(proposal["proposed"])
    proposed["proposed_reader_ref"] = {
        "path": col.rel(staged_reader),
        "sha256": core.sha256_bytes(result["proposed_canonical"])}
    proposed["proposed_reader_sha256"] = core.sha256_bytes(result["proposed_canonical"])
    proposal = dict(proposal)
    proposal["proposed"] = proposed
    state = core.load_json(col.safe(state_path, "Production State"))
    profile = _load_profile(col, state)
    if scope_review_path is None:
        outcome = RESULT_REQUIRED
    else:
        outcome = _validate_scope(col, root_path, scope_review_path, proposal, state, profile)
    col.reverify()
    return {"result": outcome,
            "input_hashes": {rel: core.sha256_bytes(data) for rel, data in col.files.items()},
            "proposal": proposal}
