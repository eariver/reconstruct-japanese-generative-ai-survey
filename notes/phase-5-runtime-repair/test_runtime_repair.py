"""Boundary integration on synthetic editions; no production/network operations.

Actual State/schema/publication/approval/stage/controller validators run. Earlier
research artifacts and reviewer judgments are fixture data, not research or QA.
"""
from __future__ import annotations
import copy
import shutil
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path
from unittest import mock
from scripts import survey_agent_control_v2 as agent
from scripts import survey_production_v2 as core
from scripts import survey_publication_v2 as publication
from scripts import survey_stage_validation_v2 as stage
from scripts import survey_release_checkpoint_v2 as release
from tests.test_survey_publication_v2 import SurveyPublicationV2Tests as PublicationFixture


class RuntimeRepairTests(unittest.TestCase):
    def setUp(self):
        self.fixture = PublicationFixture()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        temp = tempfile.TemporaryDirectory(dir=Path.cwd())
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        cfg = core.load_json(Path.cwd()/core.DEFAULT_CONFIG)
        needed = set(cfg["contract_files"]["pipeline"] + cfg["contract_files"]["quality"])
        needed.update(str(p.relative_to(Path.cwd())) for p in (Path.cwd()/"schemas").glob("*.json"))
        needed.add(str(core.DEFAULT_CONFIG))
        for rel in needed:
            target = self.root/rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(Path.cwd()/rel, target)
        self.fixture.root = self.root
        self.now = self.fixture.now
        self.cfg = core.load_json(self.root/core.DEFAULT_CONFIG)
        original_profile = self.fixture._profile
        def profile(*args):
            path = original_profile(*args)
            value = core.load_json(path)
            value["contract"] = core.contract_identity(self.root, self.cfg, value["research_profile"], value["publication_profile"])
            core.write_json(path, value)
            return path
        self.fixture._profile = profile
        original_arch = self.fixture._architecture
        def architecture(*args):
            path, approval = original_arch(*args)
            value = core.load_json(approval)
            for field, filename in (("architecture_review_summary_sha256", "architecture-review-summary-v2.json"),
                                    ("architecture_review_attention_sha256", "architecture-review-attention-v2.json")):
                target = path.parent/filename
                core.write_json(target, {"synthetic_upstream": filename})
                value[field] = core.sha256_file(target)
            core.write_json(approval, value)
            return path, approval
        self.fixture._architecture = architecture

    def ref(self, path):
        return {"path": path.relative_to(self.root).as_posix(), "sha256": core.sha256_file(path)}

    def edition(self, research="THEMATIC", publication_profile="LONGFORM_SPECIAL"):
        issue = "2026-W35" if research == "WEEKLY" else "SP-REPAIR-" + research
        paths = self.fixture._candidate(issue, research, publication_profile)
        profile = core.load_json(paths["profile"])
        source = paths["profile"].parent
        state_path = source/"production-state.json"
        impl = core.repository_commit_sha(self.root)
        state = core.initial_state(self.root, self.cfg, profile, paths["profile"], impl, "PUBLICATION_PREVIEW", self.now)
        aliases = {"issue-architecture": paths["architecture"],
                   "architecture-review-summary": source/"architecture-review-summary-v2.json",
                   "architecture-review-attention": source/"architecture-review-attention-v2.json",
                   "reader-manuscript": paths["manifest"], "validated-source": paths["source"],
                   "publication-pdf": paths["pdf"], "quality-regression-bundle": paths["bundle"],
                   "semantic-review": paths["semantic"], "visual-review": paths["visual"],
                   "publication-candidate": paths["candidate"]}
        contract = core.contract_identity(self.root, self.cfg, research, publication_profile)
        # Construct explicit historical fixtures, never run upstream authoring.
        for lifecycle in core.LIFECYCLE[:core.LIFECYCLE.index("RELEASE_CANDIDATE")]:
            plan = self.cfg["orchestration"]["stage_plan"][lifecycle]
            artifacts=[]
            for name in sorted(stage.REQUIRED_CURRENT[lifecycle]):
                path=aliases.get(name, source/"synthetic-upstream"/(name+".json"))
                if not path.exists(): core.write_json(path, {"synthetic_upstream": name})
                artifacts.append({"name":name, **self.ref(path)})
            report_path=source/"synthetic-upstream"/(lifecycle+"-report.json")
            report={"schema_version":"2.0-rc1", "check_id":"CORE_STAGE_CONTRACT", "status":"PASS",
                    "issue_id":issue,"from_state":lifecycle,"to_state":plan["next_state"],
                    "production_state":{"path":state_path.relative_to(self.root).as_posix(),"sha256":"0"*64},
                    "production_profile":self.ref(paths["profile"]),"implementation_commit_sha":impl,
                    "contract":contract,"artifacts":artifacts,"recorded_at":core.iso_utc(self.now)}
            core.write_json(report_path, report)
            checkpoint=source/"orchestration/v2/checkpoints"/(lifecycle+".json")
            core.write_json(checkpoint,{"schema_version":"2.0-rc1","issue_id":issue,
                "from_state":lifecycle,"to_state":plan["next_state"],"checkpoints":plan["checkpoints"],
                "recorded_at":core.iso_utc(self.now),"implementation":{"repository_commit_sha":impl,"orchestrator_version":self.cfg["orchestrator_version"]},
                "contract":contract,"artifacts":artifacts,"reviews":[{"check_id":"CORE_STAGE_CONTRACT","kind":"DETERMINISTIC","status":"PASS",
                "executor":"synthetic upstream fixture","evidence":"Fixture only; no source research or editorial QA claim","result":self.ref(report_path)}],"summary":"Synthetic upstream history"})
            for name in plan["checkpoints"]:
                state["machine_checkpoints"][name]="passed"
                state["checkpoint_provenance"][name]=self.ref(checkpoint)
            state["history"].append({"from":lifecycle,"to":plan["next_state"],"recorded_at":core.iso_utc(self.now),"repository_commit_sha":impl})
        state["lifecycle_state"]="RELEASE_CANDIDATE"
        state["human_gates"]["architecture_review"]="approved"
        state["human_gate_provenance"]["architecture_review"]=self.ref(paths["approval"])
        state=core.refresh_state_control(state,self.cfg)
        core.write_json(state_path,state)
        self.assertEqual(agent.validate_agent_state(self.root,self.cfg,state),[])
        # Real approval function in a synthetic edition; not a production Human act.
        agent.approve_publication_preview(self.root,self.cfg,state_path,"fixture-human",self.now,"fixture:preview")
        paths.update(state=state_path, preview=source/"gates/publication-preview-approval.json")
        paths["freeze"]=paths["publication_dir"]/"freeze-record-v2.json"
        paths["release_manifest"]=paths["publication_dir"]/"release-manifest-v2.json"
        publication.build_freeze(self.root,paths["candidate"],paths["preview"],self.now,paths["freeze"],paths["release_manifest"])
        return paths

    def freeze(self,p):
        supplied={"freeze-record":p["freeze"],"release-manifest":p["release_manifest"],"visual-review-record":p["visual"]}
        report=p["publication_dir"]/"freeze-core-report.json"
        stage.validate_stage(self.root,self.cfg,p["state"],supplied,report,self.now)
        reviews=p["publication_dir"]/"freeze-reviews.json"
        core.write_json(reviews,{"reviews":[{"check_id":"CORE_STAGE_CONTRACT","kind":"DETERMINISTIC","executor":"stage validator",
              "evidence":"Real boundary validation on synthetic publication", "result_path":report.relative_to(self.root).as_posix()}]})
        checkpoint=agent.build_stage_checkpoint(self.root,self.cfg,p["state"],supplied,reviews,"fixture freeze",self.now)
        result=agent.advance_with_checkpoint(self.root,self.cfg,p["state"],checkpoint)
        self.assertEqual(result["lifecycle_state"],"FROZEN")
        return checkpoint

    def external_record(self,p):
        # Fixed external-success observation; no GitHub calls, upload or re-create.
        verification=p["publication_dir"]/"merge-verification-v2.json"
        record=p["publication_dir"]/"release-record-v2.json"
        publication.build_merge_verification(self.root,p["release_manifest"],"a"*40,self.now,verification)
        publication.build_release_record(self.root,p["release_manifest"],verification,self.now,"fixture:external-success",record)
        return verification,record

    def test_weekly_special_freeze_release_and_retry_after_local_failure(self):
        for research,profile in (("WEEKLY","WEEKLY_MAGAZINE"),("THEMATIC","LONGFORM_SPECIAL"),("RETROSPECTIVE_PERIOD","LONGFORM_SPECIAL")):
            with self.subTest(profile=(research,profile)):
                p=self.edition(research,profile); self.freeze(p)
                verification,record=self.external_record(p)
                before=record.read_bytes()
                checkpoint=release.build_release_checkpoint(self.root,self.cfg,p["state"],verification,record,self.now)
                original=checkpoint.read_bytes()
                # Failure occurs after external success/local checkpoint write, before State advance.
                again=release.build_release_checkpoint(self.root,self.cfg,p["state"],verification,record,self.now+timedelta(minutes=1))
                self.assertEqual(again.read_bytes(),original)
                result=agent.advance_with_checkpoint(self.root,self.cfg,p["state"],checkpoint)
                self.assertEqual(result["lifecycle_state"],"RELEASED")
                self.assertEqual(agent.validate_agent_state(self.root,self.cfg,result),[])
                self.assertEqual(record.read_bytes(),before)

    def test_freeze_rejects_drift_in_approved_authorities(self):
        p=self.edition()
        for key in ("preview","candidate","pdf","visual"):
            with self.subTest(key=key):
                raw=p[key].read_bytes(); p[key].write_bytes(raw+b" ")
                try:
                    with self.assertRaises(ValueError): self.freeze(p)
                finally: p[key].write_bytes(raw)

    def test_gate_profile_issue_and_ambiguous_pointer_fail_closed(self):
        p=self.edition(); original=core.load_json(p["state"])
        changes=[("pending",lambda s:s["human_gates"].update(publication_preview="pending")),
                 ("other-profile",lambda s:s.update(publication_profile="WEEKLY_MAGAZINE")),
                 ("other-issue",lambda s:s.update(issue_id="SP-OTHER")),
                 ("missing-authority",lambda s:s["human_gate_provenance"].update(publication_preview=None)),
                 ("conflicting-authority",lambda s:s["human_gate_provenance"].update(publication_preview=self.ref(p["candidate"])))]
        for name,change in changes:
            with self.subTest(name=name):
                state=copy.deepcopy(original);change(state);core.write_json(p["state"],state)
                with self.assertRaises(ValueError): self.freeze(p)
        core.write_json(p["state"],original)

    def test_wrong_visual_same_bytes_at_other_path_is_not_approved(self):
        p=self.edition(); duplicate=p["visual"].with_name("other-visual.json");duplicate.write_bytes(p["visual"].read_bytes());p["visual"]=duplicate
        with self.assertRaisesRegex(ValueError,"exact visual_review|pre-preview"): self.freeze(p)

    def test_release_rejects_rebound_wrong_manifest_and_issue(self):
        p=self.edition();self.freeze(p);verification,record=self.external_record(p)
        original=record.read_bytes()
        for key,value in (("issue_id","SP-OTHER"),("release_identity","weekly/2026-W35")):
            with self.subTest(key=key):
                payload=core.load_json(record);payload[key]=value;core.write_json(record,payload)
                with self.assertRaises(ValueError): release.build_release_checkpoint(self.root,self.cfg,p["state"],verification,record,self.now)
                record.write_bytes(original)
        other=p["release_manifest"].with_name("other-manifest.json");other.write_bytes(p["release_manifest"].read_bytes())
        verification_data=core.load_json(verification);verification_data["release_manifest_path"]=other.relative_to(self.root).as_posix();core.write_json(verification,verification_data)
        value=core.load_json(record);value["merge_verification_sha256"]=core.sha256_file(verification);value["release_manifest_path"]=other.relative_to(self.root).as_posix();core.write_json(record,value)
        with self.assertRaisesRegex(ValueError,"accepted Release Manifest"): release.build_release_checkpoint(self.root,self.cfg,p["state"],verification,record,self.now)

    def test_controller_rejects_changed_report_basis(self):
        p=self.edition();self.freeze(p);verification,record=self.external_record(p)
        checkpoint=release.build_release_checkpoint(self.root,self.cfg,p["state"],verification,record,self.now)
        payload=core.load_json(checkpoint);review=next(r for r in payload["reviews"] if r["check_id"]=="CORE_STAGE_CONTRACT")
        result=self.root/review["result"]["path"]; value=core.load_json(result);value["production_state"]["sha256"]="0"*64;core.write_json(result,value)
        review["result"]=self.ref(result);core.write_json(checkpoint,payload)
        with self.assertRaisesRegex(ValueError,"Production State authority mismatch"): agent.advance_with_checkpoint(self.root,self.cfg,p["state"],checkpoint)

    def test_invalid_active_revalidation_is_not_ignored(self):
        p=self.edition();state=core.load_json(p["state"])
        state["publication_revalidation_provenance"]={"path":"missing.json","sha256":"0"*64};core.write_json(p["state"],state)
        with self.assertRaises(ValueError): self.freeze(p)


class RevalidatedFreezeTests(unittest.TestCase):
    def test_active_revalidation_survives_approval_and_freeze(self):
        from tests.test_survey_publication_revalidation_v2 import PublicationRevalidationTests, T0, ISSUE
        helper = PublicationRevalidationTests()
        helper.setUp()
        temp, fix = helper.make_fixture()
        self.addCleanup(temp.cleanup)
        helper.regenerate(fix)
        helper._operate(fix)
        root, cfg = helper.root, helper.cfg
        state_path = fix.src / "production-state.json"
        old_state = core.load_json(state_path)
        history_ref = old_state["checkpoint_provenance"]["validation"]
        history_path = root/history_ref["path"]
        history_bytes = history_path.read_bytes()
        directory = fix.src/"publication/v2"
        candidate = directory/"publication-candidate-v2.json"
        publication.build_candidate(root, ISSUE, "WEEKLY_MAGAZINE",
            directory/"reader-manuscript-v2.json", fix.survey/"main.tex", fix.survey/"main.pdf", 1,
            directory/"quality-regression-bundle-v2.json", directory/"semantic-editorial-review-v2.json",
            directory/"visual-review-v2.json", candidate)
        report = directory/"candidate-stage-report.json"
        stage.validate_stage(root,cfg,state_path,{"publication-candidate":candidate},report,T0+timedelta(hours=2))
        reviews=directory/"candidate-stage-reviews.json"
        core.write_json(reviews,{"reviews":[{"check_id":"CORE_STAGE_CONTRACT","kind":"DETERMINISTIC",
            "executor":"fixture real validator","evidence":"Revalidated fixed publication boundary",
            "result_path":report.relative_to(root).as_posix()}]})
        checkpoint=agent.build_stage_checkpoint(root,cfg,state_path,{"publication-candidate":candidate},reviews,"fixture candidate",T0+timedelta(hours=3))
        agent.advance_with_checkpoint(root,cfg,state_path,checkpoint)
        agent.approve_publication_preview(root,cfg,state_path,"fixture-human",T0+timedelta(hours=4),"fixture:approved")
        approval=fix.src/"gates/publication-preview-approval.json"
        freeze=directory/"freeze-record-v2.json";manifest=directory/"release-manifest-v2.json"
        publication.build_freeze(root,candidate,approval,T0+timedelta(hours=5),freeze,manifest)
        adapter=RuntimeRepairTests()
        adapter.root=root;adapter.cfg=cfg;adapter.now=T0+timedelta(hours=5)
        adapter.freeze({"freeze":freeze,"release_manifest":manifest,"visual":directory/"visual-review-v2.json",
                        "publication_dir":directory,"state":state_path})
        state=core.load_json(state_path)
        self.assertEqual(state["lifecycle_state"],"FROZEN")
        self.assertEqual(agent.validate_agent_state(root,cfg,state),[])
        self.assertEqual(history_path.read_bytes(),history_bytes)


if __name__=="__main__": unittest.main()
