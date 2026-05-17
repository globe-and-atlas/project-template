# project-template

Profile-based project scaffolding for the `/Users/danielbally/Git` workshop.

This template keeps the same workshop laws as the original template:

- Layer 1: `directives/`
- Layer 2: thin orchestration
- Layer 3: deterministic execution

But instead of assuming every project is Python-first, it combines:

- a shared `core/`
- one selected profile from `profiles/`

## Available Profiles

- `dashboard-static`
- `frontend-app`
- `workflow-python`
- `hybrid-geospatial`

## Create A Project

```bash
cd /Users/danielbally/Git/project-template
python3 scripts/create_project.py --name my-new-project --profile dashboard-static
```

Optional overrides:

```bash
python3 scripts/create_project.py \
  --name sentinel-explorer-v2 \
  --profile hybrid-geospatial \
  --deploy iis \
  --knowledge-level heavy \
  --loop-mode hybrid
```

List profiles:

```bash
python3 scripts/create_project.py --list-profiles
```

## Design Notes

See [PROJECT_TEMPLATE_V2.md](/Users/danielbally/Git/project-template/PROJECT_TEMPLATE_V2.md) for the full blueprint and rationale.
See [STRUCTURE_GUIDE.md](/Users/danielbally/Git/project-template/STRUCTURE_GUIDE.md) for the practical folder-by-folder guide, system-directive alignment, and profile rules.
