# Phase 4-C r1 independent review

Verdict: REPAIR REQUIRED for the bounded lab semantic chain. Four blocking findings below; no production approval or full canonical execution verdict. The reviewer did not author candidates or replacement prose. Frozen source expectations remain unchanged at SHA256 `8b129b38f6ea899eebe2df2f50943f5a4e966f0ceecf1a78b79abb695741a817`.

## Frozen target and verified mechanics

Reviewed `r1-freeze.json`, SHA256 `a9292fd978e1640af22d342dbeb22ebb7ed3632d79be520076746b879554a51e`. All 16 named r1 file hashes matched. Read full Task/Card/View for C1–C3, selection and package lab envelopes, complete Draft and manuscript, and supporting screening/authorship/mechanical-check records. The two package embedded Cards exactly equal their standalone Card objects. Manuscript exactly renders headline/deck/block texts. All 27 Draft reference occurrences resolve to the named event/claim/metric/limitation and matching subject ID/role. These observations do not establish factual sufficiency.

Preflight candidly records that Selection and Package contain canonical semantic fields in non-admitted lab envelopes. This is a legitimate predeclared observation boundary, not an undisclosed defect to solve through fake approvals. Full canonical Selection/Package, production acceptance/authority, CI execution, schema implementation correctness, historical release validation and deployment remain untested. I did not independently rerun the full schema checker or inspect its implementation/contracts; its reported PASS is corroborated here only for exact frozen bytes, embedding, references and rendering.

## Blocking findings

### R1 — P1: P-EAGLE paper's headline range is promoted to a table-result range

Affected: `r1/c1-card.json` metric `p-paper-speed` (name, value scope and context), performance verification/contradictions; embedded copy in `package.lab.json`; `draft.json` b3; manuscript paragraph beginning P-EAGLE論文.

The Card calls 1.10–1.36 'paper reported best serving speedup' and cites abstract plus section5.3/Table10. The manuscript calls this the paper's result without delimiting it to the abstract's summary. Table10's best values include 120B/MT/C4 = 1.03, 120B/HE/C4 = 1.04 and Qwen30B/MT/C2 = 1.04; thus 1.10 is not even a lower bound over all per-condition best results. At fixed K, some results are slower than baseline: Qwen30B/HumanEval K3,C4 = 0.92. Generic discussion that verification cost may grow does not expose this already-observed adverse result, while the displayed numeric range implies uniformly >=10% gains.

Source: `peagle-paper-v1.html`, abstract, section5.3, Table10. Additional internal discrepancy: Qwen30B/HumanEval K3,C2 is 0.94 in Table10 versus 0.98 in section5.3 text. No independent adjudication has been made.

Required disposition: preserve the difference between an abstract summary and actual table scope; remove or narrow the misleading range, and carry a source-grounded qualification of the observed low-depth slowdown into both evidence and reader interpretation. If a disputed exact cell is used, account for its discrepancy; the unambiguous C4 cell is sufficient. Do not silently substitute an inferred new aggregate. Refresh all affected bindings.

### R2 — P2: Actual research/report authorship has been lost throughout the chain

Affected: C1/C2 Card attribution fields or claims and source metadata, embedded Cards, Draft b1/b4 and manuscript corresponding passages. C3's source metadata can also preserve its byline, but C3 requires no new reader prose because it is held.

The protocol explicitly requires author/project attribution. Every entity organization is null and sources contain no byline; the reader is told 'vLLMの3月13日付報告' and 'DFlash v1' without who produced the report/research. This identifies the publisher/site and artifact but loses the distinction between Amazon/NVIDIA's report, the P-EAGLE paper team, and UC San Diego's DFlash work. It also weakens whose performance claim is being repeated.

Source: P-EAGLE blog header 'Amazon and NVIDIA Team' plus acknowledgement; P-EAGLE v1 title/author block (Mude Hui/UCSC with AWS internship and AWS coauthors); DFlash v1 title/author block (Jian Chen, Yesheng Liang, Zhijian Liu, UC San Diego). Hidden-state blog byline is Fynn Schmitt-Ulms.

Required disposition: retain accurate source-specific author/project attribution in the evidence chain and concise reader-facing attribution for the selected report/research. Do not assign a publishing framework as the sole research inventor or conflate the blog team and paper authors. Newly added prose must refer to newly captured Card evidence, not only the author's source memory.

### R3 — P2: DFlash Card repeats an internally inconsistent EAGLE-3 denominator as verified

Affected: `c2-card.json` metric `d-transformers.context`, performance verification and contradictions; embedded Card in package. The current Draft does not consume this particular metric, so its prose is not itself wrong on this number, but the required complete evidence chain still contains the defect.

The context says 4.9x AR speedup corresponds to 2.4x over 'EAGLE-3 tree16'. This copies section5.1 prose but labels the comparator as resolved despite conflicting Table1 values. Greedy Qwen3-4B mean speeds are DFlash4.91, tree16=1.81 and tree60=2.08; Qwen3-8B means are 4.86,1.76,2.02. Ratios of displayed means to tree16 are approximately 2.71/2.76, whereas tree60 gives approximately 2.36/2.41. This does not prove how authors intended to average ratios, but it invalidates unqualified reconciliation as the Card presently presents it. The source-first expectation had identified this before r1.

Required disposition: do not certify that precise correspondence as resolved. Remove the unnecessary correspondence or preserve it explicitly as a source-prose/table inconsistency with its comparator and uncertainty. Do not silently 'correct' the paper's intended denominator without evidence. Keep the correctly supported 4.9x mean or Table3 5.1x separate as appropriate; rereview the embedded Card and downstream dependencies after repair.

### R4 — P2: Main P-EAGLE comparator is too generic for a report about what the gain establishes

Affected: `c1-card.json` `p-blog-setup`/`p-blog-speed`/verification as appropriate, embedded Card, Draft b2 and manuscript's main benchmark paragraph.

The manuscript describes 'EAGLE-3比' but does not preserve that this is the blog's publicly available vanilla EAGLE-3 checkpoint. The Card stores the P-EAGLE 4-layer setup yet does not explicitly identify that checkpoint baseline either. The paper's separately trained/HCA baseline is acknowledged elsewhere in the Card; this makes source-specific checkpoint identity consequential, not interchangeable framework nomenclature. In addition, the reader receives no indication in the main comparison that a specific 4-layer trained P-EAGLE drafter and improved acceptance length contribute to the measured gain. The text could be read as isolating only sequential versus parallel order.

Source: P-EAGLE blog 'vLLM Benchmarking on P-EAGLE' and acceptance-length discussion; paper section5.1 for the separately trained HCA baseline. The blog says comparison is with the publicly available vanilla EAGLE-3 checkpoint, uses a 4-layer P-EAGLE model, and says improved acceptance length also drives throughput.

Required disposition: bind the main comparison to its actual released vanilla checkpoint baseline and preserve the important capacity/acceptance qualification so that the speedup is not presented as a controlled causal estimate for parallel ordering alone. No need to reproduce the entire training recipe or every acceptance-length number. Keep the paper's baseline distinct and update affected references.

## Optional improvements (non-blocking)

- O1: b4 acknowledges the DFlash same-data LLaMA comparison but says only that it exists. A concise indication of its observed direction plus its separate SGLang/Spec-v1 context would better show the rival's substantive evidence. A numerical table is unnecessary. C2 is already meaningfully consumed via method, training, actual SGLang performance and deployment limitation, so this is not a finding that DFlash was omitted wholesale.
- O2: Define K when it first appears and lightly explain draft/target in Japanese. The manuscript is navigable for specialists but uses a dense mix of English nouns; the primary reader question concerns interpretation, and these definitions would reduce prerequisite knowledge. This does not require a wholesale style rewrite.

## Aspects that meet the bounded requirements

The March13 report is selected as a report rather than a new method launch; February P-EAGLE/DFlash research is treated as prior background. DFlash v2 content is not used. The blog's 1.69x denominator, single B200/GPT-OSS20B case, workload/concurrency, optimized K and load-dependent gains are otherwise preserved. DFlash's 5.1x is correctly over non-speculative AR, on Qwen3-8B Math500/C1 under SGLang FA4/Spec-v2, and is explicitly not ranked against P-EAGLE's 1.69x. Target verification, dedicated draft training, the P-EAGLE PR36684 patch, benchmark configuration, verification cost and unproven SLA/total cost are carried to the reader.

C3 is substantively dispositioned: its Card describes what implementation report it is, explicit March30 label, real prerequisite and unknown before-cutoff availability; View/Selection HOLD and Package exclusion are consistent. The text does not infer that the implementation first existed on March30. Its additional prompt-only/disk-write/connector limitations from the source-first expectation need not be exhaustively copied when the source is excluded for the stated temporal reason and supports no manuscript claim. No further history investigation is required to justify this bounded HOLD.

Meaningful provenance: apart from identified missing/misleading Card content, Draft references support their nearby statements, named coverage/boundary mappings correspond to relevant blocks, and source bytes are bound through Tasks. No affirmative current Draft claim demonstrably requires a source outside the named Cards. Root necessarily saw raw sources while authoring Cards; the design is not a fresh-context isolation experiment. `raw_sources_forbidden` at drafting is therefore not proof of cognitive non-exposure. The present assessment can establish attributable output support, not absence of source-memory influence. Review independently rereads source bytes and must count this work.

## Review work record

Read preflight and r1 freeze; verified all16 file hashes; read candidates and local records. One combined output was truncated inside repeated embedded Card content; a focused followup verified exact embedded objects and printed all nonembedded package fields. Manuscript rendering and all27 ID/subject/role references were checked with Python standard library. Reread original P-EAGLE Table10/section5.3 and title/abstract/author context; DFlash section5.1 prose and section5.3/Table3 and section5.4.1/Table4, with other source facts retained from frozen source-first examination. No network followups, benchmark execution, external messages, candidate editing or replacement prose.

Tools: functions.exec + exec_command (PowerShell/Python json/hashlib/HTMLParser) and clock, plus coordination message to root. Existing source-first assessment cost remains separate and is not waived. Active reasoning time, model-token/billing usage and strictly allocatable role times remain unknown; elapsed wall time includes all review operations and reasoning. No account quota or character count converted to usage.

Observed r1-review start: 2026-09-12T06:51:25+00:00. Findings write time: 2026-09-12T06:54:07.783379+00:00. Elapsed wall time: 162.8 seconds.
