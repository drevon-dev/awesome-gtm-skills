# Library file templates

Copy these when creating a voice folder. Keep the formats exactly, because `voice_check.py` parses `not-me.md` and `approved-language.md`.

Entry conventions across all files:

- One entry per line, starting with `- `.
- Matchable text goes in backticks for `not-me.md` and in double quotes for `approved-language.md`.
- Fields separated by ` | `.
- Dates are `YYYY-MM-DD`.
- Nothing is deleted. Superseded entries get ` | superseded by: <text>` appended.

## profile.md

```
# Voice profile: <handle>

kind: person            # or brand
learned: 2026-09-23
samples: 6 files, 7,205 words
registers: build (default for social), essay (blog, long LinkedIn)

## Summary in the writer's words
<two or three sentences the writer approved describing how they write>

## Dials
| Dial | Setting | Evidence (quoted from samples) |
|---|---|---|
| Word choice | plain, no profanity, tool names unhedged | "I opened Notion, Linear, and a blank doc" |
| Sentence length | short in build (mean 9), medium in essay (mean 17), varied | "5 minutes. Done." / "I've been fortunate enough to witness..." |
| Structure | fragments load-bearing, questions as pivots, anaphora | "More tokens. More latency. More things that can break." |
| Evidence lean | personal, own numbers and dates, never a study | "I shipped my first paid product in 2019" |
| Person | I-led in essays, you-led in how-tos | ... |
| Warmth | direct, no hedging, no apology | ... |
| Humor | dry, rare, in closers | ... |
| Paragraphing | one to two sentences | ... |
| Formatting | zero emoji, bold for the operative term, blockquote for thesis | ... |
| Openers | cold open with the claim, no setup | "Software work is changing." |
| Closers | flat last paragraph then "Cheers." | ... |
| Mechanics | spaced hyphen not em dash, contractions in build only, two exclamation marks in 7k words | ... |

## Load-bearing patterns a slop pass must keep
- fragments
- "Rule of thumb:" as a teaching closer

## Do not
- <things the writer never does, with evidence of absence>
```

## stances.md

```
# Stances: <handle>

Commodity ideas the writer has taken a side on. One per line. Source is a sample file, "interview", or "correction".

## <topic>
- AGREE | <the idea in the writer's wording> | source | date
- DISAGREE | <the idea> | source | date
- OPEN | <a debate in this topic the writer has not settled; ask before using> | date
```

## stories.md

```
# Stories: <handle>

Personality details and formative stories. Use the approved wording verbatim where one exists.

## Facts
- <fact> | approved wording: "<exact sentence>" | source | date

## Stories
- <title> | when it happened | one-line summary | approved wording: "<the sentence that opens it>" | used in: <files> | source | date

## Recurring lines the writer says in person but has not written yet
- <line> | interview | date
```

## approved-language.md

```
# Approved language: <handle>

Sentences and phrasings to reuse verbatim. Each has been written or accepted by the writer.

## Hooks
- "<sentence>" | source: samples/<file> | tags: hook, personality | times reused: 0

## Openers
- "<sentence>" | source | tags

## Closers
- "<sentence>" | source | tags

## Recurring phrases
- "<phrase>" | source | tags

## Accepted from drafts
- "<sentence>" | source: draft <date> <title> | accepted | tags
```

## not-me.md

```
# Not me: <handle>

Words, phrases, and moves the writer rejected. Backticked text is matched by voice_check.py.

## Words and phrases
- `leverage` | "I'd never say leverage" | 2026-09-23
- `game changer` | removed from draft without comment | 2026-09-23

## Moves (not matched, read before drafting)
- ending on a metaphor | "cut the last line, too cute" | 2026-09-23
- opening with a question | replaced twice in a row | 2026-09-24
```

## changelog.md

```
# Changelog: <handle>

- 2026-09-23 | learn | profile created from 6 samples
- 2026-09-24 | evolve | sentence length in essay register moved from "long" to "medium" | "the paragraphs read like a textbook" | draft: linkedin_agents.md
- 2026-09-24 | evolve | added stance DISAGREE "cold email is dead" | user typed "I don't think cold email is dead, I think untargeted cold email is dead"
- 2026-09-25 | evolve | banked accepted hook "I built an AI coworker in 2 days" | draft accepted unchanged
```

## samples/

One file per piece, named `<YYYY-MM-DD>_<format>_<slug>.md` when the date is known, otherwise `<format>_<slug>.md`. Never edit a sample.
