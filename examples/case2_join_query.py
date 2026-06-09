from experta import Fact

def case_join_query():
    return [
        Fact(select_star=True),
        Fact(where=True),
        Fact(join=True),
        Fact(equality_predicate=True),
        Fact(multi_column_predicate=True),

        Fact(table="orders", large=True),
        Fact(table="orders", tuples=500000),
        Fact(table="orders", pk=True),
        Fact(table="orders", fk=True),
        Fact(table="orders", stats_fresh=True),
        Fact(table="orders", data_known=True),
        Fact(table="orders", fits_mem=False),

        Fact(table="orders", index=True),
        Fact(table="orders", clustered=True),
        Fact(table="orders", supports_order=True),
        Fact(table="orders", card_high=True),

        Fact(table="customers", small=True),
        Fact(table="customers", tuples=50000),
        Fact(table="customers", pk=True),
        Fact(table="customers", stats_fresh=True),
        Fact(table="customers", data_known=True),
        Fact(table="customers", fits_mem=True),

        Fact(table="customers", index=True),
        Fact(table="customers", nonclustered=True),
        Fact(table="customers", on_join=True),
        Fact(table="customers", supports_join=True),

        Fact(table="products", small=True),
        Fact(table="products", tuples=10000),
        Fact(table="products", pk=True),
        Fact(table="products", stats_fresh=False),
        Fact(table="products", data_known=False),
        Fact(table="products", fits_mem=True),

        Fact(nested_loop_possible=True),
        Fact(hash_join_possible=True),
        Fact(merge_join_possible=True),
        Fact(sort_merge_ok=True),
        Fact(hash_build_ok=True),
        Fact(one_small=True),
        Fact(join_equality=True),
        Fact(join_ordering_possible=True),

        Fact(has_small_table=True),
        Fact(indexes_healthy=True),
        Fact(read_heavy=True),
        Fact(temp_allowed=True),
        Fact(batch=True),

        Fact(stats_outdated=True),
        Fact(intermediate_large=True),
        Fact(cardinality_inaccurate=True),
        Fact(histogram_available=False),
    ]
