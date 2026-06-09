from experta import Fact

def case_simple_select():
    return [
        Fact(select_star=True),
        Fact(where=True),
        Fact(limit=True),
        Fact(equality_predicate=True),

        Fact(table="employees", large=True),
        Fact(table="employees", tuples=1000000),
        Fact(table="employees", stats_fresh=True),
        Fact(table="employees", data_known=True),
        Fact(table="employees", pk=True),

        Fact(table="employees", index=True),
        Fact(table="employees", selective=True),
        Fact(table="employees", clustered=True),
        Fact(table="employees", on_predicate=True),
        Fact(table="employees", supports_join=True),
        Fact(table="employees", supports_order=True),

        Fact(read_heavy=True),
        Fact(fast_response=True),
        Fact(response_critical=True),
        Fact(temp_allowed=True),

        Fact(cardinality_accurate=True),
        Fact(histogram_available=True),
    ]
