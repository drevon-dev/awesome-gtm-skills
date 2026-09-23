#!/usr/bin/env python3
"""voice_stats.py: measure the dials of a writer's voice from their own samples.

Usage:
    python3 voice_stats.py PATH [PATH ...] [-o fingerprint.json] [--quiet]

PATH is a .md or .txt file, or a directory whose .md and .txt files are read.
Writes a JSON fingerprint (to stdout unless -o is given) and prints a short
dial summary to stderr. Standard library only.

The numbers are evidence, not the profile. Read the samples too.
"""
import argparse
import json
import os
import re
import statistics
import sys
from collections import Counter
from datetime import date

STOPWORDS = set("""
a about above after again against all am an and any are as at be because been
before being below between both but by can did do does doing down during each
few for from further had has have having he her here hers herself him himself
his how i if in into is it its itself just me more most my myself no nor not
now of off on once only or other our ours ourselves out over own same she
should so some such than that the their theirs them themselves then there
these they this those through to too under until up very was we were what when
where which while who whom why will with would you your yours yourself
yourselves im ive id ill youre youve dont doesnt didnt isnt arent wasnt werent
cant couldnt wouldnt shouldnt wont thats theres heres whats lets get got go
going one two also like really thing things way make made even much many still
back new use used take know think see want need say said says
""".split())

BANNED = [
    "delve", "foster", "leverage", "utilize", "facilitate", "empower",
    "streamline", "robust", "cutting-edge", "paradigm shift", "game changer",
    "game-changer", "this is huge", "this changes everything", "tapestry",
    "realm", "beacon", "multifaceted", "meticulous", "intricate", "paramount",
    "transformative", "elevate", "embark", "supercharge", "harness",
    "ever-evolving", "seamless", "testament", "pivotal", "underscore",
]

HEDGES = [
    "i think", "i guess", "maybe", "probably", "perhaps", "i suspect",
    "i believe", "it seems", "sort of", "kind of", "in my opinion",
    "i feel like", "not sure", "arguably", "i'd argue",
]
INTENSIFIERS = [
    "very", "really", "super", "extremely", "incredibly", "totally",
    "absolutely", "literally", "honestly", "actually", "truly", "insanely",
    "massively", "hugely", "genuinely",
]
CITATION = [
    "according to", "study", "studies", "research shows", "survey", "report",
    "data shows", "found that", "per the", "source:", "cited", "percent",
]
PROFANITY = ["fuck", "fucking", "shit", "damn", "crap", "bullshit", "ass"]
FIRST = {"i", "me", "my", "mine", "myself", "i'm", "i've", "i'd", "i'll",
         "im", "ive"}
SECOND = {"you", "your", "yours", "yourself", "you're", "you've", "you'd",
          "you'll", "youre", "youve"}
WE = {"we", "us", "our", "ours", "ourselves", "we're", "we've", "we'd",
      "we'll"}
CONJ_OPENERS = {"and", "but", "so", "or", "because", "yet"}

ABBREVIATIONS = re.compile(
    r"\b(e\.g|i\.e|vs|etc|mr|mrs|ms|dr|st|inc|ltd|no|jr|sr|u\.s|a\.m|p\.m|"
    r"approx|dept|est|fig|vol)\.$", re.I)
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿\U0001F000-\U0001F2FF]")
WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’-]*")


# --------------------------------------------------------------------------
# text handling
# --------------------------------------------------------------------------

def strip_markdown(text):
    """Return (prose, formatting_counts). Prose keeps paragraph breaks."""
    fmt = Counter()
    text, n = re.subn(r"```.*?```", " ", text, flags=re.S)
    fmt["code_blocks"] = n
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"</?[A-Za-z][^>\n]*>", " ", text)  # html / mdx components

    out = []
    in_front_matter = False
    for i, raw in enumerate(text.split("\n")):
        s = raw.strip()
        if i == 0 and s == "---":
            in_front_matter = True
            continue
        if in_front_matter:
            if s == "---":
                in_front_matter = False
            continue
        if not s:
            out.append("")
            continue
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", s):
            out.append("")
            continue
        if s.startswith("|"):
            fmt["table_rows"] += 1
            continue
        if re.match(r"^#\s", s):
            fmt["h1"] += 1
            continue  # the title is not the first sentence
        if re.match(r"^#{2,6}\s", s):
            fmt["headers"] += 1
            s = re.sub(r"^#{2,6}\s+", "", s)
            if not s.endswith((".", "!", "?")):
                s += "."
        elif re.match(r"^[-*+]\s", s):
            fmt["bullets"] += 1
            s = re.sub(r"^[-*+]\s+", "", s)
        elif re.match(r"^\d+[.)]\s", s):
            fmt["numbered"] += 1
            s = re.sub(r"^\d+[.)]\s+", "", s)
        elif s.startswith(">"):
            fmt["blockquotes"] += 1
            s = s.lstrip("> ").strip()
        out.append(s)
    text = "\n".join(out)

    fmt["bold"] = len(re.findall(r"\*\*[^*\n]+\*\*", text)) + \
        len(re.findall(r"__[^_\n]+__", text))
    fmt["italic"] = len(re.findall(r"(?<![*\w])\*[^*\n]+\*(?![*\w])", text))
    fmt["links"] = len(re.findall(r"\[[^\]]+\]\([^)]+\)", text))
    fmt["emoji"] = len(EMOJI.findall(text))

    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"[*_`#]+", "", text)
    return text, fmt


def split_paragraphs(prose):
    if "\n\n" in prose:
        parts = re.split(r"\n\s*\n", prose)
    else:
        parts = prose.split("\n")
    return [p.strip() for p in parts if p.strip()]


def split_sentences(paragraph):
    text = re.sub(r"\s*\n\s*", " \n ", paragraph)
    pieces = re.split(r"(?<=[.!?…])[\"'”’)\]]*\s+(?=[\"'“‘(\[A-Z0-9])|\s*\n\s*",
                      text)
    sentences = []
    buf = ""
    for p in pieces:
        p = p.strip()
        if not p:
            continue
        if buf:
            buf = buf + " " + p
        else:
            buf = p
        if ABBREVIATIONS.search(buf):
            continue
        sentences.append(buf)
        buf = ""
    if buf:
        sentences.append(buf)
    return sentences


def words_of(sentence):
    return WORD.findall(sentence)


def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and not w.endswith(("le", "ee", "ye")) and n > 1:
        n -= 1
    return max(1, n)


def is_contraction(tok):
    t = tok.lower().replace("’", "'")
    if "'" not in t:
        return False
    if t.endswith("'s"):
        return t in ("it's", "that's", "there's", "here's", "what's", "let's",
                     "he's", "she's", "who's", "where's", "how's")
    return bool(re.search(r"(n't|'re|'ve|'ll|'d|'m)$", t))


def count_phrases(text_lower, phrases):
    return sum(len(re.findall(r"(?<![a-z])" + re.escape(p) + r"(?![a-z])",
                              text_lower)) for p in phrases)


# --------------------------------------------------------------------------
# analysis
# --------------------------------------------------------------------------

def analyze_texts(named_texts):
    """named_texts: list of (name, raw_text). Returns the fingerprint dict."""
    per_sample = []
    all_sentences = []
    all_words = []
    all_paragraphs = []
    fmt_total = Counter()
    prose_total = []
    sentence_sets = []
    ngram_by_sample = []

    for name, raw in named_texts:
        prose, fmt = strip_markdown(raw)
        fmt_total.update(fmt)
        prose_total.append(prose)
        paragraphs = split_paragraphs(prose)
        sentences = []
        for p in paragraphs:
            ps = split_sentences(p)
            sentences.extend(ps)
            all_paragraphs.append(ps)
        words = [w for s in sentences for w in words_of(s)]
        lens = [len(words_of(s)) for s in sentences] or [0]
        per_sample.append({
            "file": name,
            "words": len(words),
            "sentences": len(sentences),
            "paragraphs": len(paragraphs),
            "sentence_mean": round(statistics.mean(lens), 1),
            "first_sentence": sentences[0] if sentences else "",
            "last_sentence": sentences[-1] if sentences else "",
        })
        all_sentences.extend(sentences)
        all_words.extend(words)
        sentence_sets.append(set(re.sub(r"\W+", " ", s.lower()).strip()
                                 for s in sentences if len(words_of(s)) >= 5))
        toks = [w.lower().replace("’", "'") for w in words]
        grams = set()
        for n in (3, 4, 5, 6):
            for i in range(len(toks) - n + 1):
                g = tuple(toks[i:i + n])
                if all(t in STOPWORDS for t in g):
                    continue
                grams.add(g)
        ngram_by_sample.append((Counter(tuple(toks[i:i + n])
                                        for n in (3, 4, 5, 6)
                                        for i in range(len(toks) - n + 1)),
                                grams))

    nw = len(all_words) or 1
    ns = len(all_sentences) or 1
    lower_words = [w.lower().replace("’", "'") for w in all_words]
    prose_all = "\n\n".join(prose_total)
    prose_lower = prose_all.lower()
    lens = [len(words_of(s)) for s in all_sentences] or [0]

    def per100w(x):
        return round(100.0 * x / nw, 2)

    def per1000w(x):
        return round(1000.0 * x / nw, 2)

    def per100s(x):
        return round(100.0 * x / ns, 1)

    first_words = [words_of(s)[0].lower() if words_of(s) else ""
                   for s in all_sentences]
    conj = sum(1 for f in first_words if f in CONJ_OPENERS)
    starts_i = sum(1 for f in first_words if f in ("i", "i'm", "i've", "i'd"))
    starts_you = sum(1 for f in first_words if f in ("you", "you're", "your"))
    questions = sum(1 for s in all_sentences if s.rstrip().endswith("?"))
    exclaims = sum(1 for s in all_sentences if s.rstrip().endswith("!"))
    fragments = sum(1 for l in lens if 0 < l <= 3)
    passive = sum(1 for s in all_sentences if re.search(
        r"\b(is|are|was|were|be|been|being|get|got|gets)\s+(\w+ed|\w+en)\b",
        s, re.I))
    syl = sum(syllables(w) for w in all_words)
    long_words = sum(1 for w in all_words if syllables(w) >= 3)
    flesch = 206.835 - 1.015 * (nw / ns) - 84.6 * (syl / nw)

    para_sent_counts = [len(p) for p in all_paragraphs] or [0]
    para_word_counts = [sum(len(words_of(s)) for s in p)
                        for p in all_paragraphs] or [0]

    content = Counter(w for w in lower_words
                      if w not in STOPWORDS and len(w) > 2
                      and not w.isdigit())
    banned_found = {}
    for b in BANNED:
        c = len(re.findall(r"(?<![a-z])" + re.escape(b) + r"(?![a-z])",
                           prose_lower))
        if c:
            banned_found[b] = c

    # repeated phrases across samples (approved-language candidates)
    gram_total = Counter()
    gram_samples = Counter()
    for counts, grams in ngram_by_sample:
        for g in grams:
            gram_total[g] += counts[g]
            gram_samples[g] += 1
    repeated = []
    for g, c in gram_total.items():
        if c >= 2 and (gram_samples[g] >= 2 or c >= 3):
            repeated.append((c, gram_samples[g], " ".join(g)))
    repeated.sort(key=lambda t: (-t[1], -t[0], -len(t[2])))
    # drop phrases contained in a longer phrase with the same counts
    kept = []
    for c, sc, phrase in repeated:
        if any(phrase in k[2] and k[0] == c for k in kept):
            continue
        kept.append((c, sc, phrase))
    repeated_phrases = [{"phrase": p, "count": c, "samples": sc}
                        for c, sc, p in kept[:40]]

    sentence_counter = Counter()
    for sset in sentence_sets:
        sentence_counter.update(sset)
    repeated_sentences = [{"sentence": s, "samples": c}
                          for s, c in sentence_counter.most_common(20)
                          if c >= 2]

    pooled = {
        "words": nw if all_words else 0,
        "sentences": ns if all_sentences else 0,
        "paragraphs": len(all_paragraphs),
        "sentence_mean": round(statistics.mean(lens), 1),
        "sentence_median": statistics.median(lens),
        "sentence_stdev": round(statistics.pstdev(lens), 1),
        "sentence_max": max(lens),
        "pct_under_8": per100s(sum(1 for l in lens if l < 8)),
        "pct_over_25": per100s(sum(1 for l in lens if l > 25)),
        "fragments_pct": per100s(fragments),
        "conjunction_openers_pct": per100s(conj),
        "sentences_starting_I_pct": per100s(starts_i),
        "sentences_starting_you_pct": per100s(starts_you),
        "questions_per_100_sentences": per100s(questions),
        "exclamations_per_100_sentences": per100s(exclaims),
        "passive_per_100_sentences": per100s(passive),
        "paragraph_mean_sentences": round(statistics.mean(para_sent_counts), 2),
        "paragraph_mean_words": round(statistics.mean(para_word_counts), 1),
        "paragraph_pct_single_sentence": per100s(
            sum(1 for c in para_sent_counts if c == 1)) if all_paragraphs else 0,
        "first_person_per_100w": per100w(sum(1 for w in lower_words if w in FIRST)),
        "second_person_per_100w": per100w(sum(1 for w in lower_words if w in SECOND)),
        "we_per_100w": per100w(sum(1 for w in lower_words if w in WE)),
        "contractions_per_100w": per100w(sum(1 for w in all_words if is_contraction(w))),
        "hedges_per_100w": per100w(count_phrases(prose_lower, HEDGES)),
        "intensifiers_per_100w": per100w(count_phrases(prose_lower, INTENSIFIERS)),
        "numbers_per_100w": per100w(sum(1 for w in all_words if re.search(r"\d", w))),
        "citation_markers_per_1000w": per1000w(count_phrases(prose_lower, CITATION)),
        "em_dashes_per_1000w": per1000w(prose_all.count("—") + len(re.findall(r"(?<!-)--(?!-)", prose_all))),
        "spaced_hyphens_per_1000w": per1000w(len(re.findall(r"\s-\s", prose_all))),
        "semicolons_per_1000w": per1000w(prose_all.count(";")),
        "colons_per_1000w": per1000w(len(re.findall(r":\s", prose_all))),
        "parentheses_per_1000w": per1000w(prose_all.count("(")),
        "ellipses_per_1000w": per1000w(len(re.findall(r"\.\.\.|…", prose_all))),
        "quotes_per_1000w": per1000w(len(re.findall(r"[\"“]", prose_all))),
        "flesch_reading_ease": round(flesch, 1),
    }
    fixed_pct_over_25 = pooled["pct_over_25"]
    pooled["pct_over_25"] = fixed_pct_over_25

    formatting = {
        "headers_per_1000w": per1000w(fmt_total["headers"]),
        "bullets_per_1000w": per1000w(fmt_total["bullets"] + fmt_total["numbered"]),
        "bold_per_1000w": per1000w(fmt_total["bold"]),
        "italic_per_1000w": per1000w(fmt_total["italic"]),
        "blockquotes_per_1000w": per1000w(fmt_total["blockquotes"]),
        "links_per_1000w": per1000w(fmt_total["links"]),
        "emoji": fmt_total["emoji"],
        "code_blocks": fmt_total["code_blocks"],
        "table_rows": fmt_total["table_rows"],
    }

    vocabulary = {
        "type_token_ratio": round(len(set(lower_words)) / nw, 3) if all_words else 0,
        "avg_word_length": round(sum(len(w) for w in all_words) / nw, 2) if all_words else 0,
        "pct_long_words": per100w(long_words),
        "profanity_count": count_phrases(prose_lower, PROFANITY),
        "banned_found": banned_found,
        "top_words": [{"word": w, "count": c} for w, c in content.most_common(40)],
        "repeated_phrases": repeated_phrases,
        "repeated_sentences": repeated_sentences,
    }

    openers = {
        "top_first_words": [{"word": w, "count": c}
                            for w, c in Counter(f for f in first_words if f).most_common(15)],
        "sample_first_sentences": [s["first_sentence"] for s in per_sample],
    }
    closers = {
        "sample_last_sentences": [s["last_sentence"] for s in per_sample],
    }

    return {
        "generated": date.today().isoformat(),
        "samples": per_sample,
        "pooled": pooled,
        "formatting": formatting,
        "vocabulary": vocabulary,
        "openers": openers,
        "closers": closers,
        "dials": interpret(pooled, formatting, vocabulary),
    }


def interpret(p, f, v):
    """Turn numbers into the settings vocabulary used in profile.md."""
    d = {}
    m = p["sentence_mean"]
    d["sentence_length"] = "short" if m < 12 else "medium" if m <= 18 else "long"
    d["sentence_variance"] = "even" if p["sentence_stdev"] < 0.5 * max(m, 1) else "varied"
    d["fragments"] = ("load-bearing" if p["fragments_pct"] >= 8
                      else "occasional" if p["fragments_pct"] >= 2 else "none")
    d["conjunction_openers"] = "common" if p["conjunction_openers_pct"] >= 8 else "rare"
    d["questions_as_pivots"] = "yes" if p["questions_per_100_sentences"] >= 3 else "no"
    d["semicolons"] = "yes" if p["semicolons_per_1000w"] >= 1 else "no"
    fp, sp, we = p["first_person_per_100w"], p["second_person_per_100w"], p["we_per_100w"]
    top = max(fp, sp, we)
    if top < 1.5:
        d["person"] = "impersonal"
    elif fp == top and fp > 1.3 * max(sp, we):
        d["person"] = "I-led"
    elif sp == top and sp > 1.3 * max(fp, we):
        d["person"] = "you-led"
    elif we == top and we > 1.3 * max(fp, sp):
        d["person"] = "we-led"
    else:
        d["person"] = "balanced"
    if p["citation_markers_per_1000w"] >= 3:
        d["evidence_lean"] = "cited-evidence"
    elif p["numbers_per_100w"] >= 1.5 and fp >= 2:
        d["evidence_lean"] = "personal-evidence"
    elif p["numbers_per_100w"] >= 1.5:
        d["evidence_lean"] = "numbers-without-person"
    else:
        d["evidence_lean"] = "assertion"
    d["hedging"] = ("hedged" if p["hedges_per_100w"] >= 0.8
                    else "light" if p["hedges_per_100w"] >= 0.3 else "blunt")
    d["intensifiers"] = "frequent" if p["intensifiers_per_100w"] >= 0.8 else "sparse"
    d["contractions"] = ("always" if p["contractions_per_100w"] >= 2
                         else "sometimes" if p["contractions_per_100w"] >= 0.5 else "rare")
    ps = p["paragraph_mean_sentences"]
    d["paragraphs"] = ("one-liners" if ps < 1.5 else "short" if ps <= 2.5
                       else "medium" if ps <= 4 else "long")
    if p["em_dashes_per_1000w"] >= 2:
        d["dash_style"] = "em dash"
    elif p["spaced_hyphens_per_1000w"] >= 1:
        d["dash_style"] = "spaced hyphen"
    else:
        d["dash_style"] = "none"
    d["exclamation"] = ("frequent" if p["exclamations_per_100_sentences"] >= 5
                        else "rare" if p["exclamations_per_100_sentences"] > 0 else "none")
    d["ellipsis"] = "yes" if p["ellipses_per_1000w"] >= 1 else "no"
    d["emoji"] = "yes" if f["emoji"] > 0 else "none"
    d["headers"] = "heavy" if f["headers_per_1000w"] >= 8 else "some" if f["headers_per_1000w"] > 0 else "none"
    d["bullets"] = "heavy" if f["bullets_per_1000w"] >= 15 else "some" if f["bullets_per_1000w"] > 0 else "none"
    d["bold"] = "heavy" if f["bold_per_1000w"] >= 8 else "some" if f["bold_per_1000w"] > 0 else "none"
    d["blockquotes"] = "yes" if f["blockquotes_per_1000w"] > 0 else "none"
    fr = p["flesch_reading_ease"]
    d["reading_level"] = ("plain" if fr >= 70 else "standard" if fr >= 55
                          else "dense")
    d["profanity"] = ("frequent" if v["profanity_count"] >= 5
                      else "occasional" if v["profanity_count"] > 0 else "none")
    d["banned_slop_words"] = "present" if v["banned_found"] else "none"
    return d


# --------------------------------------------------------------------------
# io
# --------------------------------------------------------------------------

def collect(paths):
    named = []
    for p in paths:
        if os.path.isdir(p):
            for fn in sorted(os.listdir(p)):
                if fn.lower().endswith((".md", ".txt", ".markdown")):
                    fp = os.path.join(p, fn)
                    with open(fp, encoding="utf-8", errors="replace") as fh:
                        named.append((fn, fh.read()))
        elif os.path.isfile(p):
            with open(p, encoding="utf-8", errors="replace") as fh:
                named.append((os.path.basename(p), fh.read()))
        else:
            sys.stderr.write("skip (not found): %s\n" % p)
    return named


def summary(fp):
    d = fp["dials"]
    p = fp["pooled"]
    lines = [
        "voice_stats: %d samples, %d words, %d sentences" % (
            len(fp["samples"]), p["words"], p["sentences"]),
        "  sentence length %s (mean %.1f, stdev %.1f), variance %s" % (
            d["sentence_length"], p["sentence_mean"], p["sentence_stdev"],
            d["sentence_variance"]),
        "  fragments %s, conj openers %s, questions %s, semicolons %s" % (
            d["fragments"], d["conjunction_openers"], d["questions_as_pivots"],
            d["semicolons"]),
        "  person %s (I %.1f / you %.1f / we %.1f per 100w)" % (
            d["person"], p["first_person_per_100w"],
            p["second_person_per_100w"], p["we_per_100w"]),
        "  evidence %s, hedging %s, intensifiers %s, contractions %s" % (
            d["evidence_lean"], d["hedging"], d["intensifiers"],
            d["contractions"]),
        "  paragraphs %s (%.1f sentences), dash %s, exclamation %s, emoji %s" % (
            d["paragraphs"], p["paragraph_mean_sentences"], d["dash_style"],
            d["exclamation"], d["emoji"]),
        "  reading level %s (flesch %.0f), banned slop words %s" % (
            d["reading_level"], p["flesch_reading_ease"],
            d["banned_slop_words"]),
    ]
    rp = fp["vocabulary"]["repeated_phrases"][:5]
    if rp:
        lines.append("  repeated phrases: " + "; ".join(
            '"%s" x%d' % (r["phrase"], r["count"]) for r in rp))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("-o", "--output", help="write fingerprint JSON here")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    named = collect(args.paths)
    if not named:
        sys.exit("no samples found")
    fp = analyze_texts(named)
    js = json.dumps(fp, indent=2, ensure_ascii=False)
    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(js + "\n")
    else:
        print(js)
    if not args.quiet:
        sys.stderr.write(summary(fp) + "\n")
        if args.output:
            sys.stderr.write("wrote %s\n" % args.output)


if __name__ == "__main__":
    main()
