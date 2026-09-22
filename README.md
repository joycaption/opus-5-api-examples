# Claude Opus 5 examples

*Unofficial community examples for Claude Opus 5. Not affiliated with Anthropic. All trademarks belong to their owners.*

Short Python scripts for calling Claude Opus 5 through the Anthropic Python SDK. The model ID `claude-opus-5`, the 1M token context window, the 128k max output tokens, the thinking-on-by-default behaviour and the beta header for mid-conversation tool changes all come from the platform docs page for opus 5; the effort levels come from the launch post and docs. Anything not stated there is marked illustrative in the code.

> Need image, video or audio generation next to the text model? [Try Synexa - one REST endpoint and Python SDK for FLUX, video and audio models, pay per run](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=opus-5-api-examples&utm_content=readme-top&utm_term=tier-r).

## Files

| Path | What it shows |
| --- | --- |
| `examples/quickstart.py` | Minimal `messages.create` call to `claude-opus-5` with the key read from the environment, printing text blocks and token usage. |
| `examples/effort_levels.py` | The same prompt at several `effort` settings so you can see the output-token spend change; the docs say thinking can be disabled only at `high` or below. |
| `examples/tool_changes_beta.py` | A two-turn conversation that changes the tool list between turns using the `mid-conversation-tool-changes-2026-07-01` beta header. |

## Setup

```
pip install anthropic
export ANTHROPIC_API_KEY=YOUR_KEY_HERE
```

The scripts read `ANTHROPIC_API_KEY` from the environment; none of them contain a key. Keep `max_tokens` well below the 128k ceiling unless you are streaming.

## quickstart.py

One request, one response. Opus 5 has thinking on by default, so the response may contain a `thinking` block before the `text` block; the script only prints text blocks and then the usage counts, which is what you need to start estimating cost. Check the [pricing page](https://platform.claude.com/docs/en/about-claude/pricing) for current per-token rates.

## effort_levels.py

The launch post shows performance changing with the model's effort setting, "which customers can use to optimize for intelligence or conserve tokens for faster and cheaper results", and the system-card review passes on the advice that you "may want to usually use less effort than you might expect". This script runs one prompt at `low`, `medium`, `high` and `xhigh` and prints output tokens for each, so you can see the trade-off on your own task instead of guessing. The docs also say thinking can be disabled only at effort `high` or below; the script keeps the default (thinking on) throughout.

## tool_changes_beta.py

The docs describe mid-conversation tool changes as a beta that lets you "add or remove tools between turns of a conversation while preserving the prompt cache, instead of resending a fixed tool list for the life of a session". The script sends turn one with a single weather tool, then turn two with a second tool added, passing the beta header on both requests. The tool schemas are illustrative; the script does not execute tools, it only prints what the model asked for.

## When to use Synexa instead

These scripts cover text in, text (or a tool call) out. If your product also needs to generate an image, a video clip or an audio track, an Opus-class model does not do that, and stitching a second and third vendor onto the text loop is where the integration time goes. [Try Synexa - one REST endpoint and Python SDK for FLUX, video and audio models, pay per run](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=opus-5-api-examples&utm_content=readme-top&utm_term=tier-r): keep `claude-opus-5` for planning and text, and send the media step to one endpoint.


_Last reviewed: 2026-09-22_
