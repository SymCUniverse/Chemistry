# Chemistry Manuscript Workspace

Status: ACTIVE WORKING DRAFT
Governing manual: SymC General Operations Manual v0.8.0
Working branch: `manuscript-rebuild-gom-v0.8.0`

This directory is the canonical living workspace for the rebuilt Chemistry manuscript. It is intentionally not a release, submission package, or claim that the paper is complete. It exists so the manuscript, its evidence state, and its pending computational insertions are tracked in the repository rather than in chat memory or an aging local copy.

## Canonical files

- `CHEMSA_MANUSCRIPT_WORKING_v0.1.md`: current prose draft.
- `CLAIM_LEDGER_v0.1.md`: claim-by-claim evidence and epistemic status.
- `FIGURE_TABLE_PLAN_v0.1.md`: planned figures/tables and the evidence needed to build them.
- `PENDING_RESULT_INSERTS_v0.1.md`: exact manuscript locations that depend on unfinished computations.
- `FUNCTION_LIMIT_MAP_v0.1.md`: Chemistry Function Map and Limit Map obligations.
- `REPRODUCIBILITY_COMPLETION_MATRIX_v0.1.md`: R1/R2/R3 and artifact-closure checklist.

## Editing rule

The working manuscript may contain clearly marked placeholders for unfinished computation, but it must not convert pending evidence into prose that reads as a result. Any result block remains `PENDING_COMPUTATION`, `PENDING_AUDIT`, or `PENDING_LITERATURE` until the corresponding evidence is closed.

Historical manuscripts remain evidence of lineage only. This workspace is the forward manuscript.
