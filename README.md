# 🏛️ Antigravity Council

An Antigravity plugin that queries multiple AI models in parallel and synthesizes their answers. Get diverse perspectives on architecture decisions, debugging dead-ends, security reviews, and any question where one model's bias could mislead you.

> **Think of it as a panel of experts** — each AI model answers your question independently, then you get a synthesis of where they agree, where they disagree, and what to do about it.

## What It Does

```
You: "Ask the council: Should I use UUID or BIGINT primary keys for a SaaS users table?"

┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  🟢 Claude   │  │  🔵 Gemini   │  │  🟣 GPT-OSS  │
│              │  │              │  │              │
│  UUIDs for   │  │  BIGINTs for │  │  UUIDs, but  │
│  distributed │  │  performance │  │  use UUIDv7  │
│  systems...  │  │  on single   │  │  for sorted  │
│              │  │  node...     │  │  inserts...  │
└──────────────┘  └──────────────┘  └──────────────┘
                        │
                   🧭 Synthesis
            Consensus: All agree indexing matters
            Divergence: Scale assumptions differ
            Recommendation: UUIDv7 if you might
            distribute later; BIGINT if you won't
```

## Install

### Option A: Clone to plugins directory

```bash
git clone https://github.com/akash/antigravity-council.git
```

Then copy or symlink to your Antigravity plugins directory:

```bash
# macOS / Linux
cp -r antigravity-council ~/.gemini/config/plugins/antigravity-council

# Windows (PowerShell)
Copy-Item -Recurse antigravity-council $env:USERPROFILE\.gemini\config\plugins\antigravity-council
```

### Option B: Clone directly into plugins

```bash
# macOS / Linux
git clone https://github.com/akash/antigravity-council.git ~/.gemini/config/plugins/antigravity-council

# Windows (PowerShell)
git clone https://github.com/akash/antigravity-council.git $env:USERPROFILE\.gemini\config\plugins\antigravity-council
```

The plugin loads automatically on the next Antigravity conversation.

## Usage

### Ask the Council

Just mention the council naturally:

```
Ask the council: Should I use SQLite or Postgres for my demo app?
Council review: Is our JWT implementation secure?
Get the council's take on microservices vs monolith for our team size
Run this past the council: Which caching strategy should we use?
```

### Check Status

```
Council status
What models are available for the council?
```

### Debate Mode

Ask for a debate to have models challenge each other:

```
Have the council debate: REST vs GraphQL for our mobile API
Council debate: Is our error handling strategy sound?
```

In debate mode, each model first answers independently (Round 1), then reads
all other answers and critiques them (Round 2). The synthesis includes the
strongest criticisms and whether any model changed its position.

### Verbosity

```
Brief council take on Redis vs Memcached
Give me a detailed council review of our auth flow
```

- **Brief**: 3–5 sentences, bullets only
- **Standard** (default): Balanced and thorough
- **Detailed**: Deep analysis with code examples and trade-offs

### Named Models

```
Ask claude and gemini about our database schema
What does GPT think about this approach?
```

## How It Works

1. **Fan out**: Your question goes to each selected AI model in parallel via
   Antigravity's workflow system. Each model answers independently — they
   can't see each other's responses.

2. **Collect**: All answers arrive simultaneously. Each is displayed verbatim
   with its model name.

3. **Synthesize**: The council produces a structured synthesis:
   - **Consensus**: What the models agree on
   - **Divergence**: Where and why they disagree
   - **Recommendation**: What the evidence supports, plus the premise that
     could flip the answer

## Available Models

The council uses whatever models your Antigravity subscription includes.
Typical seats:

| Model | Vendor | Notes |
|-------|--------|-------|
| Claude Opus 4.6 | Anthropic | Deep reasoning, thinking model |
| Claude Sonnet 4.6 | Anthropic | Fast, capable |
| Gemini 3.8 Flash | Google | Fast, multiple quality tiers |
| GPT-OSS 120B | OpenAI | Open-source weights |

Run "council status" to see your current available models and quota.

## When to Use the Council

**Great for:**
- Architecture decisions (monolith vs microservices, database choices)
- Security reviews (auth flows, API design, data handling)
- Debugging dead-ends (fresh eyes from different models)
- Build vs buy decisions
- Framework/library evaluation
- Code review of critical paths

**Not needed for:**
- Simple implementation tasks
- Questions with one clear answer
- Quick fixes and small changes

## Auto-Suggestions

The plugin includes rules that automatically suggest the council when it
detects you're facing a decision that would benefit from multiple perspectives.
You can always decline — it's a suggestion, not an interruption.

## Project Structure

```
antigravity-council/
├── plugin.json                           # Plugin manifest
├── README.md                             # This file
├── LICENSE                               # MIT
├── assets/
│   └── logo.svg                          # Plugin icon
├── skills/
│   ├── council-ask/
│   │   ├── SKILL.md                      # Main council query skill
│   │   └── scripts/
│   │       └── council_workflow.py       # Parallel query workflow
│   └── council-status/
│       └── SKILL.md                      # Status & available models
└── rules/
    └── AGENTS.md                         # Auto-suggestion rules
```

## Differences from claude-council

This plugin is inspired by [hex/claude-council](https://github.com/hex/claude-council)
(a Claude Code plugin) but built natively for Antigravity:

| Feature | claude-council | antigravity-council |
|---------|---------------|-------------------|
| Platform | Claude Code | Antigravity |
| Multi-model | External API calls (bash/curl) | Native workflow system |
| Parallelism | Bash background jobs | Antigravity parallel agents |
| Models | External APIs + CLIs | All models in your Antigravity subscription |
| Pane/UI | tmux pane or Claude Code mod | Inline in Antigravity chat |
| External APIs | Yes (OpenAI, Gemini, Grok, etc.) | Uses Antigravity's built-in models |
| Setup | API keys required | Zero config — uses your existing subscription |

The key advantage: **zero API keys needed**. Your Antigravity subscription
already includes Claude, Gemini, and GPT models, so the council works
out of the box.

## Contributing

PRs welcome! To add features:

1. Fork this repo
2. Make your changes
3. Test by copying to `~/.gemini/config/plugins/antigravity-council/`
4. Submit a PR

## License

MIT — see [LICENSE](LICENSE).
