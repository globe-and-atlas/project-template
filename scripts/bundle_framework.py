#!/usr/bin/env python3
"""Bundle the complete AI Programming Framework into a portable zip file."""

import shutil
import zipfile
import os
from pathlib import Path

# Paths relative to this script
GIT_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_DIR = GIT_ROOT / "project-template"
AGENT_DIR = GIT_ROOT / ".agent"
GLOBAL_AGENTS_DIR = Path.home() / ".agents"

# Global instruction files at root
ROOT_MD_FILES = [
    "AGENTS.md",
    "GEMINI.md",
    "CLAUDE.md",
    "WORKSHOP_PHILOSOPHY.md"
]

# Output file
BUNDLE_NAME = "ai_framework_bundle.zip"
TEMP_DIR = GIT_ROOT / ".tmp" / "framework_bundle"

def log(icon, msg):
    print(f"{icon} {msg}")

def bundle():
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir(parents=True)

    log("📂", "Starting framework bundle...")

    # 1. Copy Root Instructions
    log("📄", "Collecting global instructions...")
    for f in ROOT_MD_FILES:
        src = GIT_ROOT / f
        if src.exists():
            shutil.copy2(src, TEMP_DIR / f)
        else:
            log("⚠️", f"Missing instruction file: {f}")

    # 2. Copy Scaffolding (project-template)
    log("🏗️", "Collecting scaffolding (project-template)...")
    if TEMPLATE_DIR.exists():
        # Avoid copying the .git folder and .tmp folder inside project-template
        shutil.copytree(TEMPLATE_DIR, TEMP_DIR / "project-template", 
                        ignore=shutil.ignore_patterns(".git", ".tmp", "__pycache__", ".venv", "node_modules"))
    else:
        log("❌", "project-template directory not found!")
        return

    # 3. Copy Local System (.agent)
    log("🧠", "Collecting local system (.agent)...")
    if AGENT_DIR.exists():
        shutil.copytree(AGENT_DIR, TEMP_DIR / ".agent",
                        ignore=shutil.ignore_patterns(".git", ".tmp", "__pycache__", ".venv", "node_modules"))
    else:
        log("⚠️", ".agent directory not found!")

    # 4. Copy Global System (~/.agents)
    log("📚", "Collecting global skills (~/.agents)...")
    if GLOBAL_AGENTS_DIR.exists():
        shutil.copytree(GLOBAL_AGENTS_DIR, TEMP_DIR / ".agents",
                        ignore=shutil.ignore_patterns(".git", ".tmp", "__pycache__", ".venv", "node_modules"))
    else:
        log("⚠️", "~/.agents directory not found!")

    # 5. Create SETUP.md
    log("✍️", "Creating SETUP.md...")
    setup_content = f"""# AI Programming Framework Setup

This bundle contains a complete replica of your agentic programming environment.

## Installation Steps

1.  **Extract to Git Root**:
    Unzip this file into your primary coding directory (e.g., `~/Git`).
    The structure should look like this:
    ```
    ~/Git/
    ├── AGENTS.md
    ├── CLAUDE.md
    ├── GEMINI.md
    ├── WORKSHOP_PHILOSOPHY.md
    ├── project-template/
    └── .agent/
    ```

2.  **Move Global Skills**:
    Move the `.agents` folder from the extracted directory to your home directory:
    ```bash
    mv ~/Git/.agents ~/.agents
    ```

3.  **Verify create_project script**:
    The scaffolding script is located at:
    `python3 ~/Git/project-template/scripts/create_project.py`

4.  **Install Global Dependencies**:
    Ensure your new machine has:
    - Python 3.10+
    - Node.js & npm
    - Git
    - gh CLI (optional, for GitHub integration)

## Quick Test
Run this to see if the framework is active:
```bash
python3 ~/Git/project-template/scripts/create_project.py --list-profiles
```

---
Generated on: {Path.home().name} at {GIT_ROOT}
"""
    (TEMP_DIR / "SETUP.md").write_text(setup_content)

    # 6. Create Zip
    output_path = GIT_ROOT / BUNDLE_NAME
    log("🤐", f"Creating {BUNDLE_NAME}...")
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(TEMP_DIR):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(TEMP_DIR)
                zipf.write(file_path, arcname)

    # Cleanup
    shutil.rmtree(TEMP_DIR)
    
    log("✅", f"Bundle created at: {output_path}")
    log("📦", f"Size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    bundle()
