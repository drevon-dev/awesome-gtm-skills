#!/usr/bin/env python3
"""voice_check.py: compare a draft against a writer's voice library.

Usage:
    python3 voice_check.py VOICE_DIR DRAFT [--json] [--register NAME]

VOICE_DIR holds fingerprint.json (required), and optionally not-me.md and
approved-language.md in the formats from references/library-templates.md.
DRAFT is a .md or .txt file, or "-" for stdin.

Prints a report. Exit code 1 on a hard fail (a banned slop word or a not-me
phrase in the draft), 0 otherwise. Dial deviations are advisory flags.

--register picks fingerprint-<NAME>.json when a writer has more than one
register measured separately.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voice_stats import analyze_texts, BANNED, WORD  # noqa: E402


# (label, section, key, kind, tolerance)
# kind: "ratio" = draft within tolerance*profile (both directions, floor applies)
#       "ceiling" = draft must not exceed profile*tolerance + floor
#       "absolute" = draft within +/- tolerance points
DIAL_CHECKS = [
    ("sentence length (mean words)", "pooled", "sentence_mean", "ratio", 0.25, 2.0),
    ("sentence variance (stdev)", "pooled", "sentence_stdev", "ratio", 0.5, 2.0),
    ("long sentences (% over 25 words)", "pooled", "pct_over_25", "ceiling", 1.5, 5.0),
    ("fragments (% sentences <=3 words)", "pooled", "fragments_pct", "ratio", 0.6, 4.0),
    ("And/But/So openers (%)", "pooled", "conjunction_openers_pct", "ratio", 0.6, 4.0),
    ("questions per 100 sentences", "pooled", "questions_per_100_sentences", "ratio", 0.6, 4.0),
    ("exclamations per 100 sentences", "pooled", "exclamations_per_100_sentences", "ceiling", 1.5, 1.0),
    ("passive per 100 sentences", "pooled", "passive_per_100_sentences", "ceiling", 1.5, 5.0),
    ("paragraph length (sentences)", "pooled", "paragraph_mean_sentences", "ratio", 0.4, 0.7),
    ("first person per 100 words", "pooled", "first_person_per_100w", "ratio", 0.5, 1.0),
    ("second person per 100 words", "pooled", "second_person_per_100w", "ratio", 0.5, 1.0),
    ("we per 100 words", "pooled", "we_per_100w", "ratio", 0.6, 1.0),
    ("contractions per 100 words", "pooled", "contractions_per_100w", "ratio", 0.5, 0.5),
    ("hedges per 100 words", "pooled", "hedges_per_100w", "ratio", 0.6, 0.4),
    ("intensifiers per 100 words", "pooled", "intensifiers_per_100w", "ratio", 0.6, 0.4),
    ("numbers per 100 words", "pooled", "numbers_per_100w", "ratio", 0.6, 0.8),
    ("citation markers per 1000 words", "pooled", "citation_markers_per_1000w", "ratio", 0.7, 2.0),
    ("em dashes per 1000 words", "pooled", "em_dashes_per_1000w", "ceiling", 1.5, 0.5),
    ("spaced hyphens per 1000 words", "pooled", "spaced_hyphens_per_1000w", "ratio", 0.7, 1.0),
    ("semicolons per 1000 words", "pooled", "semicolons_per_1000w", "ceiling", 1.5, 0.5),
    ("ellipses per 1000 words", "pooled", "ellipses_per_1000w", "ceiling", 1.5, 0.5),
    ("parentheses per 1000 words", "pooled", "parentheses_per_1000w", "ceiling", 1.5, 2.0),
    ("reading ease (flesch)", "pooled", "flesch_reading_ease", "absolute", 12.0, 0.0),
    ("headers per 1000 words", "formatting", "headers_per_1000w", "ceiling", 1.5, 1.0),
    ("bullets per 1000 words", "formatting", "bullets_per_1000w", "ceiling", 1.5, 2.0),
    ("bold per 1000 words", "formatting", "bold_per_1000w", "ceiling", 1.5, 1.0),
    ("blockquotes per 1000 words", "formatting", "blockquotes_per_1000w", "ceiling", 1.5, 1.0),
    ("emoji (count)", "formatting", "emoji", "ceiling", 1.0, 0.0),
    ("avg word length", "vocabulary", "avg_word_length", "absolute", 0.5, 0.0),
    ("long words (% 3+ syllables)", "vocabulary", "pct_long_words", "absolute", 4.0, 0.0),
]


def load_entries(path, pattern):
    """Return list of (text, line) for entries matched by pattern in a library file."""
    if not os.path.isfile(path):
        return []
    out = []
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            s = ln.strip()
            if not s.startswith("- ") or "superseded by" in s:
                continue
            m = re.search(pattern, s)
            if m:
                out.append((m.group(1).strip(), s))
    return out


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9' ]+", " ", s.lower())).strip()


def phrase_in(draft_norm, phrase):
    p = norm(phrase)
    if not p:
        return False
    if p in draft_norm:
        return True
    toks = p.split()
    if len(toks) >= 8:
        for i in range(len(toks) - 5):
            if " ".join(toks[i:i + 6]) in draft_norm:
                return True
    return False


def find_lines(raw, phrase):
    hits = []
    pat = re.compile(r"(?<![a-z])" + re.escape(phrase.lower()) + r"(?![a-z])")
    for i, ln in enumerate(raw.split("\n"), 1):
        if pat.search(ln.lower()):
            hits.append(i)
    return hits


def check(voice_dir, draft_name, draft_raw, register=None):
    fp_name = "fingerprint-%s.json" % register if register else "fingerprint.json"
    fp_path = os.path.join(voice_dir, fp_name)
    if not os.path.isfile(fp_path):
        sys.exit("no %s in %s (run voice_stats.py first)" % (fp_name, voice_dir))
    with open(fp_path, encoding="utf-8") as fh:
        profile = json.load(fh)
    draft = analyze_texts([(draft_name, draft_raw)])
    draft_norm = norm(draft_raw)

    rows = []
    flags = 0
    for label, section, key, kind, tol, floor in DIAL_CHECKS:
        pv = profile.get(section, {}).get(key)
        dv = draft.get(section, {}).get(key)
        if pv is None or dv is None:
            continue
        verdict = "ok"
        if kind == "ratio":
            lo = max(pv * (1 - tol) - floor, 0)
            hi = pv * (1 + tol) + floor
            if dv < lo:
                verdict = "low (target %.1f to %.1f)" % (lo, hi)
            elif dv > hi:
                verdict = "high (target %.1f to %.1f)" % (lo, hi)
        elif kind == "ceiling":
            hi = pv * tol + floor
            if dv > hi:
                verdict = "high (limit %.1f)" % hi
        elif kind == "absolute":
            if abs(dv - pv) > tol:
                verdict = "off (target %.1f +/- %.1f)" % (pv, tol)
        if verdict != "ok":
            flags += 1
        rows.append((label, pv, dv, verdict))

    hard = []
    for b in BANNED:
        lines = find_lines(draft_raw, b)
        if lines:
            hard.append(("banned word", b, lines))
    for phrase, entry in load_entries(os.path.join(voice_dir, "not-me.md"), r"`([^`]+)`"):
        lines = find_lines(draft_raw, phrase)
        if lines:
            hard.append(("not-me", phrase, lines))

    approved = load_entries(os.path.join(voice_dir, "approved-language.md"), r'"([^"]+)"')
    reused = [p for p, _ in approved if phrase_in(draft_norm, p)]

    profile_dials = profile.get("dials", {})
    draft_dials = draft.get("dials", {})
    dial_diffs = [(k, profile_dials[k], draft_dials.get(k))
                  for k in profile_dials
                  if k in draft_dials and profile_dials[k] != draft_dials[k]]

    return {
        "draft": draft_name,
        "voice_dir": voice_dir,
        "fingerprint": fp_name,
        "fingerprint_date": profile.get("generated"),
        "profile_samples": len(profile.get("samples", [])),
        "draft_words": draft["pooled"]["words"],
        "rows": rows,
        "flags": flags,
        "hard": hard,
        "approved_total": len(approved),
        "approved_reused": reused,
        "dial_diffs": dial_diffs,
    }


def render(r):
    out = []
    out.append("voice_check: %s against %s/%s (%s, %d samples), draft %d words" % (
        r["draft"], r["voice_dir"], r["fingerprint"], r["fingerprint_date"],
        r["profile_samples"], r["draft_words"]))
    out.append("")
    out.append("%-36s %9s %9s  %s" % ("dial", "profile", "draft", "verdict"))
    for label, pv, dv, verdict in r["rows"]:
        mark = "  " if verdict == "ok" else "! "
        out.append("%s%-34s %9.1f %9.1f  %s" % (mark, label, pv, dv, verdict))
    out.append("")
    if r["dial_diffs"]:
        out.append("setting changes (profile -> draft):")
        for k, a, b in r["dial_diffs"]:
            out.append("  %s: %s -> %s" % (k, a, b))
        out.append("")
    if r["hard"]:
        out.append("HARD FAILS:")
        for kind, text, lines in r["hard"]:
            out.append("  %s: \"%s\" on line %s" % (
                kind, text, ", ".join(str(l) for l in lines)))
    else:
        out.append("hard fails: none")
    if r["approved_total"]:
        out.append("approved language reused: %d of %d banked lines" % (
            len(r["approved_reused"]), r["approved_total"]))
        for p in r["approved_reused"]:
            out.append("  \"%s\"" % (p if len(p) <= 90 else p[:87] + "..."))
    else:
        out.append("approved language: no approved-language.md found")
    out.append("")
    out.append("result: %d dial flag%s, %d hard fail%s" % (
        r["flags"], "" if r["flags"] == 1 else "s",
        len(r["hard"]), "" if len(r["hard"]) == 1 else "s"))
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("voice_dir")
    ap.add_argument("draft")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--register")
    args = ap.parse_args()

    if args.draft == "-":
        raw = sys.stdin.read()
        name = "stdin"
    else:
        with open(args.draft, encoding="utf-8", errors="replace") as fh:
            raw = fh.read()
        name = os.path.basename(args.draft)
    if not WORD.findall(raw):
        sys.exit("draft is empty")

    r = check(args.voice_dir, name, raw, args.register)
    if args.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
    else:
        print(render(r))
    sys.exit(1 if r["hard"] else 0)


if __name__ == "__main__":
    main()
