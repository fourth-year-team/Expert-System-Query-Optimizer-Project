from experta import Fact
from engine.rules import QueryOptimizerRules

PRIORITY_ORDER = {"HIGH": 3, "MEDIUM": 2, "LOW": 1, "INFO": 0}

CONFLICT_GROUPS = {
    "access_path": {
        "Use Full Table Scan - table is large with no suitable index",
        "Use Index Scan instead of Full Scan for better performance",
        "Table is small - use Full Table Scan even if an index exists",
        "Use Covering Index Scan - the index covers all required columns",
    },
}

SUPPRESSED_BY_TEXT = {
    "Current join structure is suitable for efficient indexed joins.": {
        "Review join order and join predicates.",
    },
}

def sort_by_priority(recs: list) -> list:
    return sorted(recs, key=lambda r: PRIORITY_ORDER.get(r["priority"], 0), reverse=True)

def _rec_key(rec) -> tuple:
    return (rec["category"], rec["recommendation_text"], rec["applies_to"])

def _is_better_rec(candidate, current) -> bool:
    return PRIORITY_ORDER.get(candidate["priority"], 0) > PRIORITY_ORDER.get(current["priority"], 0)

def resolve_recommendation_conflicts(recs: list) -> list:
    unique = []
    seen = set()

    for rec in recs:
        key = _rec_key(rec)
        if key not in seen:
            seen.add(key)
            unique.append(rec)

    active_texts = {rec["recommendation_text"] for rec in unique}
    suppressed = set()
    for active_text, blocked_texts in SUPPRESSED_BY_TEXT.items():
        if active_text in active_texts:
            suppressed.update(blocked_texts)

    resolved = [rec for rec in unique if rec["recommendation_text"] not in suppressed]

    for group_texts in CONFLICT_GROUPS.values():
        matching = [rec for rec in resolved if rec["recommendation_text"] in group_texts]
        if len(matching) <= 1:
            continue

        winner = matching[0]
        for rec in matching[1:]:
            if _is_better_rec(rec, winner):
                winner = rec
        resolved = [rec for rec in resolved if rec["recommendation_text"] not in group_texts or rec is winner]

    return sort_by_priority(resolved)

class QueryOptimizer:
    def __init__(self):
        self.engine = QueryOptimizerRules()

    def analyze(self, facts: list = None):
        self.engine.reset()
        for f in facts or []:
            self.engine.declare(f)
        self.engine.run()

        sorted_recs = resolve_recommendation_conflicts(self.engine.recommendations)
        reasoning_log = [f"[{r['priority']}] {r['category']}: {r['recommendation_text']} => {r['reasoning']}" for r in sorted_recs]

        return {
            "recommendations": sorted_recs,
            "reasoning_log": reasoning_log,
            "total_recommendations": len(sorted_recs)
        }
