#!/usr/bin/env python3
"""
Six Sigma Failure-Mode Classifier (v0.2)
Supervised failure-mode classification on 44 real failures.
No external dependencies.
"""

import json
from collections import defaultdict, Counter
import random

def load_corpus():
    """Load and filter to failures only."""
    with open('corpus.json') as f:
        corpus = json.load(f)
    
    failures = [t for t in corpus if t['mast_score'] == 1]
    print(f"Loaded corpus: {len(corpus)} traces total")
    print(f"Failures (score==1): {len(failures)} traces")
    return failures

def extract_features(trace):
    """Extract lightweight features from a trace."""
    steps = trace.get('full_trace', [])
    agent = trace['mas_name']
    llm = trace['llm_name']
    benchmark = trace['benchmark_name']
    mode = trace['primary_mast_mode']
    trace_id = trace['trace_id']
    
    # Simple numeric encoding
    agent_code = hash(agent) % 256
    llm_code = hash(llm) % 256
    bench_code = hash(benchmark) % 256
    
    return {
        'trace_id': trace_id,
        'agent_code': agent_code,
        'llm_code': llm_code,
        'bench_code': bench_code,
        'num_steps': len(steps),
        'mode': mode,
        'agent': agent,
        'llm': llm,
        'benchmark': benchmark,
    }

def simple_classifier(failures):
    """Simple majority-vote classifier by (agent, benchmark) pair."""
    # Train: group by (agent, benchmark) and find most common mode
    pairs = defaultdict(list)
    for trace in failures:
        agent = trace['mas_name']
        bench = trace['benchmark_name']
        mode = trace['primary_mast_mode']
        pairs[(agent, bench)].append(mode)
    
    mode_map = {}
    for pair, modes in pairs.items():
        mode_map[pair] = Counter(modes).most_common(1)[0][0]
    
    # Evaluate: predict on all data
    predictions = {}
    correct = 0
    for trace in failures:
        agent = trace['mas_name']
        bench = trace['benchmark_name']
        actual_mode = trace['primary_mast_mode']
        pred_mode = mode_map.get((agent, bench), '1.1')
        predictions[trace['trace_id']] = {
            'actual': actual_mode,
            'predicted': pred_mode,
            'correct': actual_mode == pred_mode,
        }
        if actual_mode == pred_mode:
            correct += 1
    
    accuracy = correct / len(failures)
    
    # Per-mode metrics
    mode_stats = defaultdict(lambda: {'tp': 0, 'fp': 0, 'fn': 0, 'tn': 0})
    for trace_id, pred in predictions.items():
        actual = pred['actual']
        predicted = pred['predicted']
        for mode in set(list(mode_stats.keys()) + [actual, predicted]):
            if actual == mode and predicted == mode:
                mode_stats[mode]['tp'] += 1
            elif predicted == mode and actual != mode:
                mode_stats[mode]['fp'] += 1
            elif actual == mode and predicted != mode:
                mode_stats[mode]['fn'] += 1
    
    results = {
        'model': 'SimpleClassifier(agent+benchmark majority vote)',
        'overall_accuracy': accuracy,
        'total_traces': len(failures),
        'correct_predictions': correct,
        'per_mode_stats': {
            str(mode): {
                'tp': stats['tp'],
                'fp': stats['fp'],
                'fn': stats['fn'],
                'precision': stats['tp'] / (stats['tp'] + stats['fp']) if (stats['tp'] + stats['fp']) > 0 else 0,
                'recall': stats['tp'] / (stats['tp'] + stats['fn']) if (stats['tp'] + stats['fn']) > 0 else 0,
            }
            for mode, stats in sorted(mode_stats.items())
        }
    }
    
    return results, predictions

def main():
    failures = load_corpus()
    
    # Get mode distribution
    modes = Counter([t['primary_mast_mode'] for t in failures])
    print(f"\nMode distribution (failures only):")
    for mode in sorted(modes.keys()):
        print(f"  Mode {mode}: {modes[mode]} traces")
    
    # Train classifier
    print(f"\n--- v0.2 Classifier Training ---")
    results, predictions = simple_classifier(failures)
    
    print(f"Model: {results['model']}")
    print(f"Accuracy: {results['overall_accuracy']:.2%} ({results['correct_predictions']}/{results['total_traces']})")
    
    print(f"\nPer-mode performance:")
    for mode in sorted(results['per_mode_stats'].keys()):
        stats = results['per_mode_stats'][mode]
        print(f"  Mode {mode}:")
        print(f"    Precision: {stats['precision']:.2%}, Recall: {stats['recall']:.2%}")
    
    # Save results
    with open('evaluation_results_v0.2.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to evaluation_results_v0.2.json")
    return 0

if __name__ == '__main__':
    exit(main())
