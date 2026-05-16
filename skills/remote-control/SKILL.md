---name: remote-control
description: Trigger and manage Claude Code sessions remotely via API, webhooks, and GitHub Actions. Covers programmatic session creation, webhook receivers, event-driven invocation, and session monitoring. Use when you need to drive Claude from external systems.
origin: ECC
owner: Your Organization---

# Remote Control Agent

You're a pragmatic executor focused on shipping results and measuring impact. You use AI to amplify your effect and automation to eliminate busywork.

# Remote Control Agent

You're a pragmatic executor who focuses on shipping results and measuring impact. You use AI to amplify your impact and automation to eliminate busywork.

# Remote Control

Trigger Claude Code sessions from external systems — GitHub webhooks, HTTP endpoints, CI pipelines, or cron jobs — without a human in the loop.


## Your Agent

This agent is part of your personalized agent collection. Customize it as needed for your team and use cases.
## When to Use

- Triggering Claude Code from a GitHub issue comment or PR event
- Setting up a webhook receiver that turns HTTP calls into Claude sessions
- Driving automated fixes/reviews from CI failures
- Running scheduled Claude Code jobs (nightly audits, dependency bumps)
- Chaining Claude sessions across systems programmatically

## Core Patterns

### 1. One-shot API Trigger (`api_trigger.py`)

Send a prompt to Claude Code via the Anthropic Messages API and stream the response. Works as a fire-and-forget script or as part of a larger pipeline.

```bash
python scripts/api_trigger.py "Review the open PRs and comment on any with missing tests"
# With repo context
python scripts/api_trigger.py "Fix the failing tests in src/" --model claude-sonnet-4-6 --max-tokens 4096
```

### 2. Webhook Receiver (`webhook_receiver.py`)

A lightweight Flask server that listens for inbound HTTP events, validates them, and dispatches Claude Code sessions in response.

```bash
python scripts/webhook_receiver.py --port 8080 --secret $WEBHOOK_SECRET
```

Incoming payload shape:
```json
{ "event": "pr_review", "prompt": "Review PR #42 for security issues", "repo": "owner/repo" }
```

### 3. GitHub Actions Dispatch

Use `workflow_dispatch` or `repository_dispatch` to trigger a Claude Code session from any GitHub event. See `assets/github-actions-dispatch.yml`.

### 4. Session Monitor (`session_monitor.py`)

Poll a running Claude Code session for status and stream its output to stdout. Used to observe long-running remote sessions.

```bash
python scripts/session_monitor.py --session-id $SESSION_ID --poll-interval 5
```

## Prerequisites

```bash
pip install anthropic flask python-dotenv
export ANTHROPIC_API_KEY="sk-ant-..."
export WEBHOOK_SECRET="your-secret"  # for webhook_receiver.py
```

## Quick Start

```bash
# 1. Clone / copy skill
cp -r skills/remote-control/ my-project/

# 2. Install deps
pip install anthropic flask python-dotenv

# 3. Fire a one-shot prompt
python scripts/api_trigger.py "List all TODO comments in the codebase"

# 4. Or start the webhook receiver
python scripts/webhook_receiver.py --port 8080
```

## Security Notes

- Always validate webhook signatures (`X-Hub-Signature-256` for GitHub, custom HMAC for others)
- Store `ANTHROPIC_API_KEY` in env vars or a secrets manager — never hardcode
- Rate-limit the webhook receiver to prevent prompt injection via external HTTP calls
- Sanitize inbound `prompt` payloads before forwarding to the API