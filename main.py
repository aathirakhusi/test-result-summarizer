#!/usr/bin/env python3
import argparse
import os
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from openai import OpenAI

DEFAULT_RESULTS_FILE = Path(__file__).parent / "sample_test_results.xml"
DEFAULT_MODEL = "gpt-4o-mini"


@dataclass
class TestCaseResult:
    classname: str
    name: str
    time: float
    status: str  # "passed", "failed", "error", "skipped"
    message: str = ""
    details: str = ""


def parse_junit_xml(path: Path) -> list[TestCaseResult]:
    root = ET.parse(path).getroot()
    suites = root.findall(".//testsuite") if root.tag == "testsuites" else [root]

    results = []
    for suite in suites:
        for case in suite.findall("testcase"):
            classname = case.get("classname", suite.get("name", ""))
            name = case.get("name", "")
            time = float(case.get("time", 0) or 0)

            failure = case.find("failure")
            error = case.find("error")
            skipped = case.find("skipped")

            if failure is not None:
                results.append(TestCaseResult(classname, name, time, "failed",
                                               failure.get("message", ""),
                                               (failure.text or "").strip()))
            elif error is not None:
                results.append(TestCaseResult(classname, name, time, "error",
                                               error.get("message", ""),
                                               (error.text or "").strip()))
            elif skipped is not None:
                results.append(TestCaseResult(classname, name, time, "skipped",
                                               skipped.get("message", "")))
            else:
                results.append(TestCaseResult(classname, name, time, "passed"))

    return results


def build_report_text(results: list[TestCaseResult]) -> str:
    total = len(results)
    passed = sum(1 for r in results if r.status == "passed")
    failed = sum(1 for r in results if r.status == "failed")
    errors = sum(1 for r in results if r.status == "error")
    skipped = sum(1 for r in results if r.status == "skipped")

    lines = [
        f"Total: {total}  Passed: {passed}  Failed: {failed}  Errors: {errors}  Skipped: {skipped}",
        "",
    ]
    for r in results:
        lines.append(f"[{r.status.upper()}] {r.classname}.{r.name} ({r.time:.3f}s)")
        if r.message:
            lines.append(f"  message: {r.message}")
        if r.details:
            lines.append(f"  details: {r.details}")
    return "\n".join(lines)


def summarize_with_ai(report_text: str, model: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

    client = OpenAI(api_key=api_key)

    system_prompt = (
        "You are a senior QA engineer summarizing an automated test run for your team. "
        "Be concise. Group related failures, call out likely root causes, and flag anything "
        "that looks like flakiness/infrastructure issues versus a real regression. "
        "Plain text only, short headers and bullet points, no markdown tables."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here is the test run report:\n\n{report_text}\n\nSummarize it."},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser(description="Read a JUnit-style test result XML file and summarize it with AI.")
    parser.add_argument("file", nargs="?", default=str(DEFAULT_RESULTS_FILE), help="Path to the JUnit XML test result file")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model to use (default: %(default)s)")
    parser.add_argument("--no-ai", action="store_true", help="Skip the AI summary and just print the parsed report")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"Error: test result file not found: {path}", file=sys.stderr)
        sys.exit(1)

    results = parse_junit_xml(path)
    report_text = build_report_text(results)

    print("=" * 70)
    print(f"TEST RESULTS - {path.name}")
    print("=" * 70)
    print(report_text)
    print()

    if args.no_ai:
        return

    print("=" * 70)
    print("AI SUMMARY")
    print("=" * 70)
    try:
        summary = summarize_with_ai(report_text, args.model)
        print(summary)
    except Exception as exc:
        print(f"Could not generate AI summary: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
