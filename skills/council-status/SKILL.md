---
name: council-status
description: >-
  Show which AI models are available for the council and their current quota
  status. Use when the user asks about council status, available models, or
  council setup — council status, what models are available, is the council
  ready, show council seats.
---

# Council Status — Available Models & Quota

Check which AI models are available as council seats and their current status.

## Step 1: Query Available Models

Run the swarm `models` action with `all: true` to get every available model:

```
swarm(action="models", all=true)
```

## Step 2: Display the Status

Format the output as a clear table:

```markdown
## 🏛️ Council Status

| Seat | Model | Vendor | Quota |
|------|-------|--------|-------|
| 1 | <display name> | <vendor> | <remaining%> |
| ... | ... | ... | ... |

**Total seats available: N**
```

### Vendor Detection

Determine vendor from the model ID prefix:
- `claude-*` → Anthropic (Claude)
- `gemini-*` → Google (Gemini)
- `gpt-*` → OpenAI (GPT)
- Other → show the model ID as-is

### Quota Status

Show quota remaining as a percentage with a visual indicator:
- 🟢 75–100% — plenty of quota
- 🟡 25–74% — moderate use
- 🔴 0–24% — running low

## Step 3: Recommendation

After the table, add:

- If 3+ models from 2+ vendors: "✅ **Council ready** — good cross-vendor diversity."
- If 2+ models from 1 vendor: "⚠️ **Limited diversity** — all models are from the same vendor. Answers may share similar biases."
- If only 1 model: "⚠️ **Single model** — the council works best with multiple models for independent perspectives."
- If 0 models: "❌ **No models available** — check your Antigravity subscription or quota."

## Step 4: Usage Hint

End with a brief usage hint:

```
💡 To ask the council a question, say:
   "Ask the council: <your question>"
   "Council review: <topic>"
   "Get the council's take on <decision>"
```
