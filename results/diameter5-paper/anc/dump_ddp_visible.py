#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dump_ddp_visible.py
===================

Purpose
-------
Extract *only what a human reader sees on chat.openai.com* for the
"Degree Diameter Problem" conversation:

    * the user prompts the user actually typed (and sent) into the browser
    * the assistant replies that the browser displays as the answer

and write them out as a clean Markdown transcript ordered by time.

What is *excluded* (and why)
----------------------------
The ChatGPT export contains a lot more than the visible turn-by-turn
exchange.  We deliberately drop everything below; see the function
`is_browser_visible_message` for the single point of truth.

    * `role=assistant, content_type=thoughts`          — chain-of-thought
          reasoning that is collapsed behind a "Thoughts" disclosure in the
          UI and not part of the answer text.
    * `role=assistant, content_type=reasoning_recap`   — the "Thought for
          22m 25s" labels.  Tiny UI affordances, not content.
    * `role=assistant, content_type=code`              — python-tool /
          browser-tool invocations shown inside the collapsible
          "Analysing…" panels, not the answer.
    * `role=tool,      content_type=execution_output`  — output of python
          tool calls; also shown only inside the analysis panels.
    * `role=tool,      content_type=text`              — other tool
          channels (search hits, file ops); not part of the answer.
    * `role=system`                                    — hidden context.
    * empty assistant `text` messages (no parts / empty parts)             —
          placeholders that the UI does not render.

What is *included*
------------------
    * `role=user,      content_type in {text, multimodal_text}`   — the
          user's typed prompts (and any attached images, kept as JSON
          stubs so nothing is silently dropped).
    * `role=assistant, content_type=text` with non-empty parts     — the
          visible answer bubbles.

Turn vs. Round
--------------
Each visible message is one *Turn* (a strictly increasing counter over the
whole transcript).  Turns are additionally grouped into *Rounds*, where a
round is one user-prompt cycle: it opens when the user sends a prompt and
covers every assistant reply up to the next user prompt.  So the Nth user
prompt and the assistant bubbles answering it together form Round N
("the Nth back-and-forth with the user").  Headings read e.g.
`## Turn 006 (Round 002) — 🤖 ASSISTANT`.  See `assign_round_numbers`.

Note: this *Round* index counts user-prompt cycles; it is unrelated to the
`phaseNN_*.zip` artifact names produced inside the session (those number
the model's own construction attempts, a different and coarser thing).

Design priorities (in order)
----------------------------
1. Reviewability — single explicit filter function, short main(), small
                    helpers. The reader of the script must be able to
                    convince themselves the filter is correct.
2. Faithfulness  — we walk only the *current branch* (the path the
                    browser is actually showing), in chronological order
                    of message create_time.  Edits/regenerations on
                    sibling branches are deliberately ignored.
3. Self-contained — stdlib only.

Usage
-----
    python3 dump_ddp_visible.py             # default paths
    python3 dump_ddp_visible.py --help
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path


# --------------------------------------------------------------------------- #
# Defaults — adjust here if the export is moved.                              #
# --------------------------------------------------------------------------- #

DEFAULT_CONVERSATIONS_PATH = Path(
    "conversations-000.json"
)
DEFAULT_TARGET_TITLE = "Degree Diameter Problem"
DEFAULT_TARGET_ID    = "6a101fde-f380-83a8-afc7-7a224426dbc9"
DEFAULT_OUTPUT_PATH  = Path("extracted/DDP_visible_transcript.md")

# Rounds after this are unrelated to this paper's discovery/verification
# and are excluded from the transcript.  Keep only Round 1..MAX_ROUND.
MAX_ROUND = 52


# --------------------------------------------------------------------------- #
# Step A — locate the conversation.                                           #
# --------------------------------------------------------------------------- #

def load_target_conversation(conversations_json_path: Path,
                             target_id: str,
                             fallback_title: str) -> dict:
    print(f"[A] loading {conversations_json_path}", file=sys.stderr)
    with conversations_json_path.open("r", encoding="utf-8") as f:
        all_conversations = json.load(f)
    print(f"    {len(all_conversations)} conversations in this shard",
          file=sys.stderr)

    for conv in all_conversations:
        if conv.get("id") == target_id or conv.get("conversation_id") == target_id:
            return conv

    exact = [c for c in all_conversations
             if (c.get("title") or "") == fallback_title]
    if len(exact) == 1:
        return exact[0]

    raise SystemExit(
        f"no conversation with id={target_id} or title={fallback_title!r}")


# --------------------------------------------------------------------------- #
# Step B — walk the current branch (root -> current_node).                    #
# --------------------------------------------------------------------------- #

def walk_current_branch(mapping: dict[str, dict],
                        current_node: str | None) -> list[str]:
    """Return node ids on the current branch from oldest to newest.

    The browser shows the path from root to `current_node`.  We walk from
    `current_node` *up* via parent links, then reverse so the order matches
    how a reader scrolls top-to-bottom.
    """
    reversed_path: list[str] = []
    cursor = current_node
    while cursor is not None and cursor in mapping:
        reversed_path.append(cursor)
        cursor = mapping[cursor].get("parent")
    reversed_path.reverse()
    return reversed_path


# --------------------------------------------------------------------------- #
# Step C — the visibility filter (single point of truth).                     #
# --------------------------------------------------------------------------- #

def is_browser_visible_message(message: dict | None) -> bool:
    """Return True iff this message would appear as a normal user prompt
    bubble or assistant answer bubble in the chat.openai.com UI.

    Read this together with the module docstring's "What is excluded /
    included" lists — those describe the *intent*; this function is the
    *implementation*.
    """
    if not message:
        return False

    author = message.get("author") or {}
    role   = author.get("role")
    content = message.get("content") or {}
    ctype  = content.get("content_type")

    if role == "user":
        # User typed something into the input box.  Plain text is the
        # overwhelming majority; multimodal_text covers attached images.
        if ctype in ("text", "multimodal_text"):
            return has_nonempty_parts(content)
        return False

    if role == "assistant":
        # The browser shows assistant *text* parts as the answer bubble.
        # Everything else (thoughts, code calls, reasoning_recap) lives in
        # collapsible UI affordances that we are not treating as "the
        # reply".
        if ctype == "text":
            return has_nonempty_parts(content)
        return False

    # role in {"tool", "system"} or unknown -> not a visible turn.
    return False


def has_nonempty_parts(content: dict) -> bool:
    """True if `content.parts` has at least one part with real data."""
    parts = content.get("parts") or []
    for part in parts:
        if isinstance(part, str):
            if part.strip():
                return True
        elif isinstance(part, dict):
            # An image / audio attachment counts as visible content.
            return True
    return False


# --------------------------------------------------------------------------- #
# Step D — render a visible message into Markdown.                            #
# --------------------------------------------------------------------------- #

def format_unix_timestamp(t: float | None) -> str:
    if t is None:
        return "(no timestamp)"
    return dt.datetime.fromtimestamp(t, tz=dt.timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC")


def render_parts_as_markdown(content: dict) -> str:
    """Render text and non-text parts.  Non-text parts are stubbed as JSON
    so that an attached image (etc.) is visible to the reviewer rather
    than silently dropped.
    """
    parts = content.get("parts") or []
    chunks: list[str] = []
    for part in parts:
        if isinstance(part, str):
            chunks.append(part)
        elif isinstance(part, dict):
            chunks.append(
                "_[non-text part — kept as JSON for review]_\n\n"
                "```json\n"
                + json.dumps(part, ensure_ascii=False, indent=2)
                + "\n```"
            )
        else:
            chunks.append(f"_[unrenderable part of type {type(part).__name__}]_")
    return "\n\n".join(chunks).strip()


def render_visible_turn(turn_index: int, round_index: int, message: dict) -> str:
    role  = (message.get("author") or {}).get("role", "?")
    ctime = message.get("create_time")
    ts    = format_unix_timestamp(ctime)
    model = ((message.get("metadata") or {}).get("model_slug") or "")
    label = {"user": "🧑 USER", "assistant": "🤖 ASSISTANT"}.get(role, role.upper())

    header = f"## Turn {turn_index:03d} (Round {round_index:03d}) — {label}"
    sub = f"_{ts}_"
    if role == "assistant" and model:
        sub += f"  ·  model: `{model}`"

    body = render_parts_as_markdown(message.get("content") or {})

    return f"{header}\n\n{sub}\n\n{body}\n"


# --------------------------------------------------------------------------- #
# Step E — main pipeline.                                                     #
# --------------------------------------------------------------------------- #

def collect_visible_messages(conv: dict) -> list[dict]:
    """Return visible messages on the current branch, in chronological
    order.  Each item is the raw `message` dict from the export.
    """
    mapping       = conv.get("mapping") or {}
    current_node  = conv.get("current_node")
    branch_ids    = walk_current_branch(mapping, current_node)
    print(f"[B] current branch has {len(branch_ids)} nodes", file=sys.stderr)

    visible: list[dict] = []
    for nid in branch_ids:
        msg = (mapping.get(nid) or {}).get("message")
        if is_browser_visible_message(msg):
            visible.append(msg)
    print(f"[C] kept {len(visible)} visible messages", file=sys.stderr)

    # The branch order is already chronological-by-construction, but we
    # sort explicitly on create_time so the script's contract ("ordered by
    # time") is enforced and not just an accident of the data.
    visible.sort(key=lambda m: m.get("create_time") or 0.0)
    return visible


def assign_round_numbers(visible: list[dict]) -> list[int]:
    """Return one round number per visible message, aligned by index.

    A *round* is one user-prompt cycle: it begins the moment the user
    sends a prompt and covers every assistant reply up to (but not
    including) the next user prompt.  The first user prompt opens round 1,
    the second opens round 2, and so on.  So a user prompt and all the
    assistant bubbles that answer it share the same round number — i.e.
    the number answers "which back-and-forth with the user is this?".

    Edge case: if the transcript begins with assistant messages before any
    user prompt (unusual but possible after some edits), those leading
    messages are labelled round 0 so that every turn still carries one.
    """
    rounds: list[int] = []
    current_round = 0
    for message in visible:
        role = (message.get("author") or {}).get("role")
        if role == "user":
            current_round += 1  # a new user prompt opens the next round
        rounds.append(current_round)
    return rounds


def render_document(conv: dict, visible: list[dict]) -> str:
    title = conv.get("title") or "(untitled)"
    n_user = sum(1 for m in visible
                 if (m.get("author") or {}).get("role") == "user")
    n_asst = sum(1 for m in visible
                 if (m.get("author") or {}).get("role") == "assistant")

    # Round = user-prompt cycle.  Computed once, indexed in lockstep with
    # `visible` so turn i carries round `rounds[i-1]`.
    rounds = assign_round_numbers(visible)
    n_rounds = max(rounds) if rounds else 0

    head_lines: list[str] = []
    head_lines.append(f"# {title} — browser-visible transcript")
    head_lines.append("")
    head_lines.append("Only the messages that the chat.openai.com UI shows "
                      "as a user prompt bubble or an assistant answer "
                      "bubble are included.  Thoughts, tool calls, "
                      "code execution output, and `reasoning_recap` "
                      "annotations are dropped.  See "
                      "`is_browser_visible_message` in this script for "
                      "the exact rule.")
    head_lines.append("")
    head_lines.append(f"- conversation_id: `{conv.get('id')}`")
    head_lines.append(f"- created: {format_unix_timestamp(conv.get('create_time'))}")
    head_lines.append(f"- updated: {format_unix_timestamp(conv.get('update_time'))}")
    head_lines.append(f"- default_model: `{conv.get('default_model_slug') or ''}`")
    head_lines.append(f"- visible turns: {len(visible)} "
                      f"(user: {n_user}, assistant: {n_asst})")
    head_lines.append(f"- rounds: {n_rounds} "
                      f"(one per user prompt; a round = a user prompt "
                      f"plus the assistant replies answering it)")
    head_lines.append("")
    head_lines.append("---")
    head_lines.append("")

    turn_blocks: list[str] = []
    for i, (msg, rnd) in enumerate(zip(visible, rounds), start=1):
        turn_blocks.append(render_visible_turn(i, rnd, msg))
        turn_blocks.append("---\n")
    return "\n".join(head_lines) + "\n".join(turn_blocks)


# --------------------------------------------------------------------------- #
# CLI                                                                         #
# --------------------------------------------------------------------------- #

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--conversations-json", type=Path,
                   default=DEFAULT_CONVERSATIONS_PATH)
    p.add_argument("--conv-id",    default=DEFAULT_TARGET_ID)
    p.add_argument("--conv-title", default=DEFAULT_TARGET_TITLE)
    p.add_argument("--output", "-o", type=Path,
                   default=DEFAULT_OUTPUT_PATH)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    conv = load_target_conversation(args.conversations_json,
                                    args.conv_id,
                                    args.conv_title)
    visible = collect_visible_messages(conv)
    # Keep only Round 1..MAX_ROUND; later rounds are unrelated to this paper
    # and are filtered out here.  Reuses the existing round numbering, so the
    # rendered header counts and body turns both reflect only these rounds.
    _rounds = assign_round_numbers(visible)
    visible = [m for m, r in zip(visible, _rounds) if r <= MAX_ROUND]
    doc = render_document(conv, visible)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(doc, encoding="utf-8")
    print(f"[D] wrote {args.output} "
          f"({args.output.stat().st_size:,} bytes, "
          f"{len(visible)} turns)", file=sys.stderr)


if __name__ == "__main__":
    main()