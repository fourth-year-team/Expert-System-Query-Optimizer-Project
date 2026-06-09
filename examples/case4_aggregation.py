from experta import Fact

def case_aggregation():
    return [
        Fact(select_minimal=True),
        Fact(range_predicate=True),
        Fact(group_by=True),
        Fact(order_by=True),
        Fact(distinct=True),
        Fact(having=True),
        Fact(aggregation=True),

        Fact(table="sales", large=True),
        Fact(table="sales", tuples=10000000),
        Fact(table="sales", fk=True),
        Fact(table="sales", has_null=True),
        Fact(table="sales", stats_fresh=False),
        Fact(table="sales", data_known=False),
        Fact(table="sales", fits_mem=False),

        Fact(table="sales", index=True),
        Fact(table="sales", selective=True),
        Fact(table="sales", clustered=True),
        Fact(table="sales", supports_order=True),
        Fact(table="sales", on_predicate=True),
        Fact(table="sales", card_high=True),
        Fact(table="sales", composite=True),

        Fact(table="sales", index=True),
        Fact(table="sales", nonclustered=True),
        Fact(table="sales", on_join=True),
        Fact(table="sales", unused=True),

        Fact(read_heavy=True),
        Fact(need_sorted=True),
        Fact(no_dups=True),
        Fact(temp_allowed=True),
        Fact(memory_constrained=True),
        Fact(batch=True),

        Fact(stats_outdated=True),
        Fact(intermediate_large=True),
        Fact(cardinality_inaccurate=True),
        Fact(histogram_available=False),
    ]
