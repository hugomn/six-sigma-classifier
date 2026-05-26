import json
from pathlib import Path

class FailureClassifier:
    """Baseline keyword-based failure detector for MAST agent traces."""
    
    FAILURE_KEYWORDS = {
        'error', 'failed', 'exception', 'traceback', 'warning',
        'crashed', 'fault', 'invalid', 'unable', 'could not',
        'cannot', 'denied', 'rejected', 'timeout'
    }
    
    def __init__(self):
        self.traces = []
        self.labels = {}
    
    def load_corpus(self, path):
        """Load the Six Sigma Phase 1 corpus (44-trace verified dedupe)."""
        with open(path) as f:
            self.traces = json.load(f)
        print(f"Loaded {len(self.traces)} traces")
        return self
    
    def detect_failure_keywords(self, trace_text):
        """Check if trace contains any failure keywords (case-insensitive)."""
        text_lower = str(trace_text).lower()
        for keyword in self.FAILURE_KEYWORDS:
            if keyword in text_lower:
                return True
        return False
    
    def label(self):
        """Label all traces by keyword detection (in-sample baseline)."""
        self.labels = {}
        for trace in self.traces:
            trace_id = trace.get('trace_id', '')
            full_trace = trace.get('full_trace', '')
            
            # Detect failure by keyword scan
            is_failure = self.detect_failure_keywords(full_trace)
            self.labels[trace_id] = {
                'trace_id': trace_id,
                'mas_name': trace.get('mas_name', 'unknown'),
                'llm_name': trace.get('llm_name', 'unknown'),
                'benchmark_name': trace.get('benchmark_name', 'unknown'),
                'predicted_failure': is_failure
            }
        return self
    
    def evaluate(self):
        """Summarize labeling results (in-sample baseline, no held-out test)."""
        if not self.labels:
            raise ValueError("No labels. Call label() first.")
        
        failure_count = sum(1 for l in self.labels.values() if l['predicted_failure'])
        success_count = len(self.labels) - failure_count
        
        results = {
            'dataset_size': len(self.traces),
            'methodology': 'in-sample keyword detection baseline',
            'disclaimer': 'Fit and evaluated on same corpus; not a generalization metric',
            'failure_count': failure_count,
            'success_count': success_count,
            'failure_rate': failure_count / len(self.traces) if self.traces else 0,
            'per_agent_breakdown': self._breakdown_by_agent()
        }
        
        return results
    
    def _breakdown_by_agent(self):
        """Count failures per agent."""
        by_agent = {}
        for label in self.labels.values():
            agent = label['mas_name']
            if agent not in by_agent:
                by_agent[agent] = {'failures': 0, 'total': 0}
            by_agent[agent]['total'] += 1
            if label['predicted_failure']:
                by_agent[agent]['failures'] += 1
        
        return {
            agent: {
                'failures': counts['failures'],
                'total': counts['total'],
                'failure_rate': counts['failures'] / counts['total'] if counts['total'] > 0 else 0
            }
            for agent, counts in sorted(by_agent.items())
        }


def main():
    # Load corpus (included in repo)
    corpus_path = Path(__file__).parent / 'corpus.json'
    
    if not corpus_path.exists():
        raise FileNotFoundError(f"corpus.json not found at {corpus_path}")
    
    # Instantiate, load, label, evaluate
    clf = FailureClassifier()
    clf.load_corpus(corpus_path)
    clf.label()
    results = clf.evaluate()
    
    # Write results
    output_path = Path(__file__).parent / 'evaluation_results.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✓ Labeled {len(clf.labels)} traces")
    print(f"✓ Results: {results['failure_count']} failures, {results['success_count']} successes")
    print(f"✓ Failure rate: {results['failure_rate']:.2%}")
    print(f"✓ Saved to {output_path}")
    
    # Show per-agent breakdown
    print("\nPer-Agent Breakdown:")
    for agent, stats in results['per_agent_breakdown'].items():
        print(f"  {agent}: {stats['failures']}/{stats['total']} ({stats['failure_rate']:.2%})")


if __name__ == '__main__':
    main()
