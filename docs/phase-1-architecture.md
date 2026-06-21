# Phase 1 Architecture — Local Test Report Summary

Scope: just what runs today for the Friday demo. Single process, one
machine, one outbound call (OpenAI). No Azure DevOps, no notifications —
those are [Phase 2](phase-2-pipeline-automation.md) and
[Phase 3](phase-3-triage-and-escalation.md). For the full long-term system
diagram, see [architecture.mmd](architecture.mmd).

Diagram source: [phase-1-architecture.mmd](phase-1-architecture.mmd).

## Components

| Step | Function (in `main.py`) | What it does |
|---|---|---|
| 1 | `parse_junit_xml` | Reads the XML, walks `testsuite`/`testcase` elements, builds a list of `TestCaseResult` (status: passed/failed/error/skipped, plus message/details for failures). |
| 2 | `build_report_text` | Aggregates pass/fail/error/skip counts and renders one line per test case into a plain-text report. |
| 3 | `summarize_with_ai` | Sends the report text to OpenAI chat completions with a QA-engineer system prompt (group failures, call out root causes, flag flakiness vs. real regressions); returns the summary text. Skipped entirely if `--no-ai` is passed. |
| 4 | `main` (CLI) | Wires the above together, prints the raw report then the AI summary to the console. |

## Inputs / config

- **File path** — CLI arg, defaults to `sample_test_results.xml`.
- **`OPENAI_API_KEY`** — required env var unless `--no-ai` is used.
- **`--model`** — overrides the default `gpt-4o-mini`.

## Demo notes

Walk through left to right: show the XML file, run the command, point out
the raw report first (so the audience sees what the AI is working from),
then the AI summary underneath it. See the checklist in
[phase-1-local-summary.md](phase-1-local-summary.md) for the run-through steps.
