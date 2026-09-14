# Living Chemistry Manuscript Workspace

**Status:** WORKING / NOT A RELEASE / NOT SUBMISSION-READY  
**Program governance:** SymC General Operations Manual v0.8.0  
**Purpose:** Keep the evolving Chemistry manuscript in the repository so scientific text, evidence status, and code/provenance can be updated together.

## Canonical working manuscript

`CHEMSA_LIVING_MAIN.tex` is the canonical editable manuscript entry point for ongoing Chemistry work on this branch.

The initial seed is the user-supplied current LaTeX source `ChemSA_Combined_Main (9).tex`. The seed is being modularized into `sections/` without silently changing its scientific wording. New research material is added only when its epistemic state is explicit.

This directory is **not** a release product. A commit here means "working scientific text preserved in the repo," not "claim approved for publication."

## Editing rules

1. Historical submitted/released PDFs and frozen evidence are not overwritten by this workspace.
2. Every material claim added from an active investigation must be traceable to an adjudicated repo record or clearly labeled as planned/provisional.
3. A numerical PASS remains distinct from untouched confirmation.
4. Historical HOLDs and negative results remain visible where they are relevant to the argument.
5. Manuscript prose cannot rescue a failed gate or promote an unresolved coordinate.
6. H/Ru(0001) System 3 remains P0-Q. Its fresh L17/V15/K24 fixed-grid gate has passed, but downstream inheritance is held pending the prospectively frozen L21 robustness challenge and then the clean-surface relaxation/reproduction gate.
7. Barrier Height/Rate Atlas v0.9 remains frozen and retrospective; future extensions must be separately versioned.
8. Dissipation/friction and quantum-nuclear claims remain bounded by their project-local readiness records.

## Directory roles

- `CHEMSA_LIVING_MAIN.tex` — canonical working entry point.
- `sections/` — editable manuscript sections.
- `notes/` — evidence-to-prose notes not yet promoted into the main narrative.
- `MANUSCRIPT_STATUS.json` — machine-readable manuscript/evidence status.
- `EDIT_LOG.md` — short record of material manuscript changes and why they were made.

## Promotion rule

A working manuscript snapshot becomes a submission/release candidate only through an explicit versioned freeze with clean-room compilation/validation, evidence synchronization, and user approval. Until then this workspace is deliberately mutable.
