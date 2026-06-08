---
description: Generate a Preparation section for an upcoming meeting with a contact, based on their Learning, Open Questions, and any Jobs on the page
---

# /prep-meeting

You are preparing Sarala for an upcoming meeting with a contact in her Notion Networking database.

**Script:** `python3 ~/.claude/tools/notion_sync.py`

## Your task

1. Fetch the current page: `source ~/.zshrc && python3 ~/.claude/tools/notion_sync.py get "<Name>"`
2. Read Learning, Open Questions, and Jobs sections.
3. Ask Sarala what the meeting title should be (or default to "Meeting [today's date]").
4. Generate a Preparation section (see format below).
5. Write the full updated Meeting section to `/tmp/meeting_<name>.md`, preserving any existing meeting entries and appending the new one.
6. Update: `python3 ~/.claude/tools/notion_sync.py update "<Name>" meeting /tmp/meeting_<name>.md`
7. Print the Preparation content in the conversation so Sarala can review it.
8. Clean up the temp file.

## Meeting section format

```
### [Meeting Title]
#### Preparation
- [Specific question to ask, drawn from Open Questions]
- [What to show or demo, based on Sarala's projects + this person's domain]
- [Key thing to listen for / learn, drawn from Learning section]
- [Job to mention, if any in Jobs section]
#### Meeting Notes
#### Next Time Agenda
```

## Rules
- Preparation bullets should be actionable and specific — not generic ("be yourself").
- Pull directly from the page's Learning and Open Questions. Don't invent new content.
- If there are Jobs on the page, include a bullet about whether/how to raise them.
- Leave Meeting Notes and Next Time Agenda empty — those get filled in after the meeting.
- Preserve all existing meeting entries in the Meeting section when writing the temp file.
