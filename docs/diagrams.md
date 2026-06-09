# Architecture Diagrams - Expert System Query Optimizer

---

## Diagram 1: General System Architecture

```mermaid
flowchart TB
    A["User Input<br/>(SQL Query Properties)"] --> B["Fact Declaration Layer"]
    B --> C["QueryFact"]
    B --> D["TableFact"]
    B --> E["IndexFact"]
    B --> F["JoinFact"]
    B --> G["WorkloadFact"]
    B --> H["StatsFact"]

    C --> I["Inference Engine<br/>(Experta - Rete Algorithm)"]
    D --> I
    E --> I
    F --> I
    G --> I
    H --> I

    I --> J["Rules Activation"]
    J --> K["RecommendationFact<br/>Generation"]

    K --> L["Report Generator"]
    L --> M["Final Optimization<br/>Recommendations"]
```

**شرح المخطط:** يوضح هذا المخطط البنية العامة للنظام الخبير. تبدأ العملية بإدخال خصائص الاستعلام (نوع الاستعلام، خصائص الجدول، الفهارس، إلخ)، ثم تحويل هذه الخصائص إلى حقائق (Facts) منظمة. تمر هذه الحقائق إلى محرك الاستدلال Experta الذي يطبق خوارزمية Rete لتفعيل القواعد المناسبة. تنتج القواعد توصيات تحسين يتم تجميعها في تقرير نهائي.

---

## Diagram 2: Query Classification and Fact Extraction

```mermaid
flowchart LR
    A["Raw SQL Query"] --> B["Lexical & Syntax Analysis"]
    B --> C{"Query Type?"}
    C -->|"SELECT"| D["Simple Select"]
    C -->|"SELECT + JOIN"| E["Join Query"]
    C -->|"SELECT + SUBQUERY"| F["Subquery Query"]
    C -->|"SELECT + AGGREGATE"| G["Aggregate Query"]
    C -->|"INSERT/UPDATE/DELETE"| H["DML Query"]

    D --> I["QueryFact<br/>Extraction"]
    E --> I
    F --> I
    G --> I
    H --> I

    I --> J["QueryFact: query_type,<br/>predicate_type, has_subquery,<br/>has_group_by, has_distinct, ..."]
```

**شرح المخطط:** يقوم النظام أولاً بتصنيف نوع الاستعلام (SELECT بسيط، JOIN، Subquery، تجميعي، DML). بناءً على التصنيف، يتم استخراج خصائص الاستعلام المختلفة وتحويلها إلى QueryFact. هذا التصنيف المبكر يوجه القواعد التي سيتم تطبيقها لاحقاً.

---

## Diagram 3: Full Scan vs Index Scan Decision

```mermaid
flowchart TD
    A["Scan Decision"] --> B{"Has Index?"}
    B -->|"No"| C["Full Table Scan"]
    B -->|"Yes"| D{"Table Size?"}
    
    D -->|"Small"| E["Full Table Scan<br/>(Index overhead not worth it)"]
    D -->|"Large"| F{"Index Selectivity?"}
    
    F -->|"High<br/>< 5% rows"| G["Index Seek/Scan"]
    F -->|"Low<br/>> 20% rows"| H["Full Table Scan<br/>(Better than random I/O)"]
    
    C --> I["Recommendation Result"]
    E --> I
    G --> I
    H --> I
```

**شرح المخطط:** أحد أهم القرارات في تحسين الاستعلامات هو كيفية الوصول إلى البيانات. يقرر النظام ما إذا كان سيستخدم Full Table Scan أو Index Scan بناءً على:
1. وجود فهرس من عدمه
2. حجم الجدول (صغير أم كبير)
3. درجة انتقائية الفهرس (Selectivity)
يتبع هذا القرار المبادئ المذكورة في Database System Concepts Chapter 16 حول تقدير كلفة الوصول.

---

## Diagram 4: Push Selection Down

```mermaid
flowchart TB
    subgraph "Before Optimization"
        A["π (Project)"] --> B["σ (Selection)"]
        B --> C["⋈ (Join)"]
        C --> D["R1"]
        C --> E["R2"]
    end

    subgraph "After Optimization"
        F["π (Project)"] --> G["⋈ (Join)"]
        G --> H["σ1 (Selection on R1)"]
        G --> I["σ2 (Selection on R2)"]
        H --> J["R1"]
        I --> K["R2"]
    end

    L["Rule: Push σ down the tree"] -.->|"Transformation"| M["Benefit:<br/>Fewer tuples<br/>in JOIN"]
```

**شرح المخطط:** تعتبر قاعدة Push Selection Down من أهم قواعد التحسين الترابطي (Heuristic Optimization). بدلاً من تطبيق شروط الاختيار (WHERE) بعد JOIN، يتم دفعها لأسفل لتُطبق مباشرة على كل جدول قبل JOIN. هذا يقلل عدد الصفوف المشاركة في JOIN بشكل كبير، مما يحسن الأداء. المصدر: Database System Concepts Ch16.3.

---

## Diagram 5: Push Projection Down

```mermaid
flowchart TB
    subgraph "Before"
        A["σ (Selection)"] --> B["π (Project)<br/>all columns"]
        B --> C["R"]
    end

    subgraph "After"
        D["σ (Selection)"] --> E["π (Project)<br/>few columns"]
        E --> F["R"]
    end

    G["Rule: Push π down"] -.-> H["Benefit:<br/>Less data in<br/>pipeline"]
```

**شرح المخطط:** دفع الإسقاط (Projection) للأسفل يقلل عدد الأعمدة التي يتم نقلها بين مراحل تنفيذ الاستعلام. بتطبيق SELECT بأسماء الأعمدة المحددة بدلاً من SELECT * في أقرب وقت ممكن، نقلل عرض الصفوف المنقولة ونحسن استخدام الذاكرة و I/O.

---

## Diagram 6: Join Algorithm Selection

```mermaid
flowchart TD
    A["Join Algorithm Decision"] --> B{"Both relations<br/>large?"}
    
    B -->|"Yes"| C{"Equality Join?"}
    C -->|"Yes"| D["Hash Join<br/>(Best for large unindexed data)"]
    C -->|"No"| E["Nested Loop Join"]
    
    B -->|"No"| F{"One relation<br/>small?"}
    F -->|"Yes"| G{"Index on join<br/>column?"}
    G -->|"Yes"| H["Nested Loop Join<br/>(Index NLJ)"]
    G -->|"No"| I["Hash Join"]
    
    F -->|"No / Equally sized"| J{"Data sorted?"}
    J -->|"Yes"| K["Merge Join<br/>(No extra sort needed)"]
    J -->|"No"| L{"Sort + Merge<br/>cost acceptable?"}
    L -->|"Yes"| M["Merge Join"]
    L -->|"No"| N["Hash Join"]

    A2["Additional Options"] --> O{"Subquery/<br/>Negation?"}
    O -->|"IN / EXISTS"| P["Semi-Join<br/>(Eliminates duplicates early)"]
    O -->|"NOT IN / NOT EXISTS"| Q["Anti-Join<br/>(Efficient negation)"]
    O -->|"No"| R{"Stats accurate?"}
    R -->|"Yes"| S["Standard Join"]
    R -->|"No"| T["Adaptive Join<br/>(Switches mid-execution)"]
```

**شرح المخطط:** اختيار خوارزمية JOIN المناسبة يعتمد على:
- **Nested Loop Join:** مثالي عندما تكون إحدى العلاقات صغيرة والأخرى مفهرسة
- **Hash Join:** الأفضل للعلاقات الكبيرة بدون فهارس (شروط المساواة)
- **Merge Join:** مناسب عندما تكون البيانات مرتبة مسبقاً أو مطلوب ترتيب النتائج
- **Semi-Join:** للاستعلامات التي تستخدم IN/EXISTS — يوقف عند أول تطابق
- **Anti-Join:** للاستعلامات التي تستخدم NOT IN/NOT EXISTS — معالجة فعالة للنفي
- **Adaptive Join:** يختار ديناميكياً بين Hash Join و Nested Loop في منتصف التنفيذ
المصدر: Database System Concepts Ch16.5، dbjournal.ro، Modern DBMS.

---

## Diagram 7: Join Order Optimization

```mermaid
flowchart LR
    A["Tables: R1, R2, R3, R4"] --> B{"Determine sizes"}
    
    B --> C["Size(R1)=100, Size(R2)=1000,<br/>Size(R3)=100000, Size(R4)=10000"]
    
    C --> D["Order by size (ascending)"]
    
    D --> E["R1 × R2 × R3 × R4<br/>= 100 × 1000 × 100000 × 10000"]
    
    E --> F["Smallest first strategy:<br/>((R1 ⋈ R2) ⋈ R3) ⋈ R4"]
    
    F --> G["Intermediate sizes minimized:<br/>Intermediate1 = 100 × 1000 = ~100k<br/>Intermediate2 = ~100k × 100k = ~10B<br/>..."]
    
    H["Benefit:<br/>Less intermediate data"] -.-> G
```

**شرح المخطط:** ترتيب JOINs يؤثر بشكل كبير على كلفة الاستعلام. القاعدة الأساسية هي وضع العلاقات الأصغر أولاً في ترتيب JOIN لتقليل حجم النتائج الوسيطة. Database System Concepts Ch16.5.5 يشرح كيف يمكن استخدام البرمجة الديناميكية لإيجاد أفضل ترتيب JOIN.

---

## Diagram 8: Subquery Rewriting

```mermaid
flowchart TD
    A["Subquery Detected"] --> B{"Correlated?"}
    
    B -->|"Yes"| C{"Has<br/>Aggregation?"}
    C -->|"No"| D["Rewrite as JOIN<br/>(Use Semi-Join semantics)"]
    C -->|"Yes"| E{"Temp table<br/>allowed?"}
    E -->|"Yes"| F["Materialize Subquery<br/>(Avoid N+1 execution)"]
    E -->|"No"| G["Keep subquery<br/>(no better option)"]
    
    B -->|"No"| H{"Uses IN?"}
    H -->|"Yes"| I["Rewrite as EXISTS<br/>(Semi-Join / Early termination)"]
    H -->|"No"| J{"Uses NOT IN?"}
    J -->|"Yes"| K{"NULL possible?"}
    K -->|"Yes"| L["Rewrite as NOT EXISTS<br/>(Anti-Join / Correctness)"]
    K -->|"No"| M["Rewrite as NOT EXISTS<br/>(Anti-Join / Better performance)"]
    J -->|"No"| N{"Has CTE (WITH)?"}
    N -->|"Yes"| O{"Temp table<br/>allowed?"}
    O -->|"Yes"| P["Materialize CTE<br/>(Avoid repeated evaluation)"]
    O -->|"No"| Q["Keep CTE inline"]
    N -->|"No"| R["Keep as-is or<br/>consider JOIN"]
    
    S["Benefit:<br/>Avoid N+1 execution"] -.-> D
    T["Benefit:<br/>Early termination"] -.-> I
    U["Benefit:<br/>Efficient negation"] -.-> L
    V["Benefit:<br/>Compute once"] -.-> P
```

**شرح المخطط:** إعادة كتابة الـ Subquery يمكن أن تحسن الأداء بشكل جذري. القاعدة:
- الـ Subquery الترابطي (Correlated) يتحول إلى JOIN مع دلالات Semi-Join
- الـ IN يتحول إلى EXISTS (توقف عند أول تطابق)
- الـ NOT IN يتحول إلى NOT EXISTS (تجنب مشاكل NULL + أداء أفضل)
- الـ CTE يتم تجسيده (Materialize) في جدول مؤقت إذا سمحت الذاكرة
المصدر: Database System Concepts Ch16.3.2، dbjournal.ro، Medium Guide.

---

## Diagram 9: WHERE vs HAVING Decision

```mermaid
flowchart LR
    A["Filtering Condition"] --> B{"Involves<br/>Aggregation?"}
    
    B -->|"Yes"| C["Must use HAVING"]
    B -->|"No"| D["Use WHERE<br/>(Before GROUP BY)"]
    
    D --> E["Result: Fewer rows grouped"]
    C --> F["Result: Filter after grouping"]
    
    G["Rule: Move non-aggregate<br/>conditions to WHERE"] -.->|"Optimization"| H["Benefit:<br/>Less work for<br/>GROUP BY"]
```

**شرح المخطط:** HAVING يُطبق بعد GROUP BY بينما WHERE يُطبق قبله. لذلك، يجب وضع شروط التصفية غير التجميعية في WHERE لتقليل عدد الصفوف التي تدخل في عملية التجميع. المصدر: Database System Concepts Ch16 و Medium Guide.

---

## Diagram 10: DISTINCT Optimization

```mermaid
flowchart TD
    A["SELECT DISTINCT Detected"] --> B{"Does query include<br/>PRIMARY KEY?"}
    
    B -->|"Yes"| C["DISTINCT is redundant<br/>- PK guarantees uniqueness"]
    B -->|"No"| D{"Are selected columns<br/>unique?"}
    D -->|"Yes"| E["DISTINCT is redundant"]
    D -->|"No"| F{"Can we rewrite<br/>with EXISTS or<br/>window function?"}
    F -->|"Yes"| G["Rewrite to avoid<br/>sort for DISTINCT"]
    F -->|"No"| H["Keep DISTINCT<br/>(necessary for correctness)"]
    
    I["DISTINCT adds sorting cost"] -.-> J["Remove unnecessary<br/>DISTINCT to avoid<br/>extra sort operation"]
```

**شرح المخطط:** DISTINCT يضيف كلفة فرز إضافية. إذا كان الاستعلام يحتوي على PRIMARY KEY أو كان الحقل فريداً، فإن DISTINCT يصبح غير ضروري ويمكن حذفه. المصدر: Database System Concepts Ch16 و Medium Guide.

---

## Diagram 11: EXISTS vs IN

```mermaid
flowchart TD
    A["Subquery Comparison"] --> B{"Need to compare<br/>values or check<br/>existence?"}
    
    B -->|"Check existence"| C["Use EXISTS"]
    B -->|"Compare values"| D{"Outer result set<br/>is large?"}
    
    D -->|"Yes"| E["Use EXISTS<br/>(stops at first match)"]
    D -->|"No"| F{"Inner result set<br/>is large?"}
    F -->|"Yes"| G["Consider IN<br/>(if NULL handling OK)"]
    F -->|"No"| H["Both small -<br/>comparable performance"]
    
    I["EXISTS: Early termination<br/>Semi-join semantics"] -.-> J["Better for large<br/>outer results"]
```

**شرح المخطط:** EXISTS يوقف التنفيذ عند أول تطابق (Early Termination) بينما IN يفحص جميع القيم. لذلك، EXISTS أفضل عندما يكون الهدف هو التحقق من الوجود فقط. مع ذلك، يجب مراعاة معالجة NULL ومقارنة الأداء حسب حجم البيانات. المصدر: dbjournal.ro و Medium Guide.

---

## Diagram 12: Index Suggestion Decision

```mermaid
flowchart TD
    A["Analyze Query Predicates"] --> B{"Columns used in<br/>WHERE/JOIN/ORDER BY?"}
    
    B -->|"Yes"| C{"Existing indexes<br/>on these columns?"}
    C -->|"No"| D{"Table is large?"}
    D -->|"Yes"| E["Suggest creating new index"]
    D -->|"No"| F["Index may not be needed<br/>(small table scan OK)"]
    
    C -->|"Yes"| G{"Index selective enough?"}
    G -->|"No"| H["Suggest index<br/>reorganization or<br/>new covering index"]
    G -->|"Yes"| I{"Index fragmented?"}
    I -->|"Yes"| J["Suggest REBUILD index"]
    I -->|"No"| K["Index is adequate"]
    
    C -->|"Multiple columns"| L{"Composite index<br/>exists?"}
    L -->|"No"| M["Suggest composite<br/>index on (col1, col2)"]
    
    E --> N["Final recommendation"]
    H --> N
    J --> N
    M --> N
```

**شرح المخطط:** قرار الفهرسة معقد ويعتمد على تحليل دقيق للأعمدة المستخدمة في WHERE و JOIN و ORDER BY. يشمل القرار:
1. إنشاء فهرس جديد للأعمدة غير المفهرسة
2. إنشاء فهرس مركب للأعمدة المتعددة
3. إعادة بناء الفهرس المجزأ
المصدر: Database System Concepts Ch16.4 و dbjournal.ro.

---

## Diagram 13: Statistics Freshness Check

```mermaid
flowchart TD
    A["Statistics Check"] --> B{"Are statistics<br/>fresh?"}
    
    B -->|"Yes"| C{"Data distribution<br/>known?"}
    C -->|"Yes"| D{"Histogram<br/>available?"}
    D -->|"Yes"| E["Quality statistics<br/>- Cost estimates reliable"]
    D -->|"No"| F["Suggest creating Histogram"]
    
    C -->|"No"| G["Suggest sampling data<br/>for distribution analysis"]
    
    B -->|"No"| H["WARNING: Statistics outdated!"]
    H --> I["Cost estimates may be wrong"]
    I --> J["Suboptimal execution plan likely"]
    J --> K["Recommend:<br/>UPDATE STATISTICS<br/>immediately"]
    
    L["Impact of outdated statistics:<br/>- Wrong cardinality estimates<br/>- Wrong join algorithm choice<br/>- Suboptimal index selection"] -.-> J
```

**شرح المخطط:** الإحصاءات القديمة تؤدي إلى خطط تنفيذ غير مثلى. عندما تكون الإحصاءات قديمة، يصبح تقدير الكلفة غير دقيق مما قد يؤدي لاختيار خوارزميات JOIN غير مناسبة أو فهارس غير صحيحة. المصدر: dbjournal.ro - الإحصاءات القديمة تزيد كلفة الاستعلام حتى 10 أضعاف.

---

## Diagram 14: Intermediate Result Reduction

```mermaid
flowchart TD
    A["Complex Query Detected"] --> B{"Multiple JOINs?"}
    B -->|"Yes"| C["Apply Selection early<br/>(Push σ down)"]
    B -->|"No"| D{"Has Subqueries?"}
    
    C --> E["Apply Projection early<br/>(Push π down)"]
    D -->|"Yes"| F["Materialize or Flatten<br/>subquery"]
    
    E --> G["Optimize Join Order"]
    G --> H["Use appropriate<br/>Join algorithm"]
    
    H --> I["Combined effect:<br/>Significantly smaller<br/>intermediate results"]
    
    J["Strategies for reducing<br/>intermediate results:"] -.-> K["1. Push Selection"]
    J -.-> L["2. Push Projection"]
    J -.-> M["3. Optimal Join Order"]
    J -.-> N["4. Efficient Join Algorithm"]
    J -.-> O["5. Subquery Materialization"]
```

**شرح المخطط:** تقليل النتائج الوسيطة هو الهدف الرئيسي لتحسين الاستعلامات المعقدة. يتم تطبيق مجموعة من القواعد الترابطية:
- دفع Selection للأسفل (تقليل عدد الصفوف)
- دفع Projection للأسفل (تقليل عدد الأعمدة)
- ترتيب JOIN الأمثل (تقليل حجم كل خطوة)
- اختيار خوارزمية JOIN مناسبة
المصدر: Database System Concepts Ch16.

---

## Diagram 15: Final Decision Assembly

```mermaid
flowchart TB
    subgraph "Input Layer"
        A1["Query Properties"]
        A2["Table Statistics"]
        A3["Index Information"]
        A4["Workload Profile"]
    end

    subgraph "Rule Engine (Experta)"
        B1["Rule: Scan Selection"]
        B2["Rule: Push Selection"]
        B3["Rule: Push Projection"]
        B4["Rule: Join Algorithm"]
        B5["Rule: Join Order"]
        B6["Rule: Subquery Rewrite"]
        B7["Rule: WHERE vs HAVING"]
        B8["Rule: DISTINCT Check"]
        B9["Rule: EXISTS vs IN"]
        B10["Rule: Index Suggestion"]
        B11["Rule: Index Maintenance"]
        B12["Rule: Statistics Check"]
        B13["Rule: Cost Analysis"]
        B14["Rule: Intermediate Result"]
        B15["Rule: UNION Optimization"]
        B16["Rule: Semi-Join / Anti-Join"]
        B17["Rule: Partition Pruning"]
        B18["Rule: Parallel Execution"]
        B19["Rule: CTE Materialization"]
        B20["Rule: View Pushdown"]
        B21["Rule: Adaptive Join"]
        B22["Rule: Workload Strategy"]
    end

    subgraph "Output Layer"
        C1["Access Path<br/>Recommendation"]
        C2["Query Rewrite<br/>Recommendations"]
        C3["Index<br/>Recommendations"]
        C4["Statistics<br/>Recommendations"]
        C5["Cost-based<br/>Plan Selection"]
        C6["Execution<br/>Strategy"]
    end

    A1 --> B1
    A1 --> B2
    A1 --> B3
    A1 --> B4
    A1 --> B5
    A1 --> B6
    A1 --> B7
    A1 --> B8
    A1 --> B9
    A1 --> B10
    A1 --> B11
    A1 --> B12
    A1 --> B16
    A1 --> B17
    A1 --> B19
    A1 --> B20
    A1 --> B21
    A2 --> B12
    A2 --> B13
    A3 --> B1
    A3 --> B10
    A3 --> B11
    A4 --> B18
    A4 --> B22

    B1 --> C1
    B2 --> C2
    B3 --> C2
    B4 --> C1
    B5 --> C1
    B6 --> C2
    B7 --> C2
    B8 --> C2
    B9 --> C2
    B10 --> C3
    B11 --> C3
    B12 --> C4
    B13 --> C5
    B14 --> C2
    B15 --> C2
    B16 --> C1
    B17 --> C1
    B18 --> C6
    B19 --> C2
    B20 --> C2
    B21 --> C1
    B22 --> C6
```

**شرح المخطط:** هذا هو المخطط النهائي الذي يوضح كيف تتكامل جميع القرارات. تبدأ العملية من طبقة الإدخال (خصائص الاستعلام، إحصاءات الجدول، معلومات الفهارس، ملف عبء العمل)، تمر عبر 22 قاعدة في محرك Experta، وتنتج توصيات في 6 فئات رئيسية: مسار الوصول، إعادة كتابة الاستعلام، الفهارس، الإحصاءات، اختيار الخطة، وإستراتيجية التنفيذ.

---

## Diagram 16: Rete Network (Experta Inference)

```mermaid
flowchart LR
    subgraph "Working Memory (Facts)"
        A["QueryFact"]
        B["TableFact"]
        C["IndexFact"]
        D["JoinFact"]
        E["WorkloadFact"]
        F["StatsFact"]
    end

    subgraph "Rete Network"
        G["Alpha Memory<br/>(Single Fact Filters)"]
        H["Beta Memory<br/>(Join Nodes)"]
        I["Conflict Resolution<br/>(Priority Ordering)"]
    end

    subgraph "Agenda"
        J["Activated Rules<br/>(Ready to Fire)"]
        K["Rule Execution"]
    end

    A --> G
    B --> G
    C --> G
    D --> G
    E --> G
    F --> G
    
    G --> H
    H --> I
    I --> J
    J --> K
    
    K -->|"Declare New Facts"| A
    
    L["Rete Algorithm Benefits:"] -.-> M["- No re-evaluation of conditions"]
    N["- Efficient pattern matching"] -.-> O["- Scales to many rules"]
    P["- Incremental fact updates"] -.-> Q["- Production rule system"]
```

**شرح المخطط:** يوضح هذا المخطط كيف يعمل محرك Experta داخلياً باستخدام خوارزمية Rete. يتم تخزين الحقائق في الذاكرة العاملة (Working Memory)، ثم تمر عبر شبكة Rete التي تحتوي على Alpha Memory (لتصفية الحقائق الفردية) و Beta Memory (لربط الحقائق المتعددة). عندما تتحقق شروط قاعدة معينة، يتم تفعيلها ووضعها في جدول الأعمال (Agenda) لتنفيذها. الميزة الرئيسية هي أن Rete لا يعيد تقييم الشروط عند إضافة حقائق جديدة، بل يحتفظ بنتائج التقييم السابقة.

---

## Diagram 17: Cost-Based Plan Selection

```mermaid
flowchart TD
    A["Multiple Execution Plans"] --> B["Plan 1: Full Scan + Hash Join<br/>Cost = 500"]
    A --> C["Plan 2: Index Scan + NLJ<br/>Cost = 150"]
    A --> D["Plan 3: Full Scan + Merge Join<br/>Cost = 300"]
    
    B --> E["Compare Estimated Costs"]
    C --> E
    D --> E
    
    E --> F{"Are statistics<br/>reliable?"}
    
    F -->|"Yes"| G["Select Plan with<br/>Minimum Cost<br/>(Plan 2: Cost=150)"]
    
    F -->|"No"| H["WARNING: Costs may be inaccurate<br/>Recommend updating statistics<br/>then re-evaluate"]
    H --> I["Use heuristic rules<br/>as fallback"]
    I --> J["Apply Push Selection<br/>+ Push Projection<br/>+ Best Practices"]
```

**شرح المخطط:** اختيار خطة التنفيذ يعتمد على تقدير الكلفة. ومع ذلك، إذا كانت الإحصاءات قديمة، فإن تقدير الكلفة قد يكون غير دقيق. في هذه الحالة، يوصي النظام أولاً بتحديث الإحصاءات قبل اختيار الخطة النهائية. المصدر: Database System Concepts Ch16.6.

---

## Diagram 18: Explain Output Flow

```mermaid
flowchart LR
    A["Rule Fires"] --> B["Generate RecommendationFact"]
    B --> C["Extract Fields:"]
    C --> D["recommendation_text<br/>- What to do"]
    C --> E["reasoning<br/>- Why do it"]
    C --> F["priority<br/>- How important"]
    C --> G["expected_improvement<br/>- What benefit"]
    C --> H["applies_to<br/>- Where to apply"]
    
    D --> I["Formatted Output"]
    E --> I
    F --> I
    G --> I
    H --> I
    
    I --> J["[HIGH] SCAN_SELECTION: Use Index Scan"]
    I --> K["Reason: Index selectivity is high, reduces I/O by ~90%"]
    I --> L["Source: Database System Concepts Ch16, dbjournal.ro"]
```

**شرح المخطط:** كل قاعدة تنتج RecommendationFact يحوي 6 حقول أساسية توفر تفسيراً كاملاً للتوصية. هذا يضمن أن النظام ليس مجرد "صندوق أسود" بل يقدم تفسيرات واضحة لكل قرار تحسيني.

---

## Diagram 19: Write-Heavy vs Read-Heavy Workload

```mermaid
flowchart TD
    A["Workload Analysis"] --> B{"Read-heavy or<br/>Write-heavy?"}
    
    B -->|"Read-heavy<br/>(OLAP / Reporting)"| C["Optimize for reads:"]
    C --> C1["Create multiple indexes"]
    C --> C2["Use covering indexes"]
    C --> C3["Materialized views"]
    C --> C4["Denormalization"]
    
    B -->|"Write-heavy<br/>(OLTP)"| D["Optimize for writes:"]
    D --> D1["Minimize indexes per table"]
    D --> D2["Remove unused indexes"]
    D --> D3["Use narrow indexes"]
    D --> D4["Avoid covering indexes"]
    D --> D5["Consider clustered vs<br/>non-clustered impact"]
    
    E["Balance based on<br/>query frequency"] -.-> C
    E -.-> D
```

**شرح المخطط:** طبيعة الحمل (Read-heavy vs Write-heavy) تؤثر على قرارات الفهرسة. في أنظمة OLAP يُفضل إنشاء فهارس متعددة لتسريع القراءة. في أنظمة OLTP يُفضل تقليل الفهارس لتجنب كلفة التحديث. المصدر: Medium Guide.

---

## Diagram 20: Complete Decision Tree Summary

```mermaid
flowchart TB
    START["SQL Query"] --> QCLASS["Classify Query"]
    QCLASS --> TABLES["Analyze Tables"]
    QCLASS --> INDEXES["Analyze Indexes"]
    QCLASS --> JOINS["Analyze Joins"]
    QCLASS --> WORKLOAD["Analyze Workload"]

    TABLES --> STATS{"Statistics<br/>Fresh?"}
    STATS -->|"No"| REC1["⚠ UPDATE STATISTICS"]
    STATS -->|"Yes"| SCAN{"Scan Type?"}
    
    INDEXES --> IDX_USE{"Index Used?"}
    IDX_USE -->|"Yes"| IDX_OK{"Index OK?"}
    IDX_OK -->|"Fragmented"| REC2["🔧 REBUILD INDEX"]
    IDX_OK -->|"Unused"| REC3["🗑 DROP UNUSED INDEX"]
    IDX_OK -->|"OK"| SCAN
    
    IDX_USE -->|"No / Missing"| REC4["➕ CREATE INDEX"]
    REC4 --> SCAN

    SCAN -->|"Index"| PUSH_SEL["Push Selection Down"]
    SCAN -->|"Full"| PUSH_SEL

    TABLES --> PART{"Partitioned<br/>Table?"}
    PART -->|"Yes| PART_KEY{"Partition key<br/>in WHERE?"}
    PART_KEY -->|"Yes"| PRUNE["✂ Partition Pruning"]
    PART_KEY -->|"No"| WARN["⚠ Scan all partitions"]
    PRUNE --> PUSH_SEL
    WARN --> PUSH_SEL
    PART -->|"No"| PUSH_SEL
    
    WORKLOAD --> HW{"Parallel<br/>Available?"}
    HW -->|"Yes & Large table"| PAR["⚡ Parallel Execution"]
    HW -->|"No / Small table"| SEQ["Sequential Execution"]
    PAR --> PUSH_SEL
    SEQ --> PUSH_SEL
    
    JOINS --> JOIN_ALG{"Choose Join<br/>Algorithm"}
    JOIN_ALG -->|"Small+Index"| NLJ["Nested Loop Join"]
    JOIN_ALG -->|"Large+Equal"| HJ["Hash Join"]
    JOIN_ALG -->|"Sorted"| MJ["Merge Join"]
    JOIN_ALG -->|"IN/EXISTS"| SEMI["Semi-Join"]
    JOIN_ALG -->|"NOT IN/NOT EXISTS"| ANTI["Anti-Join"]
    JOIN_ALG -->|"Stats uncertain"| ADAPT["Adaptive Join"]
    
    PUSH_SEL --> PUSH_PROJ["Push Projection Down"]
    PUSH_PROJ --> JOIN_ORDER{"Optimize<br/>Join Order?"}
    JOIN_ORDER -->|"Yes (3+ tables)"| REORDER["Reorder: Smallest First"]
    JOIN_ORDER -->|"No"| SUB{"Subquery/CTE?"}
    
    REORDER --> SUB
    SUB -->|"Correlated"| REWRITE1["↻ Rewrite as JOIN (Semi-Join)"]
    SUB -->|"IN"| REWRITE2["→ Use EXISTS / Semi-Join"]
    SUB -->|"NOT IN"| REWRITE3["→ Use NOT EXISTS / Anti-Join"]
    SUB -->|"CTE (WITH)"| CTE{"Referenced<br/>multiple times?"}
    CTE -->|"Yes & Temp allowed"| MATERIALIZE["Materialize CTE"]
    CTE -->|"No"| GROUP
    MATERIALIZE --> GROUP
    SUB -->|"View"| VIEW_PUSH["Push predicates through view"]
    VIEW_PUSH --> GROUP
    SUB -->|"None"| GROUP{"GROUP BY?"}
    
    GROUP -->|"WHERE+HAVING"| WH_REWRITE["Move conditions to WHERE"]
    GROUP -->|"DISTINCT"| DIST_REWRITE{"PK in SELECT?"}
    DIST_REWRITE -->|"Yes"| DROP_DIST["Drop DISTINCT"]
    DIST_REWRITE -->|"No"| KEEP_DIST["Keep DISTINCT"]
    
    WORKLOAD --> WL{"Workload<br/>Type?"}
    WL -->|"Read-heavy"| READ_IDX["Maintain indexes<br/>Consider covering indexes"]
    WL -->|"Write-heavy"| WRITE_IDX["Minimize indexes<br/>Drop unused indexes"]
    READ_IDX --> FINAL
    WRITE_IDX --> FINAL
    
    FINAL["📋 FINAL OPTIMIZATION REPORT<br/>with reasoning for each decision"]
    
    REC1 --> SCAN
    REC2 --> SCAN
    REC3 --> SCAN
    WH_REWRITE --> FINAL
    REWRITE1 --> FINAL
    REWRITE2 --> FINAL
    REWRITE3 --> FINAL
    NLJ --> FINAL
    HJ --> FINAL
    MJ --> FINAL
    SEMI --> FINAL
    ANTI --> FINAL
    ADAPT --> FINAL
    KEEP_DIST --> FINAL
    DROP_DIST --> FINAL
    PUSH_SEL --> FINAL
    PUSH_PROJ --> FINAL
```

**شرح المخطط:** هذا هو المخطط الشامل الذي يلخص جميع قرارات النظام الخبير من البداية إلى النهاية. يبدأ بتصنيف الاستعلام، ثم تحليل الجداول والفهارس و JOINs، ثم تطبيق سلسلة من قواعد التحسين، وينتهي بتقرير تحسيني شامل مع تبرير لكل قرار.

---

## Diagram 21: Semi-Join vs Anti-Join Decision

```mermaid
flowchart TD
    A["Subquery or Join Decision"] --> B{"Purpose?"}
    
    B -->|"Check existence<br/>(IN / EXISTS)"| C["Semi-Join Path"]
    B -->|"Check non-existence<br/>(NOT IN / NOT EXISTS)"| D["Anti-Join Path"]
    
    subgraph "Semi-Join"
        C1["Scan outer relation"]
        C2["For each outer row,<br/>probe inner relation"]
        C3["Stop at first match"]
        C4["Yield outer row once"]
        C1 --> C2 --> C3 --> C4
    end
    
    subgraph "Anti-Join"
        D1["Scan outer relation"]
        D2["For each outer row,<br/>probe inner relation"]
        D3["If NO match found,"]
        D4["Yield outer row"]
        D1 --> D2 --> D3 --> D4
    end
    
    E["Benefit over Subquery:<br/>- Stops at first match<br/>- No duplicate elimination needed<br/>- Set semantics built-in"] -.-> C4
    F["Benefit over NOT IN:<br/>- Handles NULL correctly<br/>- Early termination possible"] -.-> D4
```

**شرح المخطط:** Semi-Join و Anti-John هما خوارزميتان متخصصتان للتعامل مع الاستعلامات الفرعية.
- **Semi-Join:** للاستعلامات التي تستخدم IN/EXISTS — يمسح العلاقة الخارجية ويتوقف عند أول تطابق في العلاقة الداخلية. هذا يمنع إنتاج صفوف مكررة ويحسن الأداء.
- **Anti-Join:** للاستعلامات التي تستخدم NOT IN/NOT EXISTS — يمسح العلاقة الخارجية ويعيد الصفوف التي ليس لها تطابق في العلاقة الداخلية. يتجنب مشاكل NULL التي يعاني منها NOT IN.
المصدر: Database System Concepts Ch16.

---

## Diagram 22: Partition Pruning Decision

```mermaid
flowchart TD
    A["Query on Partitioned Table"] --> B{"Does WHERE clause<br/>use the partition key?"}
    
    B -->|"Yes"| C["Identify relevant partitions"]
    C --> D["Eliminate non-matching partitions"]
    D --> E["Scan only matching partitions"]
    E --> F["Benefit: Skip up to 90%<br/>of irrelevant data"]
    
    B -->|"No"| G["All partitions must be scanned"]
    G --> H["Full table scan across all partitions"]
    H --> I["Warning: Partition key not used<br/>- Consider adding it to WHERE"]
    
    J["Example: Table partitioned by sale_date"] -.-> K["WHERE sale_date BETWEEN '2024-01-01' AND '2024-01-31'<br/>→ Scan only 1 partition (Jan 2024)"]
    J -.-> L["WHERE region = 'East'<br/>→ No partition key → Scan ALL 12 partitions"]
```

**شرح المخطط:** تقسيم الجداول (Partitioning) يحسن الأداء عندما يستخدم الاستعلام مفتاح التقسيم (Partition Key) في WHERE. يقوم النظام بقص (Prune) الأقسام غير الضرورية ومسح الأقسام ذات الصلة فقط. إذا لم يستخدم الاستعلام مفتاح التقسيم، يجب مسح جميع الأقسام مما يلغي فائدة التقسيم.
المصدر: Database System Concepts Ch16.

---

## Diagram 23: Parallel Execution Strategy

```mermaid
flowchart TD
    A["Query Analysis"] --> B{"Hardware supports<br/>parallelism?"}
    
    B -->|"No"| C["Sequential execution<br/>(no parallel option available)"]
    B -->|"Yes"| D{"Query involves<br/>large tables?"}
    
    D -->|"No / Small tables"| E["Sequential execution<br/>(parallel overhead not worth it)"]
    D -->|"Yes"| F["Enable Parallel Execution"]
    
    F --> G["Split operations across CPU cores"]
    G --> H1["Parallel Scan: Split table into N ranges"]
    G --> H2["Parallel Sort: Each core sorts its range"]
    G --> H3["Parallel Join: Hash/merge join across cores"]
    
    H1 --> I["Linear speedup<br/>proportional to<br/>CPU core count"]
    
    J["Considerations:"] -.-> K["- Memory overhead for parallelism"]
    J -.-> L["- CPU cost of thread management"]
    J -.-> M["- I/O contention on shared storage"]
```

**شرح المخطط:** التنفيذ المتوازي (Parallel Execution) يوزع عمليات الاستعلام الثقيلة (Scan، Sort، Join) عبر أنوية المعالجة المتعددة. هذا مفيد بشكل خاص للجداول الكبيرة والاستعلامات المعقدة. التحسن النظري خطي مع عدد الأنوية، لكن يجب مراعاة كلفة إدارة الخيوط والذاكرة.
المصدر: Database System Concepts Ch16.

---

## Diagram 24: CTE Materialization Decision

```mermaid
flowchart TD
    A["CTE (WITH clause) Detected"] --> B{"How many times is<br/>the CTE referenced?"}
    
    B -->|"Once"| C["Inline the CTE<br/>(No materialization needed)"]
    B -->|"Multiple times"| D{"Temp table<br/>allowed?"}
    
    D -->|"Yes"| E["Materialize CTE into temp table"]
    D -->|"No"| F["Keep CTE inline<br/>(may be re-evaluated)"]
    
    E --> G["Compute CTE once"]
    G --> H["Store results in temp table"]
    H --> I["All references use<br/>the materialized result"]
    
    J["Benefits of Materialization:"] -.-> K["- Compute once, use many times"]
    J -.-> L["- Avoids repeated Subquery execution"]
    J -.-> M["- Can index the temp table"]
    
    N["Cost of Materialization:"] -.-> O["- Disk/memory for temp storage"]
    N -.-> P["- Writing overhead"]
```

**شرح المخطط:** CTE (Common Table Expression / WITH clause) يمكن تجسيده (Materialize) في جدول مؤقت إذا تمت الإشارة إليه مرات متعددة في الاستعلام الرئيسي. هذا يمنع إعادة تنفيذ نفس الاستعلام لكل إشارة. إذا تمت الإشارة إلى CTE مرة واحدة فقط، فمن الأفضل تركه Inline لتجنب كلفة الكتابة في الجدول المؤقت.
المصدر: Database System Concepts Ch16.

---

## Diagram 25: Predicate Pushdown Across Views

```mermaid
flowchart TD
    subgraph "Before Optimization"
        A["SELECT * FROM (SELECT * FROM employees WHERE salary > 50000) v WHERE v.dept_id = 10"] --> B["Query View v"]
        B --> C["Scan all rows of v"]
        C --> D["Filter: dept_id = 10"]
        D --> E["Large intermediate result"]
    end

    subgraph "After Optimization"
        F["Push WHERE through view"] --> G["Rewrite: SELECT * FROM (SELECT * FROM employees WHERE salary > 50000 AND dept_id = 10) v"]
        G --> H["Push both predicates down"]
        H --> I["Scan employees with combined filter"]
        I --> J["Much smaller intermediate result"]
    end

    K["Rule: Predicates on views can be pushed into the view definition"] -.-> L["Benefit: Filters applied earlier = less data to process"]
```

**شرح المخطط:** عندما يستخدم الاستعلام VIEW، يمكن دفع شروط WHERE إلى داخل تعريف الـ VIEW. هذا يسمح بتطبيق التصفية مباشرة على الجداول الأساسية، مما يقلل النتائج الوسيطة ويحسن الأداء. تعتبر هذه التقنية امتداداً لقاعدة Push Selection Down.
المصدر: Database System Concepts Ch16.

---

## Diagram 26: Adaptive Join Decision

```mermaid
flowchart TD
    A["Large Join with<br/>Uncertain Cardinality"] --> B{"Are statistics<br/>accurate?"}
    
    B -->|"Yes"| C["Use standard Join selection<br/>(Hash / Merge / NLJ based on cost)"]
    B -->|"No / Uncertain"| D["Use Adaptive Join"]
    
    D --> E["Start with Hash Join<br/>(build phase for inner relation)"]
    E --> F{"Inner relation<br/>size matches estimate?"}
    
    F -->|"Yes"| G["Continue with Hash Join"]
    F -->|"No - smaller than expected"| H["Switch to Nested Loop Join<br/>(Use index on inner)"]
    F -->|"No - larger than expected"| I["Continue with Hash Join<br/>(it scales better for large data)"]
    
    J["Benefit:"] -.-> K["- No 'wrong join algorithm' risk"]
    J -.-> L["- Adaptive to runtime conditions"]
    J -.-> M["- Robust when statistics are outdated"]
```

**شرح المخطط:** Adaptive Join هي تقنية حديثة (متوفرة في SQL Server 2017+ و PostgreSQL) تسمح باختيار خوارزمية JOIN في منتصف التنفيذ بناءً على الإحصاءات الفعلية في وقت التشغيل. تبدأ بـ Hash Join، وإذا تبين أن العلاقة الداخلية أصغر من المتوقع، تتحول إلى Nested Loop Join تلقائياً. هذا يوفر أداءً قوياً حتى عندما تكون إحصاءات النظام قديمة أو غير دقيقة.
المصدر: Modern DBMS (SQL Server 2017+, PostgreSQL).
