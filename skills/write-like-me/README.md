# write-like-me

A Claude Code skill that learns how you write from your own samples, then drafts, edits, and checks writing in your voice with no AI slop. It keeps a small library per writer (dial settings, stances, stories, approved sentences, rejected words) and updates that library from every correction you make.

Built on Nicolas Cole's model from ["$30M Writer: Never write AI slop again"](https://www.youtube.com/watch?v=YuOSyRj3sXg) (Greg Isenberg, Sept 2026): language is open source, voice is a handful of dials, slop is the model not knowing your stances and your stories, and the model's job is to repeat what you already said well.

## Install

Copy this folder into a skills directory:

```
# one project
cp -r write-like-me <project>/.claude/skills/

# every project
cp -r write-like-me ~/.claude/skills/
```

Requirements: Python 3.8 or newer (standard library only). Nothing else. The `no-ai-slop` skill is bundled inside the folder at `no-ai-slop/`, so the full slop pass works on a fresh install. If a project already has its own tuned `no-ai-slop`, the skill prefers that copy.

## Quick start

1. Put 3 to 10 pieces you wrote yourself (no AI) into `voice/<your-handle>/samples/`, one file each.
2. Say: `/write-like-me learn my style from voice/<handle>/samples`
3. Correct the summary it shows you. Up to three corrections.
4. Say: `/write-like-me write a LinkedIn post about <topic>`
5. Edit whatever is wrong and paste it back, or say "that's not me, the second paragraph". The profile updates and logs why.

Repeat step 5 for a few pieces. The library converges fast because each correction moves one dial.

## What is in the box

| Path | Purpose |
|---|---|
| `SKILL.md` | The modes: learn, write, edit, check, evolve, add, status |
| `eval.md` | 30 checks run after every draft |
| `references/voice-dials.md` | The twelve dials that make up a voice, with how to measure and apply each |
| `references/content-tiers.md` | Commodity, personality, original; timely versus timeless; the three hook types |
| `references/library-templates.md` | Templates for the eight library files |
| `references/learn-interview.md` | The question bank for filling stances and stories |
| `references/evolution-protocol.md` | How a correction becomes a profile change |
| `no-ai-slop/` | The full no-ai-slop editor and its eval, bundled (MIT licensed, see its LICENSE.txt) |
| `references/slop-floor.md` | One-screen summary of the slop rules |
| `scripts/voice_stats.py` | Measures the dials from samples, writes `fingerprint.json` |
| `scripts/voice_check.py` | Compares a draft against the fingerprint and the not-me list |

## Scripts

```
python3 scripts/voice_stats.py voice/<handle>/samples -o voice/<handle>/fingerprint.json
python3 scripts/voice_check.py voice/<handle> draft.md
```

`voice_check.py` exits 1 on a hard fail (banned slop word or a not-me phrase in the draft) so it can gate a pipeline. Dial deviations are advisory and printed as flags.

## Library layout

```
voice/<handle>/
  samples/               your raw writing
  fingerprint.json       measured dials
  profile.md             dial settings in words, with quoted evidence
  stances.md             which commodity ideas you agree and disagree with
  stories.md             your personality details and formative stories
  approved-language.md   sentences and hooks to reuse verbatim
  not-me.md              words and moves you rejected
  changelog.md           every change, dated, with the quote that caused it
```

Nothing in the library is deleted. Entries get marked superseded.
