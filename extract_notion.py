import os
from datetime import datetime, timezone
from notion.client import NotionClient
from collections import deque

# If you handle all kind of them, it must add dfs
# def dfs(block):
#     stack = deque()
    
def parsing(block):
    text = ""
    # Handles H1
    if (block.type == 'header'):
        text += '# ' + block.title + '\n\n'
    # Handles H2
    if (block.type == 'sub_header'):
        text += '## ' + block.title + '\n\n'
    # Handles H3
    if (block.type == 'sub_sub_header'):
        text += '### ' + block.title + '\n\n'
    # Handles Code Blocks
    if (block.type == 'code'):
        text += '```\n' + block.title + '\n```\n'
    # Handles Images
    if (block.type == 'image'):
        text += '![' + block.id + '](' + block.source + ')\n\n'
    # Handles Bullets
    if (block.type == 'bulleted_list'):
        text += '* ' + block.title + '\n'
    # Handles Numbers
    if (block.type == 'numbered_list'):
        text += '1. ' + block.title + '\n'
    # Handles Dividers
    if (block.type == 'divider'):
        text += '---' + '\n'                
    # Handles Basic Text, Links, Single Line Code
    if (block.type == 'text'):
        text += block.title + '\n\n'
        
            
    return text
    
client = NotionClient(token_v2="TOKEN_V2")
blog_home = client.get_block("PAGE_URL")
# Main Loop
for post in blog_home.children:
    # Handle Frontmatter
    text = """---
title: "%s"
date: %s
description: ""
---""" % (post.title, datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds'))
    # Handle Title
    text += '\n\n' + '# ' + post.title + '\n\n'
    for block in post.children:
        text += parsing(block)
        # Handles Column List
        if (block.type == 'column_list'):
            for column in block.children:
                for sub_block in column.children:
                    text += parsing(sub_block)
    title = post.title.replace(' ', '-')
    title = title.replace(',', '')
    title = title.replace(':', '')
    title = title.replace(';', '')
    title = title.lower()

    file_path = os.path.dirname(os.path.abspath(__file__))
    try:
        os.mkdir(file_path + '/' + title)
    except:
        pass
    file = open(file_path + '/' + title + '/index.md', 'w')
    # print('Wrote A New Page')
    # print(text)
    file.write(text)
