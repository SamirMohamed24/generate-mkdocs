# MkDocs Auto-Generator

This repository includes a script to automatically generate `mkdocs.yml` and `mkdocs.json` navigation configuration files based on the directory structure inside the `docs/` folder.

## 📘 Purpose

The `generate-mkdocs.py` script scans the Markdown files in the `docs/` directory and generates a consistent navigation structure for use with [MkDocs](https://www.mkdocs.org/) and [TechDocs](https://backstage.io/docs/features/techdocs/overview/).

This is useful for:

- Automatically keeping documentation navigation up-to-date
- Generating TechDocs-compatible output for platforms like Backstage
- Avoiding manual edits to navigation when adding/removing documentation

## 🛠️ How It Works

- Converts folder and `.md` file names into readable titles (Title Case)
- Builds a `nav:` structure reflecting the folder hierarchy
- Outputs:
  - `mkdocs.yml` — standard MkDocs config
  - `mkdocs.json` — structured JSON version (optional, useful for debugging or pipelines)

## 🚀 Usage

From the root of the project, run:

```bash
cd scripts/generate-mkdocs
python generate-mkdocs.py


# MkDocs Auto-Generator

This script generates `mkdocs.yml` and `mkdocs.json` based on the folder structure in the `docs/` directory. It helps automate navigation configuration for MkDocs and TechDocs.

---

## ⚙️ Output Files

- **`mkdocs.yml`**: YAML configuration for MkDocs
- **`mkdocs.json`**: Intermediate JSON used for transformation/debugging

---

## 📁 Example `docs/` Structure 

docs/
├── index.md
├── overview.md
├── deployment/
│   ├── index.md
│   ├── dev.md
│   └── prod.md
├── getting-started/
│   ├── index.md
│   ├── prerequisites.md
│   └── installation.md
└── reference/
    ├── index.md
    ├── api.md
    └── faq.md


🤖 ## Automation

This script is also used in a GitHub Actions workflow:

Automatically runs on changes to the docs/ folder

Commits updated mkdocs.yml if there are changes


## 👤 Author

**Samir Mohamed**  
DevOps Engineer
