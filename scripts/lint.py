#!/usr/bin/env python3
import os
import re
import sys
import yaml

WIKI_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(WIKI_DIR, "SCHEMA.md")
INDEX_PATH = os.path.join(WIKI_DIR, "index.md")

# Simple frontmatter parser
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[(.*?)\]\]")

def load_schema_tags():
    if not os.path.exists(SCHEMA_PATH):
        return set()
    with open(SCHEMA_PATH, "r") as f:
        content = f.read()
    # Extract tags under '## Tag Taxonomy'
    tags = set()
    in_taxonomy = False
    for line in content.splitlines():
        if "## Tag Taxonomy" in line:
            in_taxonomy = True
            continue
        if in_taxonomy and line.startswith("## "):
            break
        if in_taxonomy and "-" in line:
            # Extract tags within code ticks, e.g. `model`, `architecture`
            for tag in re.findall(r"`([^`]+)`", line):
                tags.add(tag)
    return tags

def lint():
    allowed_tags = load_schema_tags()
    all_pages = {}
    wikilinks = {}
    errors = []
    warnings = []

    # Directories to scan
    wiki_dirs = ["entities", "concepts", "comparisons", "queries"]
    for d in wiki_dirs:
        full_dir = os.path.join(WIKI_DIR, d)
        if not os.path.exists(full_dir):
            continue
        for root, _, files in os.walk(full_dir):
            for file in files:
                if not file.endswith(".md"):
                    continue
                path = os.path.join(root, file)
                slug = os.path.splitext(file)[0]
                all_pages[slug] = path

                with open(path, "r") as f:
                    content = f.read()

                # Extract Links
                links = WIKILINK_RE.findall(content)
                # Parse aliases like [[slug|alias]]
                cleaned_links = [l.split("|")[0].strip() for l in links]
                wikilinks[slug] = cleaned_links

                # Parse Frontmatter
                match = FRONTMATTER_RE.match(content)
                if not match:
                    errors.append(f"[{d}/{file}] Missing or malformed YAML frontmatter.")
                    continue
                try:
                    meta = yaml.safe_load(match.group(1))
                except Exception as e:
                    errors.append(f"[{d}/{file}] Failed to parse YAML frontmatter: {e}")
                    continue

                # Validate Frontmatter keys
                required = ["title", "created", "updated", "type", "tags", "sources"]
                for req in required:
                    if req not in meta:
                        errors.append(f"[{d}/{file}] Missing required frontmatter field: '{req}'")

                # Validate Type
                expected_type = d[:-1]
                if d == "entities":
                    expected_type = "entity"
                if meta.get("type") != expected_type:
                    warnings.append(f"[{d}/{file}] type '{meta.get('type')}' does not match folder '{d}'")

                # Validate Tags against taxonomy
                tags = meta.get("tags", [])
                if not isinstance(tags, list):
                    errors.append(f"[{d}/{file}] 'tags' must be a list.")
                elif allowed_tags:
                    for tag in tags:
                        if tag not in allowed_tags:
                            warnings.append(f"[{d}/{file}] Tag '{tag}' is not defined in SCHEMA.md taxonomy.")

    # 2. Check Broken Links & Outbound Links
    for slug, links in wikilinks.items():
        if len(links) < 2:
            warnings.append(f"[{slug}] has {len(links)} outbound link(s) ( SCHEMA.md recommends >= 2 ).")
        for link in links:
            if link not in all_pages and link != "index":
                errors.append(f"[{slug}] contains broken link [[{link}]]")

    # 3. Check Orphans (pages with 0 inbound links, excluding index)
    inbound_counts = {slug: 0 for slug in all_pages}
    # Read index to find starting links
    index_links = []
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "r") as f:
            index_content = f.read()
        index_links = [l.split("|")[0].strip() for l in WIKILINK_RE.findall(index_content)]
        for link in index_links:
            if link in inbound_counts:
                inbound_counts[link] += 1

    for slug, links in wikilinks.items():
        for link in links:
            if link in inbound_counts:
                inbound_counts[link] += 1

    for slug, count in inbound_counts.items():
        if count == 0:
            warnings.append(f"[{slug}] is an orphan page (0 inbound links).")

    # 4. Check Index Completeness
    for slug in all_pages:
        if slug not in index_links:
            warnings.append(f"[{slug}] is not listed in index.md.")

    # Output Results
    print("=== LLM Wiki Lint Report ===")
    print(f"Total Pages Scanned: {len(all_pages)}\n")

    if errors:
        print(f"❌ ERRORS ({len(errors)}):")
        for err in errors:
            print(f"  - {err}")
    else:
        print("✅ No critical errors found.")

    if warnings:
        print(f"\n⚠️ WARNINGS ({len(warnings)}):")
        for warn in warnings:
            print(f"  - {warn}")
    else:
        print("\n✅ No warnings found.")

    if errors:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    lint()
