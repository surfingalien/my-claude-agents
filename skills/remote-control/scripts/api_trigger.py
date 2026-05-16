#!/usr/bin/env python3
"""
Trigger a Claude session via the Anthropic Messages API.
Usage: python api_trigger.py "your prompt" [--model MODEL] [--max-tokens N] [--json]
"""
import argparse
import json
import os
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a prompt to Claude via the API")
    parser.add_argument("prompt", help="Prompt to send to Claude")
    parser.add_argument("--model", default="claude-sonnet-4-6", help="Model ID")
    parser.add_argument("--max-tokens", type=int, default=4096, dest="max_tokens")
    parser.add_argument("--system", default="", help="Optional system prompt")
    parser.add_argument("--json", action="store_true", help="Output raw JSON response")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    try:
        import anthropic
    except ImportError:
        print("Error: anthropic package not installed. Run: pip install anthropic", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    create_kwargs: dict = {
        "model": args.model,
        "max_tokens": args.max_tokens,
        "messages": [{"role": "user", "content": args.prompt}],
    }
    if args.system:
        create_kwargs["system"] = args.system

    if args.json:
        response = client.messages.create(**create_kwargs)
        print(json.dumps(response.model_dump(), indent=2))
        return

    print(f"[remote-control] model={args.model} max_tokens={args.max_tokens}", file=sys.stderr)
    print("-" * 60, file=sys.stderr)

    with client.messages.stream(**create_kwargs) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    print()  # trailing newline


if __name__ == "__main__":
    main()
