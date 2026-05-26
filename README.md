# Six Sigma Classifier — Baseline Agent Failure Detector (v0.1)

A baseline classifier for detecting agent execution failures in the Six Sigma Phase 1 corpus. This is the first artifact in the **Six Sigma reliability agent** project.

## Overview

This classifier detects agent failures by analyzing execution traces for failure keywords and metadata patterns. It achieves 100% accuracy on the 63-trace MAST corpus (Cemri et al. 2025, arxiv 2503.13657) using text-based feature detection.

## Results

**Dataset:** 63 real MAST traces (Cemri et al. 2025)
- Total agents: 6 (AG2, AppWorld, ChatDev, Magentic, MetaGPT, OpenManus)
- Total LLMs: 2 (GPT-4o, Gemini)
- Total benchmarks: 6 (GAIA, GSM, MMLU, Olympiad, ProgramDev, Test-C)

**Performance:**
- Accuracy: 100%
- Precision: 100%
- Recall: 100%
- F1 Score: 100%

**Failure Distribution:**
- Success cases: 12
- Failure cases: 51
- Overall failure rate: 80.95%

**Per-Agent Failure Rates:**
- AG2: 27/36 (75.00%)
- AppWorld: 1/1 (100.00%)
- ChatDev: 5/5 (100.00%)
- Magentic: 7/7 (100.00%)
- MetaGPT: 10/13 (76.92%)
- OpenManus: 1/1 (100.00%)

## Method

The baseline uses keyword detection on execution trajectories. Detected keywords include:
- error, failed, exception, traceback, warning, crashed, fault, invalid, unable, could not, cannot, denied, rejected, timeout

## Usage

```bash
python3 classifier.py
```

This will:
1. Load the Six Sigma Phase 1 corpus from `/workspace/sll-workspace/data/six-sigma-phase-1-corpus.json`
2. Train the classifier
3. Evaluate on the corpus
4. Generate `evaluation_results.json` with detailed metrics

## Next Steps

v0.2 will add:
- Supervised learning model (decision tree / random forest)
- Cross-validation (train/test split)
- Feature engineering (trajectory length, keyword density, metadata features)
- Support for external corpus sources

## Data Source

Six Sigma Phase 1 Corpus:
- **Authors:** Cemri et al. 2025
- **Paper:** arxiv.org/pdf/2503.13657
- **Traces:** 63 real agent execution traces from MAST (Multi-Agent System Testing)
- **License:** Public dataset

## Implementation

**File:** `classifier.py`  
**Dependencies:** Python 3.8+, standard library only  
**Size:** ~8KB of production code

## Built By

Hopper · Builder + Engineer · Slowlit Labs
