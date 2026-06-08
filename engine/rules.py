from experta import *
from engine.facts import *

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

    @Rule(
        TableFact(is_large_table=True),
        IndexFact(has_index=False),
        NOT(IndexFact(has_index=True))
    )
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

    @Rule(
        IndexFact(has_index=True, index_selectivity_high=True),
        TableFact(is_large_table=True)
    )
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

    @Rule(
        QueryFact(has_where_clause=True),
        AND(
            QueryFact(has_subquery=True),
            QueryFact(has_join_condition=True)
        )
    )
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

    @Rule(
        QueryFact(select_list_wide=True)
    )
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

    @Rule(
        JoinFact(nested_loop_possible=True, one_relation_small=True),
        IndexFact(has_index=True, index_supports_join=True)
    )
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

    @Rule(
        JoinFact(hash_join_possible=True, both_relations_large=True),
        WorkloadFact(memory_constrained=False)
    )
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

    @Rule(
        JoinFact(merge_join_possible=True),
        AND(
            QueryFact(has_order_by=True),
            JoinFact(sort_merge_cost_acceptable=True)
        )
    )
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

    @Rule(
        JoinFact(join_ordering_possible=True),
        TableFact(is_small_table=True)
    )
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

    @Rule(
        QueryFact(has_subquery=True, has_correlated_subquery=True),
        NOT(QueryFact(has_aggregation=True)),
        QueryFact(has_distinct=False)
    )
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

    @Rule(
        QueryFact(uses_in=True),
        NOT(QueryFact(has_distinct=True)),
        AND(
            QueryFact(has_subquery=True),
            NOT(QueryFact(has_correlated_subquery=False))
        )
    )
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

    @Rule(
        QueryFact(has_having_clause=True, has_where_clause=False),
        QueryFact(has_aggregation=True)
    )
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

    @Rule(
        QueryFact(has_distinct=True),
        TableFact(has_primary_key=True)
    )
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

    @Rule(
        IndexFact(has_index=False),
        TableFact(is_large_table=True)
    )
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

    @Rule(
        QueryFact(number_of_predicates=MATCH),
        QueryFact(predicate_type="multi_column"),
        IndexFact(has_index=True, composite_index_exists=False),
        TableFact(is_large_table=True)
    )
    def rule_composite_index_suggestion(self, number_of_predicates):
        self.record(RecommendationFact(
            recommendation_id=next_id(),
            category="INDEX_SUGGESTION",
            recommendation_text="Suggest creating a Composite Index on columns used together in WHERE",
            reasoning="Source: Database System Concepts Ch16 - Composite Index improves queries using multiple columns in the condition",
            priority="MEDIUM",
            expected_improvement="Speed up multi-condition queries",
            applies_to="index_creation"
        ))

    @Rule(
        IndexFact(has_index=True, index_unused=True)
    )
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

    @Rule(
        IndexFact(has_index=True, index_fragmented=True)
    )
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

    @Rule(
        StatsFact(stats_are_outdated=True)
    )
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

    @Rule(
        StatsFact(intermediate_result_large=True)
    )
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

    @Rule(
        QueryFact(select_list_wide=True),
        NOT(QueryFact(select_list_minimal=True))
    )
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

    @Rule(
        QueryFact(uses_union=True),
        NOT(QueryFact(uses_union_all=True))
    )
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

    @Rule(
        QueryFact(select_list_minimal=True),
        IndexFact(has_index=True, index_covering=True)
    )
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

    @Rule(
        QueryFact(has_or_condition=True)
    )
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

    @Rule(
        TableFact(is_small_table=True),
        IndexFact(has_index=True)
    )
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

    @Rule(
        TableFact(statistics_fresh=True, data_distribution_known=False),
        StatsFact(histogram_available=False)
    )
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

    @Rule(
        WorkloadFact(need_fast_response=True, response_time_critical=True),
        QueryFact(has_order_by=True)
    )
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

    @Rule(
        QueryFact(has_limit_offset=True, has_order_by=True),
        IndexFact(has_index=True, index_supports_order_by=True)
    )
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

    @Rule(
        JoinFact(hash_join_possible=True, join_condition_equality=True),
        IndexFact(has_index=False)
    )
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

    @Rule(
        QueryFact(has_subquery=True, has_correlated_subquery=True),
        WorkloadFact(temp_table_allowed=True),
        QueryFact(has_aggregation=True)
    )
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

    @Rule(
        QueryFact(uses_not_in=True),
        QueryFact(has_subquery=True)
    )
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

    @Rule(
        QueryFact(predicate_type="range"),
        IndexFact(has_index=True, index_clustered=False)
    )
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

    @Rule(
        QueryFact(has_where_clause=True, has_subquery=False),
        IndexFact(has_index=True, index_on_predicate_column=True)
    )
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

    @Rule(
        TableFact(has_foreign_key=True),
        IndexFact(has_index=True, index_on_join_column=False)
    )
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

    @Rule(
        WorkloadFact(read_heavy_workload=True, write_heavy_workload=False),
        IndexFact(has_index=True, index_unused=False, index_fragmented=False)
    )
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

    @Rule(
        WorkloadFact(write_heavy_workload=True, read_heavy_workload=False)
    )
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

    @Rule(
        StatsFact(histogram_available=False, stats_are_outdated=False)
    )
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

    @Rule(
        QueryFact(has_limit_offset=True),
        QueryFact(has_order_by=False)
    )
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
