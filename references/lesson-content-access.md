# Workshop-scoped lesson identity

## Resolve, do not guess

Human20 has separate workshop cohorts. `human20` identifies Cursor + OpenClaw;
`human20-codex-hermes` identifies Codex + Hermes. An active community subscription,
manual tariff label, valid token or access to one cohort does not authorize all
workshop lessons. Token authentication and item authorization are separate.

Resolve the requested workshop from the user's intent and live catalog. Ask only
when the intended cohort cannot be established. For every numbered lesson, obtain
the current lesson catalog first, then preserve its exact ID and workshop scope.
Use the returned title and sequence label to match the requested lesson. Never
build `lesson-N`, substitute prefixes, or silently fetch another cohort's item.

`get_workshop` can present a different or stale lesson list. Use `get_section`
for current lesson discovery; do not invent missing entries. If listing itself is
denied, stop and report the exact scope/error, not an inferred token problem.

## Direct MCP commands

Run from the standalone helper repository root. These read-only calls reuse the
existing local Human20 token; never paste the token into a command or report.
For a request explicitly about Codex + Hermes, discover first:

```bash
python3 scripts/human20_mcp_client.py tools/call --tool get_section --args '{"section":"lessons","workshop_id":"human20-codex-hermes"}'
```

Only if the current catalog confirms these IDs, retrieve their details:

```bash
python3 scripts/human20_mcp_client.py tools/call --tool get_content_detail --args '{"item_id":"june-lesson-4","workshop_id":"human20-codex-hermes"}'
python3 scripts/human20_mcp_client.py tools/call --tool get_content_detail --args '{"item_id":"jun-lesson-5","workshop_id":"human20-codex-hermes"}'
python3 scripts/human20_mcp_client.py tools/call --tool get_content_detail --args '{"item_id":"jun-lesson-6","workshop_id":"human20-codex-hermes"}'
```

These illustrate literal, non-uniform IDs, not a permanent alias table. The live
catalog wins. `lesson-4`, `lesson-5` and `lesson-6` identify different,
Cursor + OpenClaw materials; changing only `workshop_id` does not remap them.

The generic direct client forwards `workshop_id` as a tool argument. Legacy
entrypoint/helper-flow numbered shortcuts do not resolve arbitrary cohorts;
use the scoped direct calls rather than treating `урок 4` as globally unique.
This guidance does not claim the legacy parser was upgraded.

## Diagnose a content-only denial

1. If `get_profile`/`get_progress` work but lesson detail returns
   `403 Workshop access required`, first compare the requested item with the
   selected catalog and its actual `workshopId`.
2. Retry only with a catalog-confirmed item from the intended workshop. Preserve
   exact IDs in detail, transcript and homework calls; pass workshop scope where
   the tool supports it. Verify the returned item before using its content.
3. If correct IDs work, explain the cohort mismatch. Do not regenerate a valid
   token, grant another workshop, or weaken authorization to mask it.
4. If the matching item remains denied, report the exact tool, item, workshop and
   non-secret error. Route a genuine entitlement issue to the authorized operator.
   Never ask for a token in a group or reveal private account/access history.

A local/backend-handler probe is not an authenticated end-to-end MCP request;
label that evidence boundary accurately. Do not claim the user's token was
verified unless an authorized request actually used it.
