# Prompts

LLM system prompts. Version-controlled per NFR-16. Each file is loaded by
`services/llm_client.py` when the corresponding feature runs.

| File | Used by |
| --- | --- |
| `extended_response_feedback.txt` | Practice mode, Past-Question-Style Practice, Core Paper extended responses |
| `explainit_persona.txt` | ExplainIT (every turn) |
| `explainit_probing_strategy.txt` | ExplainIT (every turn, alongside persona) |
| `short_answer_grading.txt` | Topic-quiz short-answer grading |

When iterating on a prompt:
1. Edit the file.
2. Run the prompt-eval suite against representative responses (TBD).
3. Spot-check at least 20 sample outputs before deploying.
4. Commit with a message that describes the behaviour change observed.
