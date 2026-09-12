# Phase 4-C / A-only research-editorial slice — protocol r1

Status: INPUT PREPARATION; no candidate output or quality verdict yet.
Started: 2026-09-12. Production is read-only. No production admission, State, approval, PDF, release, or adoption is represented by this lab.

## Question and scope fixed before candidate authoring

Reader: Japanese technical readers deciding what an inference-speed report actually establishes and what deployment work remains.
Question: For the week 2026-03-09 00:00 UTC through 2026-03-16 00:00 UTC (exclusive), what does the P-EAGLE/vLLM report establish about parallel speculative drafting, compared with related research, and which speed/deployment conclusions are not warranted?
This is a bounded WEEKLY research/editorial slice, not the historical J-GAS edition for that week and not a claim of complete news discovery.

Candidate universe (three leads; dispositions not assigned here):
- C1: P-EAGLE serving report, with the P-EAGLE paper as supporting technical authority. Blog: https://vllm.ai/blog/2026-03-13-p-eagle ; paper: arXiv 2602.01469 v1.
- C2: DFlash, arXiv 2602.06036 v1, as potentially relevant competing/background research.
- C3: vLLM hidden-state extraction report: https://vllm.ai/blog/2026-03-30-extract-hidden-states . Test whether related implementation information is temporally eligible rather than silently importing it.

Selection rationale for the universe: one serving report linked to a paper; a strong related performance claim that could affect omission/comparison; and a different dated implementation surface. Do not force one article per source or manufacture a new launch from a report's publication date. No prior Phase 3/4-A calibration case is included.
Author exposure before this protocol: discovery search snippets, P-EAGLE blog, DFlash current-version abstract/metadata, hidden-state blog, and opening P-EAGLE paper excerpt. No candidate Card/View/Selection/Draft has been authored. This is not a test of model pretraining unfamiliarity, random sampling, or A/B superiority. DFlash v2 preview is known to exist; v2 results must not be used as v1/as-of evidence.

## Quality requirements

All three candidates need source-grounded disposition. The evaluator must independently identify needed facts/counterexamples from source + question before seeing candidate outputs.
- Separate drafting method, training cost/requirements, verifier, exact evaluation baseline, hardware, concurrency, and reported speed metric. Do not rank methods by headline multipliers across incompatible tests.
- Distinguish source publication time, model/method release, integration/version availability, current capture time, and unknown historical page state. Later captured bytes do not prove exact historical availability.
- Preserve author/project attribution, required special draft training/checkpoints, source-specific limitations, and deployment prerequisites that affect interpretation.
- Negative-space evaluation must consider C2 as a substantive rival, not reject all papers because they are author-reported. A legitimate HOLD is allowed. C3's temporal status requires explicit treatment.
- Japanese reader prose must convey what is useful and what remains unestablished without exposing internal IDs/status/repair language.
- Unsupported claim, meaningful omission, wrong subject/comparator, or unsupported temporal promotion cannot be offset by brevity or low cost.

## Roles and review

Root acts as experiment coordinator and semantic author/editor. A single separately authorized subagent is the non-author evaluator. Same model is acceptable but is not evidence of production role/model equivalence. No extra permanent production role is proposed.
Evaluator first receives protocol + source corpus only and writes source expectations without candidate access. Root does not read these expectations before freezing r1 outputs. Then evaluator receives exact r1 files/hashes and reports findings without editing candidate prose. Root repairs; evaluator rereviews exact changed and affected files. No planted defects or assumed positive result.
User explicitly authorized one review subagent in this task. No messages to production agents or external recipients are authorized by this protocol.

## Artifacts and observation limits

Use canonical Task/Card/View and editorial artifact fields, exact references and hashes from local lab inputs. Mechanically generated binding metadata must not claim production approval. The small lab check covers schema and named local bindings only; admission, concurrent execution, complete historical validation, full-issue coverage, CI/runtime, PDF/visual QA, and Human Gates remain unevaluated.
One Japanese manuscript, all candidate dispositions, findings/repair/re-review, and work record are the unit of completion. No A-only cost superiority or lifecycle ROI claim.
Runtime timestamps and observable operations are recorded. Active reasoning time and role-token/billing usage are unknown unless actual logs expose them; no allocation from character count or account quota. Preparation and reviewer source reread count as work, not free assistance.
If input retrieval/connection requires a material scope change, record an amendment before output generation. If review or repair cannot finish, preserve exact incomplete version and spent work. Do not shrink scope after seeing defects to declare completion.
