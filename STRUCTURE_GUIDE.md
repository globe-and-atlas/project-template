# project-template-v2 Structure Guide

This file explains what each major folder in `project-template-v2` does, why it matters, how it aligns with [WORKSHOP_PHILOSOPHY.md](/Users/danielbally/Git/WORKSHOP_PHILOSOPHY.md), and how to specify a project profile.

## First Principle

This template is built around the workshop laws:

- `Use`: the project should do something real
- `Purpose`: the project should serve a clear mission
- `Beauty`: the project should show visible craft

It also preserves the 3-layer architecture:

- `Layer 1`: `directives/`
- `Layer 2`: the agent as thin orchestration
- `Layer 3`: deterministic execution in code

That means the template is not just a file tree. It is an operating model.

## Top-Level Template Folders

### `core/`

What it does:
Contains the files every project should start with, no matter the profile.

Why it matters:
This is the workshop constitution made practical. It keeps all projects anchored to the same habits of documentation, directives, memory, and profile awareness.

Important contents:

- `README.md`: human-readable overview
- `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`: mirrored agent instructions
- `task.md`: the current work ledger
- `project.profile.json`: declares the active project profile
- `directives/`: Layer 1 intent
- `knowledge/`: durable project memory
- `scripts/health_check.py`: profile-aware sanity check
- `.tmp/`: scratch space for loop artifacts and experiments

### `profiles/`

What it does:
Holds the profile overlays that make the template fit the actual shape of a project.

Why it matters:
Your Git folder is not one thing. Some projects are dashboards, some are frontend apps, some are Python workflows, and some are hybrids like `sentinel-explorer`. Profiles let one workshop system support all of them without pretending they are identical.

Current profiles:

- `dashboard-static`
- `frontend-app`
- `workflow-python`
- `hybrid-geospatial`

### `scripts/`

What it does:
Contains meta-tools for working with the template itself.

Why it matters:
This is where project creation should live, rather than burying setup logic inside chat or spread across shell snippets.

Important contents:

- `create_project.py`: combines `core/` with a selected profile and writes the new project

## Folders Inside A Generated Project

These folders appear in every generated project or in some profiles.

### `directives/`

What it does:
Stores the Standard Operating Procedures for the project.

Why it matters:
This is Layer 1. It captures intent clearly before execution starts. If the work is not defined here or in `task.md`, it is probably not stable enough yet.

Typical contents:

- workflow directives
- evaluation directives
- loop instructions
- operating checklists

### `knowledge/`

What it does:
Stores project memory that should survive a single session.

Why it matters:
This supports iteration, continuity, and knowledge graduation. It keeps the project from relearning the same lessons.

Important files:

- `INDEX.md`: map of what the knowledge base contains
- `SESSION.md`: current or recent working state
- `DECISIONS.md`: durable choices and why they were made
- `ERRORS.md`: recurring mistakes and fixes
- `context.md`: project mission, constraints, stakeholders, environment
- `domain/`: domain-specific notes
- `procedural/`: repeatable local workflows

### `.tmp/`

What it does:
Provides a safe place for temporary outputs.

Why it matters:
Karpathy loops need a place for artifacts, eval outputs, screenshots, notes, and experiments that should not pollute source folders.

Typical uses:

- screenshot comparisons
- report drafts
- eval outputs
- scratch exports
- temporary logs

### `src/`

What it does:
Stores the main application code for the active profile.

Why it matters:
This is usually where the user-facing logic lives. For dashboards and frontend apps, it is the heart of the interface.

### `execution/`

What it does:
Stores deterministic scripts and business logic for workflow-heavy or hybrid projects.

Why it matters:
This is Layer 3 in action. If a process has loops, parsing, retries, transforms, or analysis, it should live here rather than inside the agent layer.

Typical uses:

- data extraction
- geospatial analysis
- report generation
- normalization and transforms
- evaluation scripts

### `data/`

What it does:
Stores static inputs, local reference files, or app-consumed JSON.

Why it matters:
Many of your dashboard and geospatial projects need a clear, visible home for runtime data. Keeping it separate from `src/` improves clarity and deployability.

### `assets/`

What it does:
Stores images, icons, visual references, and other non-code design assets.

Why it matters:
This supports the `Beauty` part of the workshop standard. It encourages intentional visual craft instead of scattered assets.

### `public/`

What it does:
Stores static frontend assets for build-tool-based apps.

Why it matters:
Some frontend stacks expect a dedicated public asset path. Keeping it explicit prevents profile confusion.

### `tests/`

What it does:
Stores smoke tests, unit tests, and verification scripts.

Why it matters:
Iteration without evaluation becomes drift. Tests are part of how the project proves `Truth`.

### `prod/`

What it does:
Stores deploy-ready artifacts or a packaging target for static deployments.

Why it matters:
Many of your normal projects end as dashboards that need simple shipping, especially to IIS or other static hosting. This folder makes deployment first-class rather than an afterthought.

## Why Profiles Exist

Profiles keep the workshop laws constant while changing the execution shape.

### `dashboard-static`

Use when:

- the project is mostly HTML, CSS, and JavaScript
- deployment should be simple
- the app behaves like a dashboard or tool

Strength:
Fast to ship and easy to host.

### `frontend-app`

Use when:

- the project needs a frontend build system
- the UI is app-like and component-driven
- Vite or another Node-based stack makes sense

Strength:
Good fit for interactive products with modern frontend tooling.

### `workflow-python`

Use when:

- the project is driven by scripts, pipelines, or structured data work
- deterministic execution matters more than UI
- tests and evaluation should be script-centered

Strength:
Best fit for heavy automation and reproducible workflows.

### `hybrid-geospatial`

Use when:

- the project has a static UI but also deterministic analysis tooling
- map, data, and reporting concerns all matter
- the project resembles `sentinel-explorer` in shape

Strength:
Lets the UI stay lightweight while serious logic stays in code.

## Skills And Where They Fit

Skills are not folders in the project. They are reusable capabilities the agent can apply while working inside the project.

Why they matter:
They are part of knowledge graduation. A pattern that becomes broadly reusable should eventually leave a single repo and become a shared skill.

Practical relationship to the folder structure:

- `directives/` says what should happen
- skills help the agent perform specialized work well
- `execution/` contains deterministic logic when the work must be repeatable
- `knowledge/` stores project-specific learnings before they graduate

Good rule:

- project-specific lesson: store in `knowledge/`
- repeatable workshop method: promote to a shared skill

## Karpathy Loops In This Structure

This v2 structure is loop-ready by default.

The loop pattern is:

1. define the target in `task.md`
2. describe the method in `directives/loop.md`
3. generate artifacts or outputs
4. evaluate them with tests, scripts, or review criteria
5. store temporary outputs in `.tmp/`
6. record durable lessons in `knowledge/`

That is why `.tmp/`, `knowledge/`, `tests/`, and `execution/` all matter.

## System Directive Alignment

This template supports [WORKSHOP_PHILOSOPHY.md](/Users/danielbally/Git/WORKSHOP_PHILOSOPHY.md) in a direct way.

### `Use`

Supported by:

- `task.md`
- deploy-aware profiles
- `prod/`
- practical runtime folders like `src/`, `data/`, and `execution/`

### `Purpose`

Supported by:

- `README.md`
- `knowledge/context.md`
- `directives/`
- `project.profile.json`

### `Beauty`

Supported by:

- intentional UI-capable profiles
- `assets/`
- explicit room for polished deploy artifacts
- a structure that makes craft visible instead of improvised

### Thin Orchestration

Supported by:

- mirrored agent files
- clear separation between directives and execution
- no assumption that business logic belongs in chat

### Deterministic Execution

Supported by:

- `execution/`
- `scripts/`
- profile-aware health checks
- `tests/`

### Knowledge Graduation

Supported by:

- `knowledge/`
- profile-aware project memory
- the distinction between local knowledge and shared skills

## How To Specify A Profile

There are two moments when a profile is specified.

### 1. At project creation time

Use the generator with `--profile`.

Example:

```bash
cd /Users/danielbally/Git/project-template-v2
python3 scripts/create_project.py --name produced-water-dashboard --profile dashboard-static
```

Available values:

- `dashboard-static`
- `frontend-app`
- `workflow-python`
- `hybrid-geospatial`

### 2. Inside the generated project

The selected profile is written into `project.profile.json`.

Example:

```json
{
  "profile": "dashboard-static",
  "deploy": "iis",
  "runtime": "static",
  "loop_mode": "artifact",
  "knowledge_level": "standard"
}
```

This file is the contract the project uses to describe itself.

## What The Profile File Means

### `profile`

The project shape.

### `deploy`

The primary deployment target or operating mode.

Examples:

- `iis`
- `vercel`
- `local-only`

### `runtime`

The main technical runtime.

Examples:

- `static`
- `node`
- `python`
- `hybrid`

### `loop_mode`

The dominant iteration style.

Examples:

- `artifact`
- `data`
- `hybrid`

### `knowledge_level`

How much project memory the project should maintain.

Examples:

- `light`
- `standard`
- `heavy`

## Recommended Default Thinking

If you are unsure which profile to choose:

- choose `dashboard-static` for most dashboards and static tools
- choose `frontend-app` for component-heavy modern web apps
- choose `workflow-python` for automations and data pipelines
- choose `hybrid-geospatial` for `sentinel-explorer` style systems

That gives you a responsible default without forcing every project into the same body.
