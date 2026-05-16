#!/usr/bin/env python3
"""
Webhook receiver that dispatches Claude sessions in response to HTTP events.
Usage: python webhook_receiver.py [--port PORT] [--secret SECRET]

Expects POST /webhook with JSON body:
  { "event": "pr_review", "prompt": "...", "repo": "owner/repo" }

Validates X-Hub-Signature-256 when --secret is set.
"""
import argparse
import hashlib
import hmac
import json
import os
import subprocess
import sys
import threading
from typing import Any


def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = "sha256=" + hmac.new(
        secret.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


def dispatch_claude(prompt: str, model: str, max_tokens: int) -> None:
    """Run api_trigger.py in a background thread."""
    script = os.path.join(os.path.dirname(__file__), "api_trigger.py")
    cmd = [sys.executable, script, prompt, "--model", model, "--max-tokens", str(max_tokens)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[webhook] dispatch failed: {result.stderr}", file=sys.stderr)
    else:
        print(f"[webhook] dispatch completed:\n{result.stdout[:500]}", file=sys.stderr)


def create_app(secret: str | None, model: str, max_tokens: int) -> Any:
    try:
        from flask import Flask, jsonify, request
    except ImportError:
        print("Error: flask not installed. Run: pip install flask", file=sys.stderr)
        sys.exit(1)

    app = Flask(__name__)

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"})

    @app.route("/webhook", methods=["POST"])
    def webhook():
        raw = request.get_data()

        if secret:
            sig = request.headers.get("X-Hub-Signature-256", "")
            if not sig or not verify_signature(raw, sig, secret):
                return jsonify({"error": "invalid signature"}), 401

        try:
            body = json.loads(raw)
        except json.JSONDecodeError:
            return jsonify({"error": "invalid JSON"}), 400

        prompt = body.get("prompt", "").strip()
        if not prompt:
            return jsonify({"error": "prompt is required"}), 400

        # Dispatch async so the HTTP response returns immediately
        thread = threading.Thread(
            target=dispatch_claude, args=(prompt, model, max_tokens), daemon=True
        )
        thread.start()

        event = body.get("event", "unknown")
        print(f"[webhook] dispatched session for event={event!r}", file=sys.stderr)
        return jsonify({"status": "dispatched", "event": event})

    return app


def main() -> None:
    parser = argparse.ArgumentParser(description="Webhook receiver for Claude remote control")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--secret", default=os.environ.get("WEBHOOK_SECRET", ""))
    parser.add_argument("--model", default="claude-sonnet-4-6")
    parser.add_argument("--max-tokens", type=int, default=4096, dest="max_tokens")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    app = create_app(args.secret or None, args.model, args.max_tokens)
    print(f"[webhook] listening on {args.host}:{args.port}", file=sys.stderr)
    app.run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
