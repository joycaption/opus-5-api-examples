#!/usr/bin/env python3
"""Change the tool list between turns on Claude Opus 5 (beta).

The platform docs describe mid-conversation tool changes as a beta that
lets you add or remove tools between turns while preserving the prompt
cache, and give the header mid-conversation-tool-changes-2026-07-01.
The tool schemas below are illustrative; nothing is executed, the
script only prints what the model asked to call.

Usage: ANTHROPIC_API_KEY=... python3 examples/tool_changes_beta.py
"""
import os
import sys

import anthropic

MODEL = "claude-opus-5"
BETA = "mid-conversation-tool-changes-2026-07-01"

WEATHER = {
    "name": "get_weather",
    "description": "Current weather for a city (illustrative tool).",
    "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
    },
}
CONVERT = {
    "name": "convert_units",
    "description": "Convert a temperature between C and F (illustrative tool).",
    "input_schema": {
        "type": "object",
        "properties": {
            "value": {"type": "number"},
            "to": {"type": "string", "enum": ["C", "F"]},
        },
        "required": ["value", "to"],
    },
}


def show_tool_calls(response):
    for block in response.content:
        if block.type == "tool_use":
            print(f"  tool_use: {block.name} {block.input}")
        elif block.type == "text":
            print(f"  text: {block.text[:120]}")


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("set ANTHROPIC_API_KEY in the environment first")
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": "What is the weather in Lisbon?"}]

    print("turn 1: tools = [get_weather]")
    first = client.beta.messages.create(
        model=MODEL, max_tokens=1024, betas=[BETA],
        tools=[WEATHER], messages=messages,
    )
    show_tool_calls(first)

    # Pretend the tool ran and returned a value (illustrative).
    messages.append({"role": "assistant", "content": first.content})
    tool_results = [
        {"type": "tool_result", "tool_use_id": b.id, "content": "22 C, clear"}
        for b in first.content if b.type == "tool_use"
    ]
    messages.append({"role": "user", "content": tool_results or "ok"})
    messages.append({"role": "user", "content": "Now give me that in Fahrenheit."})

    print("turn 2: tools = [get_weather, convert_units]  (list changed mid-conversation)")
    second = client.beta.messages.create(
        model=MODEL, max_tokens=1024, betas=[BETA],
        tools=[WEATHER, CONVERT], messages=messages,
    )
    show_tool_calls(second)


if __name__ == "__main__":
    main()
