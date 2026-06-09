from experta import Fact
from engine.rules import QueryOptimizerRules

PRIORITY_ORDER = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}

def sort_by_priority(recs: list) -> list:
    return sorted(recs, key=lambda r: PRIORITY_ORDER.get(r["priority"], 0), reverse=True)

class QueryOptimizer:
    def __init__(self):
        self.engine = QueryOptimizerRules()

    def analyze(self, facts: list = None):
        self.engine.reset()
        for f in facts or []:
            self.engine.declare(f)
        self.engine.run()

        sorted_recs = sort_by_priority(self.engine.recommendations)
        reasoning_log = [f"[{r['priority']}] {r['category']}: {r['recommendation_text']} => {r['reasoning']}" for r in sorted_recs]

        return {
            "recommendations": sorted_recs,
            "reasoning_log": reasoning_log,
            "total_recommendations": len(sorted_recs)
        }
