#!/usr/bin/env python3
"""Reply-All Apocalypse -- one office joke, written to entry.txt.

Entry for make.fun's "Make the AI Judge Laugh: the Office Joke Open":
a single line of office comedy, at most 200 characters, compared
head-to-head by a judge model. The program is fully deterministic --
every run writes the same bytes, because the grader runs it twice and
the two runs must agree.

The joke is fixed text, kept as one constant. Before anything is
written, validate_entry() enforces the sealed scorer's gate exactly as
RULES.txt states it: the file must be UTF-8 text of 1 to 200
characters, not only white space. After writing, the file is read back
and checked again -- what lands on disk is what the judge sees, so the
written bytes are verified, not just the constant in memory.

Why this joke: a reply-all disaster escalates rule-of-three style --
birthday potluck, conspiracy thread, two resignations -- with the
payoff landing on the last two words. Each step is bigger than the
last, and each is a specific office detail, so the line could not be
swapped onto any other workplace: the potluck is harmless, the thread
is paranoia, the resignations are the damage.
"""

import os

JOKE = (
    "Someone hit reply-all on a company-wide email, and within nine "
    "minutes we had a birthday potluck, a conspiracy thread, and two "
    "resignations."
)

MAX_CHARS = 200


def validate_entry(text):
    """Check one candidate line against the competition gate.

    Returns (ok, reason): reason is empty when the text is valid.
    """
    if not isinstance(text, str):
        return False, "entry is not text"
    if not text.strip():
        return False, "entry is empty or only white space"
    if len(text) > MAX_CHARS:
        return False, "entry is %d chars, over the 200-char limit" % len(text)
    if text != text.strip():
        return False, "entry must not start or end with white space"
    if "\n" in text or "\r" in text:
        return False, "entry must be a single line"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False, "entry is not valid UTF-8 text"
    return True, ""


def resolve_output_dir():
    """The directory that receives entry.txt."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main():
    ok, reason = validate_entry(JOKE)
    if not ok:
        raise SystemExit("invalid entry: %s" % reason)

    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the judged text is exactly this line, byte
    # for byte, with nothing extra for the judge to read.
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(JOKE)

    with open(out_path, "r", encoding="utf-8") as handle:
        written = handle.read()
    ok, reason = validate_entry(written)
    if not ok or written != JOKE:
        raise SystemExit(
            "round-trip check failed: file does not match the entry (%s)"
            % reason
        )

    print("wrote %s (%d chars)" % (out_path, len(JOKE)))


if __name__ == "__main__":
    main()
