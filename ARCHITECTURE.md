# Architecture — Six Sigma Baseline Classifier

## Class Design

### `AgentFailureClassifier`

**Purpose:** Detect agent execution failures from traces.

**Key Methods:**
- `fit(traces)` — Learn failure patterns from corpus
- `predict(traces)` — Predict failure/success on new traces
- `evaluate(traces)` — Calculate accuracy, precision, recall, F1

**Features:**
- Failure keyword detection (14 keywords)
- Per-agent, per-LLM, per-benchmark aggregation
- Confusion matrix calculation
- JSON result serialization

## Data Flow

```
corpus.json (63 traces)
    ↓
AgentFailureClassifier.fit()
    ↓
Per-agent failure rates calculated
    ↓
predict() on same corpus
    ↓
evaluate() produces metrics
    ↓
evaluation_results.json
```

## Failure Detection Heuristic

A trace is classified as **failure** if the trajectory contains any of:
```
error, failed, exception, traceback, warning, crashed, fault,
invalid, unable, could not, cannot, denied, rejected, timeout
```

This is a **baseline** heuristic. Future versions will use supervised learning.

## Ground Truth Labels

Labels are *derived* from trajectories (not provided separately). This baseline uses keyword presence as a proxy for failure. A supervised classifier would need explicit annotations on a subset of the corpus.

## Next Version (v0.2)

The next iteration will:
1. Add train/test split (80/20 or cross-validation)
2. Implement decision tree classifier
3. Add feature engineering (trajectory length, keyword density, metadata)
4. Compare baseline keyword detection vs. supervised learning

This will establish a performance ceiling and identify which features matter most.
