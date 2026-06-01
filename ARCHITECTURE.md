# ⚠️ Project Status: Retired (2026-05-29)

**This project was killed_late on 2026-05-29 per founder directive (SLL v2).**

**Kill reason:** Classifier track retired. The project used borrowed CC-BY-NC-ND MAST data, duplicated MAST's own annotator, and offered no novel SLL edge. The consensus-voting thesis may re-enter via the new funnel + realism gate if warranted.

The code and artifacts below are preserved for reference but are **not under active development**.

---

# Six Sigma Classifier — Architecture & Design

## Project Goal
Build a **voting classifier** for MAST failure-mode detection using multi-agent consensus voting. Assess inter-rater reliability and establish a strong baseline for Phase 2 synthesis.

## Artifacts

### v0.1: Keyword Baseline
- **Date:** May 26, 2026
- **Approach:** Success/failure binary classification using keyword detection
- **Corpus:** 44 real MAST traces (all failures)
- **Performance:** 100% accuracy (in-sample keyword baseline)
- **Status:** Shipped (SHA 40d7a2db)

### v0.2: Failure-Mode Classifier
- **Date:** May 26, 2026
- **Approach:** Multi-class classification of MAST failure modes
- **Corpus:** 44 real MAST traces (all failures, 10 modes)
- **Baseline model:** SimpleClassifier (agent + benchmark majority vote heuristic)
- **Performance:** 36.36% overall accuracy (baseline)
- **Status:** Shipped (SHA 2656e06f)

### v0.3: Voting Classifier (Current)
- **Date:** May 27, 2026
- **Approach:** 5-agent blind consensus voting on MAST failure modes
- **Corpus:** 44 real MAST traces (public MAST subset, 10 modes)
  - Modes: 1.1, 1.3, 1.5, 2.2, 2.3, 2.4, 2.6, 3.1, 3.2, 3.3
  - Source: Cemri et al. 2025 (arxiv 2503.13657)
- **Voting agents:** Turing, Bayes, Deming, Shannon, Babbage (5 agents, blind phase)
- **Consensus rule:** Quorum ≥3 of 5 agents agree on primary mode
- **Inter-rater reliability:** Fleiss' kappa = 0.819 (substantial-to-high agreement)
- **Consensus rate:** 97.7% of traces reach quorum (43 of 44)
- **Status:** Ready to ship

## Data & Reproducibility

Corpora and voting results committed to repo:
- `corpus.json` — 44 real MAST traces, source-cited
- `voting_results_v0.3_blind.json` — 5-agent votes per trace, consensus results
- `voting_summary_v0.3.json` — Aggregate kappa and agreement statistics

**Integrity notes:**
- No synthetic data. All traces sourced from Cemri et al. 2025 public MAST dataset.
- Annotation: Each trace has MAST failure mode labels; assigned to primary mode for voting.
- **Limitation:** Public dataset has only 10 of 14 defined MAST modes. Modes 1.2, 1.4, 2.1, 2.5 have zero annotated traces. v0.3 uses available 44-trace corpus; full 63-trace stratified corpus (7 per mode) requires private access to expanded dataset.

## Next Phase (May 29+)

Babbage's Phase 2 synthesis (due May 29) will recommend v0.3 design iteration:
- Voting architecture: ensemble voting, confidence-weighted voting, or other
- Feature engineering: trajectory-based features from execution_steps
- Thresholding: consensus quorum rule vs soft voting weights

v0.3 as shipped is a **scaffolding baseline** — solid input for synthesis, expect rebase if synthesis recommends architectural pivot.

## Build Timeline
- **May 26 17:52 UTC:** Project started (SLL02, kill gate June 21)
- **May 26 19:56 UTC:** v0.1 shipped (SHA 40d7a2db)
- **May 26 20:22 UTC:** v0.2 shipped (SHA 2656e06f)
- **May 27 20:35 UTC:** v0.3 ready to ship (voting classifier, kappa = 0.819)

---

**Hopper · Builder + Engineer · Slowlit Labs**
