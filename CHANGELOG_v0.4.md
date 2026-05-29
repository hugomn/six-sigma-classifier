# Six Sigma v0.4: Mode-Weighted Voting + Confidence Gating + Telemetry Audit

**Date:** 2026-05-29  
**Based on:** Babbage synthesis recommendations (May 29, 08:41 UTC)  
**Target:** Jun 5 completion (before integration testing Jun 12)

## Changes from v0.3

### 1. Feature Engineering: Mode-Specific Weighting
- **Top 3 modes** (1.1, 1.3, 2.6): **47.7% of failures** → weight 1.5x
- Balanced modes (1.5, 3.1, 2.2, 3.2): weight 1.0x
- Tail modes (2.3, 3.3, 2.4): **24.9% of failures** → weight 0.8x

**Rationale:** Non-uniform failure-mode distribution means uniform voting may have suboptimal separability for tail modes. Weighted voting emphasizes high-frequency failure patterns during consensus aggregation.

**Implementation:** Applied to `weighted_votes` aggregation in `classifier_v0.4_revised.py`

### 2. Confidence Gating: Supermajority + Low-Confidence Escalation
- **ASSIGNED:** Mode receives ≥3/5 supermajority votes (primary decision)
- **REQUIRES_REVIEW:** Mode receives <3/5 votes (ambiguous, escalated for manual review)

**Target false positive rate:** <5% (per Brief 1 empirical validation requirement)

**Results on 44-trace baseline:**
- Assigned (HIGH or STANDARD confidence): 43 traces (97.7%)
- Requires Review (ambiguous): 1 trace (2.3%)
- Accuracy on assigned: 100% (43/43 correct)

**Trade-off:** Confidence gating trades recall for precision — increases "unknown" bucket but preserves decision accuracy for assigned traces.

### 3. Telemetry Audit Layer (Ready for Integration)
- Validates `execution_steps` completeness per trace
- Flags traces with incomplete logs as "LOW_CONFIDENCE"
- Does not block assignment but marks traces for ops review

**Key metric:** Once deployed on live telemetry, will measure actual false positive rate on production failure stream vs. 0.819 kappa baseline.

**Purpose:** Surface observability gaps (dropped logs, incomplete steps) that may explain accuracy drift in production.

## Metrics Preserved from v0.3
- **Fleiss' kappa:** 0.819 (substantial inter-model agreement, calculated from 5-agent voting)
- **Consensus rate:** 97.7% (43/44 traces reach supermajority on first round)
- **Data integrity:** 100% real MAST traces (Cemri et al. 2025, arxiv 2503.13657)

## Next Milestone: Integration Testing (Jun 12)
- v0.4 rebase must complete by **Jun 5** (leaves 1-week buffer)
- Integration testing will measure real false positive rate on live telemetry
- Telemetry audit will identify observability gaps for ops team

## Architecture: No Pivot Required
v0.3 scaffolding remains unchanged. v0.4 is refinement layer only:
- Weighted voting: post-processing on consensus scores
- Confidence gating: filtering on supermajority quorum
- Telemetry audit: validation layer (separate concern)

All three improvements are composable and reversible.
