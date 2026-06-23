def generate_report(answers, facts, results):
    report = []
    report.append("\n" + "=" * 60)
    report.append("  SQL QUERY OPTIMIZATION REPORT")
    report.append("=" * 60)

    report.append("\n## Query Profile")
    for q, a in answers.items():
        report.append(f"- {q}: {a}")

    report.append("\n## Generated Facts")
    for f in facts:
        f_items = [f"{k}={v}" for k, v in f.items() if k != '__factid__']
        report.append(f"  Fact({', '.join(f_items)})")

    report.append("\n## Optimization Strengths")
    strengths = []
    if answers.get('stats_up_to_date'): strengths.append("Statistics are up to date")
    if answers.get('index_join'): strengths.append("Join columns are indexed")
    if answers.get('composite_index'): strengths.append("Composite index exists")
    if answers.get('parallel_available'): strengths.append("Parallel execution is available")
    if answers.get('partitioned'): strengths.append("Partitioning is configured")
    if answers.get('histogram_available'): strengths.append("Histogram statistics are available")
    if answers.get('normalized_schema'): strengths.append("Schema is properly normalized")
    if answers.get('fk_indexed'): strengths.append("Foreign key columns are indexed")
    if answers.get('clustered_index'): strengths.append("Clustered index is configured")
    if not answers.get('select_star'): strengths.append("Specific columns are selected (not SELECT *)")
    if answers.get('join_equality') and answers.get('join_indexed'): strengths.append("Equality joins on indexed columns are optimal")

    if strengths:
        for s in strengths:
            report.append(f"[+] {s}")
    else:
        report.append("No specific optimization strengths detected.")

    report.append("\n## Execution Summary")
    report.append(f"Total Facts Generated: {len(facts)}")
    report.append(f"Total Recommendations: {results['total_recommendations']}")

    report.append("\n## Recommendations")
    if not results['recommendations']:
        report.append("No recommendations triggered. Your query appears well-optimized.")
    else:
        for i, rec in enumerate(results['recommendations'], 1):
            report.append(f"\n### [{i}] {rec['category']}  [{rec['priority']}]")
            report.append(f"**Recommendation**: {rec['recommendation_text']}")
            report.append(f"**Reasoning**: {rec['reasoning']}")
            report.append(f"**Expected Impact**: {rec['expected_improvement']}")

    report.append("\n## Priority Action Plan")
    sorted_recs = sorted(results['recommendations'], key=lambda r: {"HIGH": 3, "MEDIUM": 2, "LOW": 1, "INFO": 0}.get(r['priority'], 0), reverse=True)
    for i, rec in enumerate(sorted_recs, 1):
        report.append(f"{i}. **{rec['recommendation_text']}** ({rec['priority']})")

    report.append("\n## Sources Referenced")
    report.append("- Database System Concepts (Silberschatz, Korth, Sudarshan)")
    report.append("- dbjournal.ro - SQL optimization techniques")
    report.append("- Medium Guide: Optimizing SQL Query Performance")

    report.append("\n" + "=" * 60)
    report.append("  END OF REPORT")
    report.append("=" * 60)

    final_report = "\n".join(report)
    print(final_report)
    return final_report
