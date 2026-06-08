# Networking Vault

A Claude Code toolkit that turns every person you meet into a structured learning opportunity — stored permanently in Notion, accessible from your browser, phone, and anywhere Google keeps you.

Built for people who network to learn, not just to collect contacts.

---

## Why I built this

During the 2026 Boston Tech Week, I was networking with dozens of high-value connections a day — founders, engineers, investors, researchers — and the bottleneck wasn't meeting people. It was acting on those meetings fast enough to matter. Follow-ups slipped, context got stale, and the value of each conversation faded before I could do anything with it.

So I automated the notes. Now every meeting goes straight into Notion, structured and searchable, with a tailored learning section written by Claude based on my specific goals. The human part stayed human. The paperwork disappeared.

---

## What it does

Every contact gets a Notion page with:
- **Context** — who they are, where you met, what you discussed
- **Learning** — what you can specifically extract from this person given your background and goals (written by Claude, tailored to you)
- **History** — chronological record of every interaction
- **Open Questions** — what to dig into next time
- **Messages** — drafting workspace for outreach

Claude writes directly to Notion via the API. No copy-paste.

---

## Commands

| Command | What it does |
|---------|-------------|
| `/create-meeting` | New contact page from notes, LinkedIn, or conversation |
| `/extract-learning` | Deepens the Learning section using your profile |
| `/draft-message` | Drafts LinkedIn DMs, emails, or texts grounded in real context |

---

## Setup

### 1. Clone and install

```bash
git clone https://github.com/saralans/networking-vault.git
cd networking-vault
chmod +x setup.sh
./setup.sh
```

### 2. Fill in your profile

```bash
open ~/.claude/networking_profile.md
```

This is what Claude reads to personalize the Learning section for every contact. Add your projects, career goals, and what makes your background unusual.

### 3. Set up Notion

1. Create a free account at [notion.so](https://notion.so)
2. Create a new **database** (not a blank page) named "Networking"
3. Add these properties:

| Property | Type |
|----------|------|
| Name | Title |
| LinkedIn | URL |
| Company | Text |
| Role | Text |
| School/Personal | Multi-select |
| Relevance to AI | Text |
| Last contact | Text |
| Reached out? | Checkbox |
| Responded? | Checkbox |
| Set Up Info Chat? | Checkbox |
| Info Chat? | Checkbox |
| Asked for Referral? | Checkbox |
| Meeting Doc | URL |
| Message | Text |

4. Go to [notion.so/profile/integrations](https://notion.so/profile/integrations) → **New integration** → copy the API key
5. Open your Networking database → `...` → **Connections** → select your integration
6. Copy the database ID from the URL: `notion.so/workspace/<DATABASE_ID>?v=...`

### 4. Add environment variables

```bash
echo 'export NOTION_API_KEY="secret_..."' >> ~/.zshrc
echo 'export NOTION_DATABASE_ID="..."' >> ~/.zshrc
source ~/.zshrc
```

### 5. Test it

Open Claude Code and run `/create-meeting` with any context about someone you've met.

---

## How the Learning section works

Claude reads your `~/.claude/networking_profile.md` and generates a tailored learning section for each contact — in second person, no category headers, focused on what *you specifically* can extract from this person given your projects and goals.

Example format:
```
What you'd learn:
- [Specific insight grounded in your work]
- ...

Your hook — [label]: [Why this is a real conversation, not generic networking]
```

---

## LinkedIn auto-search

If no LinkedIn URL is provided, the script auto-generates a search link:
```
https://www.linkedin.com/search/results/all/?keywords=Name+Company
```
These are flagged **yellow** in Notion (`LinkedIn Source = Search`). Once you find and verify the real profile, paste the `/in/` URL into Notion and it turns **green** (`Direct`). The script never overwrites a real `/in/` URL.

---

## Requirements

- Python 3.8+
- `requests` library (`pip install requests`)
- [Claude Code](https://claude.ai/code) CLI
- Free Notion account

---

## File structure

```
networking-vault/
├── notion_sync.py                  # Notion API bridge script
├── setup.sh                        # One-command install
├── networking_profile_template.md  # Fill in → save as ~/.claude/networking_profile.md
├── commands/
│   ├── create-meeting.md           # /create-meeting command
│   ├── extract-learning.md         # /extract-learning command
│   └── draft-message.md            # /draft-message command
└── README.md
```
