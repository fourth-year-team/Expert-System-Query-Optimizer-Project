# التقرير الأكاديمي
## Expert System Query Optimizer
### نظام خبير لتحسين استعلامات SQL باستخدام تقنيات قواعد المعرفة والاستدلال

---

## 1. المقدمة

تعد قواعد البيانات من الركائز الأساسية في نظم المعلومات الحديثة، حيث تستخدم في تخزين وإدارة كميات هائلة من البيانات. مع تزايد حجم البيانات وتعقيد الاستعلامات، أصبح تحسين أداء استعلامات SQL ضرورة حتمية لضمان سرعة الاستجابة وكفاءة استخدام الموارد. مشكلة تحسين الاستعلامات (Query Optimization) هي واحدة من أكثر المشكلات تحدياً في مجال قواعد البيانات، حيث تتطلب موازنة دقيقة بين عدة عوامل مثل كلفة الإدخال/الإخراج (I/O)، استخدام الذاكرة، وكلفة المعالجة.

النظم الخبيرة (Expert Systems) هي أحد فروع الذكاء الاصطناعي التي تهدف إلى محاكاة قدرة الخبير البشري في اتخاذ القرارات في مجال معين. تتكون النظم الخبيرة من ثلاثة مكونات رئيسية: قاعدة المعرفة (Knowledge Base) التي تحتوي على الحقائق والقواعد، محرك الاستدلال (Inference Engine) الذي يطبق القواعد على الحقائق، وواجهة المستخدم (User Interface) التي تتيح التفاعل مع النظام.

هذا المشروع يقدم نظاماً خبيراً لتحسين استعلامات SQL باستخدام مكتبة Experta في Python، والتي تطبق خوارزمية Rete للاستدلال. يقوم النظام بتحليل خصائص الاستعلام وخصائص الجداول والفهارس والإحصاءات، ثم يطبق مجموعة من القواعد التحسينية المستمدة من المراجع الأكاديمية المعتمدة ليقدم توصيات ذكية لتحسين أداء الاستعلام.

---

## 2. مشكلة البحث

تواجه تطبيقات قواعد البيانات تحديات كبيرة في تحسين أداء الاستعلامات، خاصة عند التعامل مع قواعد البيانات الكبيرة والمعقدة. المشكلات الرئيسية التي يعالجها هذا المشروع هي:

1. **صعوبة اختيار خطة التنفيذ المثلى:** عند تنفيذ استعلام SQL، هناك العديد من خطط التنفيذ الممكنة (مثل استخدام Full Table Scan أو Index Scan، اختيار خوارزمية JOIN المناسبة). اختيار الخطة الخطأ يؤدي إلى أداء ضعيف.

2. **الحاجة إلى خبرة متخصصة:** يتطلب تحسين الاستعلامات خبرة عميقة في قواعد البيانات ومحركاتها، وهو ما قد لا يتوفر لدى جميع المطورين.

3. **تعقيد القرارات التحسينية:** تتداخل عوامل متعددة في قرار التحسين مثل حجم الجداول، جودة الإحصاءات، وجود الفهارس، توزيع البيانات، وطبيعة الحمل (Read-heavy vs Write-heavy).

4. **الاعتماد على منطق إجرائي تقليدي:** في كثير من الأنظمة، يتم اتخاذ قرارات التحسين باستخدام منطق إجرائي (if/else, for loops) مما يجعل النظام صعب التوسع والصيانة.

يهدف هذا المشروع إلى تقديم حل يعتمد على النظم الخبيرة وقواعد المعرفة للتغلب على هذه التحديات، بحيث تكون القرارات التحسينية ناتجة من تطبيق قواعد الاستدلال على الحقائق، وليس من منطق إجرائي.

---

## 3. أهمية المشروع

تتجلى أهمية هذا المشروع في النقاط التالية:

1. **أتمتة عملية تحسين الاستعلامات:** يوفر النظام طريقة آلية لتحليل الاستعلامات واقتراح تحسينات، مما يقلل الحاجة إلى الخبراء البشريين في المهام الروتينية.

2. **قابلية التوسع:** باستخدام قاعدة معرفة تعتمد على القواعد (Rules)، يمكن إضافة قواعد جديدة أو تعديل القواعد الحالية بسهولة دون إعادة هيكلة النظام.

3. **الشفافية والتفسير:** على عكس تقنيات التعلم الآلي (Black Box)، يقدم النظام تفسيرات واضحة لكل توصية، مما يساعد المستخدم على فهم لماذا تم اتخاذ قرار معين.

4. **الاعتماد على مراجع أكاديمية:** تستند جميع القرارات إلى مراجع أكاديمية موثوقة (Database System Concepts, dbjournal.ro, Medium Guide) مما يضمن المصداقية الأكاديمية.

5. **تطبيق عملي لمفاهيم النظم الخبيرة:** يقدم المشروع تطبيقاً عملياً لمفاهيم النظم الخبيرة باستخدام مكتبة Experta في Python، وهو نموذج يمكن استخدامه في التعليم والبحث.

---

## 4. أهداف المشروع

الأهداف الرئيسية للمشروع هي:

1. **بناء نظام خبير** لتحسين استعلامات SQL باستخدام Python ومكتبة Experta.

2. **تصميم قاعدة معرفة واسعة** تغطي جميع جوانب تحسين الاستعلامات الرئيسية (اختيار مسار الوصول، اختيار خوارزمية JOIN، إعادة كتابة الاستعلام، الفهرسة، الإحصاءات).

3. **تطبيق قواعد استدلال غير إجرائية** يكون فيها القرار ناتجاً من تطبيق القواعد على الحقائق عبر محرك الاستدلال، دون استخدام حلقات تكرارية أو شروط إجرائية في منطق القرار.

4. **تقديم توصيات مفسرة** بحيث تكون كل توصية مصحوبة بتبرير يشرح السبب ومرجع المصدر.

5. **توثيق المشروع** بتقرير أكاديمي ومخططات (Flowcharts) منظمة تشرح كل قرار تحسيني.

---

## 5. منهجية العمل

تم اتباع المنهجية التالية في تنفيذ المشروع:

### 5.1 جمع المعرفة
- تمت دراسة المصادر الأكاديمية المعتمدة لاستخراج قواعد تحسين الاستعلامات
- تم تحليل تقنيات التحسين المختلفة وتصنيفها

### 5.2 تصميم قاعدة المعرفة
- تم تصميم 7 فئات من الحقائق (Facts) لتغطية جميع جوانب الاستعلام
- تم تعريف أكثر من 20 قاعدة تحسين (Rules)

### 5.3 بناء محرك الاستدلال
- استخدام مكتبة Experta التي تطبق خوارزمية Rete
- ربط القواعد بالحقائق عبر نمط المطابقة (Pattern Matching)

### 5.4 بناء النظام
- كتابة الكود بلغة Python
- تصميم هيكل المشروع على شكل مجلدات منظمة
- إنشاء أمثلة تشغيل متنوعة

### 5.5 التوثيق
- كتابة تقرير أكاديمي شامل
- إنشاء مخططات Mermaid لكل قرار تحسيني
- كتابة README ووثائق التشغيل

---

## 6. مصادر المعرفة

يعتمد هذا المشروع على ثلاثة مصادر رئيسية للمعرفة:

### 6.1 Database System Concepts - Chapter 16
**المرجع:** Abraham Silberschatz, Henry F. Korth, S. Sudarshan (7th Edition)
**الرابط:** https://www.db-book.com

هذا المرجع هو المصدر الأساسي لمفاهيم تحسين الاستعلامات في نظم قواعد البيانات. الفصل 16 يغطي:
- مقدمة في تحسين الاستعلامات وخطط التنفيذ
- تحويل التعبيرات العلائقية باستخدام قواعد التكافؤ
- معلومات الكتالوج لتقدير الكلفة
- المعلومات الإحصائية لتقدير الكلفة
- التحسين المعتمد على الكلفة (Cost-based optimization)
- البرمجة الديناميكية لاختيار خطط التنفيذ
- تحسين Heuristic: Push Selection, Push Projection
- ترتيب JOIN واختيار خوارزمية JOIN
- Nested Loop Join, Hash Join, Merge Join

### 6.2 Query Optimization Techniques in Microsoft SQL Server
**المصدر:** Database Systems Journal, Volume 16, Issue 4
**الرابط:** https://www.dbjournal.ro/archive/16/16_4.pdf

هذا المقال العلمي يركز على تقنيات تحسين الاستعلامات في SQL Server ويغطي:
- تحسين الاستعلام المعتمد على الكلفة
- انتقائية الفهرس وأهمية الإحصاءات
- اختيار آلية الوصول إلى البيانات
- اختيار خوارزمية JOIN بناءً على خصائص البيانات
- تأثير تجزؤ الفهارس على الأداء
- حداثة الإحصاءات وجودة خطة التنفيذ
- مقارنة أداء EXISTS vs IN
- تحليل استخدام الفهارس ومراقبتها

### 6.3 Optimizing SQL Query Performance: A Comprehensive Guide
**المصدر:** Medium - Women in Technology
**الرابط:** https://medium.com/womenintechnology/optimizing-sql-query-performance-a-comprehensive-guide-6cb72b9f52ef

هذا الدليل الشامل يقدم نصائح عملية لتحسين الاستعلامات:
- استخدام أسماء الأعمدة بدلاً من SELECT *
- تجنب DISTINCT غير الضروري
- استخدام WHERE بدلاً من HAVING للشروط غير التجميعية
- EXISTS vs IN
- UNION ALL vs UNION
- تحسين JOIN واستخدام الفهارس
- تقنيات إعادة كتابة Subquery
- أفضل ممارسات صيانة الإحصاءات

---

## 7. قاعدة المعرفة (Knowledge Base)

قاعدة المعرفة في هذا النظام تتكون من 7 فئات رئيسية من الحقائق (Facts)، كل فئة تغطي جانباً محدداً من جوانب الاستعلام وبيئة قاعدة البيانات.

### 7.1 QueryFact

تصف هذه الفئة خصائص الاستعلام نفسه:

| الحقل | الوصف | مثال |
|---|---|---|
| query_type | نوع الاستعلام | SELECT, SELECT_JOIN, SELECT_SUBQUERY |
| predicate_type | نوع الشرط | equality, range, IN_subquery |
| has_subquery | هل يحتوي على Subquery | True/False |
| has_group_by | هل يحتوي على GROUP BY | True/False |
| has_order_by | هل يحتوي على ORDER BY | True/False |
| has_distinct | هل يحتوي على DISTINCT | True/False |
| has_limit_offset | هل يحتوي على LIMIT/OFFSET | True/False |
| uses_exists | هل يستخدم EXISTS | True/False |
| uses_in | هل يستخدم IN | True/False |
| uses_not_in | هل يستخدم NOT IN | True/False |
| uses_union | هل يستخدم UNION | True/False |
| uses_union_all | هل يستخدم UNION ALL | True/False |
| select_list_wide | قائمة SELECT واسعة (SELECT *) | True/False |
| select_list_minimal | قائمة SELECT محدودة | True/False |
| has_where_clause | هل يحتوي على WHERE | True/False |
| has_having_clause | هل يحتوي على HAVING | True/False |
| has_join_condition | هل يحتوي على JOIN | True/False |
| has_correlated_subquery | هل Subquery ترابطي | True/False |
| has_aggregation | هل يحتوي على دوال تجميع | True/False |
| has_or_condition | هل يحتوي على OR | True/False |
| number_of_tables | عدد الجداول | عدد صحيح |
| number_of_predicates | عدد الشروط | عدد صحيح |

### 7.2 TableFact

تصف خصائص الجدول/الجداول المشاركة في الاستعلام:

| الحقل | الوصف |
|---|---|
| relation_name | اسم الجدول |
| tuples_count | عدد الصفوف |
| blocks_count | عدد الكتل |
| tuple_size | حجم الصف (بايت) |
| blocking_factor | عامل التكتل (صفوف/كتلة) |
| statistics_fresh | هل الإحصاءات حديثة |
| data_distribution_known | هل توزيع البيانات معروف |
| relation_fits_in_memory | هل الجدول يناسب الذاكرة |
| distinct_values | عدد القيم المميزة |
| has_null_values | هل يوجد قيم NULL |
| has_primary_key | هل يوجد مفتاح رئيسي |
| has_foreign_key | هل يوجد مفتاح خارجي |
| is_small_table | هل الجدول صغير |
| is_large_table | هل الجدول كبير |
| selectivity_estimate | تقدير الانتقائية |

### 7.3 IndexFact

تصف الفهارس الموجودة على الجداول:

| الحقل | الوصف |
|---|---|
| relation_name | اسم الجدول |
| column_name | اسم العمود المفهرس |
| has_index | هل يوجد فهرس |
| index_type | نوع الفهرس (B+TREE, NON_CLUSTERED) |
| index_selectivity_high | هل انتقائية الفهرس عالية |
| index_supports_join | هل يدعم JOIN |
| index_supports_order_by | هل يدعم ORDER BY |
| index_fragmented | هل الفهرس مجزأ |
| index_unused | هل الفهرس غير مستخدم |
| index_covering | هل الفهرس غطاء (Covering) |
| index_clustered | هل هو Clustered Index |
| index_nonclustered | هل هو Non-Clustered Index |
| index_on_predicate_column | على عمود الشرط |
| index_on_join_column | على عمود JOIN |
| index_cardinality_high | هل التوحيد عالٍ |
| index_usage_count | عدد مرات الاستخدام |
| composite_index_exists | هل يوجد فهرس مركب |

### 7.4 JoinFact

تصف عمليات JOIN في الاستعلام:

| الحقل | الوصف |
|---|---|
| join_type | نوع JOIN |
| join_keys_indexed | هل أعمدة JOIN مفهرسة |
| outer_relation_size | حجم العلاقة الخارجية |
| inner_relation_size | حجم العلاقة الداخلية |
| merge_join_possible | هل Merge Join ممكن |
| hash_join_possible | هل Hash Join ممكن |
| nested_loop_possible | هل Nested Loop ممكن |
| both_relations_large | هل كلتا العلاقتين كبيرتان |
| one_relation_small | هل إحدى العلاقتين صغيرة |
| join_condition_equality | هل شرط JOIN مساواة |

### 7.5 WorkloadFact

تصف طبيعة الحمل وتفضيلات الأداء:

| الحقل | الوصف |
|---|---|
| need_fast_response | هل نحتاج استجابة سريعة |
| read_heavy_workload | هل الحمل قراءة مكثفة |
| write_heavy_workload | هل الحمل كتابة مكثفة |
| need_sorted_output | هل نحتاج مخرجات مرتبة |
| need_no_duplicates | هل نحتاج بدون مكررات |
| temp_table_allowed | هل الجداول المؤقتة مسموحة |
| memory_constrained | هل الذاكرة محدودة |
| concurrent_users_high | هل المستخدمون المتزامنون كثيرون |

### 7.6 StatsFact

تصف إحصاءات التكلفة والأداء:

| الحقل | الوصف |
|---|---|
| cost_estimate_available | هل تقدير الكلفة متاح |
| stats_are_outdated | هل الإحصاءات قديمة |
| estimated_rows | عدد الصفوف المقدر |
| estimated_cost | الكلفة المقدرة |
| intermediate_result_large | هل النتائج الوسيطة كبيرة |
| most_selective_predicate | أكثر شرط انتقائية |
| histogram_available | هل الـ Histogram متاح |
| sampling_freshness_pct | نضارة العينة (نسبة مئوية) |

### 7.7 RecommendationFact

تمثل التوصيات الناتجة عن النظام:

| الحقل | الوصف |
|---|---|
| recommendation_id | معرف فريد للتوصية |
| category | فئة التوصية (SCAN_SELECTION, JOIN_ALGORITHM, ...) |
| recommendation_text | نص التوصية |
| reasoning | التبرير العلمي |
| priority | الأولوية (HIGH, MEDIUM, LOW) |
| expected_improvement | التحسين المتوقع |
| applies_to | مجال التطبيق |

---

## 8. محرك الاستدلال (Inference Engine)

### 8.1 خوارزمية Rete

يستخدم النظام محرك الاستدلال Experta الذي يطبق خوارزمية Rete. خوارزمية Rete هي خوارزمية فعالة لمطابقة الأنماط (Pattern Matching) في أنظمة إنتاج القواعد (Production Rule Systems). تتميز الخوارزمية بما يلي:

1. **Alpha Network:** تقوم بتصفية الحقائق الفردية بناءً على شروط بسيطة
2. **Beta Network:** تقوم بربط الحقائق المتعددة عبر عمليات JOIN
3. **Agenda:** تحتفظ بقائمة القواعد المفعلة (Activated Rules) التي تنتظر التنفيذ
4. **Conflict Resolution:** تحل تعارضات التنشيط بين القواعد المتعددة

### 8.2 آلية عمل القواعد

كل قاعدة (Rule) في Experta تعرف باستخدام المزين `@Rule` وتحتوي على:
- **الشروط (Conditions):** أنماط تطابق الحقائق (QueryFact, TableFact, IndexFact, ...)
- **الإجراء (Action):** ما يتم تنفيذه عند تفعيل القاعدة (إضافة توصية)

مثال لقاعدة:
```python
@Rule(
    QueryFact(predicate_type=MATCH()),
    IndexFact(has_index=True, index_selectivity_high=MATCH()),
    TableFact(is_large_table=True)
)
def rule_index_scan(self, query_type, predicate_type):
    # إنشاء توصية باستخدام Index Scan
```

### 8.3 القواعد المطبقة في النظام

يحتوي النظام على 27 قاعدة تحسين تغطي جميع القرارات الرئيسية:

| الرقم | اسم القاعدة | القرار | الأولوية |
|---|---|---|---|
| 1 | rule_full_scan | استخدام Full Table Scan | HIGH |
| 2 | rule_index_scan | استخدام Index Scan | HIGH |
| 3 | rule_push_selection_down | دفع الشرط للأسفل | HIGH |
| 4 | rule_push_projection_down | دفع الإسقاط للأسفل | HIGH |
| 5 | rule_nested_loop_join | استخدام Nested Loop Join | HIGH |
| 6 | rule_hash_join | استخدام Hash Join | HIGH |
| 7 | rule_merge_join | استخدام Merge Join | MEDIUM |
| 8 | rule_join_order_optimization | ترتيب JOIN | HIGH |
| 9 | rule_subquery_to_join | إعادة كتابة Subquery | HIGH |
| 10 | rule_exists_vs_in | استخدام EXISTS بدلاً من IN | MEDIUM |
| 11 | rule_where_vs_having | WHERE بدلاً من HAVING | HIGH |
| 12 | rule_distinct_optimization | تحسين DISTINCT | MEDIUM |
| 13 | rule_index_suggestion | اقتراح فهرس | HIGH |
| 14 | rule_composite_index_suggestion | فهرس مركب | MEDIUM |
| 15 | rule_unused_index_detection | كشف فهرس غير مستخدم | LOW |
| 16 | rule_fragmented_index | فهرس مجزأ | MEDIUM |
| 17 | rule_statistics_freshness | حداثة الإحصاءات | HIGH |
| 18 | rule_reduce_intermediate_results | تقليل النتائج الوسيطة | HIGH |
| 19 | rule_select_list_optimization | تحسين قائمة SELECT | HIGH |
| 20 | rule_union_all_instead_of_union | UNION ALL | MEDIUM |
| 21 | rule_covering_index_scan | Covering Index | HIGH |
| 22 | rule_or_condition_optimization | تحسين OR | MEDIUM |
| 23 | rule_small_table_scan | مسح الجدول الصغير | MEDIUM |
| 24 | rule_data_distribution_check | التحقق من توزيع البيانات | MEDIUM |
| 25 | rule_fast_response_strategy | استراتيجية الاستجابة السريعة | HIGH |
| 26 | rule_limit_offset_index | تحسين LIMIT/OFFSET | HIGH |
| 27 | rule_hash_join_no_index | Hash Join بدون فهرس | HIGH |
| 28 | rule_materialize_subquery | تجسيد Subquery | MEDIUM |
| 29 | rule_not_in_to_not_exists | NOT IN -> NOT EXISTS | HIGH |
| 30 | rule_clustered_index_for_range | Clustered Index للمدى | MEDIUM |

### 8.4 مبدأ عدم استخدام المنطق الإجرائي

من أهم مبادئ هذا النظام أن جميع القرارات التحسينية تتخذ من خلال تطبيق القواعد على الحقائق، وليس من خلال برمجة إجرائية (if/else, for loops). عندما يتم تغذية النظام بالحقائق، يقوم محرك Experta تلقائياً بمطابقة هذه الحقائق مع شروط القواعد وتفعيل القواعد المناسبة. لا يوجد في النظام أي كود إجرائي يقرر "إذا كان كذا افعل كذا" - هذا القرار يتم بالكامل عبر آلية مطابقة الأنماط في Experta.

المسموح به من الكود الإجرائي يقتصر على:
- قراءة المدخلات وتحويلها إلى حقائق
- طباعة النتائج وتنسيق الإخراج
- تشغيل المحرك

---

## 9. دور Experta

مكتبة Experta هي مكتبة Python لبناء النظم الخبيرة. توفر المكتبة:

### 9.1 Fact
فئة أساسية لتمثيل الحقائق. جميع فئات الحقائق في هذا النظام ترث من `Fact`.

### 9.2 KnowledgeEngine
الفئة الأساسية لمحرك المعرفة. يجب أن ترث منها وتُعرف القواعد كدوال باستخدام `@Rule`.

### 9.3 Rule Decorator
المزين `@Rule` يستخدم لتعريف شروط القاعدة باستخدام:
- `MATCH()`: لمطابقة أي قيمة وتخزينها
- `AND()`: للربط المنطقي AND
- `OR()`: للربط المنطقي OR
- `NOT()`: للنفي

### 9.4 مزايا استخدام Experta في هذا المشروع

1. **فصل المعرفة عن المعالجة:** يتم تعريف المعرفة (الحقائق والقواعد) بشكل منفصل عن منطق المعالجة
2. **قابلية التوسع:** يمكن إضافة قواعد جديدة بسهولة دون تعديل القواعد الموجودة
3. **إعادة استخدام القواعد:** يمكن تطبيق نفس القاعدة على سيناريوهات مختلفة
4. **شفافية الاستدلال:** يمكن تتبع كيفية وصول النظام إلى قرار معين
5. **توافق مع Python:** يمكن دمج Experta مع مكتبات Python الأخرى

---

## 10. المخططات (Diagrams)

يحتوي المشروع على 20 مخططاً تغطي جميع جوانب النظام. المخططات منفصلة ومركزة بحيث يخدم كل مخطط فكرة واحدة أو قراراً واحداً. يمكن الاطلاع على جميع المخططات في ملف `docs/diagrams.md`.

### قائمة المخططات:

| الرقم | اسم المخطط | الوصف |
|---|---|---|
| 1 | General System Architecture | البنية العامة للنظام |
| 2 | Query Classification | تصنيف الاستعلام |
| 3 | Full Scan vs Index Scan | قرار مسار الوصول |
| 4 | Push Selection Down | دفع شروط الاختيار |
| 5 | Push Projection Down | دفع الإسقاط |
| 6 | Join Algorithm Selection | اختيار خوارزمية JOIN |
| 7 | Join Order Optimization | ترتيب JOIN |
| 8 | Subquery Rewriting | إعادة كتابة Subquery |
| 9 | WHERE vs HAVING | مقارنة WHERE و HAVING |
| 10 | DISTINCT Optimization | تحسين DISTINCT |
| 11 | EXISTS vs IN | مقارنة EXISTS و IN |
| 12 | Index Suggestion Decision | قرار الفهرسة |
| 13 | Statistics Freshness | حداثة الإحصاءات |
| 14 | Intermediate Result Reduction | تقليل النتائج الوسيطة |
| 15 | Final Decision Assembly | تجميع القرارات النهائية |
| 16 | Rete Network | شبكة Rete |
| 17 | Cost-Based Plan Selection | اختيار الخطة الأقل كلفة |
| 18 | Explain Output Flow | تدفق الإخراج التوضيحي |
| 19 | Write-Heavy vs Read-Heavy | مقارنة الحمل |
| 20 | Complete Decision Tree | شجرة القرارات الكاملة |

---

## 11. هيكل المشروع البرمجي

```
├── main.py                          # نقطة الدخول
├── README.md                        # التوثيق
├── requirements.txt                 # المتطلبات
├── engine/
│   ├── __init__.py
│   ├── facts.py                     # فئات الحقائق
│   ├── rules.py                     # قواعد التحسين
│   └── optimizer.py                 # المحسن الرئيسي
├── knowledge_base/
│   ├── __init__.py
│   └── source_references.py         # مراجع المعرفة
├── examples/
│   ├── __init__.py
│   ├── case1_simple_select.py       # مثال 1
│   ├── case2_join_query.py          # مثال 2
│   ├── case3_subquery.py            # مثال 3
│   └── case4_aggregation.py         # مثال 4
└── docs/
    ├── report.md                    # هذا التقرير
    └── diagrams.md                  # جميع المخططات
```

---

## 12. أمثلة التشغيل

### 12.1 المثال الأول: استعلام SELECT بسيط
استعلام بسيط مع شرط WHERE ومؤشر على عمود الشرط. يتوقع النظام اقتراح استخدام Index Scan نظراً لوجود فهرس انتقائي على جدول كبير.

### 12.2 المثال الثاني: استعلام JOIN متعدد الجداول
استعلام يربط 3 جداول (orders, customers, products) مع إحصاءات قديمة. يتوقع النظام اقتراح تحديث الإحصاءات وإعادة ترتيب JOINs واختيار Hash Join المناسب.

### 12.3 المثال الثالث: استعلام Subquery
استعلام يحتوي على Subquery ترابطي مع IN. يتوقع النظام اقتراح إعادة كتابة Subquery إلى JOIN أو استخدام EXISTS.

### 12.4 المثال الرابع: استعلام تجميعي
استعلام مع GROUP BY و HAVING و DISTINCT وإحصاءات قديمة. يتوقع النظام اقتراح نقل الشروط إلى WHERE، فحص ضرورة DISTINCT، تحديث الإحصاءات.

---

## 13. الخلاصة والاستنتاجات

### 13.1 النتائج المحققة

تم بنجاح بناء نظام خبير لتحسين استعلامات SQL باستخدام:
- قاعدة معرفة منظمة تغطي 7 فئات من الحقائق
- 30 قاعدة تحسين تغطي جميع القرارات الرئيسية
- محرك استدلال قائم على خوارزمية Rete عبر مكتبة Experta
- 20 مخططاً تنظيمياً وتفسيرياً
- 4 أمثلة تشغيل متنوعة

### 13.2 المزايا

1. **النظام غير إجرائي:** جميع القرارات ناتجة من تطبيق القواعد على الحقائق
2. **قابلية التوسع:** يمكن إضافة قواعد جديدة بسهولة
3. **الشفافية:** كل توصية مصحوبة بتفسير ومرجع
4. **التوثيق الكامل:** تقرير أكاديمي + مخططات + كود + أمثلة

### 13.3 التوسعات المستقبلية

1. دمج محلل SQL فعلي لاستخراج الحقائق تلقائياً من استعلامات SQL الحقيقية
2. إضافة واجهة مستخدم رسومية (GUI) أو واجهة ويب
3. ربط النظام بقواعد بيانات حقيقية (PostgreSQL, MySQL) لجلب الإحصاءات مباشرة
4. إضافة قواعد تحسين أكثر تقدماً
5. دمج تقنيات التعلم الآلي لتحديد أولويات التوصيات بناءً على أنماط الاستخدام

### 13.4 الكلمة الختامية

يمثل هذا المشروع تطبيقاً عملياً لمفاهيم النظم الخبيرة في مجال تحسين استعلامات قواعد البيانات. يجمع المشروع بين المعرفة الأكاديمية (من المصادر المعتمدة) والتقنيات البرمجية الحديثة (Python + Experta) لتقديم نظام متكامل يمكن استخدامه في التعليم والبحث والتطبيقات العملية.

---

## 14. المراجع

1. **Database System Concepts, 7th Edition**
   Abraham Silberschatz, Henry F. Korth, S. Sudarshan
   Chapter 16: Query Optimization
   https://www.db-book.com

2. **Query Optimization Techniques in Microsoft SQL Server**
   Database Systems Journal, Volume 16, Issue 4
   https://www.dbjournal.ro/archive/16/16_4.pdf

3. **Optimizing SQL Query Performance: A Comprehensive Guide**
   Women in Technology - Medium
   https://medium.com/womenintechnology/optimizing-sql-query-performance-a-comprehensive-guide-6cb72b9f52ef

4. **Experta Documentation**
   https://github.com/nilp0inter/experta

5. **Rete Algorithm**
   Charles Forgy, "Rete: A Fast Algorithm for the Many Pattern/Many Object Pattern Match Problem"
   Artificial Intelligence, 1982
