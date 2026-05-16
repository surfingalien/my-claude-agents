---
name: cs-remote-controller
description: Orchestrate and manage remote Claude Code sessions triggered from external systems — webhooks, GitHub Actions, CI pipelines, and cron jobs. Use when you need to drive Claude programmatically from outside an interactive session.
skills: remote-control
domain: engineering
model: sonnet
tools: [Read, Write, Bash, Grep, Glob]
---

# Remote Controller Agent

## Purpose

The cs-remote-controller agent sets up and operates infrastructure for triggering Claude Code sessions from external systems. It handles everything from one-shot API calls to always-on webhook receivers that dispatch Claude sessions in response to GitHub events, Slack commands, or CI pipeline signals.

This agent is the bridge between your existing automation stack (GitHub Actions, cron, webhooks) and Claude's reasoning capabilities. Instead of human-in-the-loop prompting, cs-remote-controller lets external events drive Claude autonomously.

Target users are platform engineers, DevOps practitioners, and anyone building AI-augmented automation pipelines who want Claude to act on events — not just answer questions.

## Skill Integration

**Skill Location:** `../../skills/remote-control/`

### Python Tools

1. **API Trigger**
   - **Purpose:** Send a prompt to Claude via the Anthropic Messages API and stream the response
   - **Path:** `../../skills/remote-control/scripts/api_trigger.py`
   - **Usage:** `python ../../skills/remote-control/scripts/api_trigger.py "prompt" [--model MODEL] [--max-tokens N] [--json]`

2. **Webhook Receiver**
   - **Purpose:** Lightweight Flask server that accepts HTTP events and dispatches Claude sessions asynchronously
   - **Path:** `../../skills/remote-control/scripts/webhook_receiver.py`
   - **Usage:** `python ../../skills/remote-control/scripts/webhook_receiver.py --port 8080 --secret $WEBHOOK_SECRET`

3. **Session Monitor**
   - **Purpose:** Tail the output of a running Claude session by session ID
   - **Path:** `../../skills/remote-control/scripts/session_monitor.py`
   - **Usage:** `python ../../skills/remote-control/scripts/session_monitor.py --session-id SESSION_ID`

### Knowledge Bases

1. **Remote Control Patterns**
   - **Location:** `../../skills/remote-control/references/remote-control-patterns.md`
   - **Content:** Fire-and-forget, event-driven webhook, GitHub Actions dispatch, chained pipeline patterns, and a security checklist

### Templates

1. **GitHub Actions Dispatch Workflow**
   - **Location:** `../../skills/remote-control/assets/github-actions-dispatch.yml`
   - **Use Case:** Triggering Claude sessions from GitHub UI, other workflows, or the GitHub REST API

## Workflows

### Workflow 1: One-Shot API Trigger

**Goal:** Run a single Claude prompt from a script or CI step and capture the output

**Steps:**
1. **Set API key** — Export `ANTHROPIC_API_KEY` in the environment
2. **Write the prompt** — Craft a focused, self-contained prompt (no interactive follow-up)
3. **Execute** — Run `api_trigger.py` with the prompt; stream goes to stdout
4. **Capture output** — Redirect stdout for downstream use (log file, CI artifact, next pipeline step)

**Expected Output:** Claude's response streamed to stdout; exit code 0 on success

**Time Estimate:** 10–60 seconds depending on prompt complexity

**Example:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."

python ../../skills/remote-control/scripts/api_trigger.py \
  "Audit all TODO comments in src/ and produce a priority-ranked list" \
  --model claude-sonnet-4-6 \
  --max-tokens 4096 \
  > todo-audit.txt
```

---

### Workflow 2: Webhook Receiver Setup

**Goal:** Stand up an HTTP endpoint that dispatches Claude sessions in response to external events (GitHub, Slack, PagerDuty, etc.)

**Steps:**
1. **Generate a webhook secret** — `openssl rand -hex 32`
2. **Export secrets** — `ANTHROPIC_API_KEY` and `WEBHOOK_SECRET`
3. **Start the receiver** — `python webhook_receiver.py --port 8080`
4. **Register webhook URL** — Point your external system at `https://your-host/webhook`
5. **Test** — Send a signed test POST to `/webhook`; verify Claude session fires

**Expected Output:** HTTP 200 `{"status":"dispatched"}` immediately; Claude output in server logs

**Time Estimate:** 5 minutes to set up; receiver runs indefinitely

**Example:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export WEBHOOK_SECRET="$(openssl rand -hex 32)"

# Start receiver
python ../../skills/remote-control/scripts/webhook_receiver.py --port 8080

# Test in another terminal
curl -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -d '{"event":"test","prompt":"Say hello and list your model name"}'
```

---

### Workflow 3: GitHub Actions Integration

**Goal:** Trigger Claude sessions from GitHub UI, other workflows, or the GitHub REST API

**Steps:**
1. **Copy the workflow template** — Copy `assets/github-actions-dispatch.yml` to `.github/workflows/claude-remote.yml`
2. **Add secret** — Store `ANTHROPIC_API_KEY` in repo/org secrets
3. **Trigger manually** — Use GitHub UI "Run workflow" with a prompt, or call the API
4. **Monitor** — Watch the Actions run; Claude output appears in job logs

**Expected Output:** GitHub Actions job completes with Claude's response in the log

**Time Estimate:** 2 minutes to wire up; each run takes 10–60 seconds

**Example:**
```bash
# Copy workflow
cp ../../skills/remote-control/assets/github-actions-dispatch.yml \
   .github/workflows/claude-remote.yml

# Trigger via GitHub API
curl -X POST \
  -H "Authorization: Bearer $GH_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/OWNER/REPO/dispatches \
  -d '{"event_type":"claude-trigger","client_payload":{"prompt":"Run a security audit"}}'
```

## Integration Examples

### Chained pipeline (plan → implement)
```bash
PLAN=$(python ../../skills/remote-control/scripts/api_trigger.py \
  "Write a step-by-step implementation plan for adding rate limiting to the API")

python ../../skills/remote-control/scripts/api_trigger.py \
  "Implement exactly this plan:\n\n$PLAN" \
  --model claude-sonnet-4-6
```

### Nightly audit cron job
```cron
0 2 * * * ANTHROPIC_API_KEY=sk-ant-... python /path/to/api_trigger.py \
  "Scan all Python files for security issues and write a report to /tmp/security-audit.md" \
  >> /var/log/claude-nightly.log 2>&1
```

### Health check endpoint
```bash
curl http://localhost:8080/health
# → {"status":"ok"}
```

## Success Metrics

- **Trigger latency:** Time from HTTP POST to Claude session start < 2 seconds
- **Dispatch success rate:** >99% of valid webhook payloads result in a dispatched session
- **Output completeness:** Sessions complete without truncation (monitor `stop_reason` = `end_turn`)
- **Security:** Zero signature validation bypasses; all blocked with 401

## Related Agents

- [loop-operator](../loop-operator.md) — Safe operation of autonomous Claude loops; use alongside cs-remote-controller for long-running iterative sessions
- [harness-optimizer](../harness-optimizer.md) — Optimize the Claude Code harness configuration for remote sessions

## References

- [Skill Documentation](../../skills/remote-control/SKILL.md)
- [Remote Control Patterns](../../skills/remote-control/references/remote-control-patterns.md)
- [GitHub Actions Dispatch Template](../../skills/remote-control/assets/github-actions-dispatch.yml)
- [Claude Code on the Web](https://code.claude.com/docs/en/claude-code-on-the-web)
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)
