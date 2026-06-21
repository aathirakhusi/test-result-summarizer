# Phase 2 — Automatic Run in Azure Pipeline + Teams Notification

## Status
Planned — not started.

## Goal
Eliminate the manual "download the report and run the script" step. After
the nightly Azure DevOps pipeline produces test results, the summary should
be generated and pushed to wherever testers already look (Teams channel,
email, etc.) without anyone running anything by hand.

## Scope
- Add a pipeline stage/step that runs after the test step, in the same job,
  so the JUnit XML is already on the agent (no cross-machine artifact fetch
  needed for this path — that's only for pulling a *past* run's results onto
  a different machine, see the root README).
- Store `OPENAI_API_KEY` as a secret pipeline variable, not a local env var.
- Extend the tool to push the generated summary to a Teams channel via an
  Incoming Webhook (POST a message card), instead of only printing to
  stdout. Email is a fallback option if Teams isn't available.
- Pipeline step fails loudly (or posts a fallback "summary unavailable"
  message) if the AI call errors, rather than silently dropping the
  notification.

## Out of scope
- Mapping a failing test to an owning team/person.
- Identifying which commit caused a failure.

(Both are [Phase 3](phase-3-triage-and-escalation.md).)

## Open questions
- Final channel: Teams webhook vs. email vs. both?
- Does every nightly run post, or only runs with failures?
- Who owns the webhook URL / secret rotation?

## Dependencies
- [Phase 1](phase-1-local-summary.md) tool working as a library/CLI (done).
- A Teams channel with an Incoming Webhook connector configured.
