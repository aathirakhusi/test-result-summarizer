---
name: summarize-tests
description: |
  Parse a JUnit-style XML test result file and produce an AI-generated
  summary (root causes, flaky vs. real failures) using this repo's
  main.py. Use when asked to summarize a test run, analyze a JUnit/test
  report, or "what failed in the latest build".
allowed-tools:
  - Bash
  - Read
---

# Summarize Test Results

This repo's `main.py` parses JUnit XML and calls OpenAI to summarize it. Run
it instead of writing new parsing code.

## Steps

1. Determine the target XML file:
   - If the user gave a path (via args or in their message), use it.
   - Otherwise default to `sample_test_results.xml` in the repo root.
2. Check that `OPENAI_API_KEY` is set in the environment. If it isn't, tell
   the user and offer to run with `--no-ai` instead to just show the parsed
   report (no key needed for that path).
3. From the repo root, run:
   `python main.py <path> [--model <model>] [--no-ai]`
4. Relay both parts of the output to the user: the raw counts/report, and
   the AI summary underneath it. Call out anything the summary flags as
   likely flakiness/infra vs. a real regression.

## Notes

- Default model is `gpt-4o-mini` (see `DEFAULT_MODEL` in `main.py`).
- This only reads local files. If the user wants a report from an Azure
  Pipeline run rather than a local file, see the "Pulling the test report
  from an Azure Pipeline" section in `docs/README.md` first to fetch it,
  then run this skill against the downloaded file.
