---
mode: agent
description: Parse a JUnit XML test result file and produce an AI summary using this repo's main.py.
---

Parse the JUnit-style XML test result file at `${input:path:sample_test_results.xml}`
and produce an AI-generated summary using this repo's `main.py`. Run it
instead of writing new parsing code.

Steps:

1. Check that `OPENAI_API_KEY` is set in the environment. If it isn't, tell
   the user and offer to run with `--no-ai` instead to just show the parsed
   report (no key needed for that path).
2. From the repo root, run:
   `python main.py ${input:path:sample_test_results.xml} ${input:extraArgs:}`
3. Show both parts of the output: the raw counts/report, and the AI summary
   underneath it.
4. Call out anything the summary flags as likely flakiness/infra vs. a real
   regression.

Notes:

- Default model is `gpt-4o-mini` (see `DEFAULT_MODEL` in `main.py`).
- This only reads local files. If the report needs to be pulled from an
  Azure Pipeline run first, see the "Pulling the test report from an Azure
  Pipeline" section in `docs/README.md`, then run this prompt against the
  downloaded file.
