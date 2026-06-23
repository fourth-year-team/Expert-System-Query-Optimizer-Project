def validate_answers(answers):
    inconsistencies = []

    if answers.get('table_size') == 'small' and answers.get('both_large'):
        inconsistencies.append("Table is marked as 'small', but 'both joined tables' are marked as 'large'.")

    if not answers.get('join_ops') and (answers.get('both_large') or answers.get('one_smaller') or answers.get('join_equality') or answers.get('join_indexed') or answers.get('data_sorted')):
        inconsistencies.append("Join operations marked as 'No', but join-specific details were provided.")

    if not answers.get('subqueries') and (answers.get('exists') or answers.get('in') or answers.get('not_in') or answers.get('correlated_subquery')):
        inconsistencies.append("Subqueries marked as 'No', but subquery-specific operators (EXISTS/IN/NOT IN/correlated) were answered.")

    if not answers.get('partitioned') and answers.get('partition_key_used'):
        inconsistencies.append("Table is not partitioned, but 'Partition Key Used' is marked as 'Yes'.")

    if not answers.get('order_by') and answers.get('data_sorted'):
        inconsistencies.append("ORDER BY marked as 'No', but 'Data already sorted' is marked as 'Yes'.")

    if answers.get('table_size') == 'small' and answers.get('excessive_joins'):
        inconsistencies.append("Table is marked as 'small', but '3+ tables joined' suggests a complex query relative to table size.")

    if not answers.get('union') and answers.get('union_all'):
        inconsistencies.append("UNION marked as 'No', but UNION ALL was answered.")

    if answers.get('table_size') == 'small' and answers.get('parallel_available') and answers.get('result_critical'):
        inconsistencies.append("Table is 'small' — parallel execution is unlikely to improve performance for small tables.")

    if answers.get('workload') == 'write-heavy' and answers.get('index_filter') == False:
        inconsistencies.append("Write-heavy workload with no filter indexes: creating new indexes improves reads but slows writes — review tradeoffs.")

    return inconsistencies
