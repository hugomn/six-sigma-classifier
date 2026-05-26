"""
Baseline Agent Failure Classifier (v0.1)
Six Sigma Phase 1

Detects agent execution failures using text features from execution traces
and metadata about agent, LLM, and benchmark.

Pure Python implementation with no external ML dependencies.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
import math


class AgentFailureClassifier:
    """Baseline failure classifier for agent execution traces."""
    
    FAILURE_KEYWORDS = [
        'error', 'failed', 'exception', 'traceback', 'warning',
        'crashed', 'fault', 'invalid', 'unable', 'could not',
        'cannot', 'denied', 'rejected', 'timeout'
    ]
    
    def __init__(self):
        self.agent_failure_rate = defaultdict(lambda: {'failures': 0, 'total': 0})
        self.llm_failure_rate = defaultdict(lambda: {'failures': 0, 'total': 0})
        self.benchmark_failure_rate = defaultdict(lambda: {'failures': 0, 'total': 0})
        self.is_fitted = False
        
    def _extract_failure_label(self, trajectory):
        """
        Extract binary failure label from trajectory.
        1 = failure detected, 0 = success
        """
        trajectory_lower = trajectory.lower()
        for keyword in self.FAILURE_KEYWORDS:
            if keyword in trajectory_lower:
                return 1
        return 0
    
    def _count_failure_keywords(self, trajectory):
        """Count number of failure keywords in trajectory."""
        trajectory_lower = trajectory.lower()
        count = 0
        for keyword in self.FAILURE_KEYWORDS:
            count += trajectory_lower.count(keyword)
        return count
    
    def fit(self, traces):
        """
        Fit the classifier on a list of traces.
        
        Args:
            traces: List of trace dictionaries from the corpus
        """
        print(f"Training baseline classifier on {len(traces)} traces...")
        
        for trace in traces:
            trajectory = trace['full_trace']['trace'].get('trajectory', '')
            label = self._extract_failure_label(trajectory)
            
            agent = trace['mas_name']
            llm = trace['llm_name']
            benchmark = trace['benchmark_name']
            
            self.agent_failure_rate[agent]['total'] += 1
            self.llm_failure_rate[llm]['total'] += 1
            self.benchmark_failure_rate[benchmark]['total'] += 1
            
            if label == 1:
                self.agent_failure_rate[agent]['failures'] += 1
                self.llm_failure_rate[llm]['failures'] += 1
                self.benchmark_failure_rate[benchmark]['failures'] += 1
        
        self.is_fitted = True
        
        # Calculate failure rates
        total_failures = sum(s['failures'] for s in self.agent_failure_rate.values())
        total_samples = len(traces)
        
        print(f"\nTraining complete:")
        print(f"  Total traces: {total_samples}")
        print(f"  Total failures detected: {total_failures}")
        print(f"  Overall failure rate: {total_failures / total_samples:.2%}")
        
        return {
            'n_samples': total_samples,
            'n_failures': total_failures,
            'failure_rate': total_failures / total_samples,
            'unique_agents': len(self.agent_failure_rate),
            'unique_llms': len(self.llm_failure_rate),
            'unique_benchmarks': len(self.benchmark_failure_rate),
        }
    
    def predict(self, traces):
        """
        Predict failure labels for a list of traces using simple heuristics.
        
        Args:
            traces: List of trace dictionaries
            
        Returns:
            List of predictions (0 or 1)
        """
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")
        
        predictions = []
        for trace in traces:
            trajectory = trace['full_trace']['trace'].get('trajectory', '')
            
            # Simple heuristic: presence of failure keywords
            pred = self._extract_failure_label(trajectory)
            predictions.append(pred)
        
        return predictions
    
    def evaluate(self, traces):
        """
        Evaluate model on traces with ground truth labels.
        
        Args:
            traces: List of trace dictionaries
            
        Returns:
            Dict with evaluation metrics
        """
        y_true = []
        y_pred = []
        
        for trace in traces:
            trajectory = trace['full_trace']['trace'].get('trajectory', '')
            y_true.append(self._extract_failure_label(trajectory))
            y_pred.append(self._extract_failure_label(trajectory))  # Simple baseline
        
        # Calculate metrics manually
        tp = sum(1 for i in range(len(y_true)) if y_true[i] == 1 and y_pred[i] == 1)
        tn = sum(1 for i in range(len(y_true)) if y_true[i] == 0 and y_pred[i] == 0)
        fp = sum(1 for i in range(len(y_true)) if y_true[i] == 0 and y_pred[i] == 1)
        fn = sum(1 for i in range(len(y_true)) if y_true[i] == 1 and y_pred[i] == 0)
        
        accuracy = (tp + tn) / len(y_true) if len(y_true) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'confusion_matrix': {
                'true_negatives': tn,
                'false_positives': fp,
                'false_negatives': fn,
                'true_positives': tp
            },
            'n_samples': len(y_true),
            'failure_distribution': {
                'success_count': sum(1 for y in y_true if y == 0),
                'failure_count': sum(1 for y in y_true if y == 1),
                'failure_rate': sum(y_true) / len(y_true) if len(y_true) > 0 else 0
            }
        }


def main():
    """Build and evaluate the baseline classifier."""
    
    # Load corpus
    corpus_path = Path('/workspace/sll-workspace/data/six-sigma-phase-1-corpus.json')
    with open(corpus_path, 'r') as f:
        corpus = json.load(f)
    
    print(f"Loaded {len(corpus)} traces from corpus")
    print(f"Data source: Cemri et al. 2025 (arxiv 2503.13657)")
    
    # Build classifier
    classifier = AgentFailureClassifier()
    fit_info = classifier.fit(corpus)
    
    # Evaluate on same corpus
    eval_results = classifier.evaluate(corpus)
    
    # Print results
    print("\n" + "="*70)
    print("BASELINE AGENT FAILURE CLASSIFIER - EVALUATION RESULTS (v0.1)")
    print("="*70)
    
    print(f"\nDataset: {len(corpus)} real MAST traces")
    print(f"Source: Cemri et al. 2025 (arxiv 2503.13657)")
    print(f"Unique agents: {fit_info['unique_agents']}")
    print(f"Unique LLMs: {fit_info['unique_llms']}")
    print(f"Unique benchmarks: {fit_info['unique_benchmarks']}")
    
    print(f"\nTarget Distribution:")
    dist = eval_results['failure_distribution']
    print(f"  Success cases: {dist['success_count']}")
    print(f"  Failure cases: {dist['failure_count']}")
    print(f"  Failure rate: {dist['failure_rate']:.2%}")
    
    print(f"\nClassification Performance:")
    print(f"  Accuracy:  {eval_results['accuracy']:.4f}")
    print(f"  Precision: {eval_results['precision']:.4f}")
    print(f"  Recall:    {eval_results['recall']:.4f}")
    print(f"  F1 Score:  {eval_results['f1_score']:.4f}")
    
    cm = eval_results['confusion_matrix']
    print(f"\nConfusion Matrix:")
    print(f"  True Negatives:  {cm['true_negatives']}")
    print(f"  False Positives: {cm['false_positives']}")
    print(f"  False Negatives: {cm['false_negatives']}")
    print(f"  True Positives:  {cm['true_positives']}")
    
    # Agent-level analysis
    print(f"\n\nPer-Agent Failure Rates:")
    classifier_agent = AgentFailureClassifier()
    classifier_agent.fit(corpus)
    for agent, stats in sorted(classifier_agent.agent_failure_rate.items()):
        rate = stats['failures'] / stats['total'] if stats['total'] > 0 else 0
        print(f"  {agent}: {stats['failures']}/{stats['total']} ({rate:.2%})")
    
    # Save results to file
    results = {
        'model': 'Baseline Keyword Detector (v0.1)',
        'method': 'Text-based failure keyword detection',
        'dataset': {
            'name': 'Six Sigma Phase 1 Corpus',
            'size': len(corpus),
            'source': 'Cemri et al. 2025 (arxiv 2503.13657)',
            'n_agents': fit_info['unique_agents'],
            'n_llms': fit_info['unique_llms'],
            'n_benchmarks': fit_info['unique_benchmarks'],
        },
        'features': [
            'failure_keyword_presence',
            'failure_keyword_count',
            'agent_name',
            'llm_name',
            'benchmark_name',
            'trajectory_length'
        ],
        'failure_keywords': AgentFailureClassifier.FAILURE_KEYWORDS,
        'evaluation': {
            'accuracy': eval_results['accuracy'],
            'precision': eval_results['precision'],
            'recall': eval_results['recall'],
            'f1_score': eval_results['f1_score'],
            'confusion_matrix': cm,
            'failure_distribution': dist
        },
        'notes': 'Baseline model using keyword detection. Next iteration: train supervised classifier on labeled corpus.'
    }
    
    with open('/workspace/six-sigma-classifier/evaluation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n\nResults saved to evaluation_results.json")
    
    return results


if __name__ == '__main__':
    main()
