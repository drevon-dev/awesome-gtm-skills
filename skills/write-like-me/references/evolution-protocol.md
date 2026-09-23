# Evolution protocol

The profile is a hypothesis about how the writer writes. Every correction is evidence. This file turns evidence into a change without over-fitting to one mood or one piece.

## The one-percent rule

Cole's client rejected a piece as "doesn't sound like me". The words were fine. The dial that was off was evidence lean: the client spoke through studies and the draft leaned on opinion. Three "according to" sentences, about one percent of the text, fixed it.

So: when the writer says a draft is not them, assume one dial is off, find it, and move that dial. Do not rewrite the piece, and do not rewrite the profile. A reader who sees one wrong adjective will call the whole thing wrong. The fix is the adjective.

## Inputs to evolve

| The writer gives you | Do first |
|---|---|
| An edited version of your draft | Diff line by line against your draft |
| "That's not me" with no detail | Ask: "Which line bothered you first?" Then diff that line |
| "I'd never say X" | Straight to `not-me.md`, then check the draft for X and remove it |
| "I always say X" or "I think X" | `approved-language.md` or `stances.md`, no diff needed |
| A new sample of their writing | Save to `samples/`, re-run `voice_stats.py`, compare dials |
| Acceptance ("perfect", "posting this", no edits) | Bank the hook and any fresh lines as `accepted` |

## Classifying a change

For each changed span, ask which of these it is. Pick one.

| What changed | Dial or file | Update |
|---|---|---|
| A word swapped for a synonym | Word choice | Add the removed word to `not-me.md` if removed twice or with a comment; add the replacement to pet words if it recurs |
| A long sentence split, or short ones joined | Sentence length | Move the setting one step; note the register |
| A fragment repaired, or a sentence fragmented | Structure | Flip the fragments setting for this register |
| "I think" added or removed | Warmth (hedging) | Move the hedge setting one step |
| A study, source, number, or "according to" added or removed | Evidence lean | This is the Cole dial. Move it and quote the added line |
| "you" rewritten as "I" or "we", or the reverse | Person | Move the ratio for this format |
| A joke removed or added | Humor | Move kind or placement |
| Paragraph merged or split | Paragraphing | Move the length setting for this format |
| Bold, bullets, header, emoji added or removed | Formatting | Change that formatting setting |
| First sentence rewritten | Openers | Bank the writer's version as a hook; note the opener type |
| Last sentence rewritten or cut | Closers | Bank the sign-off; if a kicker was cut, add "no kicker" to not-me moves |
| Dash, contraction, exclamation, ellipsis changed | Mechanics | Change that setting |
| A position reversed or softened | `stances.md` | Add AGREE or DISAGREE in the writer's wording; supersede any conflicting line |
| A life detail corrected or added | `stories.md` | Fix the fact, keep the old line marked superseded, bank the approved wording |
| A line rewritten from scratch with no dial explanation | Approved language | Bank the writer's line; mark yours as `rejected` in not-me moves if the shape recurs |
| A slop pattern removed (contrast, kicker, colon reveal) | Slop floor | No profile change; note in changelog that the floor missed it |

## Thresholds

- One correction: record it as an observation in the changelog and, where the table says so, in the file. Do not change a dial setting in `profile.md` on one edit unless the writer stated the rule ("I never use em dashes").
- Two consistent corrections on the same dial: change the setting and quote both.
- A correction that contradicts an earlier one: do not overwrite. Ask which is right, offer the format as an explanation ("short posts versus essays?"), and record the answer. If the writer does not answer, keep both with their formats.
- A writer-stated rule always wins over an inferred setting.

## Confidence marks

In `profile.md`, tag each setting:

- `stated`: the writer said it
- `observed:N`: seen in N samples or corrections
- `inferred`: your read, not yet confirmed

Ask about `inferred` settings only when a draft depends on them.

## Approved language grows two ways

1. From samples, at learn time.
2. From use. Any sentence the writer typed into a correction, and any sentence you wrote that the writer accepted unchanged, gets banked. Mark the source. Increment `times reused` each time a banked line goes into a draft. High reuse counts are the writer's owned lines; prefer them for hooks.

## New samples

When new samples arrive, re-run `voice_stats.py` on the whole `samples/` folder. Compare the new `dials` block to the old one. Any dial that moved more than 20 percent gets a changelog line and a look: did the writer change, or did the new samples come from a different register?

## What never evolves from a draft

Facts. If a draft contained a number, date, or credential and the writer did not correct it, that is not confirmation. Only `stories.md`, the brief, or the writer's explicit statement can source a fact.

## The changelog entry

```
- <date> | evolve | <dial or file>: <old> -> <new> | "<the writer's words or the diff line>" | draft: <file>
```

Every change gets one. The changelog is how the writer audits what the skill believes about them, and how a second session picks up where the first left off.
