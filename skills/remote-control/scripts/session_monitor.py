#!/usr/bin/env python3
"""
Poll and stream output from a running Claude Code session.
Usage: python session_monitor.py --session-id SESSION_ID [--poll-interval N]

Reads from a session log file written by api_trigger.py or webhook_receiver.py.
Set SESSION_LOG_DIR to override the default log directory.
"""
import argparse
import os
import sys
import time


def tail_file(path: str, poll_interval: float) -> None:
    """Stream new lines appended to a file, like `tail -f`."""
    try:
        with open(path) as f:
            f.seek(0, 2)  # seek to end
            print(f"[monitor] streaming {path}", file=sys.stderr)
            while True:
                line = f.readline()
                if line:
                    print(line, end="", flush=True)
                else:
                    time.sleep(poll_interval)
    except FileNotFoundError:
        print(f"[monitor] session log not found: {path}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[monitor] stopped", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description="Monitor a remote Claude session")
    parser.add_argument("--session-id", required=True, dest="session_id")
    parser.add_argument("--poll-interval", type=float, default=1.0, dest="poll_interval")
    parser.add_argument(
        "--log-dir",
        default=os.environ.get("SESSION_LOG_DIR", "/tmp/claude-sessions"),
        dest="log_dir",
    )
    args = parser.parse_args()

    log_path = os.path.join(args.log_dir, f"{args.session_id}.log")
    tail_file(log_path, args.poll_interval)


if __name__ == "__main__":
    main()
