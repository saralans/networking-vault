#!/bin/bash
# setup.sh — installs networking-vault into your Claude Code environment

set -e

echo "Setting up Networking Vault..."

# 1. Create directories
mkdir -p ~/.claude/tools
mkdir -p ~/.claude/commands

# 2. Copy the sync script
cp notion_sync.py ~/.claude/tools/notion_sync.py
chmod +x ~/.claude/tools/notion_sync.py
echo "✓ Installed notion_sync.py → ~/.claude/tools/"

# 3. Copy Claude commands
cp commands/create-meeting.md ~/.claude/commands/create-meeting.md
cp commands/extract-learning.md ~/.claude/commands/extract-learning.md
cp commands/update-history.md ~/.claude/commands/update-history.md
cp commands/draft-message.md ~/.claude/commands/draft-message.md
echo "✓ Installed commands → ~/.claude/commands/"

# 4. Copy profile template (don't overwrite if already exists)
if [ ! -f ~/.claude/networking_profile.md ]; then
  cp networking_profile_template.md ~/.claude/networking_profile.md
  echo "✓ Created ~/.claude/networking_profile.md — fill this in with your background"
else
  echo "↷ ~/.claude/networking_profile.md already exists — skipping"
fi

echo ""
echo "Next steps:"
echo ""
echo "1. Fill in your profile:"
echo "   open ~/.claude/networking_profile.md"
echo ""
echo "2. Create a free Notion account at notion.so"
echo ""
echo "3. Create a Networking database in Notion with these properties:"
echo "   Name (Title), LinkedIn (URL), Company (Text), Role (Text),"
echo "   School/Personal (Multi-select), Relevance to AI (Text),"
echo "   Last contact (Text), Reached out? (Checkbox), Responded? (Checkbox),"
echo "   Set Up Info Chat? (Checkbox), Info Chat? (Checkbox),"
echo "   Asked for Referral? (Checkbox), Meeting Doc (URL), Message (Text)"
echo ""
echo "4. Create a Notion integration at notion.so/profile/integrations"
echo "   → copy the API key"
echo ""
echo "5. Share your Networking database with the integration"
echo "   (open database → ... → Connections → select your integration)"
echo ""
echo "6. Copy your database ID from the URL:"
echo "   notion.so/workspace/<DATABASE_ID>?v=..."
echo ""
echo "7. Add to ~/.zshrc:"
echo '   export NOTION_API_KEY="secret_..."'
echo '   export NOTION_DATABASE_ID="..."'
echo "   source ~/.zshrc"
echo ""
echo "8. Test: claude (open Claude Code) → /create-meeting"
echo ""
echo "Done!"
