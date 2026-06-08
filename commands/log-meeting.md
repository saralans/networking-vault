---
description: Log notes from a completed meeting into the Meeting section of a contact's Notion page
---

# /log-meeting

You are logging notes from a completed meeting into a contact page in Sarala's Notion Networking database.

**Script:** `python3 ~/.claude/tools/notion_sync.py`

## Your task

1. Fetch the current page: `source ~/.zshrc && python3 ~/.claude/tools/notion_sync.py get "<Name>"`
2. Find the meeting entry in the Meeting section (by title or most recent Preparation block).
3. Add Meeting Notes and Next Time Agenda under that entry using the notes Sarala provides.
4. Write the full updated Meeting section to `/tmp/meeting_<name>.md`.
5. Update: `python3 ~/.claude/tools/notion_sync.py update "<Name>" meeting /tmp/meeting_<name>.md`
6. Check the Info Chat? checkbox: `python3 ~/.claude/tools/notion_sync.py check "<Name>" "Info Chat?"`
7. Clean up the temp file.

## Meeting section format

```
### [Meeting Title]
#### Preparation
[existing preparation content — preserve as-is]
#### Meeting Notes
[Sarala's notes from the meeting]
#### Next Time Agenda
[Topics, questions, or ideas for the next conversation]
```

## Rules
- Preserve all existing content in the Meeting section (other meetings, the Preparation block).
- Only record what Sarala provides — do not invent or summarize beyond her notes.
- Next Time Agenda should be concrete: specific questions to ask or topics to follow up on, not generic reminders.
- After logging, suggest 1-2 Learning section updates if the meeting revealed new insights (but don't auto-update — ask Sarala first).
