# Phase 1 — Local Test Report Summary (MVP)

## Status
Done — ready to demo.

## Goal
Read a JUnit-style test result XML file and produce a human-readable AI
summary, run entirely from a developer's machine. This is the baseline
capability everything else builds on.

## Scope
- Parse JUnit XML (`testsuites`/`testsuite`/`testcase`, including
  `failure`/`error`/`skipped`) into structured results.
- Build a plain-text report with pass/fail/error/skip counts and per-test
  detail.
- Send that report to an LLM (OpenAI, default `gpt-4o-mini`) with a
  QA-engineer system prompt: group related failures, call out likely root
  causes, flag flakiness vs. real regressions.
- Print both the raw report and the AI summary to the console.
- `--no-ai` escape hatch to see the parsed report without calling the API.

## Out of scope
- Anything automatic ([Phase 2](phase-2-pipeline-automation.md)) or any
  notion of "whose commit broke this"
  ([Phase 3](phase-3-triage-and-escalation.md)).

## Components
- `main.py`: `parse_junit_xml`, `build_report_text`, `summarize_with_ai`,
  CLI entry point.

## Demo checklist
- [ ] `OPENAI_API_KEY` set in the shell.
- [ ] Run against a real exported nightly-build report, not just
      `sample_test_results.xml`, so the summary reflects an actual failure
      pattern.
- [ ] Walk through: raw report -> AI summary -> point out a grouped /
      likely-root-cause call-out in the output.
