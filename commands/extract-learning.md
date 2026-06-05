---
description: Deepen the Learning section of an existing Notion meeting page without modifying History or Messages
---

# /extract-learning

You are updating the Learning section of a contact page in the user's Notion Networking database.

**Script:** `python3 ~/.claude/tools/notion_sync.py`
**User profile:** Read `~/.claude/networking_profile.md` for the user's background, projects, and career goals.

## Your task

1. Read `~/.claude/networking_profile.md`.
2. Fetch the current page: `source ~/.zshrc && python3 ~/.claude/tools/notion_sync.py get "<Name>"`
3. Read the full page content — Context, History, Learning sections.
4. Write an improved Learning section to `/tmp/learning_<name>.md`.
5. Update: `python3 ~/.claude/tools/notion_sync.py update "<Name>" learning /tmp/learning_<name>.md`
6. Clean up the temp file.

## What good Learning looks like

Write in second person ("You'd learn...", "Your hook..."). No category headers.
Short narrative bullets. Deduplicate — don't repeat insights already listed.

Format:
```
What you'd learn:
- [Specific insight this person's background unlocks for the user]
- ...

Your hook — [label]: [Why this is a real conversation given the user's actual work/background]
```

Ground every insight in what is specifically valuable for THIS user given their profile —
their projects, goals, and what makes their background unusual. Ask: given who this person
is and what they've done, what can the user specifically extract that advances their work
or career — not what anyone could learn, but what THEY could use.

## Rules
- Do NOT modify History.
- Do NOT generate Messages.
- Do NOT invent new facts — derive learning only from context in the document.
- One precise insight beats three vague bullets.
