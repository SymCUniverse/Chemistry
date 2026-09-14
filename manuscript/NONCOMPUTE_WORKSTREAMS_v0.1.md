# Chemistry Non-Computational Workstreams

Version: 0.1
Status: ACTIVE
Purpose: keep productive work moving while long-running computations are active.

## Workstreams that can proceed without waiting on current computations

1. **Living manuscript maintenance**
   - Continue drafting Introduction, conceptual architecture, Methods, limitations, experimental opportunities, reproducibility language, and non-claim boundaries.
   - Keep result-dependent prose behind explicit `PENDING_*` gates.

2. **GOM v0.8.0 migration integrity**
   - Preserve project-specific Chemistry safeguards locally.
   - Reconcile authority naming from historical GP language to active GOM language without altering frozen science.
   - Do not merge governance changes into an execution-bearing branch while an active run could be affected.

3. **System 1 evidence reconciliation**
   - Identify the canonical first-system lineage.
   - Compare historical prose against current evidence.
   - Preserve HOLDs, failed assumptions, and refusals.
   - Produce manuscript-ready result structure without inventing missing numbers.

4. **Barrier Height / Rate Atlas provenance closure**
   - Audit same-system/phase/temperature/medium/reaction-event matching.
   - Complete source-family lineage tagging.
   - Separate FULL, ABSTRACT, SNIPPET, and BLOCKED evidence.
   - Record refusals explicitly.
   - Build the final Atlas table schema and provenance summary.

5. **Native comparator program**
   - Define, for each prospective predictive claim, the strongest scientifically appropriate comparator.
   - Freeze the task and evaluation metric before the combined outcome is examined.
   - Prepare `FAILS / EQUIVALENT / ADDS` result language.

6. **Function Map / Limit Map completion**
   - Map every existing system and estimator to supported and unsupported regimes.
   - Freeze scalar-refusal rules and memory/Markov boundaries before final results are inserted.

7. **Estimator-equivalence audit**
   - Build a table of every damping/friction/linewidth/relaxation estimator used or proposed.
   - For each pair, record whether equivalence is derived, calibrated, approximate, or refused.
   - Audit amplitude-vs-energy decay, FWHM/HWHM, angular/ordinary frequency, and dephasing contributions.

8. **Experimental-opportunity program**
   - Turn candidate experiments into falsifiable protocols before literature searching them.
   - Then perform literature collision searches to identify what has already been done.
   - Rank surviving experiments by discrimination power, feasibility, cost, and dependence on specialized equipment.

9. **Figure and table architecture**
   - Draft method-only schematics now.
   - Keep empirical plots blocked until terminal evidence is available.
   - Do not reuse legacy figures whose labels encode outdated claims.

10. **Reproducibility release planning**
    - Prebuild R1/R2/R3 checklists, manifest structure, environment capture, checksum plan, and clean-room procedure.
    - Separate software-integrity tests from scientific tests in the reported counts.

11. **Claim ledger and epistemic control**
    - Keep all prospective conclusions in the claim ledger.
    - Promote only after the exact evidence gate closes.
    - Record negative results and failed hypotheses as evidence rather than deleting them from the narrative.

12. **Cross-system comparison freeze**
    - Define what counts as inheritance at modal, scalar, and conglomerate levels before combining terminal system outcomes.
    - Define uncertainty, missingness, discordance, and refusal handling in advance.

## Workstreams blocked by current computations

- final CO/Cu numerical result prose;
- final H/Ru(0001) L21 result prose;
- any cross-system quantitative inheritance claim using those unfinished outputs;
- final abstract numerical claims;
- final conclusion about cross-system transfer;
- final native-comparator outcome if it depends on the unfinished system outputs;
- final R2 classification for those active computational results.

## Operating rule

When one of the blocked items becomes available, update the relevant `PENDING_RESULT_INSERTS` entry first, then the claim ledger, then the manuscript. This prevents a fresh result from jumping directly into narrative prose without its audit trail.
