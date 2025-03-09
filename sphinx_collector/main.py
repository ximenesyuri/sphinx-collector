import os
import yaml
import re

def collect(directory, pattern='*.md'):
    def extract_frontmatter(content):
        frontmatter = {}
        if content.startswith('---'):
            end = content.find('---', 3)
            if end != -1:
                frontmatter = yaml.safe_load(content[3:end].strip())
                content = content[end + 3:].strip()
        return frontmatter, content

    markdown_files = {}
    base_path = os.path.abspath(directory)
    conf_py_dir = os.getcwd()

    for root, _, files in os.walk(base_path):
        for file_name in files:
            if re.match(pattern.replace('.', r'\.').replace('*', r'.*'), file_name):
                full_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(full_path, conf_py_dir)
                url = os.path.splitext(relative_path)[0]
                with open(full_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    frontmatter, content = extract_frontmatter(content)

                    markdown_files[file_name] = {
                        'path': {
                            'full': full_path,
                            'relative': relative_path,
                            'url': url,
                        },
                        'frontmatter': frontmatter,
                        'content': content
                    }

    return markdown_files
