# HCN/HNC Rowan post-freeze traceability archive

This directory preserves externally inspectable identifiers and selected numerical outputs for the HCN<->HNC modal workflow used in CSA R9.1.

The manuscript correctly describes the calculation as **internally frozen**. This archive was created later and therefore does **not** retroactively convert that status into a prospectively public freeze. Its purpose is narrower: a reviewer can verify that the cited Rowan workflows exist, completed successfully, and reproduce the endpoint/transition-state quantities reported in Supplement S18.

The JSON snapshot records:
- HCN and HNC optimized endpoint coordinates, energies, and harmonic frequencies;
- the optimized transition-state coordinates, energy, and one-imaginary-mode spectrum;
- the independent fixed-geometry transition-state frequency validation;
- bidirectional IRC and endpoint-optimization workflow identifiers.

No damping/lifetime quantity is introduced here. Lowercase chi remains unavailable for this HCN/HNC record.

Source workflow UUIDs are immutable Rowan identifiers and are reported verbatim.
