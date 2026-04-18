#!/usr/bin/env python3
"""Create a new project from project-template-v2.

Combines core/ with a selected profile overlay, replaces placeholders,
and performs full post-scaffold initialization (git, venv, hooks, health check).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

TEMPLATE_ROOT = Path(__file__).resolve().parents[1]
CORE_DIR = TEMPLATE_ROOT / "core"
PROFILES_DIR = TEMPLATE_ROOT / "profiles"

PROFILE_DEFAULTS = {
    "dashboard-static": {"deploy": "iis", "runtime": "static", "loop_mode": "artifact", "knowledge_level": "standard"},
    "frontend-app": {"deploy": "vercel", "runtime": "node", "loop_mode": "artifact", "knowledge_level": "standard"},
    "workflow-python": {"deploy": "local-only", "runtime": "python", "loop_mode": "data", "knowledge_level": "heavy"},
    "hybrid-geospatial": {"deploy": "iis", "runtime": "hybrid", "loop_mode": "hybrid", "knowledge_level": "heavy"},
}

TEXT_EXTENSIONS = {
    ".md", ".txt", ".py", ".json", ".toml", ".yaml", ".yml",
    ".html", ".css", ".js", ".jsx", ".ts", ".tsx", ".env", ".example",
}

PASS = "\033[92m✓\033[0m"
FAIL = "\033[91m✗\033[0m"
WARN = "\033[93m⚠\033[0m"
INFO = "\033[94m·\033[0m"


def slugify(name: str) -> str:
    return name.strip().lower().replace(" ", "-").replace("_", "-")


def replace_placeholders(root: Path, replacements: dict[str, str]) -> None:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS and path.name not in {
            ".gitignore", ".editorconfig", ".env.example", "Makefile",
        }:
            continue
        try:
            text = path.read_text()
        except (UnicodeDecodeError, PermissionError):
            continue
        original = text
        for key, value in replacements.items():
            text = text.replace(key, value)
        if text != original:
            path.write_text(text)


def copy_overlay(src: Path, dest: Path) -> None:
    shutil.copytree(src, dest, dirs_exist_ok=True)


def run_cmd(args: list[str], cwd: Path, label: str) -> bool:
    """Run a command, print result. Returns True on success."""
    try:
        result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"  {PASS}  {label}")
            return True
        else:
            print(f"  {FAIL}  {label}")
            if result.stderr.strip():
                for line in result.stderr.strip().splitlines()[:3]:
                    print(f"       {line}")
            return False
    except FileNotFoundError:
        print(f"  {WARN}  {label} — command not found")
        return False
    except subprocess.TimeoutExpired:
        print(f"  {WARN}  {label} — timed out")
        return False


# ── Post-scaffold initialization ──────────────────────────────────────────────

def init_env(destination: Path, profile: str) -> None:
    """Create .env from .env.example if present."""
    env_example = destination / ".env.example"
    env_file = destination / ".env"
    if env_example.exists() and not env_file.exists():
        shutil.copy2(env_example, env_file)
        print(f"  {PASS}  Created .env from .env.example")
        print(f"       → Fill in your API keys in .env before running the project.")
    elif env_file.exists():
        print(f"  {PASS}  .env already exists")
    else:
        print(f"  {INFO}  No .env.example found for this profile — skipping")


def init_venv(destination: Path, profile: str) -> None:
    """Create Python venv for Python-based profiles."""
    if profile not in ("workflow-python", "hybrid-geospatial"):
        print(f"  {INFO}  Profile '{profile}' does not use a Python venv — skipping")
        return

    venv_path = destination / ".venv"
    if venv_path.exists():
        print(f"  {PASS}  .venv already exists")
        return

    print(f"  {INFO}  Creating Python virtual environment...")
    if not run_cmd(["python3", "-m", "venv", ".venv"], destination, "python3 -m venv .venv"):
        return

    pip = venv_path / "bin" / "pip"
    run_cmd([str(pip), "install", "--quiet", "--upgrade", "pip"], destination, "pip upgrade")

    req = destination / "requirements.txt"
    if req.exists():
        run_cmd([str(pip), "install", "--quiet", "-r", str(req)], destination, "pip install requirements.txt")

    print(f"       → Activate with: source .venv/bin/activate")


def init_node(destination: Path, profile: str) -> None:
    """Run npm install for Node-based profiles."""
    if profile != "frontend-app":
        return

    pkg = destination / "package.json"
    if not pkg.exists():
        print(f"  {INFO}  No package.json found — skipping npm install")
        return

    node_modules = destination / "node_modules"
    if node_modules.exists():
        print(f"  {PASS}  node_modules already exists")
        return

    print(f"  {INFO}  Running npm install...")
    run_cmd(["npm", "install"], destination, "npm install")


def init_git(destination: Path, project_name: str) -> None:
    """Initialize git, stage files carefully, create initial commit, install hooks."""
    git_dir = destination / ".git"
    if git_dir.exists():
        print(f"  {PASS}  Git already initialized")
    else:
        run_cmd(["git", "init"], destination, "git init")

    # Install pre-commit hook
    hook_src = destination / ".git-hooks" / "pre-commit"
    hook_dst = destination / ".git" / "hooks" / "pre-commit"
    if hook_src.exists():
        hook_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(hook_src, hook_dst)
        hook_dst.chmod(0o755)
        print(f"  {PASS}  Pre-commit hook installed (blocks .env and credential files)")

    # Stage all tracked files (git add respects .gitignore)
    run_cmd(["git", "add", "-A"], destination, "git add -A")

    # Initial commit
    commit_msg = (
        f"chore: initialize project from template\n\n"
        f"Project: {project_name}\n"
        f"Template: project-template-v2 (3-layer architecture)\n"
    )
    run_cmd(["git", "commit", "-m", commit_msg], destination, "Initial commit")


def run_health_check(destination: Path) -> None:
    """Run the profile-aware health check."""
    health_script = destination / "scripts" / "health_check.py"
    if health_script.exists():
        run_cmd(["python3", str(health_script)], destination, "Health check")
    else:
        print(f"  {WARN}  scripts/health_check.py not found — skipping")


def offer_github(destination: Path, project_name: str) -> None:
    """Offer to create a GitHub repo (interactive only)."""
    try:
        result = subprocess.run(["gh", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  {INFO}  gh CLI not available — skipping GitHub setup")
            return
    except FileNotFoundError:
        print(f"  {INFO}  gh CLI not found — install: https://cli.github.com")
        return

    print(f"\n  {INFO}  GitHub: run 'gh repo create {project_name} --private --source=. --push' to publish")


# ── Main ──────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a new project from project-template-v2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python3 scripts/create_project.py --name my-dashboard --profile dashboard-static\n"
            "  python3 scripts/create_project.py --name my-app --profile frontend-app --deploy vercel\n"
            "  python3 scripts/create_project.py --list-profiles\n"
        ),
    )
    parser.add_argument("--name", help="Project name (used as directory name)")
    parser.add_argument("--profile", help="Project profile to use")
    parser.add_argument("--dest", default="/Users/danielbally/Git", help="Parent directory for the new project")
    parser.add_argument("--deploy", help="Override default deploy target")
    parser.add_argument("--runtime", help="Override default runtime")
    parser.add_argument("--loop-mode", help="Override default loop mode")
    parser.add_argument("--knowledge-level", help="Override default knowledge level")
    parser.add_argument("--force", action="store_true", help="Overwrite existing directory")
    parser.add_argument("--skip-git", action="store_true", help="Skip git init and initial commit")
    parser.add_argument("--skip-venv", action="store_true", help="Skip venv/npm install")
    parser.add_argument("--list-profiles", action="store_true", help="List available profiles and exit")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.list_profiles:
        print("\nAvailable profiles:\n")
        for profile, defaults in PROFILE_DEFAULTS.items():
            print(f"  {profile}")
            print(f"    deploy: {defaults['deploy']}, runtime: {defaults['runtime']}, "
                  f"loop: {defaults['loop_mode']}, knowledge: {defaults['knowledge_level']}")
        print()
        return 0

    if not args.name or not args.profile:
        print("Both --name and --profile are required unless using --list-profiles.")
        return 1

    if args.profile not in PROFILE_DEFAULTS:
        print(f"Unknown profile: {args.profile}")
        print(f"Available: {', '.join(PROFILE_DEFAULTS.keys())}")
        return 1

    destination_root = Path(args.dest).expanduser().resolve()
    destination = destination_root / args.name

    if destination.exists() and any(destination.iterdir()) and not args.force:
        print(f"Destination already exists and is not empty: {destination}")
        print("Use --force only if you want to overwrite/merge into it.")
        return 1

    # ── Scaffold ──────────────────────────────────────────────────────────────

    print(f"\n{'='*52}")
    print(f"  Creating: {args.name}")
    print(f"  Profile:  {args.profile}")
    print(f"{'='*52}")

    print(f"\nScaffolding...")
    destination.mkdir(parents=True, exist_ok=True)

    copy_overlay(CORE_DIR, destination)
    print(f"  {PASS}  Copied core/ files")

    copy_overlay(PROFILES_DIR / args.profile, destination)
    print(f"  {PASS}  Applied {args.profile} profile overlay")

    # ── Placeholder replacement ───────────────────────────────────────────────

    defaults = PROFILE_DEFAULTS[args.profile]
    replacements = {
        "__PROJECT_NAME__": args.name,
        "__PROJECT_SLUG__": slugify(args.name),
        "__PROFILE__": args.profile,
        "__DEPLOY__": args.deploy or defaults["deploy"],
        "__RUNTIME__": args.runtime or defaults["runtime"],
        "__LOOP_MODE__": args.loop_mode or defaults["loop_mode"],
        "__KNOWLEDGE_LEVEL__": args.knowledge_level or defaults["knowledge_level"],
    }
    replace_placeholders(destination, replacements)
    print(f"  {PASS}  Replaced placeholders")

    # Prettify profile JSON
    profile_path = destination / "project.profile.json"
    if profile_path.exists():
        profile_data = json.loads(profile_path.read_text())
        profile_path.write_text(json.dumps(profile_data, indent=2) + "\n")

    # ── Post-scaffold initialization ──────────────────────────────────────────

    print(f"\nInitializing...")

    init_env(destination, args.profile)

    if not args.skip_venv:
        init_venv(destination, args.profile)
        init_node(destination, args.profile)

    if not args.skip_git:
        init_git(destination, args.name)

    # ── Health check ──────────────────────────────────────────────────────────

    print(f"\nVerifying...")
    run_health_check(destination)

    # ── Summary ───────────────────────────────────────────────────────────────

    offer_github(destination, args.name)

    print(f"\n{'─'*52}")
    print(f"  Setup complete: {args.name}")
    print(f"{'─'*52}")
    print()
    print("  Next steps:")

    if args.profile in ("workflow-python", "hybrid-geospatial"):
        print("    1. source .venv/bin/activate")
        print("    2. Edit .env with your API keys")
    elif args.profile == "frontend-app":
        print("    1. cd into the project and run: npm run dev")
    else:
        print("    1. cd into the project")

    print("    2. Tell your agent: 'bootstrap this project' and describe your vision")
    print("       → It will populate knowledge/context.md, README.md, and directives/")
    if args.profile in ("workflow-python", "hybrid-geospatial"):
        print("    3. make help   ← see all available commands")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
