# Architecture Diagrams - Expert System Query Optimizer

---

## Diagram 1: Professional System Architecture
This diagram shows the end-to-end pipeline from the interactive Streamlit interview to the final professional report.

```mermaid
flowchart TB
    User(["User"]) --> Streamlit["Streamlit Web UI (Chat-based Glassmorphism)"]
    Streamlit --> Q["Interactive Questionnaire (44 Questions, Conditional)"]
    Q --> V["Validation Layer (10 Consistency Checks)"]
    
    V -->|"Inconsistent"| Q
    V -->|"Consistent"| FB["Fact Builder (61+ Facts, Table-Qualified + Derived + Cardinality)"]
    
    FB --> IE["Inference Engine (Experta - Rete Algorithm)"]
    
    subgraph KB["Knowledge Base (68 Rule Groups)"]
        R1["Join Rules (Hash/Merge/Nested-Loop/Semi/Anti/Adaptive)"]
        R2["Index Rules (Filter/Join/Composite/Fragmented/Unused/FK/Clustered/Range/Covering)"]
        R3["Subquery/CTE Rules (Exists/IN/NOT IN/Correlated/Materialization/Merge)"]
        R4["Aggregation Rules (Group By/Summary Tables/Having/Filter Pushdown)"]
        R5["Stats Rules (Up-to-date/Histogram/Cardinality/Data Distribution)"]
        R6["Partition Rules (Pruning/Key Usage/Review)"]
        R7["Wildcard/DataType Rules (Leading Wildcard/Appropriate Types)"]
        R8["Cursor/Stored Proc Rules (Set-based Rewrite/Pre-compiled Logic)"]
        R9["Denormalization Rules (Excessive Joins/Schema Refactoring)"]
        R10["Workload Rules (Read-heavy/Write-heavy/Tradeoff/Parallel/Work-Table)"]
        R11["EXPLAIN Rules (Join/Subquery/Aggregation with WHERE)"]
        R12["Scan Selection Rules (Index Scan/Full Scan/Small Table Scan)"]
    end
    
    KB --> IE
    IE --> RF["RecommendationFact Generation (Category/Priority/Reasoning/Impact)"]
    
    RF --> RG["Professional Report Generator"]
    
    RG --> Out["Final Report: Query Profile / Generated Facts / Strengths / Execution Summary / Recommendations / Priority Action Plan / Sources"]
```

**Description:** The system starts with a Streamlit web UI featuring dark glassmorphism design. A conditional 44-question interview passes through 10 validation checks, maps answers to 61+ facts (including table-qualified `Fact(table=t1, large=True)`, derived join algorithm facts, and cardinality facts), and uses the Rete algorithm to fire 68 rule groups from the knowledge base. The final report includes a query profile, generated facts, optimization strengths, recommendations with priority/impact, and a sorted priority action plan.

---

## Diagram 2: Conditional Questioning Flow
This diagram illustrates how the system avoids irrelevant questions to create an "intelligent" interview experience.

```mermaid
flowchart TD
    Start([Start Interview]) --> Q1{Join Operations?}
    
    Q1 -->|No| SkipJoin["Skip 5 Join Detail Questions (Size, Equality, Indexing, Sorted)"]
    Q1 -->|Yes| JoinQ["Ask Join Detail (both_large, one_smaller, equality, indexed, sorted)"]
    
    SkipJoin --> Q2{Subqueries?}
    JoinQ --> Q2
    
    Q2 -->|No| SkipSub["Skip 4 Subquery Questions (EXISTS, IN, NOT IN, Correlated)"]
    Q2 -->|Yes| SubQ["Ask Subquery Operators (EXISTS, IN, NOT IN, Correlated)"]
    
    SkipSub --> Q3{Partitioned?}
    SubQ --> Q3
    
    Q3 -->|No| SkipPart["Skip Partition Key Question"]
    Q3 -->|Yes| PartQ["Ask Partition Key Usage"]
    
    SkipPart --> Q4["Index on Join? (only if JOIN=Yes)"]
    PartQ --> Q4
    
    Q4 --> End

    End --> V["10 Validation Checks\n- small + both_large\n- no joins + join details\n- no subqueries + subquery ops\n- no partition + key used\n- no order_by + data_sorted\n- small + excessive_joins\n- no union + union_all\n- small + parallel + critical\n- write-heavy + no indexes\n- no joins + excessive_joins"]
```

**Description:** To improve user experience, the system uses conditional logic with `depends_on` tuples. If a primary feature is absent, all dependent sub-questions are skipped. The validation layer then runs 10 consistency checks before facts are built.

---

## Diagram 3: The Validation Process
How the system ensures that the provided facts are logically consistent.

```mermaid
flowchart TD
    A["Collected Answers"] --> B{"Consistency Check"}
    
    B --> C1["Table Small AND Both Joined Large?"]
    C1 -->|Yes| W1["Warning: Size Contradiction"]
    
    B --> C2["Join=No AND Join Info Provided?"]
    C2 -->|Yes| W2["Warning: Join Logic Error"]
    
    B --> C3["Partitioned=No AND Key Used=Yes?"]
    C3 -->|Yes| W3["Warning: Partition Logic Error"]
    
    B --> C4["Order By=No AND Data Sorted=Yes?"]
    C4 -->|Yes| W4["Warning: Order Logic Error"]
    
    B --> C5["Table Small AND Excessive Joins?"]
    C5 -->|Yes| W5["Warning: Size/Complexity Mismatch"]
    
    B --> C6["Union=No AND Union All=Yes?"]
    C6 -->|Yes| W6["Warning: Union Logic Error"]
    
    B --> C7["Small Table AND Parallel + Critical?"]
    C7 -->|Yes| W7["Warning: Parallel Unnecessary"]
    
    B --> C8["Write-heavy AND No Filter Indexes?"]
    C8 -->|Yes| W8["Warning: Index Tradeoff"]
    
    B --> C9["No Joins AND Excessive Joins?"]
    C9 -->|Yes| W9["Warning: Join Contradiction"]
    
    W1 --> Choice
    W2 --> Choice
    W3 --> Choice
    W4 --> Choice
    W5 --> Choice
    W6 --> Choice
    W7 --> Choice
    W8 --> Choice
    W9 --> Choice
    
    C1 -->|No| Choice
    C2 -->|No| Choice
    C3 -->|No| Choice
    C4 -->|No| Choice
    C5 -->|No| Choice
    C6 -->|No| Choice
    C7 -->|No| Choice
    C8 -->|No| Choice
    C9 -->|No| Choice
    
    Choice{"User Choice"}
    Choice -->|"Correct Answers"| A
    Choice -->|"Continue Anyway"| FB["Build 61+ Facts (Table-Qualified + Derived + Cardinality)"]
```

**Description:** The validation layer now contains 10 contradiction checks. Each detected inconsistency produces a specific warning. The user can either correct answers or proceed — preventing the inference engine from processing contradictory data.

---

## Diagram 4: Final Decision Assembly (Updated)
Mapping the updated rule categories to the final output.

```mermaid
flowchart LR
    subgraph Inputs["Input Facts (61+)"]
        F1["Query Facts (Join/Subquery/CTE/Union/etc.)"]
        F2["Table Facts (size=large, partitioned, table=t1, large=True)"]
        F3["Index Facts (filter/join/fragmented/composite/unused/FK/range/covering)"]
        F4["Stats/Workload Facts (stats_fresh, read_heavy, parallel, temp_allowed, cardinality)"]
        F5["Derived Facts (hash_join_possible, semi_join_possible, selective, supports_order, where)"]
    end
    
    subgraph Rules["Knowledge Base (68 Rule Groups)"]
        R1["Filter/Join Index Opt (Create indexes, avoid full scan, covering)"]
        R2["Group By / Distinct Opt (Summary tables, index distinct cols)"]
        R3["Join Strategy (Hash/Merge/Nested-Loop/Semi/Adaptive selection)"]
        R4["Subquery/CTE Rewrite (Materialization, semi-join/anti-join rewrite)"]
        R5["Partition/Stats Opt (Pruning, histograms, cardinality, data distribution)"]
        R6["Query Rewrite (OR->UNION ALL, SELECT*, HAVING->WHERE, NOT IN->NOT EXISTS)"]
        R7["Wildcard/DataType/Cursor (Avoid leading %, set-based rewrite)"]
        R8["Denormalization/Excessive Joins (Schema refactoring, reduce JOIN count)"]
        R9["Workload Tuning (Read vs Write tradeoff, Parallel/Work-Table, write-heavy guards)"]
        R10["EXPLAIN Analysis (Join/Subquery/Aggregation with WHERE clause)"]
        R11["Scan Selection (Index Scan/Full Scan/Small Table Scan)"]
        R12["Pagination (LIMIT/OFFSET with index, ORDER BY index)"]
    end
    
    subgraph Output["Report Sections"]
        S1["Query Profile & Generated Facts"]
        S2["Optimization Strengths"]
        S3["Recommendations (with Priority + Impact)"]
        S4["Priority Action Plan (HIGH->MEDIUM->LOW)"]
        S5["Sources Referenced"]
    end
    
    Inputs --> Rules
    Rules --> S1
    Rules --> S2
    Rules --> S3
    Rules --> S4
    Rules --> S5
```

**Description:** The updated assembly shows 61+ input facts including table-qualified, derived join-algorithm facts, derived selectivity/ordering facts, and cardinality facts, feeding into 68 rule groups across 25 categories. The output now includes a full query profile, recommendations with priority/impact, and a sorted priority action plan.

---

## Diagram 5: Complete Expert System Lifecycle
The high-level view of the project's operational cycle.

```mermaid
flowchart LR
    Step1["Streamlit Interview (44 Conditional Questions)"] --> Step2["Validate & Build Facts (10 Checks to 61+ Facts)"]
    Step2 --> Step3["Inference Engine (Experta Rete Algorithm, 68 Rules, 25 Categories)"]
    Step3 --> Step4["Report Generation (Prioritized Action Plan)"]
    Step4 --> Step5["DBA Implementation"]
    Step5 -.->|"Feedback"| Step1
```

**Description:** The lifecycle begins with a Streamlit web-based interview. The feedback loop allows the DBA to refine answers based on real-world implementation results, creating a continuous improvement cycle.
