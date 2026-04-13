---
name: ai-opportunity-scanner
description: Identify hidden business opportunities where AI-driven cost reduction makes previously uneconomical tasks viable. Use when analyzing industries, value chains, or business models to find "long-tail" opportunities unlocked by AI. Triggers on requests like "find AI opportunities in X industry", "analyze cost inversion", "discover hidden markets", "what becomes viable with AI", or comparisons across industries.
---

# AI Opportunity Scanner

Identify business opportunities where AI flips the economics of a task — making something previously unprofitable viable by dramatically lowering marginal costs.

## Core Concept

The fundamental pattern this skill hunts for:

> **Before AI**: Fixed cost (expert labor) > project/task value → not viable  
> **After AI**: Marginal cost drops by 10-100x → same task becomes profitable at scale

This applies across project execution, supply chain, compliance, finance, information services, and knowledge work.

## Workflow

### Step 1 — Frame the Industry or Domain

Understand the user's target:
- Specific industry (e.g., energy storage, legal services, agriculture)
- Value chain position (upstream, midstream, downstream)
- Current constraint they observe (e.g., "engineers won't do small projects")

Read [references/framework.md](references/framework.md) for the complete analytical framework before proceeding.

### Step 2 — Scan for Cost Inversion Patterns

Load [references/patterns.md](references/patterns.md) and systematically check which patterns apply to the domain. Map each pattern to concrete actors in the value chain.

### Step 3 — Generate Opportunities

For each identified pattern, generate:

| Field | Description |
|-------|-------------|
| **Task** | What exactly was not viable before |
| **Why it was skipped** | The cost/value mismatch (e.g., engineer time > project margin) |
| **AI enabler** | Which AI capability changes the equation |
| **New economics** | Approximate cost reduction (e.g., 2 days → 5 minutes) |
| **Who benefits** | Specific player in the value chain |
| **Business model** | How to capture value (SaaS, service, product, platform) |
| **Barriers** | Data access, regulation, trust, integration friction |

### Step 4 — Structure and Compare

Use [assets/opportunity-matrix-template.md](assets/opportunity-matrix-template.md) to produce a clean output. When comparing multiple industries, use the same matrix structure for each so patterns can be compared side-by-side.

### Step 5 — Prioritize

Score opportunities by:
1. **Cost reduction magnitude** (10x, 100x?)
2. **Market size of newly viable tasks** (number of previously ignored units)
3. **Defensibility** (can anyone else easily replicate?)
4. **Execution feasibility** (does the user have access to data/customers?)

## Reference Library

- **Framework**: [references/framework.md](references/framework.md) — analytical lenses and workflow
- **Patterns**: [references/patterns.md](references/patterns.md) — 12 reusable AI cost-inversion archetypes
- **Examples**: [references/examples.md](references/examples.md) — worked example from energy storage and other industries
- **Output template**: [assets/opportunity-matrix-template.md](assets/opportunity-matrix-template.md) — standard deliverable format

## Output Contract

Always produce:
1. A concise **executive summary** (3-5 bullets)
2. A filled **opportunity matrix** using the asset template
3. **Cross-industry comparisons** if multiple industries are requested
4. **Next-step recommendations** — which opportunity to prototype first

When the user provides only a vague prompt (e.g., "find AI opportunities"), ask 1-2 clarifying questions:
- Which industry or value chain do you want to analyze?
- Do you have a specific constraint or cost pain point you've already observed?
