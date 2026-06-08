---
description: Write or log any message for a contact — initial outreach, follow-ups, received replies, or quick responses. Updates the Messages section of their Notion page.
---

# /draft-message

You are drafting an outreach message using a contact page in the user's Notion Networking database.

**Script:** `python3 ~/.claude/tools/notion_sync.py`
**User profile:** Read `~/.claude/networking_profile.md` for the user's background and voice.

## Your task

1. Read `~/.claude/networking_profile.md`.
2. Fetch the current page: `source ~/.zshrc && python3 ~/.claude/tools/notion_sync.py get "<Name>"`
3. Read Context, Meeting notes, and existing Messages to ground the message in real shared moments.
4. Draft or log the message the user requests.
5. Write the Messages section content to `/tmp/messages_<name>.md`:
   ```
   ### [Message type]
   [Draft here]
   ---
   ```
6. Update: `python3 ~/.claude/tools/notion_sync.py update "<Name>" messages /tmp/messages_<name>.md`
7. Print the drafted message directly in the conversation so the user can copy it without opening Notion.
8. Clean up the temp file.

## Rules
- Use for ANY message: initial outreach, follow-ups, logging a received reply, drafting a quick response.
- Only write what is explicitly requested — do NOT generate follow-up sequences or hypothetical future messages.
- Do NOT invent prior interactions not present in the page.
- Match the tone specified (casual text, professional email, LinkedIn DM).
- Reference real shared moments, real topics, real advice — never invented context.
- When logging a received reply, use `### [Name]'s reply` with verbatim text, then draft the response as `### Response`.
- Do NOT auto-check any Notion checkboxes — the user checks "Reached out?" and similar manually.
- Message headers use `### [Label]` with no date appended.
- If asked for multiple variants, label them clearly (Option A, Option B).
