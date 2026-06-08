import sys
import json
from engine.facts import *
from engine.optimizer import QueryOptimizer
from examples.case1_simple_select import case_simple_select
from examples.case2_join_query import case_join_query
from examples.case3_subquery import case_subquery
from examples.case4_aggregation import case_aggregation

SEPARATOR = "=" * 60

def print_header(title):
    print("\n" + SEPARATOR)
    print(f"  {title}")
    print(SEPARATOR)

def print_fact_section(name: str, fact):
    if fact is None:
        return
    lines = [f"    {k}: {v}" for k, v in fact.items() if not k.startswith('_')]
    print(f"\n  [{name}]")
    for line in lines:
        print(line)

def print_results(results: dict):
    print(f"\n{SEPARATOR}")
    print("  RECOMMENDATIONS REPORT")
    print(SEPARATOR)
    print(f"  Total Recommendations: {results['total_recommendations']}")
    print(SEPARATOR)

    for i, rec in enumerate(results['recommendations'], 1):
        print(f"\n  [{i}] {rec['category']}")
        print(f"      Recommendation: {rec['recommendation_text']}")
        print(f"      Reasoning: {rec['reasoning']}")
        print(f"      Priority: {rec['priority']}")
        print(f"      Expected Improvement: {rec['expected_improvement']}")
        print(f"      Applies To: {rec['applies_to']}")
        print("  " + "-" * 50)
    print(SEPARATOR)

def run_single_case(name, inputs_func):
    print_header(f"Running: {name}")
    qf, tfs, infs, jfs, wf, sf = inputs_func()
    print_fact_section("Query Fact", qf)
    for i, tf in enumerate(tfs or []):
        print_fact_section(f"Table Fact [{i}]", tf)
    for i, inf in enumerate(infs or []):
        print_fact_section(f"Index Fact [{i}]", inf)
    for i, jf in enumerate(jfs or []):
        print_fact_section(f"Join Fact [{i}]", jf)
    print_fact_section("Workload Fact", wf)
    print_fact_section("Stats Fact", sf)
    optimizer = QueryOptimizer()
    results = optimizer.analyze(qf, tfs, infs, jfs, wf, sf)
    print_results(results)

def run_all_cases():
    run_single_case("CASE 1: Simple SELECT with WHERE clause", case_simple_select)
    run_single_case("CASE 2: Multi-table JOIN query", case_join_query)
    run_single_case("CASE 3: Subquery with IN clause", case_subquery)
    run_single_case("CASE 4: Aggregation with GROUP BY and HAVING", case_aggregation)

if __name__ == "__main__":
    print_header("EXPERT SYSTEM QUERY OPTIMIZER")
    print("  An Expert System for SQL Query Optimization")
    print("  Using Experta (Python) - Rete-based Inference Engine")
    print(f"  Python {sys.version}")

    run_all_cases()

    print_header("PROJECT COMPLETED SUCCESSFULLY")
    print("  All 4 test cases executed.")
    print("  See docs/report.md for the academic report.")
    print("  See docs/diagrams.md for the architecture diagrams.")
