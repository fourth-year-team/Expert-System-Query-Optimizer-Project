from engine.facts import *

def case_subquery():
    query = QueryFact(
        query_type="SELECT_SUBQUERY",
        predicate_type="IN_subquery",
        has_subquery=True,
        has_group_by=False,
        has_order_by=False,
        has_distinct=False,
        has_limit_offset=False,
        uses_exists=False,
        uses_in=True,
        uses_not_in=False,
        uses_union=False,
        uses_union_all=False,
        select_list_wide=False,
        select_list_minimal=True,
        has_where_clause=True,
        has_having_clause=False,
        has_join_condition=False,
        has_correlated_subquery=True,
        has_aggregation=False,
        has_or_condition=False,
        number_of_tables=2,
        number_of_predicates=2
    )

    tables = [
        TableFact(
            relation_name="employees",
            tuples_count=100000,
            blocks_count=2000,
            tuple_size=256,
            blocking_factor=50,
            statistics_fresh=True,
            data_distribution_known=True,
            relation_fits_in_memory=False,
            distinct_values=80000,
            has_null_values=False,
            has_primary_key=True,
            has_foreign_key=True,
            is_small_table=False,
            is_large_table=False,
            rows_per_block=50,
            total_size_mb=25.0,
            selectivity_estimate=0.01,
            most_selective_column="employee_id"
        ),
        TableFact(
            relation_name="departments",
            tuples_count=500,
            blocks_count=10,
            tuple_size=128,
            blocking_factor=100,
            statistics_fresh=True,
            data_distribution_known=True,
            relation_fits_in_memory=True,
            distinct_values=500,
            has_null_values=False,
            has_primary_key=True,
            has_foreign_key=False,
            is_small_table=True,
            is_large_table=False,
            rows_per_block=100,
            total_size_mb=0.5,
            selectivity_estimate=0.002,
            most_selective_column="department_id"
        )
    ]

    indexes = [
        IndexFact(
            relation_name="employees",
            column_name="employee_id",
            has_index=True,
            index_type="B+TREE",
            index_selectivity_high=True,
            index_supports_join=True,
            index_supports_order_by=True,
            index_fragmented=True,
            index_unused=False,
            index_covering=False,
            index_clustered=True,
            index_nonclustered=False,
            index_on_predicate_column=False,
            index_on_join_column=True,
            index_cardinality_high=True,
            index_usage_count=10000,
            composite_index_exists=False,
            index_columns_count=1
        ),
        IndexFact(
            relation_name="departments",
            column_name="department_id",
            has_index=True,
            index_type="B+TREE",
            index_selectivity_high=True,
            index_supports_join=True,
            index_supports_order_by=True,
            index_fragmented=False,
            index_unused=False,
            index_covering=False,
            index_clustered=True,
            index_nonclustered=False,
            index_on_predicate_column=True,
            index_on_join_column=True,
            index_cardinality_high=True,
            index_usage_count=500,
            composite_index_exists=False,
            index_columns_count=1
        )
    ]

    joins = []

    workload = WorkloadFact(
        need_fast_response=True,
        read_heavy_workload=True,
        write_heavy_workload=True,
        need_sorted_output=False,
        need_no_duplicates=True,
        temp_table_allowed=True,
        temporary_index_allowed=True,
        query_execution_frequency="HIGH",
        response_time_critical=True,
        batch_processing=False,
        memory_constrained=False,
        disk_space_limited=False,
        concurrent_users_high=True
    )

    stats = StatsFact(
        cost_estimate_available=True,
        stats_are_outdated=False,
        estimated_rows=500,
        estimated_cost=5.0,
        intermediate_result_large=False,
        most_selective_predicate="department_id IN (SELECT ...)",
        best_candidate_plan="Nested Loop Semi Join",
        actual_execution_time_ms=45.0,
        estimated_io_cost=3.0,
        estimated_cpu_cost=2.0,
        cardinality_estimate_accurate=True,
        histogram_available=True,
        sampling_freshness_pct=90.0
    )

    return query, tables, indexes, joins, workload, stats
