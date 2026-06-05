---
description: Draft a message (LinkedIn, email, text) using an existing Notion meeting page. Updates only the Messages section.
---

# /draft-message

You are drafting an outreach message using a contact page in the user's Notion Networking database.

**Script:** `python3 ~/.claude/tools/notion_sync.py`
**User profile:** Read `~/.claude/networking_profile.md` for the user's background and voice.

## Your task

1. Read `~/.claude/networking_profile.md`.
2. Fetch the current page: `source ~/.zshrc && python3 ~/.claude/tools/notion_sync.py get "<Name>"`
3. Read Context and History to ground the message in real shared moments.
4. Draft the message the user requests.
5. Write the Messages section content to `/tmp/messages_<name>.md`:
   ```
   ### [Message type] — [Date]
   [Draft here]
   ---
   ```
6. Update: `python3 ~/.claude/tools/notion_sync.py update "<Name>" messages /tmp/messages_<name>.md`
7. Print the drafted message directly in the conversation so the user can copy it without opening Notion.
8. Clean up the temp file.

## Rules
- Only draft what the user explicitly requests.
- Do NOT assume the recipient has replied.
- Do NOT generate follow-up sequences or hypothetical future messages.
- Do NOT invent prior interactions not in the History section.
- Match the tone the user specifies (casual text, professional email, LinkedIn DM).
- Reference real shared moments, real topics, real advice — never invented context.
- If the user asks for multiple variants, label them clearly (Option A, Option B).
