from experta import *
from engine.facts import RecommendationFact

recommendation_counter = iter(range(1, 1000))

def next_id():
    return next(recommendation_counter)

class QueryOptimizerRules(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.recommendations = []
        self.reasoning_log = []

    def record(self, rec: RecommendationFact):
        self.recommendations.append(rec)
        self.reasoning_log.append(f"[{rec['priority']}] {rec['category']}: {rec['recommendation_text']} => {rec['reasoning']}")

    # ── Derived intermediate facts (chaining) ──

    @Rule(Fact(select_star=True))
    def derive_select_list_wide(self):
        self.declare(Fact(select_list_wide=True))

    @Rule(Fact(select_minimal=True))
    def derive_select_list_narrow(self):
        self.declare(Fact(select_list_minimal=True))

    @Rule(Fact(where=True) & Fact(subquery=True) & Fact(join=True))
    def derive_push_selection(self):
        self.declare(Fact(push_selection_possible=True))

    @Rule(Fact(table=MATCH.t, large=True) & NOT(Fact(table=MATCH.t, index=True)))
    def derive_full_scan_scenario(self, t):
        self.declare(Fact(table=t, full_scan_scenario=True))

    @Rule(Fact(table=MATCH.t, index=True) & Fact(table=MATCH.t, selective=True) & Fact(table=MATCH.t, large=True))
    def derive_index_scan_scenario(self, t):
        self.declare(Fact(table=t, index_scan_possible=True))

    # ── Access Path Rules ──

    @Rule(Fact(table=MATCH.t, large=True) & NOT(Fact(table=MATCH.t, index=True)))
    def rule_full_scan(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="SCAN_SELECTION",
            recommendation_text="Use Full Table Scan - table is large with no suitable index",
            reasoning="Source: Database System Concepts Ch16 - Full Scan is the only option when no index exists",
            priority="HIGH",
            expected_improvement="Avoid using non-existent index",
            applies_to="access_path"
        ))

    @Rule(Fact(table=MATCH.t, index=True) & Fact(table=MATCH.t, selective=True) & Fact(table=MATCH.t, large=True))
    def rule_index_scan(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="SCAN_SELECTION",
            recommendation_text="Use Index Scan instead of Full Scan for better performance",
            reasoning="Source: dbjournal.ro - Index Scan significantly reduces blocks read when selectivity is high",
            priority="HIGH",
            expected_improvement="Reduce I/O by up to 90%",
            applies_to="access_path"
        ))

    @Rule(Fact(table=MATCH.t, small=True))
    def rule_small_table_scan(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="SCAN_SELECTION",
            recommendation_text="Table is small - use Full Table Scan even if an index exists",
            reasoning="Source: Database System Concepts Ch16 - Index ACCESS + table read cost may exceed Full Scan for small tables",
            priority="MEDIUM",
            expected_improvement="Avoid unnecessary index overhead for small tables",
            applies_to="access_path"
        ))

    @Rule(Fact(select_minimal=True) & Fact(table=MATCH.t, index=True) & Fact(table=MATCH.t, covering=True))
    def rule_covering_index_scan(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="INDEX_SCAN",
            recommendation_text="Use Covering Index Scan - the index covers all required columns",
            reasoning="Source: Database System Concepts Ch16.4 - Covering Index eliminates the need to access the original table data, reducing I/O",
            priority="HIGH",
            expected_improvement="Fastest way to read data without touching the base table",
            applies_to="access_path"
        ))

    # ── Heuristic Optimization Rules ──

    @Rule(Fact(where=True) & Fact(subquery=True) & Fact(join=True))
    def rule_push_selection_down(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="HEURISTIC_OPTIMIZATION",
            recommendation_text="Push Selection predicates down closer to the base tables",
            reasoning="Source: Database System Concepts Ch16.3 - Push selection down reduces rows early, lowering JOIN cost",
            priority="HIGH",
            expected_improvement="Reduce intermediate results by up to 70%",
            applies_to="query_tree_transformation"
        ))

    @Rule(Fact(select_list_wide=True))
    def rule_push_projection_down(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="HEURISTIC_OPTIMIZATION",
            recommendation_text="Push Projection down to reduce columns passed between operators",
            reasoning="Source: Database System Concepts Ch16 - Push projection down reduces row width and improves memory usage",
            priority="HIGH",
            expected_improvement="Reduce transferred data size proportionally to table width",
            applies_to="query_tree_transformation"
        ))

    @Rule(Fact(view=True) & Fact(where=True))
    def rule_predicate_pushdown_view(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="HEURISTIC_OPTIMIZATION",
            recommendation_text="Push predicates through the view into the underlying base table query to reduce intermediate results",
            reasoning="Source: Database System Concepts Ch16 - Predicate pushdown across views filters rows earlier, reducing the data volume the outer query must process",
            priority="HIGH",
            expected_improvement="Reduce intermediate results and improve overall query performance",
            applies_to="view_optimization"
        ))

    @Rule(Fact(select_star=True) & NOT(Fact(select_minimal=True)))
    def rule_select_list_optimization(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="QUERY_REWRITE",
            recommendation_text="Use specific column names instead of SELECT * to reduce transferred data",
            reasoning="Source: dbjournal.ro - SELECT * transfers all columns including unnecessary ones, increasing I/O and network traffic",
            priority="HIGH",
            expected_improvement="Reduce data transfer, I/O, and memory usage",
            applies_to="select_optimization"
        ))

    # ── Join Algorithm Rules ──

    @Rule(Fact(nested_loop_possible=True) & Fact(one_small=True) & Fact(table=MATCH.t, index=True) & Fact(table=MATCH.t, supports_join=True))
    def rule_nested_loop_join(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="JOIN_ALGORITHM",
            recommendation_text="Use Nested Loop Join - ideal when one relation is small and the other is indexed",
            reasoning="Source: Database System Concepts Ch16.5.2 - Nested Loop Join is efficient when outer relation is small and indexes exist",
            priority="HIGH",
            expected_improvement="Excellent performance with small indexed relations",
            applies_to="join_execution"
        ))

    @Rule(Fact(hash_join_possible=True) & Fact(both_large=True) & NOT(Fact(memory_constrained=True)))
    def rule_hash_join(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="JOIN_ALGORITHM",
            recommendation_text="Use Hash Join - best choice when both relations are large",
            reasoning="Source: dbjournal.ro - Hash Join is suitable for queries handling large amounts of data without indexes",
            priority="HIGH",
            expected_improvement="Good performance with large unindexed data",
            applies_to="join_execution"
        ))

    @Rule(Fact(merge_join_possible=True) & Fact(order_by=True) & Fact(sort_merge_ok=True))
    def rule_merge_join(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="JOIN_ALGORITHM",
            recommendation_text="Use Merge Join - query already requires sorted output, making it ideal",
            reasoning="Source: Database System Concepts Ch16.5.3 - Merge Join is effective when data is pre-sorted or sorted output is needed",
            priority="MEDIUM",
            expected_improvement="Avoid extra sort if ORDER BY already exists",
            applies_to="join_execution"
        ))

    @Rule(Fact(hash_join_possible=True) & Fact(join_equality=True) & NOT(Fact(table=MATCH.t, on_join=True)))
    def rule_hash_join_no_index(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="JOIN_ALGORITHM",
            recommendation_text="Use Hash Join - optimal choice when no indexes exist on JOIN columns",
            reasoning="Source: Database System Concepts Ch16.5.4 - Hash Join does not require pre-existing indexes and works efficiently with unindexed data",
            priority="HIGH",
            expected_improvement="Best when no JOIN indexes exist",
            applies_to="join_execution"
        ))

    @Rule(Fact(semi_join_possible=True) & Fact(subquery=True))
    def rule_semi_join(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="JOIN_ALGORITHM",
            recommendation_text="Use Semi-Join instead of subquery to eliminate duplicates early and reduce intermediate results",
            reasoning="Source: Database System Concepts Ch16 - Semi-Join efficiently handles subquery IN/EXISTS by stopping at the first match per outer row",
            priority="HIGH",
            expected_improvement="Reduce intermediate results significantly for subquery IN/EXISTS",
            applies_to="join_execution"
        ))

    @Rule(Fact(anti_join_possible=True) & Fact(not_in=True))
    def rule_anti_join(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="JOIN_ALGORITHM",
            recommendation_text="Use Anti-Join instead of NOT IN/NOT EXISTS for efficient negation",
            reasoning="Source: Database System Concepts Ch16 - Anti-Join processes negation more efficiently by scanning only until a match is found",
            priority="HIGH",
            expected_improvement="Faster execution of negative subqueries by up to 70%",
            applies_to="join_execution"
        ))

    @Rule(Fact(adaptive_join_possible=True) & Fact(both_large=True) & NOT(Fact(cardinality_accurate=True)))
    def rule_adaptive_join(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="JOIN_ALGORITHM",
            recommendation_text="Use Adaptive Join to dynamically choose between Hash Join and Nested Loop based on actual runtime statistics",
            reasoning="Source: Modern DBMS (SQL Server 2017+, PostgreSQL) - Adaptive Join switches strategies mid-execution when cardinality estimates are inaccurate",
            priority="MEDIUM",
            expected_improvement="Robust performance when statistics are inaccurate or data skew exists",
            applies_to="adaptive_join_execution"
        ))

    @Rule(Fact(join_ordering_possible=True) & Fact(has_small_table=True))
    def rule_join_order_optimization(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="JOIN_ORDER",
            recommendation_text="Reorder JOINs: place smaller relations first to minimize intermediate result sizes",
            reasoning="Source: Database System Concepts Ch16.5.5 - JOIN order significantly impacts query cost; smallest first reduces Intermediate Results",
            priority="HIGH",
            expected_improvement="Significant performance improvement with 3+ tables",
            applies_to="join_ordering"
        ))

    # ── Query Rewrite Rules ──

    @Rule(Fact(subquery=True) & Fact(correlated_subquery=True) & NOT(Fact(aggregation=True)) & NOT(Fact(distinct=True)))
    def rule_subquery_to_join(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="QUERY_REWRITE",
            recommendation_text="Rewrite the Subquery as a JOIN for significant performance improvement",
            reasoning="Source: Database System Concepts Ch16.3.2 - Rewriting Subquery as JOIN allows the optimizer to use more efficient execution strategies",
            priority="HIGH",
            expected_improvement="Performance improvement of 50-80% in correlated queries",
            applies_to="query_rewriting"
        ))

    @Rule(Fact(in_operator=True) & NOT(Fact(distinct=True)) & Fact(subquery=True) & Fact(correlated_subquery=True))
    def rule_exists_vs_in(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="QUERY_REWRITE",
            recommendation_text="Use EXISTS instead of IN in subqueries for better performance",
            reasoning="Source: dbjournal.ro - EXISTS stops at first match while IN scans all values in the subquery result",
            priority="MEDIUM",
            expected_improvement="EXISTS is faster especially with large result sets",
            applies_to="subquery_optimization"
        ))

    @Rule(Fact(having=True) & NOT(Fact(where=True)) & Fact(aggregation=True))
    def rule_where_vs_having(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="QUERY_REWRITE",
            recommendation_text="Move non-aggregate filter conditions from HAVING to WHERE to reduce rows before aggregation",
            reasoning="Source: Database System Concepts Ch16 - WHERE is applied before GROUP BY, reducing rows entering aggregation; HAVING is applied after",
            priority="HIGH",
            expected_improvement="Significantly reduce rows being aggregated",
            applies_to="filter_pushdown"
        ))

    @Rule(Fact(distinct=True) & Fact(pk=True))
    def rule_distinct_optimization(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="QUERY_REWRITE",
            recommendation_text="DISTINCT is unnecessary if the query includes a PRIMARY KEY or unique column",
            reasoning="Source: Database System Concepts Ch16 - DISTINCT adds extra sorting; can be removed when column is unique",
            priority="MEDIUM",
            expected_improvement="Avoid unnecessary extra sort operation",
            applies_to="duplicate_removal"
        ))

    @Rule(Fact(union=True) & NOT(Fact(union_all=True)))
    def rule_union_all_instead_of_union(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="QUERY_REWRITE",
            recommendation_text="Use UNION ALL instead of UNION if duplicate elimination is not needed",
            reasoning="Source: Database System Concepts Ch16 - UNION sorts to remove duplicates while UNION ALL merges results directly",
            priority="MEDIUM",
            expected_improvement="Avoid unnecessary sort operation to speed up the query",
            applies_to="set_operation_optimization"
        ))

    @Rule(Fact(or_condition=True))
    def rule_or_condition_optimization(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="QUERY_REWRITE",
            recommendation_text="Rewrite OR conditions using UNION ALL with separate indexes for each part",
            reasoning="Source: dbjournal.ro - OR prevents index usage in most cases, while UNION ALL allows index usage per sub-query",
            priority="MEDIUM",
            expected_improvement="Improve queries with OR conditions by 40-60%",
            applies_to="condition_rewriting"
        ))

    @Rule(Fact(not_in=True) & Fact(subquery=True))
    def rule_not_in_to_not_exists(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="QUERY_REWRITE",
            recommendation_text="Use NOT EXISTS instead of NOT IN to avoid NULL issues and improve performance",
            reasoning="Source: Database System Concepts Ch16 - NOT IN returns empty results when NULL exists in the Subquery, while NOT EXISTS works correctly",
            priority="HIGH",
            expected_improvement="Correct results with better performance",
            applies_to="subquery_optimization"
        ))

    @Rule(Fact(cte=True) & NOT(Fact(cte_materialized=True)) & Fact(temp_allowed=True))
    def rule_cte_materialization(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="QUERY_REWRITE",
            recommendation_text="Materialize the CTE (WITH clause) into a temporary table to avoid repeated evaluation",
            reasoning="Source: Database System Concepts Ch16 - CTE materialization prevents re-execution of the same subquery for each reference, reducing total work",
            priority="MEDIUM",
            expected_improvement="Avoid repeated CTE evaluation for multiple references",
            applies_to="cte_optimization"
        ))

    @Rule(Fact(subquery=True) & Fact(correlated_subquery=True) & Fact(temp_allowed=True) & Fact(aggregation=True))
    def rule_materialize_subquery(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="QUERY_REWRITE",
            recommendation_text="Materialize the Subquery into a temporary table to avoid repeated execution",
            reasoning="Source: Database System Concepts Ch16 - Materializing Subquery in a temp table prevents executing it for each outer query row",
            priority="MEDIUM",
            expected_improvement="Avoid N+1 repeated execution of the Subquery",
            applies_to="subquery_optimization"
        ))

    @Rule(Fact(limit=True) & NOT(Fact(order_by=True)))
    def rule_order_by_with_limit(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="QUERY_REWRITE",
            recommendation_text="Add ORDER BY with LIMIT/OFFSET to ensure consistent result ordering",
            reasoning="Source: Medium Guide - LIMIT without ORDER BY yields inconsistent results across executions",
            priority="LOW",
            expected_improvement="Ensure consistent result ordering",
            applies_to="query_correctness"
        ))

    # ── Index Rules ──

    @Rule(Fact(table=MATCH.t, large=True) & NOT(Fact(table=MATCH.t, index=True)))
    def rule_index_suggestion(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="INDEX_SUGGESTION",
            recommendation_text="Suggest creating an index on the column used in WHERE to improve search performance",
            reasoning="Source: dbjournal.ro - Creating a selective index significantly reduces I/O accesses and speeds up queries",
            priority="HIGH",
            expected_improvement="Speed up queries by 90%+ in search operations",
            applies_to="index_creation"
        ))

    @Rule(Fact(multi_column_predicate=True) & Fact(table=MATCH.t, index=True) & NOT(Fact(table=MATCH.t, composite=True)) & Fact(table=MATCH.t, large=True))
    def rule_composite_index_suggestion(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="INDEX_SUGGESTION",
            recommendation_text="Suggest creating a Composite Index on columns used together in WHERE",
            reasoning="Source: Database System Concepts Ch16 - Composite Index improves queries using multiple columns in the condition",
            priority="MEDIUM",
            expected_improvement="Speed up multi-condition queries",
            applies_to="index_creation"
        ))

    @Rule(Fact(range_predicate=True) & Fact(table=MATCH.t, index=True) & NOT(Fact(table=MATCH.t, clustered=True)))
    def rule_clustered_index_for_range(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="INDEX_SUGGESTION",
            recommendation_text="Use Clustered Index for range queries (BETWEEN, >, <) to speed up range searches",
            reasoning="Source: Database System Concepts Ch16 - Clustered Index physically orders data, making range queries significantly faster",
            priority="MEDIUM",
            expected_improvement="Speed up range queries by 50-80%",
            applies_to="index_type_selection"
        ))

    @Rule(Fact(fk=True) & Fact(table=MATCH.t, index=True) & NOT(Fact(table=MATCH.t, on_join=True)))
    def rule_index_on_foreign_key(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="INDEX_SUGGESTION",
            recommendation_text="Create an index on Foreign Key columns to speed up JOIN operations",
            reasoning="Source: Database System Concepts Ch16.4 - Indexes on foreign keys significantly improve JOIN performance",
            priority="HIGH",
            expected_improvement="Speed up JOIN on foreign keys by up to 80%",
            applies_to="index_creation"
        ))

    @Rule(Fact(table=MATCH.t, index=True) & Fact(table=MATCH.t, unused=True))
    def rule_unused_index_detection(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="INDEX_MAINTENANCE",
            recommendation_text="Unused index detected - consider dropping it to reduce UPDATE/INSERT/DELETE overhead",
            reasoning="Source: dbjournal.ro - Unused indexes increase write operation costs without benefiting reads",
            priority="LOW",
            expected_improvement="Improve write performance by removing unnecessary indexes",
            applies_to="index_maintenance"
        ))

    @Rule(Fact(table=MATCH.t, index=True) & Fact(table=MATCH.t, fragmented=True))
    def rule_fragmented_index(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="INDEX_MAINTENANCE",
            recommendation_text="Index is fragmented - consider REBUILD or REORGANIZE the index",
            reasoning="Source: Database System Concepts Ch16 - Index fragmentation increases I/O and degrades query performance",
            priority="MEDIUM",
            expected_improvement="Improve read performance by up to 30%",
            applies_to="index_maintenance"
        ))

    @Rule(Fact(where=True) & NOT(Fact(subquery=True)) & Fact(table=MATCH.t, index=True) & Fact(table=MATCH.t, on_predicate=True))
    def rule_use_index_for_filter(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="INDEX_USAGE",
            recommendation_text="Use the existing index on the WHERE predicate column to speed up filtering",
            reasoning="Source: Database System Concepts Ch16 - An index on the WHERE column enables direct access to required rows",
            priority="HIGH",
            expected_improvement="Speed up filtering by 90%+",
            applies_to="filter_optimization"
        ))

    @Rule(Fact(limit=True) & Fact(order_by=True) & Fact(table=MATCH.t, index=True) & Fact(table=MATCH.t, supports_order=True))
    def rule_limit_offset_index(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="PERFORMANCE_TUNING",
            recommendation_text="Use an index that supports ORDER BY with LIMIT/OFFSET to avoid a full sort",
            reasoning="Source: Database System Concepts Ch16 - An ordered index allows LIMIT execution without sorting all data",
            priority="HIGH",
            expected_improvement="Avoid Full Sort and improve pagination query performance",
            applies_to="limit_offset_optimization"
        ))

    # ── Statistics Rules ──

    @Rule(Fact(stats_outdated=True))
    def rule_statistics_freshness(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="STATISTICS",
            recommendation_text="Table statistics are outdated - recommend updating statistics (UPDATE STATISTICS)",
            reasoning="Source: dbjournal.ro - Outdated statistics lead to suboptimal execution plans costing up to 10x more",
            priority="HIGH",
            expected_improvement="Improve execution plan selection by up to 50%",
            applies_to="statistics_maintenance"
        ))

    @Rule(Fact(intermediate_large=True))
    def rule_reduce_intermediate_results(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="PERFORMANCE_TUNING",
            recommendation_text="Intermediate results are too large - apply Selection and Projection before JOIN to reduce size",
            reasoning="Source: Database System Concepts Ch16 - Reducing intermediate results is the key to improving complex query performance",
            priority="HIGH",
            expected_improvement="Performance improvement by up to 60%",
            applies_to="intermediate_result_optimization"
        ))

    @Rule(Fact(table=MATCH.t, stats_fresh=True) & NOT(Fact(table=MATCH.t, data_known=True)) & NOT(Fact(histogram_available=True)))
    def rule_data_distribution_check(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="STATISTICS",
            recommendation_text="Create a Histogram on columns used in WHERE to improve selectivity estimation",
            reasoning="Source: Database System Concepts Ch16.4 - Histogram improves cardinality estimation for queries with non-uniform data distribution",
            priority="MEDIUM",
            expected_improvement="Improve cost estimation accuracy by 30-50%",
            applies_to="statistics_enhancement"
        ))

    @Rule(NOT(Fact(histogram_available=True)) & NOT(Fact(stats_outdated=True)))
    def rule_create_histogram(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="STATISTICS",
            recommendation_text="Create detailed statistics (Histogram) to improve cardinality estimation",
            reasoning="Source: Database System Concepts Ch16.4 - Histogram provides more accurate data distribution information",
            priority="MEDIUM",
            expected_improvement="Improve execution plan accuracy",
            applies_to="statistics_enhancement"
        ))

    # ── Workload Strategy Rules ──

    @Rule(Fact(fast_response=True) & Fact(response_critical=True) & Fact(order_by=True))
    def rule_fast_response_strategy(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="WORKLOAD_STRATEGY",
            recommendation_text="Use Top-N Optimization: apply LIMIT/FETCH FIRST to reduce data volume",
            reasoning="Source: Database System Concepts Ch16 - Top-N Optimization reduces the data volume the optimizer must process",
            priority="HIGH",
            expected_improvement="Significantly faster initial response time",
            applies_to="response_time_optimization"
        ))

    @Rule(Fact(read_heavy=True) & NOT(Fact(write_heavy=True)) & Fact(indexes_healthy=True))
    def rule_maintain_indexes_read_heavy(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="WORKLOAD_STRATEGY",
            recommendation_text="In read-heavy environments, maintain existing indexes as they improve query performance",
            reasoning="Source: Medium Guide - In OLAP/Reporting systems, indexes are crucial for query performance",
            priority="MEDIUM",
            expected_improvement="Ensure sustained good query performance",
            applies_to="index_maintenance"
        ))

    @Rule(Fact(write_heavy=True) & NOT(Fact(read_heavy=True)))
    def rule_minimize_indexes_write_heavy(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="WORKLOAD_STRATEGY",
            recommendation_text="In write-heavy environments, minimize indexes to reduce UPDATE/INSERT/DELETE overhead",
            reasoning="Source: dbjournal.ro - Each additional index increases the cost of write operations",
            priority="MEDIUM",
            expected_improvement="Speed up write operations proportionally to the number of indexes removed",
            applies_to="index_strategy"
        ))

    @Rule(Fact(parallel_available=True) & Fact(table=MATCH.t, large=True))
    def rule_parallel_execution(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="PARALLEL_EXECUTION",
            recommendation_text="Enable Parallel Execution to distribute large table scans across multiple CPU cores",
            reasoning="Source: Database System Concepts Ch16 - Parallel Query Execution splits large operations (Scan, Sort, Join) across multiple processors to reduce response time",
            priority="HIGH",
            expected_improvement="Linear speedup proportional to available CPU cores",
            applies_to="execution_parallelism"
        ))

    # ── Partition Rules ──

    @Rule(Fact(table=MATCH.t, partitioned=True) & Fact(partition_key_used=True))
    def rule_partition_pruning(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="PARTITION_OPTIMIZATION",
            recommendation_text="Use Partition Pruning to eliminate irrelevant partitions based on query predicates",
            reasoning="Source: Database System Concepts Ch16 - Partition Pruning reduces I/O by scanning only the relevant partitions matching the WHERE clause",
            priority="HIGH",
            expected_improvement="Skip up to 90% of irrelevant partitions",
            applies_to="partition_access"
        ))

    @Rule(Fact(table=MATCH.t, partitioned=True) & NOT(Fact(partition_key_used=True)))
    def rule_partition_key_missing(self):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="PARTITION_OPTIMIZATION",
            recommendation_text="Query does not use the partition key - consider including it in WHERE to enable Partition Pruning",
            reasoning="Source: Database System Concepts Ch16 - Without the partition key in WHERE, all partitions must be scanned",
            priority="MEDIUM",
            expected_improvement="Enable partition pruning to skip irrelevant partitions",
            applies_to="partition_access"
        ))
