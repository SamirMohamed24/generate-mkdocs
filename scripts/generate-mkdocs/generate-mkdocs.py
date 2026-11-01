import json
import yaml
import re
import os

# Define the default JSON structure
DEFAULT_JSON = {
    "site_name": "GitOps @ Samir IT",
    "plugins": ["techdocs-core"],
    "nav": []
}

def to_title_case(text):
    """Convert kebab-case or snake_case to Title Case with capital letters at the start of each word."""
    words = re.split(r'[-_]', text)
    return ' '.join(word.capitalize() for word in words)

# def transform_keys(obj):
#     """Recursively transform dictionary keys to Title Case."""
#     if isinstance(obj, dict):
#         return {to_title_case(k) if k.lower() != "nav" else "nav": transform_keys(v) for k, v in obj.items()}
#     elif isinstance(obj, list):
#         return [transform_keys(item) for item in obj]
#     return obj
#########
#########
def transform_keys(obj):
    """Recursively transform dictionary keys to Title Case, but preserve mkdocs keys."""
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            if k in ("site_name", "plugins", "nav"):
                new_obj[k] = transform_keys(v)
            else:
                new_obj[to_title_case(k)] = transform_keys(v)
        return new_obj
    elif isinstance(obj, list):
        return [transform_keys(item) for item in obj]
    return obj
##########
##########
def get_docs_structure(base_path):
    """Recursively detect directories and markdown files in the specified path."""
    structure = {}
    for root, dirs, files in os.walk(base_path):
        dirs.sort()   # NEW: folders A–Z
        files.sort(key=lambda f: (f != 'index.md',  f))  # NEW: index.md first, then A–Z
        rel_path = os.path.relpath(root, base_path)
        current_level = structure
        
        if rel_path != '.':
            for part in rel_path.split(os.sep):
                current_level = current_level.setdefault(part, {})
        
        for file in files:
            if file.endswith('.md'):
                name = os.path.splitext(file)[0]
                current_level[to_title_case(name)] = os.path.join(rel_path, file).replace('\\', '/')
    
    return structure

def build_nav_structure(structure):
    """Construct the nav structure for mkdocs from the detected directories and files."""
    nav = []
    for section, content in structure.items():
        if isinstance(content, dict):
            section_nav = build_nav_structure(content)
            if section_nav:
                nav.append({to_title_case(section): section_nav})
            elif 'index' in content:
                nav.append({to_title_case(section): content['index']})
        else:
            nav.append({to_title_case(section): content})
    return nav

# Ensure mkdocs.json exists
json_file = 'mkdocs.json'
if not os.path.exists(json_file):
    with open(json_file, 'w') as f:
        json.dump(DEFAULT_JSON, f, indent=4)

# Load the JSON data
with open(json_file, 'r') as f:
    data = json.load(f)

# Transform JSON keys
transformed_data = transform_keys(data)

# Ensure only one occurrence of site_name and plugins
transformed_data["site_name"] = "GitOps @ Samir IT"
transformed_data["plugins"] = ["techdocs-core"]

# Detect directory structure and build nav
base_docs_path = '../../docs'
docs_structure = get_docs_structure(base_docs_path)
transformed_data['nav'] = build_nav_structure(docs_structure)

# Save the transformed data to JSON
json_output_file = 'mkdocs.json'
with open(json_output_file, 'w') as f:
    json.dump(transformed_data, f, indent=4)

# Save the transformed data to YAML
yaml_output_file = 'mkdocs.yml'
with open(yaml_output_file, 'w') as f:
    yaml.dump({
        "site_name": transformed_data["site_name"],
        "plugins": transformed_data["plugins"],
        "nav": transformed_data["nav"]
    }, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

print(f"Transformed data saved to {json_output_file} and {yaml_output_file}")