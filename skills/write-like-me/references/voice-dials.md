# Voice dials

Voice feels like one intangible thing. It is a small set of settings that a reader adds up into "sounds like them". Cole names four: word choice, sentence length, sentence structure, and opinion versus evidence. This file expands the set to twelve so a profile can be written from evidence and a correction can be traced to a single dial.

For each dial: what to look at, what `fingerprint.json` reports, the vocabulary to use in `profile.md`, and how to apply it when drafting. Always quote a real line from the samples next to a setting. A setting without a quote is a guess.

## 1. Word choice

Look at: plain versus elevated vocabulary, slang, profanity, jargon, named tools and brands, intensifiers, the writer's pet words and pet phrases.

Fingerprint: `vocabulary.avg_word_length`, `vocabulary.pct_long_words`, `pooled.flesch_reading_ease`, `pooled.intensifiers_per_100w`, `vocabulary.profanity_count`, `vocabulary.top_words`, `vocabulary.banned_found`.

Settings: plain / mixed / elevated. Profanity none / occasional / frequent. Jargon avoided / used unexplained / used and explained. Pet words as a list.

Apply: take the plainer synonym unless the profile says otherwise. Use the pet words where they fit. Never use a word from `not-me.md`. Cole's example: "really cool", "exquisite", and "fucking dope" describe the same thing and three different people.

## 2. Sentence length

Fingerprint: `pooled.sentence_mean`, `sentence_median`, `sentence_stdev`, `pct_under_8`, `pct_over_25`.

Settings: short (mean under 12), medium (12 to 18), long (over 18). Variance even (stdev under half the mean) or varied.

Apply: match the mean within 25 percent. Match the variance shape. A writer who mixes four-word and thirty-word sentences must not get uniform fifteen-word ones back.

## 3. Sentence structure

Look at: fragments, sentences opening with And, But, or So, questions followed by their answer, anaphora (three sentences sharing an opener), semicolons, parentheses, lists inside sentences, whether subordinate clauses come first or last.

Fingerprint: `pooled.fragments_pct`, `conjunction_openers_pct`, `questions_per_100_sentences`, `semicolons_per_1000w`, `parentheses_per_1000w`, `passive_per_100_sentences`.

Settings: fragments none / occasional / load-bearing. Conjunction openers rare / common. Questions as pivots yes / no. Semicolons yes / no. Anaphora yes / no.

Apply: if fragments are load-bearing, a slop pass must not repair them. Write in the profile: "Fragments are the writer's. Keep them."

## 4. Evidence lean

Look at: how the writer backs a claim. Their own timeline and numbers, conversations they had, cited studies and publications, or bare assertion.

Fingerprint: `pooled.numbers_per_100w`, `citation_markers_per_1000w`, `hedges_per_100w`, `first_person_per_100w`.

Settings: personal-evidence / cited-evidence / assertion / mixed. Numbers dense / sparse.

Apply: this is the dial in Cole's ghostwriting story. The client spoke through studies, the draft leaned on opinion, and three "according to" sentences fixed it. When the words look right and the piece still feels wrong, check this dial first.

## 5. Person

Fingerprint: `pooled.first_person_per_100w`, `second_person_per_100w`, `we_per_100w`, `sentences_starting_I_pct`, `sentences_starting_you_pct`.

Settings: I-led / you-led / we-led / balanced. Record per format. Social posts and documentation often differ.

Apply: "you should" pulls a piece toward commodity. "I did" and "I think" pull it toward personality. Match the profile, and shift toward I for personality-tier pieces.

## 6. Warmth and bluntness

Look at: hedges and softeners versus flat statements, apology, how disagreement is phrased, imperatives, exclamation.

Fingerprint: `pooled.hedges_per_100w`, `intensifiers_per_100w`, `exclamations_per_100_sentences`.

Settings: blunt / direct-but-warm / hedged / diplomatic.

Apply: keep the writer's hedges when the samples have them. "I think" every third sentence is a voice, not filler. Do not add hedges to a blunt writer.

## 7. Humor

Look at: none, dry aside, self-deprecating, absurd image, sarcasm. Where it lands: openers, closers, parentheticals.

Fingerprint: nothing reliable. Read for it.

Settings: none / dry / self-deprecating / playful, plus placement.

Apply: never add jokes to a writer who makes none. Match the kind, not just the presence.

## 8. Paragraphing

Fingerprint: `pooled.paragraph_mean_sentences`, `paragraph_pct_single_sentence`, `paragraph_mean_words`.

Settings: one-liners / short (1 to 2 sentences) / medium (3 to 4) / long.

Apply: paragraph length is often the strongest visual signal of a writer. A four-sentence paragraph from a one-liner writer reads as someone else.

## 9. Formatting

Fingerprint: `formatting.headers_per_1000w`, `bullets_per_1000w`, `bold_per_1000w`, `blockquotes_per_1000w`, `emoji`, `links_per_1000w`.

Settings: for each, none / occasional / heavy. What bold is used for. What blockquotes carry.

Apply: zero emoji in the samples means zero emoji. Bold only for the use the profile names.

## 10. Openers

Fingerprint: `openers.top_first_words`, `openers.sample_first_sentences`.

Settings: cold open with the claim / scene / question / "I" statement / data point. Setup paragraphs yes / no.

Apply: the first sentence is the highest-value banked language. Check `approved-language.md` for reusable hooks before writing a new one.

## 11. Closers

Fingerprint: `closers.sample_last_sentences`.

Settings: sign-off word. Last paragraph flat / call to action / question / punch.

Apply: copy the sign-off exactly. If the writer ends flat, do not add a kicker.

## 12. Punctuation and mechanics

Fingerprint: `pooled.em_dashes_per_1000w`, `spaced_hyphens_per_1000w`, `ellipses_per_1000w`, `exclamations_per_100_sentences`, `contractions_per_100w`, `quotes_per_1000w`.

Settings: dash style em / spaced hyphen / none. Contractions always / mostly / never / by register. Exclamation none / rare. Ellipsis yes / no. Oxford comma yes / no (read for it). Capitalisation quirks. Numerals versus spelled numbers.

Apply: mechanics are cheap to match and loud when wrong. A writer who types " - " and gets "—" back notices in the first line.

## Registers

Many writers have two: a short build or social register, and a longer essay register. When the samples split, run `voice_stats.py` on each group separately and record two dial sets in `profile.md` with the trigger for each (format, length, audience). Within one piece, never mix registers.

## What the numbers cannot tell you

Humor, warmth, what the writer is proud of, what they are tired of saying, which examples they reach for, and whether a line is theirs or borrowed. Read every sample. The fingerprint tells you where to look. It does not tell you who the person is.
