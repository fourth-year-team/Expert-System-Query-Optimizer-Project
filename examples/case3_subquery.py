from experta import Fact

def case_subquery():
    return [
        Fact(select_minimal=True),
        Fact(where=True),
        Fact(subquery=True),
        Fact(correlated_subquery=True),
        Fact(in_operator=True),

        Fact(table="employees", tuples=100000),
        Fact(table="employees", pk=True),
        Fact(table="employees", fk=True),
        Fact(table="employees", stats_fresh=True),
        Fact(table="employees", data_known=True),

        Fact(table="employees", index=True),
        Fact(table="employees", selective=True),
        Fact(table="employees", clustered=True),
        Fact(table="employees", supports_join=True),
        Fact(table="employees", supports_order=True),
        Fact(table="employees", fragmented=True),
        Fact(table="employees", card_high=True),

        Fact(table="departments", small=True),
        Fact(table="departments", tuples=500),
        Fact(table="departments", pk=True),
        Fact(table="departments", stats_fresh=True),
        Fact(table="departments", data_known=True),
        Fact(table="departments", fits_mem=True),

        Fact(table="departments", index=True),
        Fact(table="departments", on_predicate=True),
        Fact(table="departments", on_join=True),
        Fact(table="departments", selective=True),
        Fact(table="departments", clustered=True),
        Fact(table="departments", supports_join=True),
        Fact(table="departments", supports_order=True),
        Fact(table="departments", card_high=True),

        Fact(semi_join_possible=True),

        Fact(read_heavy=True),
        Fact(write_heavy=True),
        Fact(fast_response=True),
        Fact(response_critical=True),
        Fact(no_dups=True),
        Fact(temp_allowed=True),

        Fact(cardinality_accurate=True),
        Fact(histogram_available=True),
    ]
