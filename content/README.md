# Content

File-based content. Synced into Postgres mirror tables on app startup
(`services/content_loader.py`).

## Layout

```
content/
├── topics/                Markdown topic files, one per topic
│   ├── core_paper_1/
│   │   └── {slug}.md
│   └── core_paper_2/
│       └── {slug}.md
├── quizzes/               YAML quiz files, one per topic
│   ├── core_paper_1/
│   │   └── {slug}-quiz.yaml
│   └── core_paper_2/
│       └── {slug}-quiz.yaml
├── command_verbs/         Markdown verb-by-verb guides
│   └── {verb}.md
├── command_verb_prompts.yaml   Practice prompts for the verbs
├── misconceptions.yaml          Library used by ExplainIT
└── specification.yaml           POs, AOs (source of truth)
```

## Adding a topic (NFR-12, NFR-14)

1. Create `content/topics/core_paper_{1|2}/{slug}.md` with frontmatter:

```yaml
---
title: Requirements Analysis
core_paper: 1
topic_number: 2
performance_outcomes: [PO1, PO3]
estimated_minutes: 25
explainit_enabled: true
last_updated: 2026-09-01
---
```

2. Create the matching `content/quizzes/core_paper_{1|2}/{slug}-quiz.yaml`.
3. Run the validation script (TBD: `scripts/validate_content.py`).
4. Restart the app or run `scripts/sync_content.py`.

## Adding a command verb (NFR-15)

1. Create `content/command_verbs/{verb}.md` with frontmatter (tier, definition,
   AO expectations).
2. Add practice prompts under the verb's key in `command_verb_prompts.yaml`.
