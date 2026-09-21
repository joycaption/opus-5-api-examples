#!/usr/bin/env python3
"""Run one prompt on Claude Opus 5 at several effort levels.

The launch post describes effort as the setting customers use to
"optimize for intelligence or conserve tokens". The docs note thinking
can be disabled only at effort high or below; this script leaves
thinking at its default (on) and only varies effort.

Usage: ANTHROPIC_API_KEY=... python3 examples/effort_levels.py
"""
import os
import sys
import time

import anthropic

MODEL = "claude-opus-5"
LEVELS = ["low", "medium", "high", "xhigh"]
PROMPT = (
    "A 3D printer nozzle is 0.4 mm. A logo has strokes 0.3 mm wide. "
    "Will they print? Answer in two sentences."
)


def run(client, effort):
    started = time.monotonic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        output_config={"effort": effort},
        messages=[{"role": "user", "content": PROMPT}],
    )
    seconds = time.monotonic() - started
    text = "".join(b.text for b in response.content if b.type == "text")
    return response.usage.output_tokens, seconds, text


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("set ANTHROPIC_API_KEY in the environment first")
    client = anthropic.Anthropic()

    print(f"{'effort':8} {'out_tok':>8} {'seconds':>8}")
    for level in LEVELS:
        out_tokens, seconds, text = run(client, level)
        print(f"{level:8} {out_tokens:>8} {seconds:>8.1f}")
        print(f"    {text.strip()[:160]}")


if __name__ == "__main__":
    main()
