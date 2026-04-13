# AI Opportunity Scanner

A [Kimi Code CLI](https://github.com/MoonshotAI/kimi-cli) skill for discovering hidden business opportunities unlocked by AI-driven cost reduction.

## Core Idea

AI doesn't just make existing tasks faster — it changes which tasks are **economically viable** in the first place.

> **Before AI**: Expert labor cost > value of the task → skipped  
> **After AI**: Marginal cost drops 10-100x → the same task becomes a profitable market

This skill systematically scans any industry for these "cost inversion" opportunities.

## What It Does

When triggered, the skill walks through a structured analysis:

1. **Framework analysis** — applies 6 lenses (information asymmetry, expert bottleneck, data deluge, etc.)
2. **Pattern matching** — checks 12 reusable AI cost-inversion archetypes
3. **Cross-industry comparison** — transferable patterns from energy, legal, agriculture, healthcare, and more
4. **Opportunity matrix** — produces a standardized deliverable with prioritized next steps

## Installation

### Option 1: Copy to your local skills directory
```bash
cp -r ai-opportunity-scanner ~/.codex/skills/
```

### Option 2: Install from GitHub (using skill-installer)
```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <your-username>/<your-repo> \
  --path ai-opportunity-scanner
```

## Usage Examples

Once installed, simply ask Kimi Code CLI:

> *"Analyze the legal services industry for AI cost-inversion opportunities"*

> *"What becomes viable in agriculture now that AI can process images and documents cheaply?"*

> *"Compare储能, healthcare, and construction using the AI opportunity scanner"*

## Skill Structure

```
ai-opportunity-scanner/
├── SKILL.md                              # Core skill instructions
├── agents/openai.yaml                    # UI metadata
├── references/
│   ├── framework.md                      # Analytical lenses & value-chain scanning
│   ├── patterns.md                       # 12 cost-inversion archetypes
│   └── examples.md                       # Worked examples across industries
└── assets/
    └── opportunity-matrix-template.md    # Standardized output template
```

## License

MIT
