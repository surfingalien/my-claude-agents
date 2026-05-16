# Remote Control Patterns

Reference for common patterns when driving Claude Code from external systems.

## Pattern 1: Fire-and-Forget API Trigger

Best for: CI steps, cron jobs, one-shot automation.

```bash
ANTHROPIC_API_KEY=sk-ant-... python api_trigger.py "Fix the TODO in src/auth.py"
```

The script streams output to stdout and exits with code 0 on success, 1 on error.

## Pattern 2: Event-Driven Webhook

Best for: GitHub webhooks, Slack slash commands, PagerDuty alerts.

```
External system → POST /webhook → webhook_receiver.py → api_trigger.py (async)
```

The receiver returns 200 immediately; the Claude session runs in the background.

### Sending a test event

```bash
# Without signature validation
curl -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -d '{"event":"test","prompt":"Say hello"}'

# With HMAC signature (GitHub-style)
SECRET=mysecret
PAYLOAD='{"event":"pr_review","prompt":"Review PR #1"}'
SIG="sha256=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)"
curl -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: $SIG" \
  -d "$PAYLOAD"
```

## Pattern 3: GitHub Actions Dispatch

Best for: triggering from other workflows, external CI systems, or the GitHub UI.

```bash
# Trigger via GitHub API
curl -X POST \
  -H "Authorization: Bearer $GH_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/OWNER/REPO/dispatches \
  -d '{"event_type":"claude-trigger","client_payload":{"prompt":"Run security audit"}}'
```

## Pattern 4: Chained Sessions (Pipeline)

Run sessions in sequence, passing output forward:

```bash
#!/bin/bash
set -e

# Step 1: generate plan
PLAN=$(python api_trigger.py "Create an implementation plan for the auth refactor" --model claude-opus-4-7)

# Step 2: implement using the plan
python api_trigger.py "Implement this plan: $PLAN" --model claude-sonnet-4-6
```

## Security Checklist

- [ ] `ANTHROPIC_API_KEY` in env var or secrets manager
- [ ] Webhook secret set and validated on every request
- [ ] Rate limiting on the webhook endpoint (e.g., nginx `limit_req`)
- [ ] Input sanitization: strip control chars from `prompt` before forwarding
- [ ] Session timeout: set `--max-tokens` to cap runaway sessions
- [ ] Logging: all dispatched prompts written to audit log
