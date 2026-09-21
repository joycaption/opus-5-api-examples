#!/usr/bin/env python3
"""Minimal Claude Opus 5 request.

Model ID claude-opus-5 comes from the platform docs. Thinking is on by
default for this model, so the response can contain a thinking block
before the text block; only text blocks are printed here.

Usage: ANTHROPIC_API_KEY=... python3 examples/quickstart.py
"""
import os
import sys

import anthropic

MODEL = "claude-opus-5"


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("set ANTHROPIC_API_KEY in the environment first")

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY

    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,  # well below the 128k ceiling; raise with streaming
        messages=[
            {
                "role": "user",
                "content": "In three bullet points, explain what an STL file is.",
            }
        ],
    )

    for block in response.content:
        if block.type == "text":
            print(block.text)

    usage = response.usage
    print("---")
    print(f"model: {response.model}")
    print(f"stop_reason: {response.stop_reason}")
    print(f"input_tokens: {usage.input_tokens}  output_tokens: {usage.output_tokens}")


if __name__ == "__main__":
    main()
