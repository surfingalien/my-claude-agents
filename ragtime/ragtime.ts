#!/usr/bin/env bun
/**
 * ragtime — Batch Document Intelligence Processor
 * github.com/surfingalien/my-claude-agents
 *
 * Processes a corpus of documents through Claude Code sessions using
 * claude-mem's specialized observation modes. Each document gets a fresh
 * session — context is managed by claude-mem's injection hook, not by
 * conversation continuation. Observations compound across files.
 *
 * Original: thedotmack/claude-mem (Apache 2.0)
 * Adapted for: financial filings, news batches, trading research corpora
 *
 * Requires: Bun runtime, claude-mem installed and worker running
 * Install Bun: curl -fsSL https://bun.sh/install | bash
 *
 * Usage:
 *   bun ragtime/ragtime.ts
 *   RAGTIME_CORPUS_PATH=./datasets/earnings-q2 bun ragtime/ragtime.ts
 *   RAGTIME_MODE=code RAGTIME_FILE_LIMIT=5 bun ragtime/ragtime.ts
 */

import { query } from "@anthropic-ai/claude-agent-sdk";
import * as fs from "fs";
import * as path from "path";
import { homedir } from "os";

// ---------------------------------------------------------------------------
// Configuration — all values overridable via environment variables
// ---------------------------------------------------------------------------

const CONFIG = {
  /** Path to the folder containing .md documents to process */
  corpusPath: process.env.RAGTIME_CORPUS_PATH ||
    path.join(process.cwd(), "ragtime", "datasets", "corpus"),

  /** Path to claude-mem plugin directory */
  pluginPath: process.env.RAGTIME_PLUGIN_PATH ||
    path.join(homedir(), ".claude", "plugins", "marketplaces", "thedotmack", "plugin"),

  /** claude-mem worker port */
  workerPort: parseInt(process.env.CLAUDE_MEM_WORKER_PORT || "37777", 10),

  /**
   * Claude-mem observation mode.
   * Options: email-investigation | code | code--chill | meme-tokens | law-study
   * Default: email-investigation (entity/relationship/timeline extraction)
   */
  mode: process.env.RAGTIME_MODE || "email-investigation",

  /** Max age of transcripts to keep (hours) */
  transcriptMaxAgeHours: parseInt(process.env.RAGTIME_TRANSCRIPT_MAX_AGE || "24", 10),

  /** Project name for grouping observations in claude-mem */
  projectName: process.env.RAGTIME_PROJECT_NAME || "ragtime-batch",

  /** Limit files to process (0 = all) — useful for testing */
  fileLimit: parseInt(process.env.RAGTIME_FILE_LIMIT || "0", 10),

  /** Delay between sessions in ms — allows worker to flush observations */
  sessionDelayMs: parseInt(process.env.RAGTIME_SESSION_DELAY || "2000", 10),

  /**
   * Custom analysis prompt.
   * Defaults to investigation prompt appropriate for the selected mode.
   * Set RAGTIME_PROMPT to override for specialized corpus types.
   */
  customPrompt: process.env.RAGTIME_PROMPT || "",
};

// ---------------------------------------------------------------------------
// Mode-specific analysis prompts
// ---------------------------------------------------------------------------

const MODE_PROMPTS: Record<string, string> = {
  "email-investigation": `Read {file} and analyze it in the context of the investigation.
    Look for entities (people, organizations, email addresses), relationships between them,
    timeline events, and any anomalies or red flags.
    Cross-reference with what you know from the injected context above.`,

  "code": `Read {file} and analyze what was built, changed, or fixed.
    Record architectural decisions, patterns established, and bugs resolved.
    Cross-reference with prior session context above.`,

  "meme-tokens": `Read {file} and extract token activity data.
    Identify pump/dump events, signal tier transitions, market conditions,
    and algorithm performance observations.
    Note specific metrics: U/m, price gains %, buy pressure, pool sizes.`,

  // FinSurfing-specific prompts
  "financial-filing": `Read {file} (an SEC filing or earnings document) and extract:
    - Key financial metrics and YoY changes
    - Management guidance and forward-looking statements
    - Risk factors that are new or materially changed
    - Any signals relevant to trading decisions
    Cross-reference with prior filings from the injected context above.`,

  "market-news": `Read {file} (a financial news article or market report) and extract:
    - Key events and their market impact
    - Companies, tickers, and sectors mentioned
    - Analyst opinions and price targets
    - Macro signals (rates, inflation, sector rotation)
    Cross-reference with prior news from the injected context above.`,

  "earnings-call": `Read {file} (an earnings call transcript) and extract:
    - Revenue, EPS, and guidance vs. expectations
    - Management tone signals (confident/cautious/defensive)
    - Key questions from analysts and management responses
    - Forward-looking statements and specific numbers
    Cross-reference with prior quarters from the injected context above.`,
};

function getAnalysisPrompt(file: string): string {
  if (CONFIG.customPrompt) {
    return CONFIG.customPrompt.replace("{file}", file);
  }
  const template = MODE_PROMPTS[CONFIG.mode] || MODE_PROMPTS["email-investigation"];
  return template.replace("{file}", file);
}

// ---------------------------------------------------------------------------
// File discovery
// ---------------------------------------------------------------------------

function getFilesToProcess(): string[] {
  if (!fs.existsSync(CONFIG.corpusPath)) {
    console.error(`\n❌ Corpus path does not exist: ${CONFIG.corpusPath}`);
    console.error("   Set RAGTIME_CORPUS_PATH or create the directory.");
    console.error(`   Example: mkdir -p ${CONFIG.corpusPath}`);
    process.exit(1);
  }

  const files = fs
    .readdirSync(CONFIG.corpusPath)
    .filter((f) => f.endsWith(".md") || f.endsWith(".txt"))
    .sort((a, b) => {
      // Sort numerically if files are numbered (0001.md, 0002.md, ...)
      const numA = parseInt(a.match(/\d+/)?.[0] || "0", 10);
      const numB = parseInt(b.match(/\d+/)?.[0] || "0", 10);
      if (numA !== numB) return numA - numB;
      // Fall back to alphabetical
      return a.localeCompare(b);
    })
    .map((f) => path.join(CONFIG.corpusPath, f));

  if (files.length === 0) {
    console.error(`\n❌ No .md or .txt files found in: ${CONFIG.corpusPath}`);
    process.exit(1);
  }

  if (CONFIG.fileLimit > 0) {
    console.log(`   (Limiting to first ${CONFIG.fileLimit} files)`);
    return files.slice(0, CONFIG.fileLimit);
  }

  return files;
}

// ---------------------------------------------------------------------------
// Transcript cleanup
// ---------------------------------------------------------------------------

async function cleanupOldTranscripts(): Promise<void> {
  const transcriptsBase = path.join(homedir(), ".claude", "projects");

  if (!fs.existsSync(transcriptsBase)) return;

  const maxAgeMs = CONFIG.transcriptMaxAgeHours * 60 * 60 * 1000;
  const now = Date.now();
  let cleaned = 0;

  try {
    const projectDirs = fs.readdirSync(transcriptsBase);

    for (const projectDir of projectDirs) {
      const projectPath = path.join(transcriptsBase, projectDir);
      if (!fs.statSync(projectPath).isDirectory()) continue;

      for (const file of fs.readdirSync(projectPath)) {
        if (!file.endsWith(".jsonl")) continue;

        const filePath = path.join(projectPath, file);
        const fileAge = now - fs.statSync(filePath).mtimeMs;

        if (fileAge > maxAgeMs) {
          try {
            fs.unlinkSync(filePath);
            cleaned++;
          } catch {
            // Best effort
          }
        }
      }

      try {
        if (fs.readdirSync(projectPath).length === 0) {
          fs.rmdirSync(projectPath);
        }
      } catch {
        // Ignore race condition
      }
    }

    if (cleaned > 0) {
      console.log(`   🧹 Cleaned up ${cleaned} old transcript(s)`);
    }
  } catch (err) {
    console.warn("   ⚠️  Transcript cleanup warning:", err);
  }
}

// ---------------------------------------------------------------------------
// Worker queue drain
// ---------------------------------------------------------------------------

async function waitForQueueToEmpty(): Promise<void> {
  const maxWaitMs = 5 * 60 * 1000; // 5 minutes
  const pollIntervalMs = 500;
  const startTime = Date.now();

  while (true) {
    try {
      const response = await fetch(
        `http://localhost:${CONFIG.workerPort}/api/processing-status`
      );

      if (!response.ok) {
        console.warn(`   ⚠️  Worker status check failed: ${response.status}`);
        break;
      }

      const status = await response.json() as { queueDepth: number; isProcessing: boolean };

      if (status.queueDepth === 0 && !status.isProcessing) break;

      if (Date.now() - startTime > maxWaitMs) {
        console.warn("   ⚠️  Queue drain timeout — continuing anyway");
        break;
      }

      await new Promise((resolve) => setTimeout(resolve, pollIntervalMs));
    } catch (error) {
      console.warn("   ⚠️  Worker unreachable:", error);
      await new Promise((resolve) => setTimeout(resolve, 1000));
      break;
    }
  }
}

// ---------------------------------------------------------------------------
// Per-file session
// ---------------------------------------------------------------------------

async function processFile(file: string, index: number, total: number): Promise<void> {
  const filename = path.basename(file);
  const pct = Math.round(((index + 1) / total) * 100);
  console.log(`\n[${index + 1}/${total}] (${pct}%) → ${filename}`);

  try {
    for await (const message of query({
      prompt: getAnalysisPrompt(file),
      options: {
        cwd: CONFIG.corpusPath,
        plugins: [{ type: "local", path: CONFIG.pluginPath }],
      },
    })) {
      if (message.type === "assistant") {
        const content = message.message.content;
        const blocks = Array.isArray(content) ? content : [{ type: "text", text: content }];

        for (const block of blocks) {
          if (block.type === "text" && block.text) {
            const preview = block.text.length > 300
              ? block.text.substring(0, 300) + "…"
              : block.text;
            console.log("   →", preview);
          }
        }
      }

      if (message.type === "result" && message.subtype === "success") {
        console.log(`   ✅ ${filename} complete`);
      }
    }
  } catch (err) {
    console.error(`   ❌ Error processing ${filename}:`, err);
  }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main(): Promise<void> {
  const divider = "─".repeat(60);

  console.log(divider);
  console.log("  ragtime — Batch Document Intelligence Processor");
  console.log("  github.com/surfingalien/my-claude-agents");
  console.log(divider);
  console.log(`  Mode:      ${CONFIG.mode}`);
  console.log(`  Corpus:    ${CONFIG.corpusPath}`);
  console.log(`  Plugin:    ${CONFIG.pluginPath}`);
  console.log(`  Worker:    http://localhost:${CONFIG.workerPort}`);
  console.log(`  Project:   ${CONFIG.projectName}`);
  console.log(`  Cleanup:   ${CONFIG.transcriptMaxAgeHours}h transcript TTL`);
  if (CONFIG.fileLimit > 0) {
    console.log(`  Limit:     ${CONFIG.fileLimit} files`);
  }
  console.log(divider);

  // Preflight: verify worker is reachable
  try {
    const check = await fetch(`http://localhost:${CONFIG.workerPort}/api/processing-status`);
    if (!check.ok) throw new Error(`HTTP ${check.status}`);
    console.log("  ✅ claude-mem worker reachable");
  } catch {
    console.error(`\n❌ claude-mem worker not running on port ${CONFIG.workerPort}`);
    console.error("   Start it with: npx claude-mem worker:start");
    process.exit(1);
  }

  // Set mode for this batch
  process.env.CLAUDE_MEM_MODE = CONFIG.mode;
  console.log(`  ✅ Mode set to: ${CONFIG.mode}\n`);

  await cleanupOldTranscripts();

  const files = getFilesToProcess();
  console.log(`  📂 Found ${files.length} file(s) to process\n`);
  console.log(divider);

  const startTime = Date.now();

  for (let i = 0; i < files.length; i++) {
    await processFile(files[i], i, files.length);

    process.stdout.write("   Draining worker queue...");
    await waitForQueueToEmpty();
    process.stdout.write(" done\n");

    if (i < files.length - 1 && CONFIG.sessionDelayMs > 0) {
      await new Promise((resolve) => setTimeout(resolve, CONFIG.sessionDelayMs));
    }

    // Periodic transcript cleanup every 10 files
    if ((i + 1) % 10 === 0) {
      await cleanupOldTranscripts();
    }
  }

  await cleanupOldTranscripts();

  const elapsed = Math.round((Date.now() - startTime) / 1000);
  const mins = Math.floor(elapsed / 60);
  const secs = elapsed % 60;

  console.log(`\n${divider}`);
  console.log("  ✅ Batch complete");
  console.log(`  Files processed: ${files.length}`);
  console.log(`  Elapsed: ${mins}m ${secs}s`);
  console.log(`  Observations stored in: ~/.claude-mem/`);
  console.log(`  Query with: npx claude-mem search "<keyword>"`);
  console.log(divider);
}

main().catch((err) => {
  console.error("\n❌ Fatal error:", err);
  process.exit(1);
});
