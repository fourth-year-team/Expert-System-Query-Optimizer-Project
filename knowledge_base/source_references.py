SOURCE_REFERENCES = {
    "DSC_Ch16": {
        "title": "Database System Concepts, Chapter 16: Query Optimization",
        "authors": "Abraham Silberschatz, Henry F. Korth, S. Sudarshan",
        "edition": "7th Edition",
        "url": "https://www.db-book.com",
        "key_concepts": [
            "Query optimization overview and evaluation plans",
            "Transformation of relational expressions using equivalence rules",
            "Catalog information for cost estimation",
            "Statistical information for cost estimation",
            "Cost-based optimization strategies",
            "Dynamic programming for choosing evaluation plans",
            "Materialized views and their optimization",
            "Heuristic optimization: push selection down, push projection down",
            "Join ordering and join algorithm selection",
            "Nested Loop Join, Hash Join, Merge Join algorithms"
        ]
    },
    "DBJournal_16_4": {
        "title": "Query Optimization Techniques in Microsoft SQL Server",
        "journal": "Database Systems Journal, Volume 16, Issue 4",
        "url": "https://www.dbjournal.ro/archive/16/16_4.pdf",
        "key_concepts": [
            "Cost-based query optimization in SQL Server",
            "Index selectivity and statistics importance",
            "Data access mechanism selection",
            "Join algorithm selection based on data characteristics",
            "Index maintenance and fragmentation impact",
            "Statistics freshness and query plan quality",
            "EXISTS vs IN performance comparison",
            "Index usage analysis and monitoring"
        ]
    },
    "Medium_Guide": {
        "title": "Optimizing SQL Query Performance: A Comprehensive Guide",
        "url": "https://medium.com/womenintechnology/optimizing-sql-query-performance-a-comprehensive-guide-6cb72b9f52ef",
        "key_concepts": [
            "SELECT specific columns instead of SELECT *",
            "Avoid DISTINCT when unnecessary",
            "Use WHERE instead of HAVING for non-aggregate filters",
            "EXISTS vs IN performance considerations",
            "UNION ALL vs UNION for set operations",
            "Join optimization and index usage",
            "Subquery rewriting techniques",
            "Statistics maintenance best practices"
        ]
    }
}

def get_source_summary():
    lines = ["=" * 60]
    lines.append("  KNOWLEDGE BASE - SOURCE REFERENCES")
    lines.append("=" * 60)
    for key, ref in SOURCE_REFERENCES.items():
        lines.append(f"\n  [{key}]")
        lines.append(f"  Title: {ref['title']}")
        lines.append(f"  Key Concepts Used:")
        for concept in ref['key_concepts']:
            lines.append(f"    - {concept}")
    lines.append("\n" + "=" * 60)
    return "\n".join(lines)
