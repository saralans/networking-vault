---
description: Add new interactions to the History section of an existing Notion meeting page
---

# /update-history

You are updating the History section of a contact page in the user's Notion Networking database.

**Script:** `python3 ~/.claude/tools/notion_sync.py`

## Your task

1. Fetch the current page: `source ~/.zshrc && python3 ~/.claude/tools/notion_sync.py get "<Name>"`
2. Read the existing History section from the output.
3. Write the new History section (existing entries + new entry, chronological order) to `/tmp/history_<name>.md`.
4. Update: `python3 ~/.claude/tools/notion_sync.py update "<Name>" history /tmp/history_<name>.md`
5. If the user confirms they reached out, also run: `python3 ~/.claude/tools/notion_sync.py check "<Name>" "Reached out?"`
6. Update other checkboxes as appropriate (Responded?, Set Up Info Chat?, Info Chat?, etc.).
7. Clean up the temp file.

## History entry format

```
- **[Date] — [Event type]:** Brief description of what happened, what was discussed, what was decided.
```

Event types: Meeting, Email, LinkedIn message, Text, Phone call, Referral, Introduction, Conference/event, Follow-up

## Rules
- Only record events the user provides. Never fabricate chronology.
- Maintain strict chronological order.
- Do NOT modify Learning unless explicitly asked.
- Do NOT generate Messages.
- Update relevant checkboxes when the user confirms an action occurred.
