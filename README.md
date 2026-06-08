# Expert System Query Optimizer

A knowledge-based expert system for SQL query optimization using Python and the Experta library. The system analyzes query characteristics, table statistics, index information, and workload patterns to provide intelligent optimization recommendations.

## Project Structure

```
├── main.py                    # Entry point - runs all test cases
├── README.md                  # This file
├── requirements.txt           # Dependencies
│
├── engine/                    # Core engine
│   ├── facts.py              # Fact classes (7 categories)
│   ├── rules.py              # Optimization rules (30 rules)
│   └── optimizer.py          # Main optimizer class
│
├── knowledge_base/           # Knowledge base documentation
│   └── source_references.py  # Reference sources
│
├── examples/                 # Test cases
│   ├── case1_simple_select.py
│   ├── case2_join_query.py
│   ├── case3_subquery.py
│   └── case4_aggregation.py
│
└── docs/                     # Documentation
    ├── report.md             # Academic report (Arabic)
    └── diagrams.md           # 20 Mermaid architecture diagrams
```

## Requirements

- Python 3.8+
- experta 1.9.4

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Run all test cases:

```bash
python main.py
```

This will execute 4 test cases and display optimization recommendations with full reasoning.

## Knowledge Base

The system uses 7 fact categories:
1. **QueryFact** - SQL query properties
2. **TableFact** - Table statistics and characteristics
3. **IndexFact** - Index information and usage
4. **JoinFact** - Join characteristics
5. **WorkloadFact** - Workload preferences
6. **StatsFact** - Cost and statistics information
7. **RecommendationFact** - Output recommendations

## Rules

30 rules covering all major optimization decisions:
- Full Scan vs Index Scan
- Push Selection/Projection down
- Join algorithm selection (NLJ, Hash, Merge)
- Join order optimization
- Subquery rewriting
- WHERE vs HAVING
- DISTINCT optimization
- EXISTS vs IN
- Index suggestions and maintenance
- Statistics freshness
- Intermediate result reduction
- Workload-based strategies

## Academic References

1. **Database System Concepts** - Silberschatz, Korth, Sudarshan (Ch. 16)
2. **Query Optimization Techniques in Microsoft SQL Server** - dbjournal.ro
3. **Optimizing SQL Query Performance** - Medium Guide

## Documentation

- `docs/report.md` - Full academic report in Arabic
- `docs/diagrams.md` - 20 Mermaid flowcharts with explanations

## License

Academic project - free to use for educational purposes.
