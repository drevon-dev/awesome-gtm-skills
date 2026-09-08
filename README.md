# Drevon Skills

Official skills published by [Drevon](https://drevon.dev). Each one is a folder under
`skills/` containing a `SKILL.md`.

Browse them at **[drevon.dev/skills](https://drevon.dev/skills)**.

## Install

One command, and the skill lands in every agent your project has configured — Claude Code,
Codex, Gemini, Copilot:

```bash
npx drevon skill add drevon-dev/skills/account-health
```

Drevon writes the skill into `.claude/skills/`, `.agents/skills/` and `.drevon/skills/`, so
whichever agent you open next already has it.

Without Drevon, install into a single agent directly:

```bash
npx skills add drevon-dev/skills --skill account-health
```

Or install from inside the Drevon app: **Settings → Skills**, search, click Install.

## Layout

```
skills/
  <skill-name>/
    SKILL.md
```

`<skill-name>` is the install identifier. It is lowercase, hyphenated, and stable — renaming a
folder breaks every existing install and the skill's page on drevon.dev.

## Writing a skill

`SKILL.md` opens with YAML frontmatter:

```yaml
---
name: account-health
description: One or two sentences saying what the skill does and when to reach for it.
---
```

`description` is what an agent reads to decide whether the skill applies, so write it as a
trigger, not a summary: say when to use this, in the words someone would actually use.

The body is the instructions the agent follows. What holds up in practice:

- Say what to do, in order. Steps beat prose.
- Show the output format literally.
- State the rules that keep the output honest — what not to claim, what to refuse, what to
  ask for instead of guessing.
- Name what the skill cannot see. A skill that admits its blind spots gets trusted with the
  ones it does cover.

## Contributing

Open a PR adding a folder under `skills/`. Keep one skill per PR.

## Licence

MIT.
