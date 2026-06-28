from experta import Fact

def build_facts(answers):
    facts = []

    table = "t1"

    # ── Query Structure Facts ──
    if answers.get('join_ops'): facts.append(Fact(join=True))
    if answers.get('subqueries'): facts.append(Fact(subquery=True))
    if answers.get('group_by'): facts.append(Fact(aggregation=True))
    if answers.get('order_by'): facts.append(Fact(order_by=True))
    if answers.get('distinct'): facts.append(Fact(distinct=True))
    if answers.get('exists'): facts.append(Fact(exists=True))
    if answers.get('in'): facts.append(Fact(in_operator=True))
    if answers.get('not_in'): facts.append(Fact(not_in=True))
    if answers.get('cte'): facts.append(Fact(cte=True))
    if answers.get('union'): facts.append(Fact(union=True))
    if answers.get('union_all'): facts.append(Fact(union_all=True))
    if answers.get('having'): facts.append(Fact(having=True))
    if answers.get('limit'): facts.append(Fact(limit=True))
    if answers.get('or_condition'): facts.append(Fact(or_condition=True))
    if answers.get('select_star'): facts.append(Fact(select_star=True))
    if answers.get('select_minimal'): facts.append(Fact(select_minimal=True))

    if answers.get('correlated_subquery'): facts.append(Fact(correlated_subquery=True))
    if answers.get('wildcard_search'): facts.append(Fact(wildcard_like=True))
    if answers.get('cursor_usage'): facts.append(Fact(cursor_used=True))
    if answers.get('stored_procedures'): facts.append(Fact(stored_proc=True))
    if answers.get('excessive_joins'): facts.append(Fact(too_many_joins=True))
    if answers.get('normalized_schema'): facts.append(Fact(schema_normalized=True))
    if answers.get('data_type_issues'): facts.append(Fact(wrong_datatype=True))
    if answers.get('result_critical'): facts.append(Fact(fast_response=True))
    if answers.get('intermediate_large'): facts.append(Fact(intermediate_large=True))
    if answers.get('range_predicate'): facts.append(Fact(range_predicate=True))
    if answers.get('fk_indexed') is not None:
        facts.append(Fact(fk_indexed=answers.get('fk_indexed')))
        facts.append(Fact(fk=True))

    # ── Table Size → Rich Table Facts ──
    ts = answers.get('table_size')
    if ts == 'large':
        facts.append(Fact(table=table, large=True))
        facts.append(Fact(table_size='large'))
    elif ts == 'small':
        facts.append(Fact(table=table, small=True))
        facts.append(Fact(table_size='small'))
    elif ts == 'medium':
        facts.append(Fact(table_size='medium'))

    # ── Partition Facts ──
    if answers.get('partitioned'):
        facts.append(Fact(table=table, partitioned=True))
    if answers.get('partition_key_used'):
        facts.append(Fact(table=table, partition_key_used=True))

    # ── Index Facts ──
    idx_filter = answers.get('index_filter', False)
    idx_join = answers.get('index_join', False) if answers.get('join_ops') else False
    idx_frag = answers.get('index_fragmented', False)
    comp_idx = answers.get('composite_index', False)
    idx_unused = answers.get('index_unused', False)

    facts.append(Fact(index_filter=idx_filter))
    facts.append(Fact(index_join=idx_join))
    facts.append(Fact(index_fragmented=idx_frag))
    facts.append(Fact(composite_index=comp_idx))

    # Map index names to table-based facts for rule matching
    if idx_filter or idx_join or comp_idx:
        facts.append(Fact(table=table, index=True))
        if idx_filter and idx_join:
            facts.append(Fact(table=table, on_join=True))
            facts.append(Fact(table=table, on_predicate=True))

    # Derive covering index: composite index + specific column selection (not SELECT *)
    if comp_idx and not answers.get('select_star', False):
        facts.append(Fact(select_minimal=True))
        facts.append(Fact(table=table, covering=True))

    has_where = answers.get('index_filter') is not None or answers.get('range_predicate') or answers.get('or_condition')
    if has_where:
        facts.append(Fact(where=True))

    if (idx_filter or idx_join) and has_where and ts == 'large':
        facts.append(Fact(table=table, selective=True))

    if answers.get('order_by') and (answers.get('clustered_index') or idx_filter or answers.get('data_sorted')):
        facts.append(Fact(table=table, supports_order=True))

    if comp_idx:
        facts.append(Fact(table=table, composite=True))

    if idx_frag:
        facts.append(Fact(table=table, fragmented=True))

    if idx_unused:
        facts.append(Fact(table=table, unused=True))

    if answers.get('clustered_index'):
        facts.append(Fact(table=table, clustered=True))

    # ── Join Info ──
    if answers.get('join_ops'):
        facts.append(Fact(join_indexed=answers.get('join_indexed', False)))
        facts.append(Fact(join_equality=answers.get('join_equality', False)))

        if answers.get('both_large'): facts.append(Fact(both_large=True))
        if answers.get('one_smaller'): facts.append(Fact(one_smaller=True))

        # Derive join algorithm possibilities
        if answers.get('one_smaller') and idx_filter:
            facts.append(Fact(nested_loop_possible=True))
            facts.append(Fact(table=table, supports_join=True))
            facts.append(Fact(one_small=True))

        if answers.get('both_large'):
            facts.append(Fact(hash_join_possible=True))
            if not answers.get('sufficient_memory', True):
                facts.append(Fact(memory_constrained=True))

        if answers.get('order_by') or answers.get('data_sorted'):
            facts.append(Fact(merge_join_possible=True))
            facts.append(Fact(sort_merge_ok=True))

        if answers.get('subqueries'):
            facts.append(Fact(semi_join_possible=True))

        if answers.get('not_in'):
            facts.append(Fact(anti_join_possible=True))

        if answers.get('both_large') and not answers.get('stats_up_to_date', True):
            facts.append(Fact(adaptive_join_possible=True))

        if answers.get('excessive_joins'):
            facts.append(Fact(join_ordering_possible=True))
            if answers.get('one_smaller'):
                facts.append(Fact(has_small_table=True))

    # ── Statistics ──
    stats_ok = answers.get('stats_up_to_date', True)
    facts.append(Fact(stats_up_to_date=stats_ok))
    facts.append(Fact(histogram_available=answers.get('histogram_available', False)))

    if not stats_ok:
        facts.append(Fact(stats_outdated=True))
    else:
        facts.append(Fact(table=table, stats_fresh=True))

    if answers.get('histogram_available'):
        facts.append(Fact(table=table, data_known=True))

    if stats_ok and answers.get('histogram_available'):
        facts.append(Fact(cardinality_accurate=True))

    # ── Workload ──
    wl = answers.get('workload')
    if wl == 'read-heavy':
        facts.append(Fact(read_heavy=True))
        if not idx_frag and (idx_filter or idx_join or comp_idx):
            facts.append(Fact(indexes_healthy=True))
    elif wl == 'write-heavy':
        facts.append(Fact(write_heavy=True))

    if answers.get('parallel_available'):
        facts.append(Fact(parallel_available=True))

    # ── Misc derived ──
    if answers.get('result_critical') and answers.get('order_by'):
        facts.append(Fact(response_critical=True))

    if answers.get('cte') and answers.get('sufficient_memory', True):
        facts.append(Fact(temp_allowed=True))

    if answers.get('subqueries') and answers.get('sufficient_memory', True) and answers.get('aggregation') or answers.get('correlated_subquery'):
        facts.append(Fact(temp_allowed=True))

    if answers.get('or_condition') and answers.get('index_filter'):
        facts.append(Fact(multi_column_predicate=True))

    if answers.get('pk_used'):
        facts.append(Fact(pk=True))

    return facts
