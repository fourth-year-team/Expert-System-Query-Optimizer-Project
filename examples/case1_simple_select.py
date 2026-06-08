from engine.facts import *

def case_simple_select():
    query = QueryFact(
        query_type="SELECT",
        predicate_type="equality",
        has_subquery=False,
        has_group_by=False,
        has_order_by=False,
        has_distinct=False,
        has_limit_offset=True,
        uses_exists=False,
        uses_in=False,
        uses_not_in=False,
        uses_union=False,
        uses_union_all=False,
        select_list_wide=True,
        select_list_minimal=False,
        has_where_clause=True,
        has_having_clause=False,
        has_join_condition=False,
        has_correlated_subquery=False,
        has_aggregation=False,
        has_or_condition=False,
        number_of_tables=1,
        number_of_predicates=1
    )

    tables = [
        TableFact(
            relation_name="employees",
            tuples_count=1000000,
            blocks_count=20000,
            tuple_size=256,
            blocking_factor=50,
            statistics_fresh=True,
            data_distribution_known=True,
            relation_fits_in_memory=False,
            distinct_values=500000,
            has_null_values=False,
            has_primary_key=True,
            has_foreign_key=False,
            is_small_table=False,
            is_large_table=True,
            rows_per_block=50,
            total_size_mb=250.0,
            selectivity_estimate=0.001,
            most_selective_column="employee_id"
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
            index_fragmented=False,
            index_unused=False,
            index_covering=False,
            index_clustered=True,
            index_nonclustered=False,
            index_on_predicate_column=True,
            index_on_join_column=False,
            index_cardinality_high=True,
            index_usage_count=1000,
            composite_index_exists=False,
            index_columns_count=1
        )
    ]

    joins = []
    workload = WorkloadFact(
        need_fast_response=True,
        read_heavy_workload=True,
        write_heavy_workload=False,
        need_sorted_output=False,
        need_no_duplicates=False,
        temp_table_allowed=True,
        temporary_index_allowed=False,
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
        estimated_rows=1000,
        estimated_cost=0.5,
        intermediate_result_large=False,
        most_selective_predicate="employee_id = ?",
        best_candidate_plan="Index Seek",
        actual_execution_time_ms=12.0,
        estimated_io_cost=0.3,
        estimated_cpu_cost=0.2,
        cardinality_estimate_accurate=True,
        histogram_available=True,
        sampling_freshness_pct=95.0
    )

    return query, tables, indexes, joins, workload, stats
