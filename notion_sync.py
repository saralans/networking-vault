#!/usr/bin/env python3
"""
notion_sync.py — Claude CLI → Notion bridge for Sarala's Networking vault.

Usage:
  python3 notion_sync.py create "Vishal" /path/to/content.md [--linkedin URL] [--company NAME] [--role ROLE] [--where WHERE]
  python3 notion_sync.py update "Vishal" history /path/to/new_section.md
  python3 notion_sync.py update "Vishal" learning /path/to/new_section.md
  python3 notion_sync.py update "Vishal" messages /path/to/new_section.md
  python3 notion_sync.py get "Vishal"
  python3 notion_sync.py check "Vishal" "Reached out?"
"""

import os
import sys
import json
import argparse
import requests
from urllib.parse import quote_plus

API_KEY = os.environ.get("NOTION_API_KEY", "")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID", "")
BASE_URL = "https://api.notion.com/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

SECTION_HEADERS = ["Context", "History", "Learning", "Open Questions", "Messages"]


# ── Notion block builders ─────────────────────────────────────────────────────

def heading2(text):
    return {"object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def heading3(text):
    return {"object": "block", "type": "heading_3",
            "heading_3": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def bullet(text):
    return {"object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def paragraph(text):
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}


# ── Markdown → Notion blocks ──────────────────────────────────────────────────

def md_to_blocks(md_text):
    """Convert our markdown document structure into Notion blocks."""
    blocks = []
    for line in md_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("## "):
            blocks.append(heading2(stripped[3:]))
        elif stripped.startswith("### "):
            blocks.append(heading3(stripped[4:]))
        elif stripped.startswith("# "):
            pass  # title handled as page property
        elif stripped.startswith("- ") or stripped.startswith("* "):
            blocks.append(bullet(stripped[2:]))
        elif stripped == "---":
            blocks.append(divider())
        else:
            blocks.append(paragraph(stripped))
    return blocks


def section_to_blocks(section_name, md_text):
    """Convert a single section's markdown content into blocks, with heading."""
    blocks = [heading2(section_name), divider()]
    for line in md_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("### "):
            blocks.append(heading3(stripped[4:]))
        elif stripped.startswith("- ") or stripped.startswith("* "):
            blocks.append(bullet(stripped[2:]))
        elif stripped == "---":
            continue
        else:
            blocks.append(paragraph(stripped))
    return blocks


# ── Notion API calls ──────────────────────────────────────────────────────────

def find_page(name):
    """Find a page in the database by Name property."""
    resp = requests.post(f"{BASE_URL}/databases/{DATABASE_ID}/query",
                         headers=HEADERS,
                         json={"filter": {"property": "Name",
                                          "title": {"equals": name}}})
    resp.raise_for_status()
    results = resp.json().get("results", [])
    return results[0] if results else None


def get_page_blocks(page_id):
    """Fetch all blocks from a page."""
    resp = requests.get(f"{BASE_URL}/blocks/{page_id}/children?page_size=100",
                        headers=HEADERS)
    resp.raise_for_status()
    return resp.json().get("results", [])


def delete_blocks(block_ids):
    """Delete a list of blocks by ID."""
    for bid in block_ids:
        requests.delete(f"{BASE_URL}/blocks/{bid}", headers=HEADERS)


def append_blocks(page_id, blocks):
    """Append blocks to a page."""
    # Notion API max 100 blocks per request
    for i in range(0, len(blocks), 100):
        chunk = blocks[i:i+100]
        resp = requests.patch(f"{BASE_URL}/blocks/{page_id}/children",
                              headers=HEADERS,
                              json={"children": chunk})
        resp.raise_for_status()


def make_linkedin_search_url(name, company=""):
    """Generate a LinkedIn search URL from name and company."""
    keyword = f"{name} {company}".strip() if company else name
    return f"https://www.linkedin.com/search/results/all/?keywords={quote_plus(keyword)}&origin=GLOBAL_SEARCH_HEADER"


def is_real_linkedin_url(url):
    """Return True if url is a real LinkedIn profile (/in/ format), not a search URL."""
    return bool(url and "linkedin.com/in/" in url)


def get_existing_linkedin(page_id):
    """Fetch the current LinkedIn URL from an existing page, if any."""
    resp = requests.get(f"{BASE_URL}/pages/{page_id}", headers=HEADERS)
    if not resp.ok:
        return None
    props = resp.json().get("properties", {})
    li = props.get("LinkedIn", {})
    return li.get("url") or None


def create_page(name, blocks, linkedin="", company="", role="", where_met="", relevance="", last_contact=""):
    """Create a new page in the Networking database."""
    properties = {
        "Name": {"title": [{"text": {"content": name}}]},
    }

    # Use provided URL if it's a real profile link; otherwise generate a search URL
    if is_real_linkedin_url(linkedin):
        properties["LinkedIn"] = {"url": linkedin}
        properties["LinkedIn Source"] = {"select": {"name": "Direct"}}
    else:
        properties["LinkedIn"] = {"url": make_linkedin_search_url(name, company)}
        properties["LinkedIn Source"] = {"select": {"name": "Search"}}

    if company:
        properties["Company"] = {"rich_text": [{"text": {"content": company}}]}
    if role:
        properties["Role"] = {"rich_text": [{"text": {"content": role}}]}
    if where_met:
        properties["School/Personal"] = {"multi_select": [{"name": where_met}]}
    if relevance:
        properties["Relevance to AI"] = {"rich_text": [{"text": {"content": relevance}}]}
    if last_contact:
        properties["Last contact"] = {"rich_text": [{"text": {"content": last_contact}}]}

    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": properties,
        "children": blocks[:100],  # first 100 blocks inline
    }
    resp = requests.post(f"{BASE_URL}/pages", headers=HEADERS, json=payload)
    resp.raise_for_status()
    page = resp.json()
    page_id = page["id"]

    # append remaining blocks if doc is long
    if len(blocks) > 100:
        append_blocks(page_id, blocks[100:])

    url = page.get("url", f"https://www.notion.so/{page_id.replace('-', '')}")
    return page_id, url


def update_section(page_id, section_name, new_md):
    """Replace a named section in a page with new content."""
    all_blocks = get_page_blocks(page_id)

    # Find the heading block for this section and collect its blocks
    section_start = None
    section_end = len(all_blocks)
    in_section = False

    for i, block in enumerate(all_blocks):
        btype = block.get("type")
        if btype == "heading_2":
            texts = block["heading_2"]["rich_text"]
            heading_text = "".join(t["text"]["content"] for t in texts)
            if heading_text == section_name:
                section_start = i
                in_section = True
            elif in_section:
                section_end = i
                break

    if section_start is None:
        # Section doesn't exist — just append it
        new_blocks = section_to_blocks(section_name, new_md)
        append_blocks(page_id, new_blocks)
        return

    # Delete old section blocks
    ids_to_delete = [b["id"] for b in all_blocks[section_start:section_end]]
    delete_blocks(ids_to_delete)

    # Append new section blocks
    new_blocks = section_to_blocks(section_name, new_md)
    append_blocks(page_id, new_blocks)


def get_page_as_text(page_id):
    """Fetch page content as plain text (for Claude to read)."""
    blocks = get_page_blocks(page_id)
    lines = []
    for block in blocks:
        btype = block.get("type")
        if btype in ("heading_1", "heading_2", "heading_3"):
            texts = block[btype]["rich_text"]
            content = "".join(t["text"]["content"] for t in texts)
            prefix = {"heading_1": "# ", "heading_2": "## ", "heading_3": "### "}[btype]
            lines.append(f"{prefix}{content}")
        elif btype == "bulleted_list_item":
            texts = block["bulleted_list_item"]["rich_text"]
            content = "".join(t["text"]["content"] for t in texts)
            lines.append(f"- {content}")
        elif btype == "paragraph":
            texts = block["paragraph"]["rich_text"]
            content = "".join(t["text"]["content"] for t in texts)
            if content:
                lines.append(content)
        elif btype == "divider":
            lines.append("---")
    return "\n".join(lines)


def set_linkedin(page_id, name, company=""):
    """Set LinkedIn URL only if no real /in/ URL already exists."""
    existing = get_existing_linkedin(page_id)
    if is_real_linkedin_url(existing):
        print(f"LinkedIn already set to a real profile URL — skipping.")
        return
    search_url = make_linkedin_search_url(name, company)
    resp = requests.patch(f"{BASE_URL}/pages/{page_id}", headers=HEADERS,
                          json={"properties": {
                              "LinkedIn": {"url": search_url},
                              "LinkedIn Source": {"select": {"name": "Search"}},
                          }})
    resp.raise_for_status()


def check_property(page_id, property_name):
    """Set a checkbox property to True."""
    resp = requests.patch(f"{BASE_URL}/pages/{page_id}",
                          headers=HEADERS,
                          json={"properties": {property_name: {"checkbox": True}}})
    resp.raise_for_status()


# ── CLI ───────────────────────────────────────────────────────────────────────

def cmd_create(args):
    if not args.file:
        print("Error: provide a markdown file path", file=sys.stderr)
        sys.exit(1)
    with open(args.file) as f:
        md = f.read()
    blocks = md_to_blocks(md)
    page_id, url = create_page(
        args.name, blocks,
        linkedin=args.linkedin or "",
        company=args.company or "",
        role=args.role or "",
        where_met=args.where or "",
        relevance=args.relevance or "",
        last_contact=args.last_contact or "",
    )
    print(f"Created: {url}")
    print(f"Page ID: {page_id}")


def cmd_update(args):
    page = find_page(args.name)
    if not page:
        print(f"Error: no page found for '{args.name}'", file=sys.stderr)
        sys.exit(1)
    with open(args.file) as f:
        new_md = f.read()
    section_map = {
        "context": "Context",
        "history": "History",
        "learning": "Learning",
        "questions": "Open Questions",
        "messages": "Messages",
    }
    section_name = section_map.get(args.section.lower(), args.section)
    update_section(page["id"], section_name, new_md)
    print(f"Updated '{section_name}' in page '{args.name}'")


def cmd_get(args):
    page = find_page(args.name)
    if not page:
        print(f"Error: no page found for '{args.name}'", file=sys.stderr)
        sys.exit(1)
    text = get_page_as_text(page["id"])
    print(text)


def cmd_check(args):
    page = find_page(args.name)
    if not page:
        print(f"Error: no page found for '{args.name}'", file=sys.stderr)
        sys.exit(1)
    check_property(page["id"], args.property)
    print(f"Checked '{args.property}' for '{args.name}'")


def main():
    if not API_KEY or not DATABASE_ID:
        print("Error: NOTION_API_KEY and NOTION_DATABASE_ID must be set", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Notion sync for networking vault")
    sub = parser.add_subparsers(dest="command")

    p_create = sub.add_parser("create")
    p_create.add_argument("name")
    p_create.add_argument("file")
    p_create.add_argument("--linkedin", default="")
    p_create.add_argument("--company", default="")
    p_create.add_argument("--role", default="")
    p_create.add_argument("--where", default="")
    p_create.add_argument("--relevance", default="")
    p_create.add_argument("--last-contact", default="")

    p_update = sub.add_parser("update")
    p_update.add_argument("name")
    p_update.add_argument("section")
    p_update.add_argument("file")

    p_get = sub.add_parser("get")
    p_get.add_argument("name")

    p_check = sub.add_parser("check")
    p_check.add_argument("name")
    p_check.add_argument("property")

    args = parser.parse_args()
    if args.command == "create":
        cmd_create(args)
    elif args.command == "update":
        cmd_update(args)
    elif args.command == "get":
        cmd_get(args)
    elif args.command == "check":
        cmd_check(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
