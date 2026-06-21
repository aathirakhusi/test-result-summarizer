# Test Result Summarizer

Parses a JUnit-style XML test result file and produces a concise, AI-generated
summary (root causes, flaky vs. real failures, etc.) using the OpenAI API.

> All commands below assume you're in the repo root (one level up from this
> `docs/` folder), since that's where `main.py` and `requirements.txt` live.

## Prerequisites

- Python 3.10+ (the script uses `list[...]` type hints)
- An OpenAI API key (only needed for the AI summary step)
- Optional: [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) with the `azure-devops` extension, if you want to pull results straight from a pipeline run

## Setup (local)

```powershell
# from the project root
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# set your API key for the current session
$env:OPENAI_API_KEY = "sk-..."
```

## Running locally

```powershell
# uses the bundled sample_test_results.xml and gpt-4o-mini
python main.py

# point at your own JUnit XML file
python main.py path\to\results.xml

# use a different model
python main.py path\to\results.xml --model gpt-4o

# skip the AI call and just print the parsed report (no API key needed)
python main.py path\to\results.xml --no-ai
```

The script prints the parsed report first, then the AI summary underneath.

## Pulling the test report from an Azure Pipeline

This tool reads a JUnit XML file from disk, so the goal is to get that file out
of the pipeline run and onto your machine (or CI agent), then feed it to
`main.py`.

### Prerequisite: publish the XML as a pipeline artifact

Your pipeline needs to actually keep the raw XML around. The `PublishTestResults`
task alone is not enough — it uploads results into Azure Test Plans/Analytics, not
as a downloadable file. Add a step to publish it as a build artifact too, e.g.:

```yaml
- task: PublishPipelineArtifact@1
  inputs:
    targetPath: '$(Common.TestResultsDirectory)/results.xml'
    artifact: 'test-results'
```

### Option 1: Azure CLI

```powershell
az login
az devops configure --defaults organization=https://dev.azure.com/<org> project=<project>

# find the latest completed run for a pipeline
$runId = az pipelines runs list --pipeline-ids <pipeline-id> --status completed --top 1 --query "[0].id" -o tsv

# download the published artifact into .\artifacts
az pipelines runs artifact download --run-id $runId --artifact-name test-results --path .\artifacts

# summarize it
python main.py .\artifacts\results.xml
```

### Option 2: REST API (no Azure CLI)

Useful for scripting this into another tool, or if you only have a Personal
Access Token (PAT).

```powershell
$org = "<org>"
$project = "<project>"
$buildId = "<build-id>"
$pat = $env:AZDO_PAT   # PAT with "Build (Read)" scope

$headers = @{ Authorization = "Basic " + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$pat")) }

$artifact = Invoke-RestMethod -Headers $headers `
  -Uri "https://dev.azure.com/$org/$project/_apis/build/builds/$buildId/artifacts?artifactName=test-results&api-version=7.1-preview.5"

Invoke-WebRequest -Headers $headers -Uri $artifact.resource.downloadUrl -OutFile artifact.zip
Expand-Archive artifact.zip -DestinationPath .\artifacts -Force

python main.py .\artifacts\test-results\results.xml
```

### If you only have Test Plans results (no XML artifact)

If the XML was never published as an artifact, you can still query results
via the [Test Runs REST API](https://learn.microsoft.com/rest/api/azure/devops/test/runs)
(`.../_apis/test/runs/{runId}/results`), but it returns JSON, not JUnit XML —
you'd need a small adapter to convert that JSON into a `TestCaseResult` list
before calling `build_report_text`/`summarize_with_ai`. Publishing the raw XML
as an artifact (Option above) is simpler and avoids writing that adapter.

## Roadmap

The long-term plan is broken into phases — see [architecture.mmd](architecture.mmd)
for the system diagram and each phase doc for scope/status:

- [Phase 1 — Local Summary](phase-1-local-summary.md) — done, this is what
  `main.py` does today.
- [Phase 2 — Pipeline Automation + Teams Notification](phase-2-pipeline-automation.md) — planned.
- [Phase 3 — Triage and Escalation](phase-3-triage-and-escalation.md) — future, deferred.

## Other ideas (not tied to a phase)

- **Other formats**: if some suites emit TRX or NUnit XML instead of JUnit,
  `parse_junit_xml` will need format detection or a separate parser.
- **Tests**: there's currently no test coverage for `parse_junit_xml` /
  `build_report_text` themselves — worth adding a few fixtures (passed-only,
  mixed failures, empty suite) to guard against regressions.
