# Write-like-me eval

Run after every write, edit, check, learn, or evolve. Answer each check pass or fail. Fix and re-run on any fail.

## Attribution (the ceiling)

1. Could a reader who knows the writer's published work pick this out of a lineup of three drafts on the same topic? If not, which dial is generic?
2. Does the draft reuse at least one line from `approved-language.md` when the library has a relevant one? Was reuse preferred over fresh phrasing?
3. For a personality-tier piece: does it carry a story or first-person detail from `stories.md`, or a clearly marked `[STORY]` slot? Is every life detail, number, and credential traceable to the library or the brief?
4. Does every position the draft takes appear in `stances.md`, or is it flagged as unsettled? Did the draft avoid picking a side the writer has not taken?
5. Is the tier and horizon label stated, and does the writing match it? A timeless piece has no "just launched" or "in 2026" unless the writer asked for a timely one.

## Dials

6. Sentence length: mean within 25 percent of the profile, and the same variance shape?
7. Structure: fragments, conjunction openers, questions, and semicolons at the profile's rate? Load-bearing fragments preserved through the slop pass?
8. Evidence lean: does the draft back claims the way the writer does (own numbers, named conversations, cited sources, or bare assertion)? This is the first dial to check when the words look right and the piece still feels wrong.
9. Person: I, you, and we at the profile's ratio for this format?
10. Word choice: plain where the writer is plain, pet words used, nothing from `not-me.md`?
11. Warmth and humor: hedges and jokes present only in the kind and amount the writer uses?
12. Paragraphing and formatting: paragraph length, headers, bullets, bold, blockquotes, and emoji at the profile's rate?
13. Openers and closers: opens the way the writer opens, closes with the writer's sign-off, no added kicker if the writer ends flat?
14. Mechanics: dash style, contractions, exclamation marks, ellipses, and numerals match the profile?
15. Register: one register per piece, the right one for the format?

## Slop floor

16. Did the draft pass the full `no-ai-slop` check (bundled at `no-ai-slop/RULES.md` and `no-ai-slop/eval.md`, or the project's own tuned copy)? No binary contrasts, throat-clearing, faux-insight setups, colon reveals, importance puffery, weasel attribution, fake-profound kickers, recap endings, banned words, decorative em dashes.
17. If any slop pattern was kept, is it one the writer demonstrably uses, recorded in `profile.md` with a quote?

## Script gates

18. Did `voice_check.py` run, and is every flag either fixed or explained in the delivery note?
19. For learn: did `voice_stats.py` run and does `fingerprint.json` exist?

## Learn mode

20. Does every dial setting in `profile.md` have a quoted line from the samples as evidence?
21. Were stances and stories mined from the samples before asking the writer anything?
22. Was the interview one round of at most five questions, with an offer to skip?
23. Was the writer shown a summary and asked for up to three corrections?

## Evolve mode

24. Was each correction classified to one dial or file, and only that dial updated?
25. Did rejected words go to `not-me.md`, writer-typed lines to `approved-language.md`, positions to `stances.md`, life details to `stories.md`?
26. Is there a dated `changelog.md` entry with the quote that caused the change?
27. Was a contradiction with an earlier correction surfaced to the writer rather than silently overwritten?
28. Was nothing deleted, only marked superseded?

## Delivery

29. Is the delivery note five lines or fewer: tier and horizon, reused lines, stances used, open slots or questions?
30. Would the writer read this and say "that's me", or at worst point at one line?
