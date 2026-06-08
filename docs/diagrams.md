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
```

**شرح المخطط:** اختيار خوارزمية JOIN المناسبة يعتمد على:
- **Nested Loop Join:** مثالي عندما تكون إحدى العلاقات صغيرة والأخرى مفهرسة
- **Hash Join:** الأفضل للعلاقات الكبيرة بدون فهارس (شروط المساواة)
- **Merge Join:** مناسب عندما تكون البيانات مرتبة مسبقاً أو مطلوب ترتيب النتائج
المصدر: Database System Concepts Ch16.5 والمقال في dbjournal.ro.

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
    C -->|"No"| D["Rewrite as JOIN"]
    C -->|"Yes"| E["Materialize Subquery<br/>(Use temp table)"]
    
    B -->|"No"| F{"Uses IN?"}
    F -->|"Yes"| G["Rewrite as EXISTS<br/>(Semi Join)"]
    F -->|"No"| H["Uses NOT IN?"]
    H -->|"Yes"| I{"NULL possible?"}
    I -->|"Yes"| J["Rewrite as NOT EXISTS"]
    I -->|"No"| K["Rewrite as NOT EXISTS<br/>(Better performance)"]
    H -->|"No"| L["Keep as-is or<br/>consider JOIN"]
    
    M["Benefit:<br/>Avoid N+1 execution"] -.-> D
    N["Benefit:<br/>Early termination"] -.-> G
```

**شرح المخطط:** إعادة كتابة الـ Subquery يمكن أن تحسن الأداء بشكل جذري. القاعدة:
- الـ Subquery الترابطي (Correlated) يتحول إلى JOIN (إذا لم يكن فيه تجميع)
- الـ IN يتحول إلى EXISTS (توقف عند أول تطابق)
- الـ NOT IN يتحول إلى NOT EXISTS (تجنب مشاكل NULL + أداء أفضل)
المصدر: Database System Concepts Ch16.3.2 و dbjournal.ro.

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
    end

    subgraph "Output Layer"
        C1["Access Path<br/>Recommendation"]
        C2["Query Rewrite<br/>Recommendations"]
        C3["Index<br/>Recommendations"]
        C4["Statistics<br/>Recommendations"]
        C5["Cost-based<br/>Plan Selection"]
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
    A2 --> B12
    A2 --> B13
    A3 --> B1
    A3 --> B10
    A3 --> B11

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
```

**شرح المخطط:** هذا هو المخطط النهائي الذي يوضح كيف تتكامل جميع القرارات. تبدأ العملية من طبقة الإدخال (خصائص الاستعلام، إحصاءات الجدول، معلومات الفهارس)، تمر عبر 15+ قاعدة في محرك Experta، وتنتج توصيات في 5 فئات رئيسية: مسار الوصول، إعادة كتابة الاستعلام، الفهارس، الإحصاءات، واختيار الخطة بناءً على الكلفة.

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
    
    JOINS --> JOIN_ALG{"Choose Join<br/>Algorithm"}
    JOIN_ALG -->|"Small+Index"| NLJ["Nested Loop Join"]
    JOIN_ALG -->|"Large+Equal"| HJ["Hash Join"]
    JOIN_ALG -->|"Sorted"| MJ["Merge Join"]
    
    PUSH_SEL --> PUSH_PROJ["Push Projection Down"]
    PUSH_PROJ --> JOIN_ORDER{"Optimize<br/>Join Order?"}
    JOIN_ORDER -->|"Yes (3+ tables)"| REORDER["Reorder: Smallest First"]
    JOIN_ORDER -->|"No"| SUB{"Subquery?"}
    
    REORDER --> SUB
    SUB -->|"Correlated"| REWRITE1["↻ Rewrite as JOIN"]
    SUB -->|"IN"| REWRITE2["→ Use EXISTS"]
    SUB -->|"NOT IN"| REWRITE3["→ Use NOT EXISTS"]
    SUB -->|"None"| GROUP{"GROUP BY?"}
    
    GROUP -->|"WHERE+HAVING"| WH_REWRITE["Move conditions to WHERE"]
    GROUP -->|"DISTINCT"| DIST_REWRITE{"PK in SELECT?"}
    DIST_REWRITE -->|"Yes"| DROP_DIST["Drop DISTINCT"]
    DIST_REWRITE -->|"No"| KEEP_DIST["Keep DISTINCT"]
    
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
    KEEP_DIST --> FINAL
    DROP_DIST --> FINAL
    PUSH_SEL --> FINAL
    PUSH_PROJ --> FINAL
```

**شرح المخطط:** هذا هو المخطط الشامل الذي يلخص جميع قرارات النظام الخبير من البداية إلى النهاية. يبدأ بتصنيف الاستعلام، ثم تحليل الجداول والفهارس و JOINs، ثم تطبيق سلسلة من قواعد التحسين، وينتهي بتقرير تحسيني شامل مع تبرير لكل قرار.
