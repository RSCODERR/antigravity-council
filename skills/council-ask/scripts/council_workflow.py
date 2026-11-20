# Council Workflow — Fan out a question to multiple AI models in parallel
#
# Args:
#   question (str):   The question to ask all models
#   models (list):    List of model IDs to query
#   verbosity (str):  "brief", "standard", or "detailed" (default: "standard")
#   context (str):    Optional code/file context to include
#   debate (bool):    If true, run a second round where models critique each other

question = args.get("question", "")
models = args.get("models", [])
verbosity = args.get("verbosity", "standard")
context = args.get("context", "")
debate = args.get("debate", False)

if not question:
    raise ValueError("No question provided")
if not models:
    raise ValueError("No models provided — pass at least one model ID")

# Build the verbosity instruction
verbosity_instructions = {
    "brief": "Answer in 3-5 sentences using bullets. No code unless specifically asked.",
    "standard": "Give a balanced, thorough answer. Include code examples only when they clarify the point.",
    "detailed": "Provide a thorough analysis with code examples, trade-offs, edge cases, and concrete recommendations.",
}
verbosity_note = verbosity_instructions.get(verbosity, verbosity_instructions["standard"])

# Build the prompt each model will receive
base_prompt = f"""You are one member of a council of AI models. You are answering a question independently — you cannot see what other models say. Give your honest, independent perspective.

## Question

{question}

## Instructions

{verbosity_note}

Focus on being genuinely helpful. If you're uncertain about something, say so rather than guessing. If the question contains assumptions you think are wrong, challenge them.
"""

if context:
    base_prompt += f"""
## Code Context

The following code/files are relevant to this question:

{context}
"""

# ── Round 1: Independent answers ──

phase("Round 1 — Independent Perspectives")
log(f"Querying {len(models)} models in parallel...")

round1_schema = {"type": "string"}

round1_results = await parallel(
    models,
    lambda m: agent(
        prompt=base_prompt,
        schema=round1_schema,
        role=f"Council: {m}",
        model=m,
    ),
)

# Log round 1 results
answers = {}
for i, m in enumerate(models):
    answers[m] = round1_results[i]
    log(f"\n--- {m} answered ({len(round1_results[i])} chars) ---")

# ── Round 2: Debate (optional) ──

if debate and len(models) > 1:
    phase("Round 2 — Debate & Critique")

    # Build a summary of all round-1 answers
    round1_summary = "\n\n".join(
        f"### {m}\n{answers[m]}" for m in models
    )

    debate_prompt = f"""You are participating in a debate among AI models. Here is the original question:

## Question

{question}

## Round 1 Answers from All Models

{round1_summary}

## Your Task

Review the other models' answers critically:
1. What do you agree with?
2. What do you disagree with, and why?
3. What did others miss?
4. Would you change your original answer based on what you've read? If so, how?

Be specific and cite which model you're responding to.
"""

    log(f"Running debate round with {len(models)} models...")

    round2_results = await parallel(
        models,
        lambda m: agent(
            prompt=debate_prompt,
            schema=round1_schema,
            role=f"Debate: {m}",
            model=m,
        ),
    )

    for i, m in enumerate(models):
        answers[f"{m}_debate"] = round2_results[i]
        log(f"\n--- {m} debate response ({len(round2_results[i])} chars) ---")

# ── Output ──

phase("Results")

output_parts = []
color_dots = ["🟢", "🔵", "🟣", "🟠", "🔴", "🟡"]

for i, m in enumerate(models):
    dot = color_dots[i % len(color_dots)]
    output_parts.append(f"---\n\n## {dot} {m}\n\n{answers[m]}")

if debate and len(models) > 1:
    output_parts.append("\n---\n\n# Round 2 — Debate Responses\n")
    for i, m in enumerate(models):
        dot = color_dots[i % len(color_dots)]
        debate_key = f"{m}_debate"
        if debate_key in answers:
            output_parts.append(f"---\n\n## {dot} {m} (Debate)\n\n{answers[debate_key]}")

result = "\n\n".join(output_parts)
log(result)
print(result)
