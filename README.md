# Six Sigma Classifier — Baseline Agent Failure Detector (v0.1)

A keyword-based baseline for detecting agent execution failures. **This is an in-sample baseline floor, not a held-out performance metric.** It establishes a labeling standard for the Six Sigma Phase 1 corpus.

## Overview

This classifier detects agent failures by analyzing execution traces for failure keywords. It is fit and evaluated on the **same 44-trace corpus** (in-sample) and should not be interpreted as a generalization metric.

This is the first artifact in the **Six Sigma reliability agent** project.

## Dataset

**Six Sigma Phase 1 Corpus (verified deduped):**
- **Traces:** 44 distinct real agent execution traces
- **Source:** Cemri et al. 2025 (arxiv 2503.13657)
- **Agents:** 6 (AG2, AppWorld, ChatDev, Magentic, MetaGPT, OpenManus)
- **LLMs:** 2 (GPT-4o, Gemini)
- **Benchmarks:** 6 (GAIA, GSM, MMLU, Olympiad, ProgramDev, Test-C)
- **File:** `corpus.json` (committed, reproducible)

## In-Sample Baseline Results

**Disclaimer:** Classifier is fit AND evaluated on the same 44-trace corpus. These metrics are **labeling floor baselines**, not generalization estimates. Held-out test split required for real performance claims.

**Keyword-Detected Failure Breakdown:**
- Success cases: 12
- Failure cases: 32
- Overall failure rate: 72.73%

**Per-Agent Failure Rates (detected keywords):**
- AG2: 15/18 (83.33%)
- AppWorld: 1/1 (100.00%)
- ChatDev: 3/5 (60.00%)
- Magentic: 5/7 (71.43%)
- MetaGPT: 7/10 (70.00%)
- OpenManus: 1/1 (100.00%)

## Method

Keyword detection on execution trajectories. Detected keywords:
- error, failed, exception, traceback, warning, crashed, fault, invalid, unable, could not, cannot, denied, rejected, timeout

## Usage

```bash
python3 classifier.py
```

This will:
1. Load `corpus.json` (included)
2. Label traces by keyword detection
3. Generate `evaluation_results.json` with labeling counts

## Next Steps (v0.2)

For real performance estimates:
- Hold-out test split (train/test, cross-validation)
- Supervised classifier (decision tree / logistic regression)
- Feature engineering (trajectory length, keyword density, agent/llm/benchmark metadata)
- Comparison against baseline

## Data Source & Reproducibility

**Corpus File:** `corpus.json` (committed to this repo)
- Authors: Cemri et al. 2025
- Paper: arxiv.org/pdf/2503.13657
- License: Public dataset
- MD5 / provenance: [verified via mechanical dedup May 26 2026]

## Implementation

**File:** `classifier.py`  
**Dependencies:** Python 3.8+, standard library only  
**Size:** ~10KB

## Built By

Hopper · Builder + Engineer · Slowlit Labs
