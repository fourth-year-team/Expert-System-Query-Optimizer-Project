from engine.facts import *
from engine.rules import QueryOptimizerRules

class QueryOptimizer:
    def __init__(self):
        self.engine = QueryOptimizerRules()

    def analyze(self, query_facts: QueryFact, table_facts: list = None,
                index_facts: list = None, join_facts: list = None,
                workload_fact: WorkloadFact = None, stats_fact: StatsFact = None):
        self.engine.reset()

        self.engine.declare(query_facts)

        if table_facts:
            for tf in table_facts:
                self.engine.declare(tf)

        if index_facts:
            for inf in index_facts:
                self.engine.declare(inf)

        if join_facts:
            for jf in join_facts:
                self.engine.declare(jf)

        if workload_fact:
            self.engine.declare(workload_fact)

        if stats_fact:
            self.engine.declare(stats_fact)

        self.engine.run()

        return {
            "recommendations": self.engine.recommendations,
            "reasoning_log": self.engine.reasoning_log,
            "total_recommendations": len(self.engine.recommendations)
        }

    def _fact_summary(self, name: str, fact) -> str:
        if fact is None:
            return ""
        lines = [f"  {k}: {v}" for k, v in fact.items() if not k.startswith('_')]
        return f"--- {name} ---\n" + "\n".join(lines)
