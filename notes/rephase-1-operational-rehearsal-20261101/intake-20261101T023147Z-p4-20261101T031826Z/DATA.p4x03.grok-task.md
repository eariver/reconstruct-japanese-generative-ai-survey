# Grok X Source Intake Task — weekly-x-2026-W34-r2


This file is the complete execution authority for this Grok/X run.


## 1. Mission


Perform a fresh, independent X Source Intake for `2026-W34` for downstream review by ChatGPT/Sol.


This is a Source Discovery / Raw Observation task. Do not make final editorial selection, Evidence acceptance, Architecture decisions, or publication decisions.


The primary objective is high-recall discovery with auditable provenance. A previous weekly run compressed too many observations into a small number of representative links. This run must preserve the actual post-level provenance discovered during search.


## 2. Strict independence requirement


This run must be independent.


Do NOT inspect, use, summarize, compare against, or anchor on:


- any DailyX files or DailyX collection results;
- `weekly-x-2026-W34-r1` or its result;
- any ChatGPT/Sol candidate list or review cache;
- any previously prepared W34 weekly X summary.


Search X again from the specified time window using your own search process.


The downstream ChatGPT/Sol process will independently compare this r2 result with other observation corpora after you finish. You must not perform that comparison yourself.


## 3. Canonical observation window


Issue: `2026-W34`
Research Profile: `WEEKLY`


Canonical ordinary window:


- Start: `2026-08-14T18:00:00-04:00`
- End: `2026-08-21T18:00:00-04:00`
- Timezone: `America/New_York`
- Interval semantics: `[start, end)`


Equivalent JST window:


- `2026-08-15 07:00 JST`
- through `2026-08-22 07:00 JST`, end-exclusive.


Do not silently include posts outside this window as ordinary-window observations.


Material after the cutoff may be mentioned only in a clearly separated `Late Breaking` section and must not be mixed into ordinary-window counts.


## 4. Search objective


Search broadly enough to detect technically material generative-AI developments and community momentum, including both official posts and independent technical observations.


At minimum cover these lanes independently:


- frontier / proprietary foundation models;
- open-weight / open-source models;
- multimodal / vision-language models;
- image generation / editing;
- video generation;
- speech / TTS / audio / music generation;
- coding models and coding agents;
- general agents, computer use, browser use, tool use, MCP;
- inference serving, routing, KV/cache, quantization, local inference;
- model distribution and cloud/platform availability;
- research papers, benchmarks, reproduction, evaluation;
- safety, alignment, cybersecurity, misuse, provenance/watermarking;
- AI infrastructure / accelerators where directly relevant to generative AI;
- developer tooling and production workflow integration;
- significant adoption, integration, deployment, failure, regression, or operational constraints;
- technically meaningful policy/regulatory developments that directly affect generative-AI systems.


Do not assume that a lane with low initial search visibility has no material activity. Use multiple query formulations and account-focused searches where useful.


## 5. High-recall search behavior


This is not a “top 5 news” task.


Search broadly first, then cluster duplicates later.


When useful, combine:


- keyword search;
- semantic search;
- official-account search;
- product/model name search;
- repository/project name search;
- benchmark name search;
- technical terms such as release, weights, API, GA, preview, benchmark, eval, reproduction, local, quantization, inference, agent, MCP, computer use, multimodal, image, video, audio, TTS, safety, security, pricing, deployment, integration.


A target of 10–30 topic clusters is reasonable when the week is active, but there is no hard topic-count ceiling. Do not suppress a technically distinct development merely to keep the report short.


## 6. Post-level provenance preservation — mandatory


This is the critical requirement for r2.


Every X post that materially contributes to a retained observation must have its exact URL preserved.


Do not replace a set of discovered posts with phrases such as:


- “multiple posts”;
- “several developers”;
- “community reactions”;
- “many users reported”;
- “representative posts”; or
- “widely discussed”


without also preserving the exact URLs of the material posts that support that statement.


You may deduplicate literal duplicate URLs, but do not discard distinct posts simply because they discuss the same event. Official announcement, technical follow-up, independent reproduction, benchmark result, failure report, integration example, and substantive counterevidence may all be separately valuable.


There is no artificial maximum number of X URLs to retain.


If you inspect a post and use it to form a retained observation, preserve its URL unless it is clearly irrelevant, spam, pure repost without added information, or otherwise excluded under the quality rules below.


Never invent or reconstruct an X URL.


## 7. Distinguish post roles


For each retained X post, classify its role using one or more of:


- `OFFICIAL_ANNOUNCEMENT`
- `OFFICIAL_TECHNICAL_FOLLOWUP`
- `AUTHOR_RESEARCH_POST`
- `INDEPENDENT_REPRODUCTION`
- `INDEPENDENT_BENCHMARK`
- `INTEGRATION_OR_DEPLOYMENT`
- `PERFORMANCE_OBSERVATION`
- `FAILURE_OR_REGRESSION`
- `SECURITY_OR_SAFETY_OBSERVATION`
- `COMMUNITY_ANALYSIS`
- `REPORTING_OR_SECONDARY`
- `OTHER_TECHNICAL_SIGNAL`


Do not equate official status with truth of performance claims. Preserve maker-reported benchmark claims as claims requiring downstream verification.


## 8. W33-origin topics


A topic whose original release occurred before W34 may still be retained only when there is a genuinely new W34 delta, for example:


- new weights or quantization;
- new cloud/platform distribution;
- new benchmark or reproduction;
- new integration/deployment;
- new pricing/access condition;
- newly observed regression or constraint;
- new safety/security evidence;
- material adoption momentum with concrete technical evidence.


Do not restate an old release as a W34 release.


Record both:


- `original_event_before_window: yes/no/unknown`
- `new_w34_delta`


for such clusters.


## 9. Primary-source links referenced by X posts


When an X post directly links to a first-party announcement, paper, repository, model card, benchmark page, or official documentation, preserve that non-X URL as a locator.


Do not perform final technical verification of every primary source in this task. Downstream ChatGPT/Sol will do that.


Separate:


- what the X post says;
- what the linked primary artifact appears to be;
- what remains unverified.


## 10. Required outputs


Save all outputs in the same run folder as this task file.


### Output A — `grok-x-result.md`


Required structure:


```markdown
---
sensor: grok-x-source-intake
task_id: "weekly-x-2026-W34-r2"
issue_id: "2026-W34"
status: raw
---


# Run metadata


- observation window:
- search methods used:
- search limitations:
- total retained topic clusters:
- total unique ordinary-window X URLs:
- total official-account X URLs:
- total independent technical X URLs:
- total linked non-X primary-source URLs:


# Observation summary


# Topic clusters


## Cluster <n>: <title>


- Category:
- Importance signal: High / Medium / Low
- Confidence of observation: Confirmed / Likely / Unverified
- Original event before window: yes / no / unknown
- New W34 delta:
- Primary-source locator(s):


### X posts


| X URL | Author / handle | Posted time | Role | What this post contributes | Claim status |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | official / observed / author-claim / unverified |


### Observation


### Follow-up for ChatGPT/Sol


# Cross-cutting patterns


# Late Breaking


# Coverage assessment
```


Topic-level prose must not be used as a substitute for the X-post table.


### Output B — `x-url-ledger.tsv`


This is mandatory and must be post-level, not topic-level.


UTF-8 TSV with one row per unique retained X URL and this exact header:


```text
x_url\tposted_at\tauthor_handle\tauthor_display_name\ttopic_cluster_id\troles\twindow_status\tofficial_account\tlinked_primary_url\tobservation_summary\tclaim_status
```


Rules:


- one exact X URL per row;
- no invented URLs;
- `window_status` must be `ORDINARY_WINDOW`, `LATE_BREAKING`, or `BACKGROUND_ONLY`;
- ordinary-window URL count in this ledger must equal the count reported in `grok-x-result.md`;
- if one post contributes to multiple clusters, keep one row and separate cluster IDs with `;`;
- preserve linked primary URL(s), separated by `;` if necessary.


### Output C — `search-accounting.md`


Record enough search accounting to audit coverage without exposing private chain-of-thought.


Include:


- major search lanes attempted;
- representative search terms / account searches;
- lanes where no useful results were found;
- known X search limitations;
- count of retained URLs by role;
- count of retained URLs by topic cluster;
- count of exclusions by broad reason if practical (`duplicate`, `spam`, `pure repost`, `out of window`, `not technically relevant`).


Do not include hidden reasoning or internal chain-of-thought.


## 11. Quality / exclusion rules


Exclude or down-rank:


- pure reposts with no added technical content when the original is available;
- engagement bait, memes, vague hype;
- unsupported price/performance claims with no useful provenance, unless the claim itself is materially influential and is clearly marked unverified;
- ordinary news aggregation when a primary or more direct technical post is available;
- posts outside the ordinary window, except clearly separated background or Late Breaking;
- irrelevant general AI commentary.


Do NOT exclude a low-engagement post merely because it is low engagement if it contains concrete technical evidence.


## 12. Validation before completion


Before declaring the run complete, validate:


1. `grok-x-result.md`, `x-url-ledger.tsv`, and `search-accounting.md` all exist.
2. Every retained material post in the report has an exact X URL in the ledger.
3. Every ordinary-window URL in the ledger satisfies the canonical time window.
4. The ordinary-window unique URL count matches between the report and ledger.
5. No topic says “multiple/several/many posts” while omitting the corresponding material URLs.
6. Topic clusters preserve distinctions between official announcement, independent reproduction, benchmark, integration, and failure reports when those exist.
7. Old releases are not falsely dated as W34 releases.
8. Late Breaking is excluded from ordinary-window counts.
9. No DailyX file, prior W34 weekly X result, or ChatGPT/Sol W34 candidate list was used as search input or comparison material.


If a required validation fails, correct the output before finishing.


## 13. Stop condition


When the three output files are saved and validation passes, stop and report:


- run folder path;
- total topic clusters;
- total unique ordinary-window X URLs;
- total unique Late Breaking X URLs;
- total linked non-X primary-source URLs;
- any material search limitation.


Do not perform downstream Evidence acceptance or editorial selection.