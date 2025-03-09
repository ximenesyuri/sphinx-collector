import os
import re
import yaml

def setup(app):
    app.add_config_value('markdown_files', {}, 'env')
    app.connect('builder-inited', lambda app: None)

    global collect
    collect = _collect

def _collect(directory, pattern='*.md'):
    markdown_files = {}
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', directory))

    for root, _, files in os.walk(base_path):
        for file_name in files:
            if re.match(pattern.replace('.', r'\.').replace('*', r'.*'), file_name):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    frontmatter, content = extract_frontmatter(content)

                    markdown_files[file_name] = {
                        'path': file_path,
                        'frontmatter': frontmatter,
                        'content': content
                    }

    return markdown_files

def extract_frontmatter(content):
    frontmatter = {}
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            frontmatter = yaml.safe_load(content[3:end].strip())
            content = content[end + 3:].strip()
    return frontmatter, content
