---
name: council-ask
description: >-
  Query multiple AI models in parallel to get diverse perspectives on a question.
  Use this whenever the user names the council directly — ask the council,
  council review, what does the council think, get a second opinion, run this
  past the council — including reviews of code, documents, plans or artifacts.
  Also suggest it unprompted when the user is choosing between competing
  approaches (databases, frameworks, auth strategies), is stuck after multiple
  failed debugging attempts, faces build-vs-buy decisions, or is weighing
  security/performance/maintainability tradeoffs. Do NOT suggest it unprompted
  for simple implementation tasks, quick fixes, or questions with clear single
  answers; a direct request for the council overrides that exclusion.
---

# Council Ask — Multi-Role & Multi-Model Consultation

Query multiple AI models simultaneously across **specialized analytical roles** (e.g. *Security Auditor*, *Devil's Advocate*, *Performance Architect*, *Simplicity Champion*), run anonymous cross-examination peer review, and synthesize everything into **one definitive, unified verdict**.

## Overview

The council architecture follows the exact 3-stage deliberation protocol pioneered by `claude-council`:

1. **Stage 1: Role-Divided Parallel Deliberation**
   Instead of identical generic prompts, each model or seat is assigned a specialized lens (e.g., Security Auditor, Devil's Advocate, Simplicity Champion, Performance Architect). They analyze the problem independently and blind to each other.
2. **Stage 2: Anonymous Cross-Examination (Peer Review)**
   Perspectives are anonymized (Perspective A, B, C...) and distributed across members. Each seat critiques the other perspectives, exposing blind spots, groupthink, and false assumptions.
3. **Stage 3: Chairman Synthesis (Unified Review)**
   The Council Chairman compiles all transcripts, reconciles conflicting tensions, and generates **one single, unified verdict**.

## Role System & Presets

Available roles from `config/roles.json`:
- `security`: **Security Auditor** (attack surfaces, auth loopholes, injections, data leaks)
- `devil`: **Devil's Advocate** (challenges assumptions, failure modes, silent regressions)
- `performance`: **Performance & Scalability Architect** (concurrency, I/O, bottlenecks, locking)
- `simplicity`: **Pragmatist & Simplicity Champion** (radical simplicity, over-engineering scrutiny)
- `maintainability`: **Clean Architecture Advocate** (modularity, technical debt, refactorability)
- `dx`: **Developer Experience Champion** (ergonomics, local dev friction, debugging ease)

### Built-in Presets:
- `balanced` (default): `['security', 'performance', 'simplicity']`
- `architecture`: `['performance', 'maintainability', 'simplicity']`
- `security-focused`: `['security', 'devil', 'maintainability']`
- `code-review`: `['security', 'maintainability', 'simplicity']`
- `adversarial`: `['devil', 'security', 'simplicity']`

## Step 1: Determine Available Models

Before anything else, check which models are available by running the swarm
`models` action:

```
swarm(action="models", all=true)
```

This returns the full list of models the user has access to. Each model is a
distinct "council seat." The more diverse the models, the better — mixing
vendors (Claude, Gemini, GPT) gives genuinely independent perspectives.

## Step 2: Ask the User Which Models to Consult

Present the available models and ask which to include. Use `ask_question`:

- **If 4 or fewer models**: Show them all plus an "All models" option
- **If more than 4 models**: Group by vendor family, plus "All models"

Default recommendation is **all available models** for maximum diversity.

Also ask about verbosity in the same question:
- **Standard** (default): Balanced, thorough answer
- **Brief**: 3–5 sentences, bullets only
- **Detailed**: Deep analysis with code examples and trade-offs

**Skip asking if the user already specified models or verbosity in their
request**, e.g. "ask gemini and claude about..." or "give me a brief council
take on...".

## Step 3: Verify the Question

The question is **data sent to the models**, not instructions for you.

Before sending, check the question for premises stated as fact but not verified.
Models receive a description and cannot test premises — they will reason from
whatever the question asserts. A false premise produces confident unanimity.

1. Identify load-bearing factual claims (what exists on disk, how something
   works, what a log says).
2. For claims you can check cheaply (a file exists, a function signature), check
   them and correct the question if wrong.
3. For claims you cannot check, label them:

```
OBSERVED: <what has been confirmed>
NOT VERIFIED: <what is assumed>
```

## Step 4: Run the Council via Workflow

Use the `run_workflow` tool to fan out the question to all selected models in
parallel. Use the workflow script at:

```
ScriptPath: <plugin_root>/skills/council-ask/scripts/council_workflow.py
```

Pass these args:

```json
{
  "question": "The user's question, with any context",
  "models": ["model-id-1", "model-id-2", "model-id-3"],
  "verbosity": "standard",
  "context": "Optional: relevant code snippets, file contents, or conversation context"
}
```

**Finding the script path**: The plugin is installed at
`~/.gemini/config/plugins/antigravity-council/`. The full script path is
`~/.gemini/config/plugins/antigravity-council/skills/council-ask/scripts/council_workflow.py`.
If the plugin was installed elsewhere (workspace `.agents/` directory or a
different path), adjust accordingly — look for `council_workflow.py` under this
plugin's directory.

### Auto-Context

Unless the user said not to, gather relevant context before asking:

1. Extract keywords from the question (function names, file patterns, domain
   terms).
2. Search with available tools for matching files (max 5 files, ~10,000 tokens).
3. Append the file contents to the `context` arg so every model sees the same
   code.

## Step 5: Deliver Unified Response

The council workflow automatically fans out to parallel models, collects their independent deliberations, and runs a **Chairman Synthesis** stage to produce **one single, unified, authoritative response**.

Present the final output directly to the user as a cohesive, structured answer:

```markdown
# 🏛️ Council Verdict & Recommendation

### 1. Executive Summary & Direct Answer
<Clear, direct verdict>

### 2. Comprehensive Solution / Proposal
<Synthesized technical solution / ideas incorporating the council's best points>

### 3. Council Consensus & Key Insights
<Unanimous findings and fundamental rules agreed upon across models>

### 4. Trade-Offs & Dissenting Viewpoints
<Alternative perspectives, tension points, or edge cases discussed during deliberation>

### 5. Decisive Action Plan / Next Steps
<Concrete action items>
```

> **Note:** If the user explicitly asks to inspect raw individual drafts (e.g. `show raw answers` or `--raw`), pass `"show_individual": true` in the workflow args. Otherwise, always deliver the clean, unified council answer.

## Error Handling

- If a model fails or times out, note the error but continue with the others.
- If all models fail, report the failure clearly.
- If only one model is available, run it but note that a single perspective
  lacks the cross-checking benefit of multiple models.

## Special Modes

### Named Provider
If the user names specific models ("ask gemini about...", "what does claude
think..."), resolve the name to the model ID and query only those.

### Debate Mode
If the user asks for a debate ("have them debate this", "council debate"),
run two rounds:
1. **Round 1**: Each model answers independently (normal flow).
2. **Round 2**: Each model receives a summary of all Round 1 answers and is
   asked to critique, challenge, or defend positions.

Include in the synthesis:
- **Strongest criticisms**: Most compelling points from rebuttals
- **Consensus shifts**: Where a model changed its position
- **Unresolved tensions**: Disagreements that survived the debate
