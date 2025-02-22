import json
import os
from datetime import datetime
import xml.etree.ElementTree as ET

MESSAGE_FILE = "messages.json"
RSS_FILE = "feed.xml"

def generate_rss():
    # Load messages
    if not os.path.exists(MESSAGE_FILE):
        messages = []
    else:
        with open(MESSAGE_FILE, "r") as f:
            messages = json.load(f)

    # Create RSS structure
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    
    ET.SubElement(channel, "title").text = "Discord Channel Feed"
    ET.SubElement(channel, "link").text = "https://discord.com"
    ET.SubElement(channel, "description").text = "RSS feed of Discord channel messages"
    ET.SubElement(channel, "lastBuildDate").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

    # Add items
    for msg in messages[-100:]:  # Limit to last 100 messages
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = f"Message from {msg['author']}"
        ET.SubElement(item, "link").text = msg["link"]
        ET.SubElement(item, "description").text = msg["content"]
        ET.SubElement(item, "pubDate").text = datetime.strptime(msg["timestamp"], "%Y-%m-%dT%H:%M:%S.%f+00:00").strftime("%a, %d %b %Y %H:%M:%S +0000")
        ET.SubElement(item, "guid").text = msg["id"]

    # Save RSS feed
    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ", level=0)
    tree.write(RSS_FILE, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    generate_rss()
