---
name: project-status
description: |
  Orient on the test-result-summarizer project: current phase status, what's
  built vs. planned, and where the docs/code live. Use when asked "what is
  this project", "what should we build next", "what phase are we on", or
  when starting fresh work in this repo without prior context.
allowed-tools:
  - Read
  - Glob
---

# Project Orientation: test-result-summarizer

A CLI tool that parses JUnit XML test results and generates an AI summary
(OpenAI) for QA teams. Long-term goal: automate failure triage all the way
from an Azure DevOps nightly build down to "who broke it and what commit."

## Where to look

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

## When asked "what should we build next"

1. Read the three phase docs and check each one's `Status` line — don't
   assume it's still accurate from memory, re-check the file.
2. Phase 2 is the active next step unless told otherwise. It needs: (a) a
   pipeline stage added after the test step, (b) `OPENAI_API_KEY` as a
   pipeline secret, (c) a Teams Incoming Webhook integration added to the
   tool.
3. Phase 3 should not be started before Phase 2 is stable — it depends on a
   test-to-owner mapping that doesn't exist yet and needs input from team
   leads, not just engineering.

## When asked "what is this project"

Summarize in a few sentences using the intro of `docs/README.md`, then point
to whichever phase is currently in progress (per the Status lines) rather
than re-explaining the entire roadmap unprompted.
