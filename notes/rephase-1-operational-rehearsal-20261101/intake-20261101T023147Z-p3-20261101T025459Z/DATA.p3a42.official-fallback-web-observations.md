# Official fallback web observations

Status: bounded Discovery-stage observations for Sol review; no Screening, Evidence, Materiality, Selection, or Architecture disposition is assigned here.

The repository-owned fallback collector was intentionally exercised first. Its run was partial because several first-party hosts timed out or returned an error. The observations below use direct first-party pages reached through the public Web as a bounded fallback. They are recorded with the URL and date shown by the source; they do not turn an index page or an inaccessible lane into a negative-space closure.

## AWS Bedrock / AgentCore

| First-party page | Date shown | Discovery observation |
| --- | --- | --- |
| [AgentCore payments GA](https://aws.amazon.com/about-aws/whats-new/2026/08/bedrock-agentcore-payments-ga/) | Aug 18, 2026 | AgentCore payments general availability; supports agents discovering/accessing/ paying for paid APIs, MCPs, and content. |
| [AgentCore Web Search filters](https://aws.amazon.com/about-aws/whats-new/2026/08/web-search-amazon-bedrock/) | Aug 19, 2026 | Web Search added per-request domain and published-date filtering and expanded to Europe and Tokyo. |
| [AgentCore Memory JSON payloads](https://aws.amazon.com/about-aws/whats-new/2026/08/agentcore-memory-json-payloads/) | Aug 20, 2026 | AgentCore Memory accepted non-conversational JSON payloads for memory extraction. |

These are distinct AWS service capability events. They are not collapsed into one Bedrock “launch”, and the dates are kept as provider announcement chronology. The AWS index, ML blog, and several documentation routes remained inaccessible to the repository collector during this run; the direct What’s New pages close only the specific observations above.

## xAI

- [Introducing Grok 4.6](https://x.ai/news/grok-4-6) is a first-party page dated Aug 12, 2026, therefore pre-window. It describes Grok 4.6 availability in Grok Build/Cursor and API/partners, but it is not an in-window W34 release event on this date.
- The repository collector separately succeeded on the xAI models and release-notes routes. The xAI root returned 403 and the guessed Grok Build URL returned 404; those are retrieval gaps, not evidence that no other in-window xAI event exists.

## Microsoft / Azure / GitHub

- The repository collector succeeded on the Microsoft Learn OpenAI “What’s new” route and on the GitHub Copilot Slack, Teams, and JetBrains changelog pages. Those findings are retained as source-intake material and reconciled against existing W34 event rows rather than duplicated.
- The direct [Microsoft Foundry/Azure OpenAI “What’s new” page](https://learn.microsoft.com/en-us/azure/foundry-classic/openai/whats-new) was reachable but exposes an authorization notice and an older dated index in the rendered view; it did not provide a new W34-dated event beyond the already captured GitHub/Microsoft surfaces.

## IBM

- The [IBM AI press-release index](https://newsroom.ibm.com/press-releases-artificial-intelligence) was reachable through the Web fallback. The visible chronology showed IBM/OpenAI on Aug 13 (pre-window), no new Aug 14–21 AI press-release row in the visible result set, and later Aug 24–Sep 2 material (post-cutoff). This is a bounded index observation, not a claim that all IBM technical material was exhaustively retrieved.
- IBM newsroom and developer routes remained timeout-prone in the repository collector; an IBM-specific technical-channel gap remains open for Sol's completeness review.

## Other fallback lane status

- Alibaba lifecycle chronology was recovered in a separate [Model Studio observation](./alibaba-model-lifecycle-official-web.md).
- Google Cloud Vertex documentation/blog routes returned timeout/502 responses in the repository collector; no fallback observation is promoted here without a directly inspected first-party page.
- Hugging Face's official blog page was collected by the repository fallback collector. It yielded no additional W34 event that is not already represented in the refreshed inventory.
