from engine.facts import *

def case_aggregation():
    query = QueryFact(
        query_type="SELECT_AGGREGATE",
        predicate_type="range",
        has_subquery=False,
        has_group_by=True,
        has_order_by=True,
        has_distinct=True,
        has_limit_offset=False,
        uses_exists=False,
        uses_in=False,
        uses_not_in=False,
        uses_union=False,
        uses_union_all=False,
        select_list_wide=False,
        select_list_minimal=True,
        has_where_clause=False,
        has_having_clause=True,
        has_join_condition=False,
        has_correlated_subquery=False,
        has_aggregation=True,
        has_or_condition=False,
        number_of_tables=1,
        number_of_predicates=2
    )

    tables = [
        TableFact(
            relation_name="sales",
            tuples_count=10000000,
            blocks_count=200000,
            tuple_size=64,
            blocking_factor=150,
            statistics_fresh=False,
            data_distribution_known=False,
            relation_fits_in_memory=False,
            distinct_values=5000000,
            has_null_values=True,
            has_primary_key=False,
            has_foreign_key=True,
            is_small_table=False,
            is_large_table=True,
            rows_per_block=150,
            total_size_mb=640.0,
            selectivity_estimate=0.05,
            most_selective_column="sale_date"
        )
    ]

    indexes = [
        IndexFact(
            relation_name="sales",
            column_name="sale_date",
            has_index=True,
            index_type="B+TREE",
            index_selectivity_high=True,
            index_supports_join=False,
            index_supports_order_by=True,
            index_fragmented=False,
            index_unused=False,
            index_covering=False,
            index_clustered=True,
            index_nonclustered=False,
            index_on_predicate_column=True,
            index_on_join_column=False,
            index_cardinality_high=True,
            index_usage_count=800,
            composite_index_exists=True,
            index_columns_count=2
        ),
        IndexFact(
            relation_name="sales",
            column_name="region_id",
            has_index=True,
            index_type="NON_CLUSTERED",
            index_selectivity_high=False,
            index_supports_join=True,
            index_supports_order_by=False,
            index_fragmented=False,
            index_unused=True,
            index_covering=False,
            index_clustered=False,
            index_nonclustered=True,
            index_on_predicate_column=False,
            index_on_join_column=True,
            index_cardinality_high=False,
            index_usage_count=5,
            composite_index_exists=False,
            index_columns_count=1
        )
    ]

    joins = []

    workload = WorkloadFact(
        need_fast_response=False,
        read_heavy_workload=True,
        write_heavy_workload=False,
        need_sorted_output=True,
        need_no_duplicates=True,
        temp_table_allowed=True,
        temporary_index_allowed=False,
        query_execution_frequency="LOW",
        response_time_critical=False,
        batch_processing=True,
        memory_constrained=True,
        disk_space_limited=False,
        concurrent_users_high=False
    )

    stats = StatsFact(
        cost_estimate_available=True,
        stats_are_outdated=True,
        estimated_rows=500000,
        estimated_cost=500.0,
        intermediate_result_large=True,
        most_selective_predicate="sale_date BETWEEN ? AND ?",
        best_candidate_plan="Hash Match (Aggregate)",
        actual_execution_time_ms=15000.0,
        estimated_io_cost=350.0,
        estimated_cpu_cost=150.0,
        cardinality_estimate_accurate=False,
        histogram_available=False,
        sampling_freshness_pct=20.0
    )

    return query, tables, indexes, joins, workload, stats
