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

        unique_recs = self._deduplicate(self.engine.recommendations)
        sorted_recs = sort_by_priority(unique_recs)
        reasoning_log = [f"[{r['priority']}] {r['category']}: {r['recommendation_text']} => {r['reasoning']}" for r in sorted_recs]

        return {
            "recommendations": sorted_recs,
            "reasoning_log": reasoning_log,
            "total_recommendations": len(sorted_recs)
        }

    @staticmethod
    def _deduplicate(recommendations):
        seen = set()
        result = []
        for rec in recommendations:
            key = (rec['category'], rec['recommendation_text'], rec['applies_to'])
            if key not in seen:
                seen.add(key)
                result.append(rec)
        return result
