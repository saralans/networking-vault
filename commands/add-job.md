---
description: Add a job listing to the Jobs section of a contact's Notion page
---

# /add-job

You are adding a job listing to a contact's page in Sarala's Notion Networking database.

**Script:** `python3 ~/.claude/tools/notion_sync.py`

## Your task

1. Fetch the current page: `source ~/.zshrc && python3 ~/.claude/tools/notion_sync.py get "<Name>"`
2. Read the existing Jobs section.
3. Append the new job entry to the Jobs section.
4. Write the full updated Jobs section to `/tmp/jobs_<name>.md`.
5. Update: `python3 ~/.claude/tools/notion_sync.py update "<Name>" jobs /tmp/jobs_<name>.md`
6. Clean up the temp file.

## Jobs section format

```
### [Job Title]
- **Company:** [company name]
- **Role:** [full role title]
- **Link:** [URL if provided]
- **Job Code:** [job code/ID if provided]
- **Status:** [Bookmarked / Applied / Referred / Interviewing]
- **Notes:** [any context — why it's relevant, who can refer, deadline]
```

## Rules
- Preserve all existing job entries when writing the temp file.
- Status defaults to "Bookmarked" if Sarala hasn't applied yet.
- Notes field is optional — only include if Sarala provides context.
- If a referral path exists (e.g. this contact offered or agreed to refer), note it.
