# Council Workflow — Multi-Role & Multi-Model Parallel Deliberation
# with Anonymous Peer Review & Unified Chairman Synthesis
#
# Args:
#   question (str):        The user's question or code review task
#   models (list):         List of model IDs/tiers ('pro', 'flash', 'flash_lite', 'inherit')
#   roles (list|str):      Role keys (e.g. ['security', 'devil', 'performance']) or preset name ('balanced', 'architecture')
#   verbosity (str):       'brief', 'standard', or 'detailed' (default: 'standard')
#   context (str):         Code/file context to evaluate
#   debate (bool):         If true, runs an anonymous peer review debate round
#   show_individual (bool): If true, renders raw individual transcripts before the unified verdict

import json

question = args.get("question", "")
raw_models = args.get("models", [])
raw_roles = args.get("roles", [])
verbosity = args.get("verbosity", "standard")
context = args.get("context", "")
debate = args.get("debate", True)  # Default true for rigorous peer-review
show_individual = args.get("show_individual", False)

if not question:
    raise ValueError("No question provided to Council")

# Built-in role definitions & presets (identical to claude-council config/roles.json)
ROLE_DEFINITIONS = {
    "security": {
        "name": "Security Auditor",
        "instruction": "Evaluate strictly through a security lens: attack surfaces, authentication/authorization loopholes, cryptographic hygiene, injection risks, data leaks, and compliance exposure."
    },
    "devil": {
        "name": "Devil's Advocate",
        "instruction": "Actively challenge assumptions and consensus. Uncover hidden failure modes, edge cases, silent regressions, operational landmines, and points where this approach will catastrophically fail."
    },
    "performance": {
        "name": "Performance & Scalability Architect",
        "instruction": "Focus on high concurrency, compute and memory complexity, I/O bottlenecks, database locking, throughput limits, caching tiers, and horizontal scaling ceilings."
    },
    "simplicity": {
        "name": "Pragmatist & Simplicity Champion",
        "instruction": "Advocate for radical simplicity and operational reality. Scrutinize over-engineering, unneeded abstractions, developer maintenance overhead, and total cost of ownership. Prefer simple, boring tools."
    },
    "maintainability": {
        "name": "Maintainability & Clean Architecture Advocate",
        "instruction": "Scrutinize modularity, decoupling, testability, readability, technical debt accumulation, and ease of future refactoring."
    },
    "dx": {
        "name": "Developer Experience Champion",
        "instruction": "Evaluate day-to-day workflow friction, API ergonomics, ease of debugging, local dev setup speed, documentation clarity, and developer happiness."
    }
}

ROLE_PRESETS = {
    "balanced": ["security", "performance", "simplicity"],
    "architecture": ["performance", "maintainability", "simplicity"],
    "security-focused": ["security", "devil", "maintainability"],
    "code-review": ["security", "maintainability", "simplicity"],
    "adversarial": ["devil", "security", "simplicity"]
}

# Resolve roles
assigned_roles = []
if isinstance(raw_roles, str) and raw_roles in ROLE_PRESETS:
    assigned_roles = ROLE_PRESETS[raw_roles]
elif isinstance(raw_roles, list) and len(raw_roles) > 0:
    for r in raw_roles:
        if r in ROLE_PRESETS:
            assigned_roles.extend(ROLE_PRESETS[r])
        elif r in ROLE_DEFINITIONS:
            assigned_roles.append(r)
        else:
            assigned_roles.append("simplicity")
else:
    # Default balanced preset
    assigned_roles = ["security", "performance", "simplicity"]

# Resolve models
VALID_MODELS = {"pro", "flash", "flash_lite", "inherit"}
def map_model(m):
    if m in VALID_MODELS:
        return m
    ml = str(m).lower()
    if "pro" in ml or "opus" in ml:
        return "pro"
    if "flash-lite" in ml or "flash_lite" in ml or "low" in ml:
        return "flash_lite"
    if "flash" in ml:
        return "flash"
    return "inherit"

if not raw_models:
    model_pool = ["pro", "flash", "inherit"]
else:
    model_pool = [map_model(m) for m in raw_models]

# Pair roles with models to create distinct Council Seats
seats = []
for i, role_key in enumerate(assigned_roles):
    model_choice = model_pool[i % len(model_pool)]
    role_info = ROLE_DEFINITIONS.get(role_key, ROLE_DEFINITIONS["simplicity"])
    seats.append({
        "id": f"seat_{i+1}",
        "role_key": role_key,
        "role_name": role_info["name"],
        "role_instruction": role_info["instruction"],
        "model": model_choice
    })

# Verbosity instruction
verbosity_instructions = {
    "brief": "Be sharp, concise, and direct in 3-5 bulleted points. Provide code only if strictly essential.",
    "standard": "Provide a thorough and balanced technical evaluation. Include minimal illustrative code if clarifying.",
    "detailed": "Provide deep technical analysis, failure modes, code examples, trade-offs, and concrete mitigation steps."
}
verbosity_note = verbosity_instructions.get(verbosity, verbosity_instructions["standard"])

# ── Stage 1: Independent Deliberation (Blind Lenses) ──

phase("Stage 1 — Independent Council Deliberation (Role-Divided)")
log(f"Dispatching to {len(seats)} specialized Council seats in parallel...")

def make_stage1_prompt(seat):
    prompt = f"""You are sitting on an expert AI Council as the: **{seat['role_name']}**.

## Your Primary Analytical Lens & Duty:
{seat['role_instruction']}

You are evaluating this task independently. You cannot see what other council members say. Evaluate with uncompromising technical rigor from your assigned perspective.

## Question / Problem Statement:
{question}

## Instructions:
{verbosity_note}

Do not be overly agreeable. If you spot flaws, false assumptions, architectural friction, or risks that standard reviewers miss, call them out directly.
"""
    if context:
        prompt += f"\n## Code / File Context:\n{context}\n"
    return prompt

stage1_results = await parallel(
    seats,
    lambda s: agent(
        prompt=make_stage1_prompt(s),
        schema={"type": "string"},
        role=f"{s['role_name']} ({s['model']})",
        model=s['model']
    )
)

seat_answers = {}
for i, s in enumerate(seats):
    seat_answers[s["id"]] = {
        "seat": s,
        "answer": stage1_results[i]
    }
    log(f"✓ {s['role_name']} [{s['model']}] submitted perspective ({len(stage1_results[i])} chars)")

# ── Stage 2: Anonymous Cross-Examination (Peer Review) ──

if debate and len(seats) > 1:
    phase("Stage 2 — Anonymous Peer Review & Cross-Examination")
    log("Cross-examining perspectives to eliminate groupthink and expose blind spots...")

    # Format blind anonymized perspectives (Perspective A, Perspective B, etc.)
    blind_summary = []
    seat_letter_map = {}
    letters = ["A", "B", "C", "D", "E", "F", "G"]
    for i, s in enumerate(seats):
        letter = letters[i % len(letters)]
        seat_letter_map[s["id"]] = letter
        blind_summary.append(f"### Perspective {letter} (Focus: {s['role_name']}):\n{seat_answers[s['id']]['answer']}")

    blind_text = "\n\n".join(blind_summary)

    def make_debate_prompt(seat):
        my_letter = seat_letter_map[seat["id"]]
        return f"""You are the **{seat['role_name']}** on the AI Council.
Your initial analysis was Perspective {my_letter}.

Here are all anonymized perspectives submitted by the council:
{blind_text}

## Your Peer Review Task:
Critique the other perspectives through your specialized lens ({seat['role_name']}):
1. What did the other perspectives get right?
2. What dangerous assumptions, missing trade-offs, or flaws did others overlook?
3. Where does your original position stand reinforced or refined?

Be incisive, objective, and reference other perspectives by letter (e.g. 'Perspective A', 'Perspective B').
"""

    stage2_results = await parallel(
        seats,
        lambda s: agent(
            prompt=make_debate_prompt(s),
            schema={"type": "string"},
            role=f"Reviewer: {s['role_name']}",
            model=s['model']
        )
    )

    for i, s in enumerate(seats):
        seat_answers[s["id"]]["critique"] = stage2_results[i]
        log(f"✓ {s['role_name']} completed peer review ({len(stage2_results[i])} chars)")

# ── Stage 3: Unified Review & Chairman Synthesis ──

phase("Stage 3 — Chairman Synthesis (Unified Review)")
log("Council Chairman synthesizing all specialized roles and reviews into one definitive verdict...")

deliberation_dossier = []
for s in seats:
    ans_data = seat_answers[s["id"]]
    entry = f"### Lens: {s['role_name']} (Model: {s['model']})\n{ans_data['answer']}"
    if "critique" in ans_data:
        entry += f"\n\n#### Peer Critique from {s['role_name']}:\n{ans_data['critique']}"
    deliberation_dossier.append(entry)

full_dossier_text = "\n\n---\n\n".join(deliberation_dossier)

chairman_prompt = f"""You are the Chairman of the AI Council. Multiple specialized agents ({', '.join([s['role_name'] for s in seats])}) have evaluated the user's inquiry from their individual lenses, followed by cross-examination.

Your task is to deliver **ONE SINGLE, UNIFIED, HIGHLY ACTIONABLE VERDICT**. 

Do not force the user to synthesize 3-5 disparate opinions. You must reconcile conflicts, discard weak arguments, elevate critical caveats, and present a definitive master recommendation.

## Original User Request:
{question}

## Council Transcripts & Peer Reviews:
{full_dossier_text}

## Required Output Structure:

# 🏛️ Council Verdict & Unified Review

### 1. Executive Summary & Definitive Verdict
A crisp, unambiguous answer upfront. No hedging. What should the developer do?

### 2. Synthesized Architecture & Technical Blueprint
Synthesize the best technical points across all lenses into one cohesive solution. Include architecture details, concrete code, or structural patterns where applicable.

### 3. Role-Divided Insights & Tensions Reconciled
Break down how the key concerns were reconciled:
- **Security & Vulnerability Angle**: Insights from the Security lens.
- **Reliability & Devil's Advocate Warnings**: Hidden traps, worst-case scenarios, and failure modes identified.
- **Performance & Operational Simplicity**: The sweet spot between scale overhead and developer velocity.

### 4. Critical Trade-offs & Unresolved Edge Cases
Explicitly state what you are sacrificing with this recommendation and what conditions would flip the decision.

### 5. Tactical Action Plan (Monday Morning Steps)
Numbered, concrete, prioritized steps to implement immediately.
"""

unified_verdict = await agent(
    prompt=chairman_prompt,
    schema={"type": "string"},
    role="Council Chairman",
    model="pro"
)

# ── Deliver Final Result ──

phase("Results")

final_output = []
if show_individual:
    final_output.append("# 🏛️ Individual Council Seat Transcripts\n")
    for s in seats:
        ans_data = seat_answers[s["id"]]
        final_output.append(f"---\n\n## 🔹 {s['role_name']} ({s['model']})\n\n{ans_data['answer']}")
        if "critique" in ans_data:
            final_output.append(f"\n*Peer Critique:* \n{ans_data['critique']}\n")
    final_output.append("\n---\n\n")

final_output.append(unified_verdict)
result = "\n\n".join(final_output)
print(result)
