# Phase 3 — Automated Triage and Escalation

## Status
Future — deferred until Phase 2 is stable. This is the hard part and
intentionally not scoped in detail yet.

## Goal
Replace the manual process testers do today: read the failure, figure out
which test/module it belongs to, find who last touched that code, and (if
several commits landed since the last green build) work out which commit
actually broke it.

## Scope (rough)
- **Test to owner mapping**: a maintained table (CODEOWNERS-style or a
  simple config file) mapping test class/namespace to an owning team or
  person.
- **Culprit commit lookup**: given a failing test and the commit range
  since the last known-good nightly build (via the Azure DevOps Build and
  Git Commit History APIs), narrow down to the commit(s) most likely
  responsible — most realistically via a heuristic (e.g., commits touching
  files/paths the failing test exercises), not true bisection (re-running
  tests per commit), which is too slow/expensive for a nightly job.
- **Enriched report**: merge the AI summary with owner + likely-culprit-
  commit info.
- **Escalation actions**: notify the responsible person directly (Teams DM)
  and/or auto-file an Azure Boards bug assigned to them.

## Known risks
- Heuristic commit attribution can misfire when multiple commits touch the
  same file — may finger the wrong person.
- The owner mapping is new state someone has to create and keep current; it
  will go stale if not maintained.
- False positives/misattributions could erode trust in the tool faster than
  manual triage would.

## Dependencies
- [Phase 2](phase-2-pipeline-automation.md) running reliably in production.
- A first cut of the test to owner mapping (needs input from team leads,
  not just engineering).
