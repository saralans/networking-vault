---
description: Create a new Meeting page in your Notion Networking database from notes, LinkedIn info, or conversation context
---

# /create-meeting

You are creating a new contact page in the user's Notion Networking database.

**Script:** `python3 ~/.claude/tools/notion_sync.py`
**User profile:** Read `~/.claude/networking_profile.md` for the user's background, projects, and career goals. Use this to personalize the Learning section.
**Env vars required:** NOTION_API_KEY, NOTION_DATABASE_ID (set in ~/.zshrc)

## Your task

1. Read `~/.claude/networking_profile.md` to understand the user's background and goals.
2. Read all context the user provides (notes, LinkedIn info, conversation details, background).
3. Generate the meeting document content as markdown (structure below).
4. Write it to `/tmp/meeting_<name>.md`.
5. Run: `source ~/.zshrc && python3 ~/.claude/tools/notion_sync.py create "<Name>" /tmp/meeting_<name>.md [--linkedin URL] [--company NAME] [--role ROLE] [--where WHERE] [--relevance TEXT]`
6. Report the Notion URL returned.
7. Clean up: `rm /tmp/meeting_<name>.md`

## Document structure

```
# Meeting [Name]

## Context
- **Who:** [name, role, company]
- **Role / Company:**
- **Where we met:**
- **Background:** [only facts the user provided]
- **Topics discussed:**
- **Advice given:** (if any)

## Learning

What you'd learn:

- [Short narrative bullet — specific knowledge this person's background unlocks for the user]
- [Another — practical, non-obvious, specific to this person]
- ...

Your hook — [label]: [One paragraph connecting the user's actual projects/background to this
person's domain. Why this is a real conversation, not generic networking.]

## Open Questions
- [Questions focused on learning, not relationship management]

## Meeting

## Messages

## Jobs
```

## How to write the Learning section

Write in second person ("You'd learn...", "Your hook..."), addressed directly to the user.
Do NOT use category headers (no "Technical / Career / Mental Models").
Use short narrative bullets — each a complete thought.

Ground every insight in what is specifically valuable for THIS user given their profile in
`~/.claude/networking_profile.md` — their projects, career goals, and what makes their
background unusual. Ask: given who this person is and what they've done, what can the user
specifically extract that advances their projects or career?

The "Your hook" paragraph: connect the user's actual work or background to this specific
person's domain — explain why the conversation is technically grounded, not generic.

## Rules
- Never invent facts, meetings, emails, or relationship history.
- Do NOT populate Meeting, Messages, or Jobs sections on creation — leave them empty.
- One precise insight beats three vague bullets.
- If a date is provided, use it. If not, leave date fields as "(date unknown)".
- `--where` must be a single word or short phrase (it's a multi_select tag in Notion).
