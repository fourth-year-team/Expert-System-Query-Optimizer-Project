import streamlit as st
import fact_builder
import optimizer_engine
import report_generator
import validation

st.set_page_config(page_title="SQL Optimizer Expert", page_icon="🚀", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg-deep: #0b1120;
    --bg-surface: #111827;
    --bg-elevated: #1a2332;
    --border-subtle: rgba(255,255,255,0.06);
    --border-glass: rgba(255,255,255,0.08);
    --border-hover: rgba(96,165,250,0.25);
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --accent-blue: #60a5fa;
    --accent-purple: #a78bfa;
    --accent-emerald: #34d399;
    --accent-amber: #fbbf24;
    --accent-rose: #fb7185;
    --glow-blue: rgba(96,165,250,0.15);
    --glow-purple: rgba(167,139,250,0.12);
}

* { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

html, body, .stApp {
    background: var(--bg-deep) !important;
    background-image:
        radial-gradient(ellipse at 20% 50%, rgba(96,165,250,0.06) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(167,139,250,0.05) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 80%, rgba(52,211,153,0.03) 0%, transparent 50%);
    min-height: 100vh;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.15); }

/* ── Header ── */
.header {
    text-align: center;
    padding: 2rem 0 0.75rem 0;
    position: relative;
}

.header::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 60px;
    height: 3px;
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));
    border-radius: 2px;
}

.header h1 {
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #e879f9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.3rem;
}

.header .subtitle {
    color: var(--text-muted);
    font-size: 0.9rem;
    font-weight: 400;
    letter-spacing: 0.02em;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(11, 17, 32, 0.85) !important;
    backdrop-filter: blur(24px) saturate(1.4);
    border-right: 1px solid var(--border-glass);
    min-width: 260px !important;
}

section[data-testid="stSidebar"] > div {
    padding: 1.5rem 1.2rem !important;
}

.sidebar-label {
    color: var(--text-secondary);
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.75rem;
}

.sidebar-stat {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.4rem 0;
    color: var(--text-secondary);
    font-size: 0.85rem;
}

.sidebar-stat .value {
    color: var(--text-primary);
    font-weight: 600;
}

/* ── Glassmorphic Cards ── */
.glass-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(16px) saturate(1.3);
    border: 1px solid var(--border-glass);
    border-radius: 16px;
    padding: 1.25rem;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.glass-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
}

.glass-card:hover {
    border-color: var(--border-hover);
    transform: translateY(-1px);
}

/* ── Chat Bubbles ── */
.chat-row {
    display: flex;
    margin: 1rem 0;
    animation: msgEnter 0.45s cubic-bezier(0.16, 1, 0.3, 1);
}

.chat-row.user { justify-content: flex-end; }
.chat-row.assistant { justify-content: flex-start; }

.chat-bubble {
    max-width: 78%;
    padding: 0.85rem 1.25rem;
    border-radius: 18px;
    font-size: 0.93rem;
    line-height: 1.6;
    position: relative;
}

.chat-bubble.assistant {
    background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
    backdrop-filter: blur(12px) saturate(1.3);
    border: 1px solid var(--border-glass);
    color: var(--text-primary);
    border-bottom-left-radius: 4px;
}

.chat-bubble.assistant::before {
    content: '🧠';
    position: absolute;
    left: -2rem;
    top: 0.2rem;
    font-size: 1.1rem;
}

.chat-bubble.user {
    background: linear-gradient(135deg, rgba(96,165,250,0.18), rgba(167,139,250,0.14));
    backdrop-filter: blur(12px) saturate(1.3);
    border: 1px solid rgba(96,165,250,0.15);
    color: var(--text-primary);
    border-bottom-right-radius: 4px;
}

.chat-bubble.user::after {
    content: '👤';
    position: absolute;
    right: -2rem;
    top: 0.2rem;
    font-size: 1.1rem;
}

/* ── Animations ── */
@keyframes msgEnter {
    0% { opacity: 0; transform: translateY(16px) scale(0.97); }
    100% { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes shimmer {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* ── Buttons ── */
.stButton > button {
    background: rgba(255, 255, 255, 0.04) !important;
    backdrop-filter: blur(8px) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    padding: 0.45rem 1.2rem !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    letter-spacing: 0.01em;
}

.stButton > button:hover {
    background: rgba(96, 165, 250, 0.1) !important;
    border-color: rgba(96, 165, 250, 0.3) !important;
    box-shadow: 0 0 24px var(--glow-blue), 0 4px 12px rgba(0,0,0,0.2) !important;
    transform: translateY(-2px);
}

.stButton > button:active {
    transform: translateY(0) scale(0.98);
}

/* ── Yes/No Segmented Control ── */
.seg-group {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.5rem;
}

.seg-btn {
    flex: 1;
    text-align: center;
    padding: 0.5rem 0;
    border-radius: 10px;
    border: 1px solid var(--border-glass);
    background: rgba(255,255,255,0.03);
    color: var(--text-secondary);
    font-weight: 500;
    font-size: 0.88rem;
    cursor: pointer;
    transition: all 0.2s ease;
    user-select: none;
}

.seg-btn:hover {
    background: rgba(96,165,250,0.08);
    border-color: rgba(96,165,250,0.2);
    color: var(--text-primary);
}

/* ── Radio ── */
div[data-testid="stRadio"] > div {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(8px);
    border: 1px solid var(--border-glass);
    border-radius: 12px;
    padding: 0.6rem 0.8rem;
}

div[data-testid="stRadio"] label {
    color: var(--text-secondary) !important;
    font-size: 0.9rem !important;
    padding: 0.2rem 0;
}

div[data-testid="stRadio"] label:hover {
    color: var(--text-primary) !important;
}

div[data-testid="stRadio"] input:checked + div {
    color: var(--accent-blue) !important;
}

/* ── Progress Bar ── */
.progress-wrap {
    background: rgba(255,255,255,0.04);
    border-radius: 4px;
    height: 4px;
    overflow: hidden;
    margin: 0.75rem 0;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple), var(--accent-blue));
    background-size: 200% 100%;
    animation: shimmer 2.5s linear infinite;
    border-radius: 4px;
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── Status Badge ── */
.badge {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}
.badge-blue { background: rgba(96,165,250,0.12); color: #93c5fd; border: 1px solid rgba(96,165,250,0.15); }
.badge-green { background: rgba(52,211,153,0.12); color: #6ee7b7; border: 1px solid rgba(52,211,153,0.15); }
.badge-amber { background: rgba(251,191,36,0.12); color: #fcd34d; border: 1px solid rgba(251,191,36,0.15); }

/* ── Report ── */
.report-section h2 {
    color: var(--accent-blue);
    font-size: 1.15rem;
    font-weight: 700;
    margin: 1.5rem 0 0.75rem 0;
    letter-spacing: -0.01em;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border-subtle);
}

.report-section p, .report-section li {
    color: var(--text-secondary);
    font-size: 0.88rem;
    line-height: 1.7;
}

.report-section hr {
    border: none;
    border-top: 1px solid var(--border-subtle);
    margin: 1rem 0;
}

.report-section strong {
    color: var(--text-primary);
    font-weight: 600;
}

/* ── Alerts ── */
div[data-testid="stAlert"] {
    background: rgba(251,191,36,0.06) !important;
    border: 1px solid rgba(251,191,36,0.12) !important;
    border-radius: 12px !important;
    padding: 0.75rem 1rem !important;
}

div[data-testid="stAlert"] p {
    color: #fcd34d !important;
    font-size: 0.88rem !important;
}

/* ── Misc ── */
.stMarkdown { color: var(--text-secondary); }
div[data-testid="stMarkdownContainer"] p { color: var(--text-secondary); }
a { color: var(--accent-blue) !important; }
.stSpinner > div { border-color: var(--accent-blue) transparent transparent transparent !important; }
hr { border-color: var(--border-subtle) !important; }
</style>
""", unsafe_allow_html=True)

QUESTIONS = [
    # ── Query Structure ──
    {"id": "join_ops", "text": "Does the query contain JOIN operations?", "type": "yn"},
    {"id": "subqueries", "text": "Does the query contain subqueries?", "type": "yn"},
    {"id": "correlated_subquery", "text": "Are the subqueries correlated (reference outer query columns)?", "type": "yn", "depends_on": ("subqueries", True)},
    {"id": "exists", "text": "Does the query use EXISTS?", "type": "yn", "depends_on": ("subqueries", True)},
    {"id": "in", "text": "Does the query use IN?", "type": "yn", "depends_on": ("subqueries", True)},
    {"id": "not_in", "text": "Does the query use NOT IN?", "type": "yn", "depends_on": ("subqueries", True)},
    {"id": "group_by", "text": "Does the query contain GROUP BY?", "type": "yn"},
    {"id": "having", "text": "Does the query use HAVING (filter after aggregation)?", "type": "yn"},
    {"id": "order_by", "text": "Does the query contain ORDER BY?", "type": "yn"},
    {"id": "distinct", "text": "Does the query use DISTINCT?", "type": "yn"},
    {"id": "cte", "text": "Does the query use a CTE (WITH clause)?", "type": "yn"},
    {"id": "union", "text": "Does the query use UNION?", "type": "yn"},
    {"id": "limit", "text": "Does the query use LIMIT / OFFSET for pagination?", "type": "yn"},
    {"id": "or_condition", "text": "Does the query contain OR conditions in WHERE?", "type": "yn"},
    {"id": "select_star", "text": "Does the query use SELECT *?", "type": "yn"},

    # ── Table / Schema ──
    {"id": "table_size", "text": "How would you describe the table size?", "type": "choice", "options": ["small", "medium", "large"]},
    {"id": "partitioned", "text": "Is the table partitioned?", "type": "yn"},
    {"id": "partition_key_used", "text": "Is the partition key used in WHERE?", "type": "yn", "depends_on": ("partitioned", True)},
    {"id": "normalized_schema", "text": "Is the database schema properly normalized?", "type": "yn"},
    {"id": "data_type_issues", "text": "Are there any inappropriate data types (e.g. VARCHAR for dates)?", "type": "yn"},
    {"id": "excessive_joins", "text": "Does the query join 3 or more tables?", "type": "yn"},

    # ── Indexes ──
    {"id": "index_filter", "text": "Are indexes available on filter (WHERE) columns?", "type": "yn"},
    {"id": "index_join", "text": "Are indexes available on join columns?", "type": "yn", "depends_on": ("join_ops", True)},
    {"id": "composite_index", "text": "Is a composite (multi-column) index available?", "type": "yn"},
    {"id": "clustered_index", "text": "Is a clustered index available?", "type": "yn"},
    {"id": "index_fragmented", "text": "Are indexes fragmented?", "type": "yn"},
    {"id": "index_unused", "text": "Are there any unused indexes?", "type": "yn"},
    {"id": "fk_indexed", "text": "Are foreign key columns indexed?", "type": "yn"},
    {"id": "range_predicate", "text": "Does WHERE use range conditions (BETWEEN, >, <)?", "type": "yn"},

    # ── Join Details ──
    {"id": "both_large", "text": "Are both joined tables large?", "type": "yn", "depends_on": ("join_ops", True)},
    {"id": "one_smaller", "text": "Is one relation significantly smaller than the other?", "type": "yn", "depends_on": ("join_ops", True)},
    {"id": "join_equality", "text": "Is the join condition equality-based?", "type": "yn", "depends_on": ("join_ops", True)},
    {"id": "join_indexed", "text": "Is the join column indexed?", "type": "yn", "depends_on": ("join_ops", True)},
    {"id": "data_sorted", "text": "Is the data already sorted on the join/sort key?", "type": "yn", "depends_on": ("join_ops", True)},

    # ── Statistics ──
    {"id": "stats_up_to_date", "text": "Are statistics up to date?", "type": "yn"},
    {"id": "histogram_available", "text": "Is histogram information available?", "type": "yn"},

    # ── Query Patterns ──
    {"id": "wildcard_search", "text": "Does the query use LIKE with a leading wildcard (e.g. LIKE '%value')?", "type": "yn"},
    {"id": "cursor_usage", "text": "Does the query use cursors for row-by-row processing?", "type": "yn"},
    {"id": "stored_procedures", "text": "Are stored procedures used for complex logic?", "type": "yn"},
    {"id": "intermediate_large", "text": "Are intermediate result sets very large?", "type": "yn"},
    {"id": "result_critical", "text": "Is fast response time critical for this query?", "type": "yn"},

    # ── Workload / Environment ──
    {"id": "workload", "text": "Is the workload read-heavy or write-heavy?", "type": "choice", "options": ["read-heavy", "write-heavy"]},
    {"id": "parallel_available", "text": "Is parallel execution available?", "type": "yn"},
    {"id": "sufficient_memory", "text": "Is sufficient memory available?", "type": "yn"},
]

if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "Hello! I am your SQL Optimization Expert. I will guide you through a series of questions to analyze your query. Let's begin!"}]
if 'stage' not in st.session_state:
    st.session_state.stage = "INTERVIEW"

def add_message(role, content):
    st.session_state.chat_history.append({"role": role, "content": content})

def reset_system():
    st.session_state.step = 0
    st.session_state.answers = {}
    st.session_state.chat_history = [{"role": "assistant", "content": "Starting over! Let's begin the analysis."}]
    st.session_state.stage = "INTERVIEW"

st.markdown("""
<div class="header">
    <h1>SQL Optimization Expert</h1>
    <div class="subtitle">Expert System for Database Performance Tuning</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="sidebar-label">System Controls</div>', unsafe_allow_html=True)

    if st.button("Reset Session", use_container_width=True):
        reset_system()
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.stage == "INTERVIEW":
        total = len(QUESTIONS)
        answered_ids = set(st.session_state.answers.keys()) | {
            q["id"] for q in QUESTIONS
            if "depends_on" in q and st.session_state.answers.get(q["depends_on"][0]) != q["depends_on"][1]
        }
        done = min(st.session_state.step, total)
        pct = int(done / total * 100) if total > 0 else 0

        st.markdown('<div class="sidebar-label">Progress</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="sidebar-stat"><span>Questions answered</span><span class="value">{done}/{total}</span></div>',
            unsafe_allow_html=True
        )
        st.markdown(f'<div class="progress-wrap"><div class="progress-fill" style="width:{pct}%"></div></div>', unsafe_allow_html=True)

        answered_count = len(st.session_state.answers)
        if answered_count > 0:
            st.markdown(
                f'<div style="margin-top:0.3rem;display:flex;gap:0.4rem;flex-wrap:wrap;">'
                + ''.join(f'<span class="badge badge-green">{k}</span>' for k in st.session_state.answers.keys())
                + '</div>',
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(
        '<div style="color:var(--accent-blue);font-size:0.8rem;font-weight:600;margin-bottom:0.5rem;">About</div>'
        '<div style="color:var(--text-muted);font-size:0.78rem;line-height:1.6;">'
        'This system uses an Experta-based Rete inference engine to provide '
        'non-procedural optimization recommendations based on established database theory.',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ── Chat History ──
for msg in st.session_state.chat_history:
    st.markdown(
        f'<div class="chat-row {msg["role"]}">'
        f'<div class="chat-bubble {msg["role"]}">{msg["content"]}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

# ── Stage: INTERVIEW ──
if st.session_state.stage == "INTERVIEW":
    # Skip questions whose dependency condition isn't met
    while st.session_state.step < len(QUESTIONS):
        q = QUESTIONS[st.session_state.step]
        skip = False
        if "depends_on" in q:
            dep_id, dep_val = q["depends_on"]
            if st.session_state.answers.get(dep_id) != dep_val:
                skip = True
        if skip:
            st.session_state.step += 1
        else:
            break

    if st.session_state.step >= len(QUESTIONS):
        st.session_state.stage = "VALIDATION"
        st.rerun()
    else:
        q = QUESTIONS[st.session_state.step]

        st.markdown(
            f'<div class="chat-row assistant">'
            f'<div class="chat-bubble assistant">{q["text"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        if q["type"] == "yn":
            cols = st.columns([1, 1, 6])
            with cols[0]:
                if st.button("Yes", key=f"yes_{q['id']}", use_container_width=True):
                    add_message("user", "Yes")
                    st.session_state.answers[q["id"]] = True
                    st.session_state.step += 1
                    st.rerun()
            with cols[1]:
                if st.button("No", key=f"no_{q['id']}", use_container_width=True):
                    add_message("user", "No")
                    st.session_state.answers[q["id"]] = False
                    st.session_state.step += 1
                    st.rerun()
        elif q["type"] == "choice":
            choice = st.radio("", q["options"], key=f"choice_{q['id']}", label_visibility="collapsed")
            if st.button("Confirm", key=f"conf_{q['id']}", use_container_width=True):
                add_message("user", choice)
                st.session_state.answers[q["id"]] = choice
                st.session_state.step += 1
                st.rerun()

# ── Stage: VALIDATION ──
elif st.session_state.stage == "VALIDATION":
    inconsistencies = validation.validate_answers(st.session_state.answers)
    if inconsistencies:
        st.markdown(
            '<div class="chat-row assistant">'
            '<div class="chat-bubble assistant">⚠️ Inconsistent answers detected!</div>'
            '</div>',
            unsafe_allow_html=True
        )
        for inc in inconsistencies:
            st.warning(inc)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Correct Answers", use_container_width=True):
                reset_system()
                st.rerun()
        with col2:
            if st.button("Continue Anyway", use_container_width=True):
                st.session_state.stage = "RESULT"
                st.rerun()
    else:
        st.session_state.stage = "RESULT"
        st.rerun()

# ── Stage: RESULT ──
elif st.session_state.stage == "RESULT":
    st.markdown(
        '<div class="chat-row assistant">'
        '<div class="chat-bubble assistant">✅ Analysis complete! Here is your optimization report.</div>'
        '</div>',
        unsafe_allow_html=True
    )
    facts = fact_builder.build_facts(st.session_state.answers)
    results = optimizer_engine.run_optimizer(facts)
    full_report = report_generator.generate_report(st.session_state.answers, facts, results)

    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(full_report)
    st.markdown("---")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Start New Analysis", use_container_width=True):
        reset_system()
        st.rerun()
