# project-template

A profile-based scaffolding system for AI-assisted development. Every project created from this template starts with the same operating model: a 3-layer architecture, a persistent knowledge system, and a deployment-aware profile — so an AI agent can pick up any project cold and know exactly where to look, what to do, and what not to touch.

---

## The problem this solves

When you work across many projects with AI coding agents, three things break down over time:

1. **Context loss between sessions.** The agent doesn't know what was decided last week, what failed last month, or what the current objective is. Every session starts from scratch.
2. **Inconsistent structure.** Each project grows its own folder conventions organically. Scripts live in different places, docs are in different formats, nothing is predictable.
3. **Business logic in the wrong layer.** The agent starts writing loops, API calls, and data transforms inline in chat. This works once and then breaks silently.

This template solves all three by giving every project the same skeleton — a Layer 1 for intent (directives), a Layer 2 contract for the agent (thin orchestration), a Layer 3 for execution (deterministic scripts), and a `knowledge/` system that survives across sessions.

---

## The 3-layer architecture

Every project generated from this template is built around three layers that separate intent from execution:

```
Layer 1 — Directives (directives/)
  What to do. Written as Markdown SOPs before any code is written.
  One directive per workflow. Each has a Validation Contract.

Layer 2 — Orchestration (the agent)
  Reads directives, calls scripts, verifies outputs.
  Makes decisions. Does not write business logic.

Layer 3 — Execution (execution/ or scripts/)
  Deterministic code. Handles loops, API calls, retries, transforms.
  Never inside the agent's reasoning. Always in a file.
```

The key constraint: **if a process has loops, parsing, retries, or multiple API calls, it must live in `execution/`, not in the agent's response.** This boundary is the difference between a reliable system and a fragile one.

---

## Repository structure

```
project-template/
├── core/                  # Files every project starts with, regardless of profile
├── profiles/              # Profile overlays that shape the project's runtime form
│   ├── dashboard-static/
│   ├── frontend-app/
│   ├── hybrid-geospatial/
│   └── workflow-python/
└── scripts/
    └── create_project.py  # The scaffold generator
```

### `core/`

Everything in `core/` lands in every generated project. It is the constitution — the files that keep all projects anchored to the same habits regardless of what they are building.

| File / Folder | Purpose |
|---|---|
| `README.md` | Human-readable project overview with placeholders |
| `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` | Mirrored agent instructions for Claude, Codex, and Gemini |
| `task.md` | The active work ledger — current objective, steps, progress log |
| `project.profile.json` | Declares the project's shape (profile, deploy target, runtime, loop mode) |
| `directives/` | Layer 1 SOPs — one file per major workflow |
| `knowledge/` | Durable project memory that survives across sessions |
| `scripts/health_check.py` | Profile-aware sanity check |
| `.tmp/` | Safe scratch space for loop artifacts, eval outputs, temp logs |
| `.git-hooks/pre-commit` | Blocks committed `.env` and secret files |
| `.claude/settings.local.json` | Tool permissions for Claude Code |

### `profiles/`

Profiles are overlays that make the template fit the actual shape of a project. A dashboard is not the same as a Python pipeline — profiles let both use the same operating model without pretending they are identical.

| Profile | Use when |
|---|---|
| `dashboard-static` | Static HTML/CSS/JS, simple deploy, no build step |
| `frontend-app` | Component-driven UI with Vite or another build tool |
| `workflow-python` | Scripts, pipelines, data work, deterministic execution matters |
| `hybrid-geospatial` | Static UI + serious Python analysis tooling (Leaflet map + data pipeline) |

Each profile adds the files its runtime needs — a `Makefile`, `requirements.txt`, `execution/` scripts, CI workflow, or frontend `package.json` — merged on top of `core/` at project creation time.

---

## What a generated project contains

After running `create_project.py`, the new project directory has:

### `directives/`

Layer 1. Every major workflow gets a directive before any code is written. A directive defines: the goal, the inputs, the expected outputs, the Validation Contract (binary pass/fail assertions that define "done"), and edge cases.

**Why directives exist before code:** if you can't write a binary test for "done" before implementation, you don't understand the problem yet. Directives force that clarity. They also give the agent a stable instruction set that outlasts any single session.

### `knowledge/`

The project's persistent memory. Every significant action in a session should leave a trace here.

| File | Purpose |
|---|---|
| `SESSION.md` | Running checkpoint log — what happened, what changed, what's next |
| `DECISIONS.md` | Durable architecture decisions and why they were made |
| `ERRORS.md` | Recurring mistakes, root causes, and fixes |
| `context.md` | Project mission, stack, constraints, stakeholders, out-of-scope |
| `INDEX.md` | Map of the entire knowledge base with dates |
| `domain/` | Domain-specific notes (APIs, naming conventions, data structures) |
| `procedural/` | Repeatable local workflows (deploy steps, test commands, patterns) |

**Why `knowledge/` exists:** AI agents have no memory between sessions by default. This folder is the workaround. When a new session starts, the agent reads `SESSION.md` and `INDEX.md` first — it knows what was done, what was decided, and what's next without needing to re-derive it from conversation.

**The graduation rule:** if a lesson applies to the underlying framework (React, Python, Vite) rather than this specific project's logic, it graduates to a shared workspace skill — not stored in `knowledge/`.

### `task.md`

The active work ledger. Contains the current objective, a short step list toward it, and a dated progress log. The agent reads this at session start and updates it throughout. It is the single source of truth for "what are we working on right now."

### `execution/` _(workflow-python and hybrid-geospatial profiles)_

Layer 3. Deterministic scripts for anything that involves loops, data transforms, API pagination, retries, or multi-step processing. The agent calls these scripts — it does not implement that logic itself.

**Why `execution/` exists:** a loop inside an agent's response is invisible, untestable, and unreproducible. The same loop in a Python script is debuggable, versionable, and runnable independently. Business logic lives in code.

### `.tmp/`

Scratch space for the agent. Loop artifacts, evaluation outputs, draft reports, screenshots, temp exports — anything that should not pollute source folders and should not be committed. A `.gitkeep` is tracked so the directory exists on clone; everything inside it is gitignored.

### `project.profile.json`

The project's self-description. Tells the agent (and any tooling) what shape this project has, how it deploys, what runtime it uses, and how it iterates.

```json
{
  "profile": "dashboard-static",
  "deploy": "iis",
  "runtime": "static",
  "loop_mode": "artifact",
  "knowledge_level": "standard"
}
```

---

## Creating a project

```bash
python3 scripts/create_project.py --name my-project --profile dashboard-static
```

The script:
1. Merges `core/` with the selected profile overlay
2. Replaces all `__PROJECT_NAME__` and `__PROFILE__` placeholders
3. Runs `git init`
4. Installs a venv (Python profiles) or `npm install` (Node profiles)
5. Installs the pre-commit hook
6. Runs the health check

**With overrides:**

```bash
python3 scripts/create_project.py \
  --name sentinel-v2 \
  --profile hybrid-geospatial \
  --deploy iis \
  --knowledge-level heavy \
  --loop-mode hybrid
```

**List available profiles:**

```bash
python3 scripts/create_project.py --list-profiles
```

---

## The knowledge system in practice

The intended session flow for any project generated from this template:

1. **Session start:** agent reads `knowledge/SESSION.md` and `knowledge/INDEX.md`. Knows current state without re-reading the whole codebase.
2. **During work:** after every significant action, append a checkpoint to `SESSION.md`.
3. **Error occurs:** log it to `knowledge/ERRORS.md` immediately — before the next action.
4. **Session end:** promote `SESSION.md` checkpoints to permanent `domain/` or `procedural/` files. Clear the checkpoint log. Leave only Last Known State for the next session.

This rhythm is why `SESSION.md` uses a checkpoint format rather than prose. It is written incrementally and read fast.

---

## Why the agent files are mirrored

`CLAUDE.md`, `AGENTS.md`, and `GEMINI.md` contain identical instructions. They exist because different AI tools look for different filenames: Claude Code reads `CLAUDE.md`, OpenAI Codex reads `AGENTS.md`, Gemini reads `GEMINI.md`. Same content, different filename — the same operating model works regardless of which tool is active.

---

## Further reading

- [`STRUCTURE_GUIDE.md`](STRUCTURE_GUIDE.md) — full folder-by-folder reference, profile selection guide, and system directive alignment
- [`core/directives/bootstrap_project.md`](core/directives/bootstrap_project.md) — how to populate a new project's knowledge before writing any code
- [`core/CLAUDE.md`](core/CLAUDE.md) — the agent contract every generated project inherits
