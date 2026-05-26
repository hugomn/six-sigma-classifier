# Six Sigma Classifier — Failure-Mode Detection (v0.2)

A supervised failure-mode classifier for detecting which **MAST failure mode** a given agent failure belongs to. **This is the second iteration building on the v0.1 baseline.**

## Overview

This classifier takes an agent execution failure and predicts which of the 10 failure modes it represents. Unlike v0.1 (binary success/failure keyword detection), v0.2 is a **multi-class failure-mode classifier** trained on real failure traces only.

**Key constraints:**
- No synthetic data (only 44 real failure traces in corpus)
- Failure-mode scope (not success/failure binary)
- Real agent execution data (Cemri et al. 2025)

## Dataset

**Six Sigma Phase 1 Corpus (Failure Subset):**
- **Traces:** 44 distinct real agent execution failures
- **Failure modes:** 10 MAST modes (1.1, 1.3, 1.5, 2.2, 2.3, 2.4, 2.6, 3.1, 3.2, 3.3)
- **Source:** Cemri et al. 2025 (arxiv 2503.13657)
- **Agents:** 6 (AG2, AppWorld, ChatDev, Magentic, MetaGPT, OpenManus)
- **LLMs:** 2 (GPT-4o, Gemini)
- **Benchmarks:** 6 (GAIA, GSM, MMLU, Olympiad, ProgramDev, Test-C)

**Mode distribution:**
- Mode 1.1: 7 traces
- Mode 1.3: 7 traces
- Mode 2.6: 7 traces
- Mode 2.2: 6 traces
- Mode 3.2: 6 traces
- Mode 1.5: 3 traces
- Mode 3.1: 3 traces
- Mode 2.3: 2 traces
- Mode 3.3: 2 traces
- Mode 2.4: 1 trace

## Baseline Results (v0.2)

**In-sample performance on 44 failure traces:**
- **Model:** SimpleClassifier (agent + benchmark majority vote)
- **Overall Accuracy:** 36.36% (16/44 correct)

**Per-mode performance (on failures only):**
- Mode 1.1: Precision 50%, Recall 57% (3/7 correct)
- Mode 1.3: Precision 20%, Recall 57% (4/7 correct)
- Mode 2.6: Precision 100%, Recall 29% (2/7 correct)
- Mode 3.2: Precision 40%, Recall 67% (4/6 correct)
- Mode 3.3: Precision 50%, Recall 100% (2/2 correct)
- Others: Precision 0% (rare classes, single samples)

**Interpretation:**
Baseline accuracy is low (36%) because failure-mode distribution is imbalanced (rare modes like 2.4, 2.3 are single samples) and purely agent/benchmark features are insufficient. Modes with multiple traces show better recall (1.1, 1.3, 3.2, 3.3); rare modes are underfitted.

**Next steps (v0.3):**
- Feature engineering from execution traces (error density, trajectory length, step types)
- Handling class imbalance (oversampling rare modes, stratified k-fold)
- Supervised ML with held-out validation set
- Comparison against v0.1 keyword-based approach

## Method

**Classifier:** SimpleClassifier (pure Python, no dependencies)
- Extracts (agent, benchmark) pairs
- Predicts most common failure mode for each pair
- Baseline for comparison with supervised learning

**Implementation:**
- `classifier_v0.2.py`: Train and evaluate classifier
- `evaluation_results_v0.2.json`: Metrics and per-mode stats

## Usage

```bash
python3 classifier_v0.2.py
```

Outputs:
1. Console: accuracy, per-mode precision/recall
2. File: `evaluation_results_v0.2.json` with full results

## Reproducibility

**Corpus:** `corpus.json` (44 real failure traces, committed)
- Deduplicated from original 63 traces (verified May 26 2026)
- Authors: Cemri et al. 2025, arxiv 2503.13657
- License: Public dataset
- Provenance: Verified real execution traces, no synthetic data

**Code:** Pure Python 3.8+, no external dependencies (sklearn, pandas, etc.)

## Design Rationale

v0.2 pivots from binary success/failure classification to **failure-mode multi-class** because:

1. **No real successes available:** MAST corpus contains only failures; synthetic success cases would violate data integrity
2. **Failure-mode value:** Predicting which failure mode reveals **why** agents failed (more actionable than binary detection)
3. **Timeline:** Single-model scope (44 failures) ships faster than corpus expansion for balanced train/test
4. **Precondition:** Failure-mode labels (`primary_mast_mode`) already present in corpus, no new labeling required

## Built By

Hopper · Builder + Engineer · Slowlit Labs
