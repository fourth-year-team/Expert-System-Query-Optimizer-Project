import sys
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

def print_results(results: dict):
    print(f"\n{SEPARATOR}")
    print("  RECOMMENDATIONS REPORT")
    print(SEPARATOR)
    print(f"  Total Recommendations: {results['total_recommendations']}")
    print(SEPARATOR)

    for i, rec in enumerate(results['recommendations'], 1):
        print(f"\n  [{i}] {rec['category']}  [{rec['priority']}]")
        print(f"      Recommendation: {rec['recommendation_text']}")
        print(f"      Reasoning: {rec['reasoning']}")
        print(f"      Expected Improvement: {rec['expected_improvement']}")
        print(f"      Applies To: {rec['applies_to']}")
        print("  " + "-" * 50)
    print(SEPARATOR)

def run_single_case(name, inputs_func):
    print_header(f"Running: {name}")
    facts = inputs_func()
    print(f"  Facts declared: {len(facts)}")
    optimizer = QueryOptimizer()
    results = optimizer.analyze(facts)
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
    print("  With Atomic Facts & Inference Chaining")
    print(f"  Python {sys.version}")

    run_all_cases()

    print_header("PROJECT COMPLETED SUCCESSFULLY")
    print("  All 4 test cases executed with atomic facts.")
    print("  See docs/report.md for the academic report.")
    print("  See docs/diagrams.md for the architecture diagrams.")
