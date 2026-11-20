# antigravity-council

An Antigravity plugin that queries multiple AI models across specialized analytical roles (Security, Devil's Advocate, Performance, Simplicity) with anonymous cross-examination, delivering **one unified review**.

Compare answers when one model's bias could mislead you: architecture decisions, debugging dead ends, security reviews, or framework choices.

Inspired by [hex/claude-council](https://github.com/hex/claude-council), but built natively for Antigravity without requiring external API keys.

---

## What It Does

```
You: "Council review: Is our authentication and session architecture sound?"

┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│ 🛡️ Security Auditor  │  │  😈 Devil's Advocate │  │ ⚡ Simplicity / Perf │
│                      │  │                      │  │                      │
│ Algorithm confusion  │  │ Single point of      │  │ DB lookup on every   │
│ & CSRF attack        │  │ failure if refresh   │  │ request kills edge   │
│ vectors...           │  │ token leaks...       │  │ latency...           │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘
            │                        │                        │
            └────────────────────────┼────────────────────────┘
                                     │
                          🔄 Anonymous Peer Review
                     (Cross-critique & blind spots exposed)
                                     │
                        🏛️ Chairman Synthesis
                      One Unified Master Verdict:
               • Executive Decision & Direct Answer
               • Synthesized Architecture Blueprint
               • Role-Divided Insights & Tensions Reconciled
               • Critical Trade-offs & Unresolved Risks
               • Immediate Tactical Action Plan
```

Instead of dumping 4 conflicting walls of text, the council runs a 3-stage deliberation and delivers **one definitive, actionable verdict**.

---

## Features

- **Multi-Role Deliberation**: Models don't just answer generically; each takes an adversarial lens (Security, Devil's Advocate, Simplicity, Scalability).
- **Anonymous Peer Review**: Models critique each other's blinded drafts (Perspective A, B, C...) to eliminate sycophancy and groupthink.
- **Unified Review**: A Chairman model synthesizes the findings into a single structured recommendation.
- **Zero API Keys Needed**: Uses the models already included in your Antigravity subscription (Claude Opus, Claude Sonnet, Gemini Flash, GPT-OSS).

---

## Installation

### Option A: Clone to plugins directory

```bash
# macOS / Linux
git clone https://github.com/akash/antigravity-council.git ~/.gemini/config/plugins/antigravity-council

# Windows (PowerShell)
git clone https://github.com/akash/antigravity-council.git $env:USERPROFILE\.gemini\config\plugins\antigravity-council
```

### Option B: Local link

If you already cloned the repository:

```bash
# macOS / Linux
ln -s /path/to/antigravity-council ~/.gemini/config/plugins/antigravity-council

# Windows (PowerShell)
Copy-Item -Recurse antigravity-council $env:USERPROFILE\.gemini\config\plugins\antigravity-council
```

The plugin loads automatically on your next Antigravity session.

---

## Usage

### Ask the Council

Mention the council naturally in your prompt:

```
Ask the council: Should I use SQLite or Postgres for a multi-tenant B2B SaaS MVP?
Council review: Is our password hashing strategy secure?
Get the council's take on microservices vs modular monolith
Run this past the council: Which caching tier should we deploy?
```

### Role Presets

You can ask the council to focus on specific angles:

```
Council review (security-focused): Audit our JWT refresh token implementation
Ask the council (adversarial): Stress test our database migration plan
Council review (architecture): Monolith vs event-driven microservices
```

Built-in presets (configured in `config/roles.json`):

| Preset | Active Roles | Best For |
|---|---|---|
| `balanced` (default) | Security + Performance + Simplicity | General architectural decisions |
| `security-focused` | Security + Devil's Advocate + Maintainability | Auth flows, sensitive data, compliance |
| `architecture` | Performance + Maintainability + Simplicity | System design, database & infra choices |
| `code-review` | Security + Maintainability + Simplicity | Pull requests, refactoring, diff reviews |
| `adversarial` | Devil's Advocate + Security + Simplicity | Stress-testing plans against worst-case traps |

### Available Roles

| Role Key | Name | Focus Area |
|---|---|---|
| `security` | **Security Auditor** | Attack surfaces, auth loopholes, injections, data leaks |
| `devil` | **Devil's Advocate** | Hidden failure modes, catastrophic traps, breaking consensus |
| `performance` | **Performance Architect** | Concurrency, I/O bottlenecks, DB locks, caching limits |
| `simplicity` | **Simplicity Champion** | Radical simplicity, eliminating over-engineering |
| `maintainability` | **Clean Architecture** | Modularity, testability, technical debt, refactorability |
| `dx` | **Developer Experience** | API ergonomics, local dev friction, debugging ease |

### Check Status

```
Council status
What models are available for the council?
```

Outputs the available models, vendor diversity, and remaining quota.

### Raw Transcripts

If you want to inspect each model's individual draft before the Chairman's synthesis:

```
Ask the council (raw): Should we use Redis or Memcached?
```

---

## Output Format

The Chairman produces a single structured verdict:

1. **Executive Summary & Direct Verdict** — Unambiguous recommendation upfront.
2. **Synthesized Architecture & Technical Blueprint** — Concrete technical solution with code/diagrams.
3. **Role-Divided Insights & Tensions Reconciled** — Specific takeaways from the Security, Devil's Advocate, and Simplicity perspectives.
4. **Critical Trade-offs & Unresolved Edge Cases** — Explicitly states what is sacrificed and what conditions would flip the decision.
5. **Tactical Action Plan** — Prioritized, immediate implementation steps.

---

## Comparison: `antigravity-council` vs `claude-council`

| Feature | `claude-council` (Claude Code) | `antigravity-council` (Antigravity) |
|---|---|---|
| **Host Environment** | Claude Code CLI | Google Antigravity |
| **Model Orchestration** | Shell scripts (`curl`, `jq`, `tmux`, background PIDs) | Native Python workflow engine (`parallel`, `agent`) |
| **Multi-Model Access** | Requires external API keys (OpenAI, Gemini, Grok, etc.) | Zero-config: uses Antigravity subscription models |
| **Deliberation Protocol** | Role-divided deliberation + peer critique + synthesis | Exact same 3-stage protocol |
| **Output Style** | Unified review or side-by-side terminal panes | Unified Master Review inline |

---

## Contributing

PRs and new role definitions are welcome! Feel free to open an issue or submit a pull request on GitHub.

## License

MIT — see [LICENSE](LICENSE).
