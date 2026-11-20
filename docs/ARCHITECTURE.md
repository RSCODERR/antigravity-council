# Council Architecture & Execution Flow

This document details the internal design of `antigravity-council` and how the 3-stage deliberation pipeline executes.

---

## High-Level Flow

```
User Prompt: "Council review: <question>"
                 │
                 ▼
  ┌──────────────────────────────────────────────┐
  │ 1. Parameter & Role Resolution               │
  │    (Parse presets from config/roles.json     │
  │     e.g., balanced -> security, perf, simple)│
  └──────────────────────┬───────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────┐
  │ 2. Stage 1: Role-Divided Deliberation        │
  │    parallel(seats, lambda s: agent(...))     │
  │    - Security Auditor                        │
  │    - Devil's Advocate                        │
  │    - Simplicity Champion                     │
  │    (All run blind to each other)             │
  └──────────────────────┬───────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────┐
  │ 3. Stage 2: Anonymous Cross-Examination      │
  │    (Perspectives anonymized as A, B, C...)   │
  │    Each seat critiques the others' blind     │
  │    spots through their specialized lens.     │
  └──────────────────────┬───────────────────────┘
                         │
                         ▼
  ┌──────────────────────────────────────────────┐
  │ 4. Stage 3: Chairman Synthesis               │
  │    (Pro/Opus agent synthesizes full dossier) │
  │    - Resolves conflicts                      │
  │    - Drops ungrounded claims                 │
  │    - Outputs 1 Unified Review                │
  └──────────────────────────────────────────────┘
```

---

## Directory Structure

```
antigravity-council/
├── README.md                          # Human-readable documentation & usage
├── LICENSE                            # MIT License
├── plugin.json                        # Antigravity plugin manifest
├── config/
│   └── roles.json                     # Role lenses & preset definitions
├── docs/
│   └── ARCHITECTURE.md                # This document
├── skills/
│   ├── council-ask/
│   │   ├── SKILL.md                   # Core skill documentation & triggers
│   │   └── scripts/
│   │       └── council_workflow.py    # Native Python orchestration workflow
│   └── council-status/
│       └── SKILL.md                   # Quota and model availability check
└── rules/
    └── AGENTS.md                      # Auto-suggestion rules for complex decisions
```

---

## Role Configuration (`config/roles.json`)

Roles provide specialized critical lenses to prevent sycophancy:

```json
{
  "roles": {
    "security": {
      "name": "Security Auditor",
      "instruction": "Evaluate strictly through a security lens..."
    },
    "devil": {
      "name": "Devil's Advocate",
      "instruction": "Actively challenge assumptions and consensus..."
    },
    "simplicity": {
      "name": "Pragmatist & Simplicity Champion",
      "instruction": "Advocate for radical simplicity and operational reality..."
    }
  },
  "presets": {
    "balanced": ["security", "performance", "simplicity"],
    "security-focused": ["security", "devil", "maintainability"],
    "adversarial": ["devil", "security", "simplicity"]
  }
}
```

---

## Antigravity Workflow Primitives

Unlike `claude-council` which relies on shell scripts (`curl`, `jq`, `tmux`), `antigravity-council` runs on Antigravity's native Python workflow runtime:

- **`parallel(items, fn)`**: Spawns concurrent asynchronous subagents.
- **`agent(prompt, role, model)`**: Runs an isolated model inference turn with dedicated system prompts.
- **`phase(title)`**: Emits structured progress phases to the Antigravity UI.
- **`log(msg)`**: Logs workflow diagnostic events.
