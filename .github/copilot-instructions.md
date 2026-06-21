# Copilot Instructions — test-result-summarizer

This is a CLI tool that parses JUnit XML test results and generates an AI
summary (OpenAI) for QA teams. Long-term goal: automate failure triage all
the way from an Azure DevOps nightly build down to "who broke it and what
commit."

## Where things live

- `main.py` — the actual tool (`parse_junit_xml`, `build_report_text`,
  `summarize_with_ai`).
- `docs/README.md` — setup, local run instructions, and how to pull results
  from an Azure Pipeline.
- `docs/architecture.mmd` — Mermaid diagram of the full planned system
  (built / planned / external-infra nodes are color-coded).
- `docs/phase-1-local-summary.md` — done. What `main.py` does today.
- `docs/phase-2-pipeline-automation.md` — planned. Run automatically after
  the Azure DevOps nightly pipeline finishes, post the AI summary to Teams.
- `docs/phase-3-triage-and-escalation.md` — future, deferred. Map failing
  tests to owning teams, identify likely culprit commits since the last
  green build, auto-escalate.

## Current priorities

- Phase 1 is done — don't re-build it; run `main.py` directly (see the
  `summarize-tests` prompt in `.github/prompts/`).
- Phase 2 is the active next step. It needs: (a) a pipeline stage added
  after the test step, (b) `OPENAI_API_KEY` as a pipeline secret, (c) a
  Teams Incoming Webhook integration added to the tool.
- Phase 3 should not be started before Phase 2 is stable — it depends on a
  test-to-owner mapping that doesn't exist yet and needs input from team
  leads, not just engineering.

When asked what this project is or what to build next, check the `Status`
line at the top of each phase doc rather than assuming it's still accurate.
