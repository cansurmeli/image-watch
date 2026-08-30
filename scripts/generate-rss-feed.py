#!/usr/bin/env python3

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree

repo = os.environ["GITHUB_REPOSITORY"]
repo_url = f"http://github.com/{repo}"

with open("prs.json", encoding="utf-8") as file_prs:
    prs = json.load(file_prs)

rss = Element("rss", version="2.0")
channel = SubElement(rss, "channel")

SubElement(channel, "title").text = f"{repo} image updates"
SubElement(channel, "link").text = repo_url
SubElement(channel, "description").text = "Contianer image updates detected by Dependabot"
SubElement(channel, "lastBuildDate").text = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z")

for pr in prs:
    item = SubElement(channel, "item")

    SubElement(item, "title").text = pr["title"]
    SubElement(item, "link").text = pr["url"]
    SubElement(item, "guid", isPermalink="true").text = pr["url"]

    created = datetime.fromisoformat(pr["createdAt"].replace("Z", "+00:00"))
    SubElement(item, "pubDate").text = created.strftime("%a, %d %b %Y %H:%M:%S %z")

Path("public").mkdir(exist_ok=True)

ElementTree(rss).write(
    "public/feed.xml",
    encoding="utf-8",
    xml_declaration=True,
)
