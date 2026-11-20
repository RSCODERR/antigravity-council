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

# Council Ask — Multi-Model Consultation

Query multiple AI models simultaneously and synthesize their perspectives into
a unified analysis of consensus, divergence, and recommendation.

## Overview

The council works by fanning out a question to multiple AI models running in
parallel — each answers independently without seeing the others — and then
synthesizing their responses. This surfaces blind spots, confirms strong
consensus, and highlights where models genuinely disagree.

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

## Step 5: Display Results

The workflow returns each model's answer. Display them **verbatim** — do not
reformat, summarize, or abbreviate individual responses. Use this format:

```markdown
---

## 🟢 <Model Display Name>

<model's full response verbatim>

---

## 🔵 <Model Display Name>

<model's full response verbatim>

---
```

Use different colored dots to visually distinguish models:
- 🟢 🔵 🟣 🟠 🔴 🟡

## Step 6: Write the Synthesis

After displaying all responses, write a synthesis under this header:

```markdown
---

## 🧭 Synthesis
```

The synthesis has three sections:

### Consensus
What do the models agree on? List the points of agreement. Agreement is not
verification — note when models share the same assumption rather than
independently confirming a fact.

### Divergence
Where do the models disagree? For each disagreement:
- State what each model said
- Explain *why* they likely diverge (different assumptions, different weighting
  of concerns, different experience domains)
- Note which position has stronger reasoning, if one clearly does

### Recommendation
Based on the full picture:
- State what the evidence supports
- Name the **premise that could change the answer** — the one assumption that,
  if wrong, flips the recommendation
- If the question is context-dependent, say what to check before committing

**Calibration rules for the synthesis:**
- Never invent consensus. If models genuinely disagree, say so.
- Never dismiss a minority view without saying why.
- If all models agree, explicitly note that agreement can mean shared bias, not
  independent confirmation.
- Name the strongest counterargument to your recommendation.

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
