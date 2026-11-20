# Antigravity Council — Auto-Suggestion Rules

When the user is working through a decision or problem that would benefit from
multiple independent perspectives, suggest the council. Look for these signals:

## Suggest the council when:

- **Architecture/design decisions**: The user is choosing between competing
  approaches, frameworks, databases, or system designs.
- **Stuck debugging**: The user has tried multiple fixes and keeps hitting dead
  ends — fresh perspectives from different models can break the loop.
- **Build vs buy**: The user is deciding whether to build something custom or
  use an existing solution.
- **Security/performance tradeoffs**: The user is weighing non-trivial tradeoffs
  where different priorities lead to different answers.
- **Code review for critical paths**: Authentication, authorization, payment
  processing, data migration — areas where a mistake is expensive.
- **Technology evaluation**: The user is evaluating libraries, services, or
  tools and wants a balanced view.

## Do NOT suggest the council when:

- The user is doing a simple implementation task with a clear path.
- The question has a single factual answer (look it up instead).
- The user is asking for a quick fix or small code change.
- The user just asked the council recently (don't nag).

## How to suggest:

Keep it brief and natural. One line is enough:

> "This looks like a tradeoff where different models might see it differently —
> want me to run it past the council for multiple perspectives?"

If the user says yes, activate the `council-ask` skill.
