# التقرير الأكاديمي
## Expert System Query Optimizer
### نظام خبير تفاعلي لتحسين استعلامات SQL باستخدام Streamlit وقواعد المعرفة

---

## 1. المقدمة

تعد قواعد البيانات من الركائز الأساسية في نظم المعلومات الحديثة. مع تزايد حجم البيانات، أصبح تحسين أداء استعلامات SQL ضرورة حتمية لضمان سرعة الاستجابة وكفاءة استخدام الموارد. يهدف هذا المشروع إلى بناء نظام خبير (Expert System) يحاكي قدرة خبير قواعد البيانات (DBA) في تحليل الاستعلامات وتقديم توصيات تحسينية دقيقة بناءً على قواعد معرفية مستمدة من مراجع أكاديمية.

يعتمد النظام على واجهة Streamlit ويب مع تصميم زجاجي (Glassmorphism) داكن، ومحرك Experta المطبق لخوارزمية Rete للاستدلال، مما يسمح بفصل المعرفة (القواعد) عن محرك المعالجة، ويضمن أن تكون التوصيات ناتجة عن استدلال منطقي وليس مجرد شروط برمجية إجرائية.

---

## 2. مشكلة البحث

تكمن المشكلة في أن تحسين الاستعلامات يتطلب خبرة عميقة في فهم كيفية عمل محرك قواعد البيانات (Optimizer)، وهو أمر قد لا يتوفر لجميع المطورين. التحديات الرئيسية تشمل:
1. **تعقيد القرارات:** تداخل عوامل مثل حجم الجداول، حالة الفهارس، وتوزيع البيانات.
2. **صعوبة التشخيص:** صعوبة معرفة لماذا تم اختيار خطة تنفيذ بطيئة (مثل Full Table Scan بدلاً من Index Scan).
3. **الاعتماد على التخمين:** لجوء المطورين لتجربة حلول عشوائية بدلاً من اتباع منهجية علمية.

يهدف هذا النظام إلى سد هذه الفجوة عبر توفير "مقابلة تفاعلية" تشخص الحالة بدقة وتطرح توصيات مبررة علمياً.

---

## 3. أهداف المشروع

1. **بناء نظام خبير تفاعلي عبر الويب:** استبدال إدخال الحقائق اليدوي بنظام مقابلة (Q&A) بواجهة Streamlit جذابة تطرح 44 سؤالاً ذكياً بناءً على إجابات المستخدم.
2. **ضمان اتساق البيانات:** إضافة طبقة تحقق (Validation Layer) تحتوي على 9 فحوصات لاكتشاف التناقضات في إجابات المستخدم.
3. **توسيع قاعدة المعرفة:** تغطية 39+ مجموعة قواعد تشمل JOIN, INDEX, SUBQUERY, GROUP BY, DISTINCT, PARTITION, CTE, STATISTICS, WILDCARD, CURSOR, STORED PROCEDURES, WORKLOAD.
4. **تقديم تقارير مهنية:** عرض نقاط القوة (Strengths) بجانب التوصيات مع خطة عمل مرتبة حسب الأولوية (HIGH, MEDIUM, LOW).
5. **الشفافية التفسيرية:** تقديم تبرير منطقي (Reasoning) ومدى التأثير المتوقع (Expected Impact) لكل توصية.

---

## 4. منهجية العمل (The Expert System Pipeline)

### 4.1 المقابلة التفاعلية عبر Streamlit (Interactive Interview)
بدلاً من طلب حقائق تقنية، يقوم النظام بطرح 44 سؤالاً بسيطاً (نعم/لا أو خيارات) عبر واجهة ويب بتصميم زجاجي داكن مع رسوم متحركة. يتميز هذا التدفق بأنه **شرطي (Conditional)**؛ فإذا أجاب المستخدم بأن الاستعلام لا يحتوي على JOIN، يتم تخطي جميع الأسئلة المتعلقة بالـ JOIN تلقائياً. كما تظهر الأسئلة تباعاً في واجهة شات (Chat Interface) مع شريط تقدم يعرض عدد الأسئلة المجابة.

### 4.2 التحقق من الاتساق (Consistency Validation)
قبل تحويل الإجابات إلى حقائق، يقوم النظام بـ 9 فحوصات للمنطق:
1. جدول صغير + كلا المربوطين كبيران
2. JOIN = لا + معلومات ربط مقدمة
3. Subqueries = لا + عوامل EXISTS/IN/NOT IN مجابة
4. غير مقسم + مفتاح التقسيم مستخدم
5. ORDER BY = لا + البيانات مرتبة مسبقاً
6. جدول صغير + 3 جداول مربوطة أو أكثر
7. UNION = لا + UNION ALL مجاب
8. جدول صغير + توازي + استجابة حرجة
9. كتابة مكثفة + لا توجد فهارس تصفية

### 4.3 بناء الحقائق (Fact Building)
يتم تحويل الإجابات إلى 44+ حقيقة قابلة للقراءة تتضمن:

#### حقائق أساسية
`Fact(join=True)`, `Fact(subquery=True)`, `Fact(aggregation=True)`, `Fact(order_by=True)`, `Fact(distinct=True)`, `Fact(cte=True)`, `Fact(having=True)`, `Fact(limit=True)`, `Fact(or_condition=True)`, `Fact(select_star=True)`, `Fact(correlated_subquery=True)`, `Fact(exists=True)`, `Fact(too_many_joins=True)`

#### حقائق مقيدة بجدول (Table-Qualified Facts)
`Fact(table=t1, large=True)`, `Fact(table=t1, partitioned=True)`, `Fact(table=t1, stats_fresh=True)`, `Fact(table=t1, fragmented=True)`, `Fact(table=t1, partition_key_used=True)`, `Fact(table=t1, covering=True)`

#### حقائق مشتقة (Derived Facts)
`Fact(hash_join_possible=True)`, `Fact(merge_join_possible=True)`, `Fact(nested_loop_possible=True)`, `Fact(semi_join_possible=True)`, `Fact(anti_join_possible=True)`, `Fact(select_minimal=True)` والتي تُشتق آلياً بناءً على خصائص الاستعلام (حجم الجداول، الفهارس، شروط الربط، اختيار الأعمدة).

#### حقائق بيئة العمل
`Fact(read_heavy=True)`, `Fact(write_heavy=True)`, `Fact(stats_fresh=True)`, `Fact(stats_outdated=True)`, `Fact(parallel_available=True)`, `Fact(temp_allowed=True)`, `Fact(response_critical=True)`

### 4.4 محرك الاستدلال (Inference Engine)
يتم تغذية الحقائق إلى محرك `Experta` الذي يطبق خوارزمية Rete لمطابقة الأنماط مع 39+ مجموعة قواعد. القواعد مرتبة حسب الأولوية:
- **HIGH:** توصيات فورية وحاسمة (فهارس، خوارزميات ربط، تحسينات هيكلية)
- **MEDIUM:** تحسينات مهمة (إحصائيات، إعادة كتابة، جداول ملخصة، تقييم مقايضات الكتابة)
- **LOW:** توصيات تأكيدية وتحقق (مراجعة CTE، التحقق من ضرورة DISTINCT)

### 4.5 توليد التقرير المهني (Professional Reporting)
يتم تجميع النتائج في تقرير مكون من 7 أقسام:
1. **Query Profile:** جميع إجابات المستخدم النهائية
2. **Generated Facts:** جميع الحقائق المولدة
3. **Optimization Strengths:** نقاط القوة المكتشفة
4. **Execution Summary:** ملخص (عدد الحقائق، عدد التوصيات)
5. **Recommendations:** التوصيات مع التصنيف، الأولوية، المبرر، الأثر المتوقع
6. **Priority Action Plan:** خطة عمل مرتبة حسب الأولوية (HIGH ثم MEDIUM ثم LOW)
7. **Sources Referenced:** المراجع الأكاديمية المستخدمة

---

## 5. قاعدة المعرفة (Knowledge Base)

### 5.1 مجموعات القواعد (Rule Groups)

| المجموعة | القواعد | الأولوية النموذجية |
|----------|---------|-------------------|
| تحسين الفهارس (Filter/Join) | إنشاء فهارس للتصفية والربط عند غيابها | HIGH |
| تحسين التقسيم (Partition) | استخدام Partition Pruning لتقليل I/O | HIGH |
| خوارزميات الربط (Join) | اختيار Hash/Merge/Nested-Loop/Semi-Join | HIGH |
| إعادة كتابة الاستعلام (Query Rewrite) | استبدال SELECT*، OR إلى UNION ALL، نقل HAVING إلى WHERE | HIGH |
| تحسين التجميع (Group By) | جداول ملخصة، فهرسة أعمدة GROUP BY | MEDIUM |
| تحسين DISTINCT | فهرسة أعمدة DISTINCT أو التحقق من ضرورته | MEDIUM |
| إحصائيات وتوزيع (Statistics) | إنشاء Histogram لتحسين تقدير الكلفة | MEDIUM |
| تحسين المحتوى الفرعي (Subquery/CTE) | تجسيد (Materialization) لتجنب التنفيذ المتكرر | MEDIUM |
| إعادة هيكلة المخطط (Denormalization) | تقليل JOINs عبر إلغاء التسوية | MEDIUM |
| أنماط البحث (Wildcard) | تجنب % البادئة في LIKE | MEDIUM |
| أنواع البيانات (Data Types) | استخدام أنواع مناسبة (DATE بدلاً من VARCHAR) | MEDIUM |
| تحسين المؤشرات (Cursors) | استبدال المعالجة صفاً صفاً بعمليات مجموعية | HIGH |
| الإجراءات المخزنة (Stored Procedures) | استخدام الإجراءات المخزنة للكود المعقد المُجمّع مسبقاً | LOW |
| بيئة العمل (Workload) | تقليل الفهارس في بيئات الكتابة المكثفة، استخدام التوازي | MEDIUM |
| فهرسة التغطية (Covering Index) | استخدام فهرس يغطي جميع الأعمدة المحددة لتجنب الوصول للجدول | HIGH |

### 5.2 الحقائق (Facts)
تتكون قاعدة المعرفة من 44+ حقيقة تغطي:
- **خصائص الاستعلام:** (JOIN, Subquery, Aggregation, Order By, Distinct, CTE, UNION, HAVING, LIMIT, OR, SELECT*)
- **خصائص الجدول:** (Table Size, Partitioning, Partition Key Usage, Normalization, Data Types)
- **حالة الفهارس:** (Filter Index, Join Index, Fragmentation, Composite, Clustered, Unused, FK, Range, Covering)
- **تفاصيل الربط:** (Size Equality, Indexing, Sorting, Large Tables)
- **الإحصاءات:** (Stats Freshness, Histogram Availability, Outdated)
- **البيئة:** (Workload Type, Parallelism, Memory, Criticality)
- **مشتقة:** (Hash Join Possible, Merge Join Possible, Semi Join Possible, Select Minimal)

---

## 6. مصادر المعرفة
تستند القواعد إلى مراجع أكاديمية معتمدة:
1. **Database System Concepts (Silberschatz, Korth, Sudarshan):** المرجع الأساسي لعمليات Push-down، Join Algorithms (16.5.3 Merge Join، 16.5.4 Hash Join)، Covering Index (16.4)، Partition Pruning، Top-N Optimization، وتقدير الكلفة بالإحصائيات.
2. **dbjournal.ro:** مصدر لتقنيات تحسين الفهارس الانتقائية ومشكلة OR وتأثير SELECT* وتجزؤ الفهارس وتكلفة الفهارس في بيئات الكتابة.
3. **Medium (Women in Tech):** دليل عملي لتحسين استعلامات SQL الشائعة، يشمل تحسين أنماط LIKE، أنواع البيانات، المؤشرات، الإجراءات المخزنة، والـ Denormalization.

---

## 7. هيكل النظام البرمجي

```
├── app.py                 # واجهة Streamlit (Glassmorphism، 44 سؤالاً، شات تفاعلي)
├── validation.py          # 9 فحوصات منطقية لاكتشاف التناقضات
├── fact_builder.py        # تحويل الإجابات إلى 44+ حقيقة (Table-Qualified + Derived)
├── optimizer_engine.py    # واجهة تشغيل محرك Experta
├── report_generator.py    # بناء التقرير المهني (توصيات + خطة عمل بالأولوية)
├── test_pipeline.py       # اختبار آلي للـ pipeline بالكامل
├── engine/
│   ├── facts.py           # تعريف هيكل RecommendationFact (category, priority, reasoning, impact)
│   ├── rules.py           # 39+ مجموعة قواعد استدلالية (Rules)
│   └── optimizer.py       # إعدادات محرك Experta وترتيب التوصيات بالأولوية
└── docs/
    ├── report.md          # هذا التقرير الأكاديمي
    └── diagrams.md        # المخططات الهيكلية (5 رسوم Mermaid)
```

---

## 8. تدفق البيانات (Data Flow)

```
إجابات المستخدم (44) ← 9 فحوصات تحقق ← 44+ حقيقة Experta ← Rete Algorithm ← 28+ توصية

  (1) Query Profile          (3) Optimization Strengths     (5) Priority Action Plan
  (2) Generated Facts        (4) Recommendations            (6) Sources Referenced
```

---

## 9. الخلاصة
يمثل هذا المشروع تطبيقاً متكاملاً للنظم الخبيرة باستخدام Streamlit و Experta. مع 44 سؤالاً شرطياً، و9 فحوصات اتساق، و39+ مجموعة قواعد موزعة على 15 فئة تغطي كامل جوانب تحسين استعلامات SQL، أصبح النظام قادراً على تشخيص حالة الاستعلام بدقة وتقديم خطة تحسين ذات أولوية مع تبرير منطقي ومرجع أكاديمي لكل توصية.

الميزات الجديدة:
- **اكتشاف تناقضات المخرجات:** منع التوصيات المتضاربة مثل "أنشئ فهرساً" مع "قلل الفهارس" في بيئات الكتابة المكثفة
- **فهرسة التغطية (Covering Index):** استنتاج آلي من عدم استخدام SELECT* مع وجود فهرس مركب
- **مقايضات الأداء:** استبدال التوصيات المتضاربة بتوصية متوازنة توضح المقايضة

يجمع النظام بين:
- **واجهة ويب حديثة:** glassmorphism، رسوم متحركة، شات تفاعلي، شريط تقدم
- **منطق استدلالي غير إجرائي:** Rete algorithm عبر Experta
- **توصيات محكمة:** أولوية + فئة + مبرر + أثر متوقع
- **مراجع معلنة:** كل توصية تستند إلى مصدر أكاديمي موثق

هذا يجعله نموذجاً مثالياً للدراسة الأكاديمية في مجال النظم الخبيرة، قواعد البيانات، والذكاء الاصطناعي.
