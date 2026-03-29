import streamlit as st # type: ignore
import time
import os
import requests # type: ignore
import json
import re
import base64
import zlib
import streamlit.components.v1 as components # type: ignore
import pandas as pd  # type: ignore
from video_ai_tutor import *
from database import *
from cache_manager import *
from mcq_ai_tutor import *
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
# ==========================================
# 0. SECURE NATIVE AUTHENTICATION
# ==========================================
# 1. Load credentials directly from Streamlit Secrets
credentials = dict(st.secrets["credentials"])
cookie_config = dict(st.secrets["cookie"])

# 2. Initialize the Authenticator
authenticator = stauth.Authenticate(
    credentials,
    cookie_config['name'],
    cookie_config['key'],
    cookie_config['expiry_days']
)

# 3. Gatekeeper & Login UI
# This IF statement ensures the login box instantly vanishes upon success
if not st.session_state.get("authentication_status"):
    try:
        authenticator.login()
    except Exception as e:
        st.error(e)

    # Stop the app from loading the dashboard if they fail or haven't logged in
    if st.session_state.get("authentication_status") is False:
        st.error('Username/password is incorrect')
        st.stop()
    elif st.session_state.get("authentication_status") is None:
        st.warning('Please enter your username and password to access the portal.')
        st.stop()

# If the code reaches here, the user is successfully logged in!
current_user_role = credentials['usernames'][st.session_state["username"]]['role']
current_user_email = credentials['usernames'][st.session_state["username"]]['email']

# ==========================================
# 1. CONFIGURATION & STYLING
# ==========================================
st.set_page_config(layout="wide", page_title="Academic Portal", initial_sidebar_state="collapsed")

# --- MOBILE SCROLL FIX FOR TABLES & CODE ---
st.markdown("""
<style>
[data-testid="stMarkdownContainer"] table { display: block !important; overflow-x: auto !important; white-space: nowrap !important; }
[data-testid="stMarkdownContainer"] pre { overflow-x: auto !important; }
</style>
""", unsafe_allow_html=True)

try:
    with open("styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

st.markdown("""
<div class="scroll-btn" onclick="const container = document.querySelector('[data-testid=\\'stAppViewContainer\\']'); if (container) { container.scrollTo({ top: 0, behavior: 'smooth' }); }"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 5l-7 7h4v7h6v-7h4z"/></svg></div><div id="top"></div><a href="#top" class="scroll-btn">↑</a>
""", unsafe_allow_html=True)

# ==========================================
# NAVIGATION (Smart Routing)
# ==========================================
st.sidebar.markdown(f"**Welcome, {st.session_state['name']}**")
authenticator.logout('Log Out', 'sidebar')

st.sidebar.markdown("### Menu")

# Base options for all students
nav_options = ["Take Assessment", "Take Test", "View Videos"]

# Reveal hidden tabs ONLY if the user's role in secrets is 'admin'
if current_user_role == "admin":
    nav_options.insert(2, "Edit Content")
    nav_options.insert(3, "View Database")

app_mode = st.sidebar.radio("Nav", nav_options, label_visibility="collapsed")

# ==========================================
# 1. CONFIGURATION & STYLING
# ==========================================
st.set_page_config(layout="wide", page_title="Academic Portal", initial_sidebar_state="collapsed")

# --- MOBILE SCROLL FIX FOR TABLES & CODE ---
# This guarantees that tables and code blocks will scroll horizontally on phones
st.markdown("""
<style>
[data-testid="stMarkdownContainer"] table {
    display: block !important;
    overflow-x: auto !important;
    white-space: nowrap !important;
}
[data-testid="stMarkdownContainer"] pre {
    overflow-x: auto !important;
}
</style>
""", unsafe_allow_html=True)

try:
    with open("styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("styles.css not found.")

st.markdown("""
<div class="scroll-btn" onclick="
    const container = document.querySelector('[data-testid=\\'stAppViewContainer\\']');
    if (container) { container.scrollTo({ top: 0, behavior: 'smooth' }); }
">
<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 5l-7 7h4v7h6v-7h4z"/></svg>
</div>
<div id="top"></div><a href="#top" class="scroll-btn">↑</a>
""", unsafe_allow_html=True)

# ------------------------------------------
# TAKE ASSESSMENT
# ------------------------------------------
if app_mode == "Take Assessment":
    st.markdown("## Add")
    
    c1, c2, c3, c4 = st.columns([1, 0.6, 1.4, 0.8])
    
    subjects = fetch_data("SELECT * FROM subjects ORDER BY name ASC")
    if not subjects: st.stop()
    s_map = {s['name']: s['id'] for s in subjects}
    s_sel = c1.selectbox("Subject", list(s_map.keys()), key="assess_sub")
    
    weeks = fetch_data("SELECT DISTINCT week_number FROM assessments WHERE subject_id=%s ORDER BY week_number ASC", (s_map[s_sel],))
    if not weeks: st.stop()
    w_sel = c2.selectbox("Week", [w['week_number'] for w in weeks], key="assess_week")
    
    assessments = fetch_data("SELECT * FROM assessments WHERE subject_id=%s AND week_number=%s ORDER BY name ASC", (s_map[s_sel], w_sel))
    if not assessments: st.stop()
    a_map = {a['name']: a['id'] for a in assessments}
    a_sel = c3.selectbox("Activity", list(a_map.keys()), key="assess_act")
    
    mode = c4.selectbox("Mode", ["Study Mode", "Exam Mode"])
    st.divider() 

    questions = fetch_data("SELECT * FROM questions WHERE assessment_id=%s ORDER BY id ASC", (a_map[a_sel],))
    
    for i, q in enumerate(questions):
        with st.container(border=True):
            st.markdown(f"Q{i+1}. {q['heading']}")    
            render_content(q['media_type'], q['media_content'])
            
            # --- NUMERICAL LOGIC ---
            if q.get('q_type') == 'numerical':
                st.markdown("<br>", unsafe_allow_html=True)
                val = st.text_input(f"Answer Q{i+1}", key=f"num_{q['id']}")
                
                if mode == "Study Mode" and val:
                    if check_numerical_answer(val, q['correct_answer']): st.success("Correct")
                    else: st.error(f"Incorrect. Answer: {q['correct_answer']}")
                
                    ai_key = f"num_{q['id']}_{val}"
                    cached_res = get_cached_ai_response(ai_key)
                    
                    if cached_res:
                        render_ai_tutor_response(cached_res, ai_key)
                    else:
                        if st.button(f"Ask AI Tutor for Q{i+1}", key=f"ai_btn_{q['id']}", width="stretch", type="secondary"):
                            with st.spinner("Consulting AI Tutor..."):
                                explanation = ask_ai_tutor(s_sel, q['heading'], q['media_type'], q['media_content'], "Numerical Input", q['correct_answer'])
                                save_ai_cache(ai_key, explanation) 
                                st.rerun()

            # --- MCQ & MSQ LOGIC ---
            else:
                st.markdown("<br>", unsafe_allow_html=True)
                options = fetch_data("SELECT * FROM options WHERE question_id=%s ORDER BY id ASC", (q['id'],))
                
                is_multi = len([o for o in options if o['is_correct']]) > 1
                
                c_disp, c_sel = st.columns([0.90, 0.10])
                
                with c_disp:
                    for idx, opt in enumerate(options):
                        content = opt['media_content'] if (opt['media_content']) else opt['option_text']
                        status = None
                        if mode == "Study Mode":
                            if is_multi:
                                is_checked = st.session_state.get(f"chk_{q['id']}_{opt['id']}", False)
                                if is_checked:
                                    status = "correct" if opt['is_correct'] else "incorrect"
                            else:
                                selected_radio = st.session_state.get(f"rad_{q['id']}")
                                if selected_radio == str(idx + 1):
                                    status = "correct" if opt['is_correct'] else "incorrect"
                        
                        render_option_card(f"OPTION {idx+1}", content, opt['media_type'], status=status)
                
                with c_sel:
                    st.markdown('<span class="option-label">SELECT</span>', unsafe_allow_html=True)
                    
                    if is_multi:
                        sel_idxs = []
                        for idx, opt in enumerate(options):                            
                            if st.checkbox(f"{idx+1}", key=f"chk_{q['id']}_{opt['id']}"): 
                                sel_idxs.append(idx)
                    else:
                        r_opts = [f"{x+1}" for x in range(len(options))]
                        choice = st.radio(f"Rad_{i}", r_opts, index=None, label_visibility="collapsed", key=f"rad_{q['id']}")

                # --- AI TUTOR BUTTON LOGIC ---
                if mode == "Study Mode":
                    has_selection = (is_multi and len(sel_idxs) > 0) or (not is_multi and choice is not None)
                    
                    if has_selection:
                        ai_key = f"mcq_{q['id']}"
                        cached_res = get_cached_ai_response(ai_key)
                        
                        if cached_res:
                            render_ai_tutor_response(cached_res, ai_key)
                        else:
                            if st.button(f"Ask AI Tutor for Q{i+1}", key=f"ai_btn_{q['id']}", width="stretch", type="secondary"):
                                with st.spinner("Consulting AI Tutor..."):
                                    # Identify images in options and wrap them in a tag for the AI payload
                                    opt_texts = []
                                    for o in options:
                                        if o['media_type'] == 'image' and o['media_content']:
                                            opt_texts.append(f"[IMAGE: {o['media_content']}]")
                                        else:
                                            opt_texts.append(o['option_text'] or o['media_content'] or "No Content")

                                    if is_multi:
                                        u_choice = [opt_texts[idx] for idx in sel_idxs]
                                        c_ans = [opt_texts[i] for i, o in enumerate(options) if o['is_correct']]
                                    else:
                                        u_choice = opt_texts[int(choice) - 1] if choice else "No Answer"
                                        c_ans_list = [opt_texts[i] for i, o in enumerate(options) if o['is_correct']]
                                        c_ans = c_ans_list[0] if c_ans_list else "Unknown"
                                    
                                    explanation = ask_ai_tutor(s_sel, q['heading'], q['media_type'], q['media_content'], opt_texts, c_ans)
                                    save_ai_cache(ai_key, explanation) 
                                    st.rerun()

# ------------------------------------------
# TAKE TEST
# ------------------------------------------
elif app_mode == "Take Test":
    st.markdown("## Add")
    if 'test_state' not in st.session_state:
        st.session_state.test_state = 'setup'
        st.session_state.test_data = [] 
        st.session_state.curr_idx = 0
        st.session_state.responses = {} 

    if st.session_state.test_state == 'setup':
        st.markdown("### Configure Test")
        subs = fetch_data("SELECT * FROM subjects ORDER BY name ASC")
        if not subs: st.stop()
        
        c1, c2 = st.columns(2)
        s_sel = c1.selectbox("1. Select Subject", [s['name'] for s in subs])
        s_id = next(s['id'] for s in subs if s['name'] == s_sel)
        
        weeks = fetch_data("SELECT DISTINCT week_number FROM assessments WHERE subject_id=%s ORDER BY week_number ASC", (s_id,))
        if not weeks: st.warning("No data"); st.stop()
        
        w_sel = c2.multiselect("2. Select Weeks (Default: All)", [w['week_number'] for w in weeks])
        w_filter = tuple(w_sel) if w_sel else tuple([w['week_number'] for w in weeks])
        if len(w_filter) == 1: w_filter = f"({w_filter[0]})"
        else: w_filter = str(w_filter)
        
        ass_types = fetch_data(f"SELECT DISTINCT name FROM assessments WHERE subject_id=%s AND week_number IN {w_filter} ORDER BY name ASC", (s_id,))
        type_opts = [a['name'] for a in ass_types]
        t_sel = st.multiselect("3. Types (Default: All)", type_opts)
        t_filter = tuple(t_sel) if t_sel else tuple(type_opts)
        if len(t_filter) == 1: t_filter = f"('{t_filter[0]}')"
        else: t_filter = str(t_filter)
        
        count = fetch_data(f"SELECT COUNT(*) as cnt FROM questions q JOIN assessments a ON q.assessment_id = a.id WHERE a.subject_id=%s AND a.week_number IN {w_filter} AND a.name IN {t_filter}", (s_id,))[0]['cnt']
        st.info(f"Pool Size: {count}")
        num_q = st.number_input("4. Question Count", min_value=1, max_value=max(1, count), value=min(20, count))
        
        if st.button("Start Test", type="secondary"):
            q_query = f"SELECT q.* FROM questions q JOIN assessments a ON q.assessment_id = a.id WHERE a.subject_id=%s AND a.week_number IN {w_filter} AND a.name IN {t_filter} ORDER BY RANDOM() LIMIT %s"
            questions = fetch_data(q_query, (s_id, num_q))
            st.session_state.test_data = []
            for q in questions:
                opts = fetch_data("SELECT * FROM options WHERE question_id=%s ORDER BY id ASC", (q['id'],))
                st.session_state.test_data.append((q, opts))
            
            st.session_state.responses = {} 
            st.session_state.test_state = 'running'
            st.session_state.curr_idx = 0
            st.session_state.start_time = time.time()
            st.rerun()

    elif st.session_state.test_state == 'running':
        q, opts = st.session_state.test_data[st.session_state.curr_idx]
        total = len(st.session_state.test_data)
        
        st.markdown(f"Q{st.session_state.curr_idx + 1}. {q['heading']}")
        render_content(q['media_type'], q['media_content'])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if q.get('q_type') == 'numerical':
            col_q, col_a = st.columns([0.6, 0.4])
            with col_q: st.write("Numerical Answer")
            with col_a:
                val = st.text_input("Value:", key=f"t_num_{q['id']}")
                if val: st.session_state.responses[q['id']] = val
        else:
            c_disp, c_sel = st.columns([0.85, 0.15])
            with c_disp:
                for idx, opt in enumerate(opts):
                    content = opt['media_content'] if (opt['media_content']) else opt['option_text']
                    render_option_card(f"OPTION {idx+1}", content, opt['media_type'])
            
            with c_sel:
                st.markdown('<span class="option-label">SELECT</span>', unsafe_allow_html=True)
                is_multi = len([o for o in opts if o['is_correct']]) > 1
                
                if is_multi:
                    sel_list = []
                    for i, opt in enumerate(opts):
                        if st.checkbox(f"{i+1}", key=f"t_chk_{q['id']}_{opt['id']}"):
                            sel_list.append(opt['id'])
                    st.session_state.responses[q['id']] = sel_list
                else:
                    curr_sel = st.session_state.responses.get(q['id'])
                    prev_idx = None
                    if curr_sel:
                         try: prev_idx = next(i for i, o in enumerate(opts) if o['id'] == curr_sel)
                         except: pass
                    
                    sel = st.radio("Sel", [f"{i+1}" for i in range(len(opts))], index=prev_idx, label_visibility="collapsed", key=f"t_rad_{q['id']}")
                    if sel: 
                        idx = int(sel) - 1
                        st.session_state.responses[q['id']] = opts[idx]['id']

        st.markdown("<hr>", unsafe_allow_html=True)
        
        user_ans = st.session_state.responses.get(q['id'])
        has_ans = False
        if q.get('q_type') == 'numerical':
            if user_ans and str(user_ans).strip(): has_ans = True
        elif user_ans:
            if isinstance(user_ans, list) and len(user_ans) > 0: has_ans = True
            elif not isinstance(user_ans, list): has_ans = True

        if st.button("Submit", type="primary"):
            if not has_ans:
                st.error("Please provide an answer.")
            else:
                if st.session_state.curr_idx < total - 1:
                    st.session_state.curr_idx += 1
                    st.rerun()
                else:
                    st.session_state.end_time = time.time()
                    st.session_state.test_state = 'results'
                    st.rerun()

    elif st.session_state.test_state == 'results':
        st.markdown("### Results")
        
        score = 0
        total = len(st.session_state.test_data)
        
        results_data = []
        for idx, (q, opts) in enumerate(st.session_state.test_data):
            user_ans = st.session_state.responses.get(q['id'])
            is_correct = False
            if q.get('q_type') == 'numerical':
                if check_numerical_answer(user_ans, q['correct_answer']): is_correct = True
            else:
                corr_ids = [o['id'] for o in opts if o['is_correct']]
                if isinstance(user_ans, list):
                    if set(user_ans) == set(corr_ids): is_correct = True
                else:
                    if user_ans in corr_ids: is_correct = True
            
            if is_correct: score += 1
            results_data.append({'q':q, 'opts':opts, 'ans':user_ans, 'ok':is_correct})

        duration = st.session_state.end_time - st.session_state.start_time
        mins, secs = divmod(int(duration), 60)
        c1, c2, c3 = st.columns(3)
        c1.metric("Score", f"{score}/{total}", border=True)
        c2.metric("Percent", f"{int(score/total*100)}%", border=True)
        c3.metric("Time", f"{mins}m {secs}s", border=True)

        for idx, item in enumerate(results_data):
            q = item['q']
            opts = item['opts']
            user_ans = item['ans']
            is_ok = item['ok']
            
            with st.container(border=True):
                st.markdown(f"##### Q{idx+1}. {q['heading']}")
                render_content(q['media_type'], q['media_content'])
                st.markdown("---")
                
                col_u, col_c = st.columns(2)
                
                with col_u:
                    st.markdown("**YOUR ANSWER**")
                    if q.get('q_type') == 'numerical':
                        if is_ok: st.success(f"{user_ans}")
                        else: st.error(f"{user_ans}" if str(user_ans).strip() else "No Answer")
                    else:
                        if not user_ans:
                            st.error("No Answer")
                        else:
                            u_ids = user_ans if isinstance(user_ans, list) else [user_ans]
                            u_opts = [o for o in opts if o['id'] in u_ids]
                            
                            for o in u_opts:
                                content = o['media_content'] if o['media_type'] else o['option_text']
                                if o['media_type'] == 'code':
                                    blocks = str(content).split("uE000")
                                    formatted_blocks = []
                                    for b in blocks:
                                        if b.strip():
                                            lang = detect_language(b)
                                            formatted_blocks.append(f"```{lang}\n{b.strip()}\n```")
                                            
                                    combined_code = "\n\n".join(formatted_blocks)
                                    if is_ok: st.success(combined_code)
                                    else: st.error(combined_code)
                                elif o['media_type'] == 'image':
                                    if is_ok: st.success("Selected Image:")
                                    else: st.error("Selected Image:")
                                    render_content('image', content)
                                else:
                                    if is_ok: st.success(content)
                                    else: st.error(content)
                
                with col_c:
                    st.markdown("**CORRECT ANSWER**")
                    if q.get('q_type') == 'numerical':
                        st.success(f"{q['correct_answer']}")
                    else:
                        c_opts = [o for o in opts if o['is_correct']]
                        for o in c_opts:
                            content = o['media_content'] if o['media_type'] else o['option_text']
                            if o['media_type'] == 'code':
                                st.success(f"```python\n{content}\n```")
                            elif o['media_type'] == 'image':
                                st.success("Correct Image:")
                                render_content('image', content)
                            else:
                                st.success(content)

        if st.button("New Test", type="primary", icon=":material/assignment:"):
            st.session_state.test_state = 'setup'
            st.rerun()

# ------------------------------------------
# EDIT CONTENT (Password Protected via Form)
# ------------------------------------------
elif app_mode == "Edit Content":
    st.markdown("## Add")
    tab_edit_q, tab_edit_v, tab_edit_hier, tab_health, tab_sql  = st.tabs(["Edit Questions", "Edit Week Videos", "Edit Hierarchy", "Content Health", "Custom SQL"])
    # ==========================================
    # TAB 1: EDIT QUESTIONS
    # ==========================================
    with tab_edit_q:
        c1, c2, c3 = st.columns([1, 0.5, 1.5])

        subjects = fetch_data("SELECT * FROM subjects ORDER BY name ASC")

        # Use if/else instead of st.stop() to allow Tab 2 to render
        if not subjects:
            st.warning("No subjects found.")
        else:
            s_map = {s['name']: s['id'] for s in subjects}
            s_sel = c1.selectbox("Subject", list(s_map.keys()), key="edit_q_sub")

            weeks_data = fetch_data(
                "SELECT DISTINCT week_number FROM assessments WHERE subject_id = %s ORDER BY week_number ASC",
                (s_map[s_sel],)
            )

            week_opts = [w['week_number'] for w in weeks_data]

            if not week_opts:
                st.warning("No weeks found.")
            else:
                sel_week = c2.selectbox("Week", week_opts, key="edit_q_week")

                assessments = fetch_data(
                    "SELECT * FROM assessments WHERE subject_id = %s AND week_number = %s ORDER BY name ASC",
                    (s_map[s_sel], sel_week)
                )

                if not assessments:
                    st.warning("No activities found.")
                else:
                    a_map = {a['name']: a['id'] for a in assessments}
                    a_sel = c3.selectbox("Activity", list(a_map.keys()), key="edit_q_act")

                    # ---------------- QUESTIONS ----------------
                    questions = fetch_data(
                        "SELECT id, heading FROM questions WHERE assessment_id = %s ORDER BY id ASC",
                        (a_map[a_sel],)
                    )

                    if not questions:
                        st.warning("No questions found.")
                    else:
                        # Dropdown showing Q.No + ID
                        q_map = {}
                        for idx, q in enumerate(questions, start=1):
                            short_head = q['heading'][:60] + ("..." if len(q['heading']) > 60 else "")
                            label = f"Q{idx} | ID {q['id']} | {short_head}"
                            q_map[label] = q['id']

                        q_sel = st.selectbox("Select Question", list(q_map.keys()), key="edit_q_sel")
                        q_id = q_map[q_sel]

                        # ---------------- LOAD QUESTION ----------------
                        q_data = fetch_data("SELECT * FROM questions WHERE id = %s", (q_id,))[0]
                        opts_data = fetch_data("SELECT * FROM options WHERE question_id = %s ORDER BY id ASC", (q_id,))

                        #st.divider()

                        st.markdown(f"#### Editing Question ID: `{q_id}`")

                        # ---------------- EDIT FORM ----------------
                        with st.form("edit_form"):
                            st.markdown("#### Question Details")

                            # BIG RAW HEADING BOX
                            raw_heading = str(q_data['heading']) if q_data['heading'] is not None else ""
                            n_head = st.text_area("Heading (Raw DB Value)", value=raw_heading, height="content", key=f"heading_raw_{q_id}")

                            c_qm1, c_qm2 = st.columns([1, 4])

                            curr_q_mtype = q_data['media_type'] if q_data['media_type'] else "text"

                            n_mtype = c_qm1.selectbox(
                                "Media Type",
                                ["text", "code", "image"],
                                index=["text", "code", "image"].index(curr_q_mtype)
                            )

                            raw_media = str(q_data['media_content']) if q_data['media_content'] is not None else ""
                            n_cont = st.text_area(
                                "Media Content (Raw DB Value)",
                                value=raw_media,
                                height="content",
                                key=f"media_edit_{q_id}"
                            )

                            # ---------------- NUMERICAL QUESTION ----------------
                            if q_data.get('q_type') == 'numerical':
                                n_ans = st.text_input("Correct Answer", value=q_data.get('correct_answer') or ""                                )

                                if st.form_submit_button("Update Question"):
                                    final_q_mtype = n_mtype if n_mtype != "text" else None
                                    execute_query(
                                        """
                                        UPDATE questions
                                        SET heading=%s,
                                            media_type=%s,
                                            media_content=%s,
                                            correct_answer=%s
                                        WHERE id=%s
                                        """,
                                        (n_head, final_q_mtype, n_cont, n_ans, q_id)
                                    )
                                    st.success("Updated Successfully")
                                    st.rerun()

                            # ---------------- MCQ QUESTION ----------------
                            else:
                                st.markdown("#### Edit Options")
                                upd_opts = []

                                for opt in opts_data:
                                    c_a, c_b, c_c = st.columns([0.2, 0.7, 0.1])
                                    curr_type = opt['media_type'] if opt['media_type'] else "text"
                                    
                                    nt = c_a.selectbox(
                                        "Type",
                                        ["text", "code", "image"],
                                        key=f"type_{opt['id']}",
                                        index=["text", "code", "image"].index(curr_type)
                                    )

                                    raw_option = (str(opt['media_content']) if opt['media_content'] is not None else str(opt['option_text']) if opt['option_text'] is not None else "")
                                    nv = c_b.text_area(
                                        "Value (Exact DB)",
                                        value=raw_option,
                                        height="content",
                                        key=f"option_raw_{opt['id']}"
                                    )

                                    nc = c_c.checkbox(
                                        "Correct",
                                        value=opt['is_correct'],
                                        key=f"correct_{opt['id']}"
                                    )
                                    upd_opts.append((opt['id'], nt, nv, nc))

                                if st.form_submit_button("Update Question"):
                                    final_q_mtype = n_mtype if n_mtype != "text" else None
                                    execute_query(
                                        """
                                        UPDATE questions
                                        SET heading=%s,
                                            media_type=%s,
                                            media_content=%s
                                        WHERE id=%s
                                        """,
                                        (n_head, final_q_mtype, n_cont, q_id)
                                    )

                                    for oid, otype, oval, ocorr in upd_opts:
                                        if otype == "text":
                                            execute_query(
                                                """
                                                UPDATE options
                                                SET option_text=%s,
                                                    media_type=NULL,
                                                    media_content=NULL,
                                                    is_correct=%s
                                                WHERE id=%s
                                                """,
                                                (oval, ocorr, oid)
                                            )
                                        else:
                                            execute_query(
                                                """
                                                UPDATE options
                                                SET option_text=NULL,
                                                    media_type=%s,
                                                    media_content=%s,
                                                    is_correct=%s
                                                WHERE id=%s
                                                """,
                                                (otype, oval, ocorr, oid)
                                            )

                                    st.success("Updated Successfully")
                                    st.rerun()

    # ==========================================
    # TAB 2: EDIT WEEK VIDEOS
    # ==========================================
    with tab_edit_v:
        st.markdown("#### Manage YouTube Videos")
        #st.info("Assign YouTube URLs to specific weeks. These will appear in the 'View Videos' tab.")
        
        c1_v, c2_v = st.columns(2)
        
        v_subs = fetch_data("SELECT * FROM subjects ORDER BY name ASC")
        if not v_subs:
            st.warning("No subjects found.")
        else:
            vs_map = {s['name']: s['id'] for s in v_subs}
            vs_sel = c1_v.selectbox("Subject", list(vs_map.keys()), key="v_edit_sub")
            
            # Fetch from the `weeks` table
            v_weeks = fetch_data("SELECT * FROM weeks WHERE subject_id=%s ORDER BY week_number ASC", (vs_map[vs_sel],))
            
            if not v_weeks:
                st.warning("No weeks configured for this subject in the weeks table.")
            else:
                vw_map = {f"Week {w['week_number']}": w['id'] for w in v_weeks}
                vw_sel = c2_v.selectbox("Week", list(vw_map.keys()), key="v_edit_week")
                
                week_id = vw_map[vw_sel]
                
                # Fetch current videos
                curr_vid_data = fetch_data("SELECT youtube_urls FROM weeks WHERE id=%s", (week_id,))
                curr_urls = curr_vid_data[0].get('youtube_urls') if curr_vid_data else []
                curr_urls_str = "\n".join(curr_urls) if curr_urls else ""
                
                with st.form("edit_v_form"):
                    st.markdown("**YouTube URLs**")
                    st.caption("Paste video URLs below (one per line).")
                    new_urls_str = st.text_area("URLs", value=curr_urls_str, height=150, label_visibility="collapsed")
                    
                    if st.form_submit_button("Save Videos", type="primary"):
                        # Clean up lines and ignore empty ones
                        new_urls_list = [u.strip() for u in new_urls_str.split("\n") if u.strip()]
                        
                        # psycopg2 automatically handles python lists -> postgres text[] arrays
                        if execute_query("UPDATE weeks SET youtube_urls=%s WHERE id=%s", (new_urls_list, week_id)):
                            st.success(f"Successfully saved {len(new_urls_list)} video(s) to {vw_sel}!")
                            st.rerun()
                        else:
                            st.error("Failed to save videos.")
    # ==========================================
    # TAB 3: MANAGE STRUCTURE (Upgraded with Edit Capabilities)
    # ==========================================
    with tab_edit_hier:
        st.markdown("##### Manage Database Structure")
        
        # --- ROW 1: ADD NEW STRUCTURE ---
        c_sub, c_week, c_act = st.columns(3)

        # 1. Add Subject
        with c_sub:
            with st.container(border=True):
                st.markdown("**Add Subject**")
                with st.form("add_sub_form"):
                    new_sub_name = st.text_input("Subject Name")
                    if st.form_submit_button("Add Subject", type="primary", width="stretch"):
                        if new_sub_name.strip():
                            if execute_query("INSERT INTO subjects (name) VALUES (%s)", (new_sub_name.strip(),)):
                                st.success(f"Added '{new_sub_name}'")
                                st.rerun()
                            else:
                                st.error("Failed to add subject.")
                        else:
                            st.warning("Please enter a name.")

        hier_subs = fetch_data("SELECT * FROM subjects ORDER BY name ASC")

        # 2. Add Week
        with c_week:
            with st.container(border=True):
                st.markdown("**Add Week**")
                if hier_subs:
                    sub_sel_w = st.selectbox("Select Subject", [s['name'] for s in hier_subs], key="add_w_sub")
                    with st.form("add_week_form"):
                        sub_id_w = next(s['id'] for s in hier_subs if s['name'] == sub_sel_w)
                        new_week_num = st.number_input("Week Number", min_value=1, max_value=50, step=1)
                        if st.form_submit_button("Add Week", type="primary", width="stretch"):
                            if execute_query("INSERT INTO weeks (subject_id, week_number) VALUES (%s, %s)", (sub_id_w, new_week_num)):
                                st.success(f"Added Week {new_week_num} to {sub_sel_w}")
                                st.rerun()
                            else:
                                st.error(f"Failed. (Does Week {new_week_num} already exist?)")
                else:
                    st.warning("Add a subject first.")

        # 3. Add Activity
        with c_act:
            with st.container(border=True):
                st.markdown("**Add Activity**")
                if hier_subs:
                    sub_sel_a = st.selectbox("Select Subject", [s['name'] for s in hier_subs], key="act_sub_sel")
                    sub_id_a = next(s['id'] for s in hier_subs if s['name'] == sub_sel_a)
                    weeks_a = fetch_data("SELECT week_number FROM weeks WHERE subject_id=%s ORDER BY week_number ASC", (sub_id_a,))
                    if weeks_a:
                        week_sel_a = st.selectbox("Select Week", [w['week_number'] for w in weeks_a], key="add_a_week")
                        with st.form("add_act_form"):
                            new_act_name = st.text_input("Activity Name")
                            if st.form_submit_button("Add Activity", type="primary", width="stretch"):
                                if new_act_name.strip():
                                    if execute_query("INSERT INTO assessments (subject_id, week_number, name) VALUES (%s, %s, %s)", (sub_id_a, week_sel_a, new_act_name.strip())):
                                        st.success(f"Added '{new_act_name}'")
                                        st.rerun()
                                    else:
                                        st.error("Failed to add activity.")
                                else:
                                    st.warning("Please enter a name.")
                    else:
                        st.warning("Add a week to this subject first.")
                else:
                    st.warning("Add a subject first.")

        # --- ROW 2: EDIT EXISTING STRUCTURE ---
        st.divider()
        st.markdown("##### Edit Existing Structure")
        ce_sub, ce_week, ce_act = st.columns(3)

        # 1. Rename Subject
        with ce_sub:
            with st.container(border=True):
                st.markdown("**Rename Subject**")
                if hier_subs:
                    edit_sub_sel = st.selectbox("Select Subject to Rename", [s['name'] for s in hier_subs], key="edit_sub_sel")
                    edit_sub_id = next(s['id'] for s in hier_subs if s['name'] == edit_sub_sel)
                    with st.form("rename_sub_form"):
                        new_sub_name = st.text_input("New Name", value=edit_sub_sel)
                        if st.form_submit_button("Rename Subject", type="primary", width="stretch"):
                            if new_sub_name.strip() and new_sub_name.strip() != edit_sub_sel:
                                if execute_query("UPDATE subjects SET name = %s WHERE id = %s", (new_sub_name.strip(), edit_sub_id)):
                                    st.success(f"Renamed to '{new_sub_name}'")
                                    st.rerun()
                else:
                    st.info("No subjects available.")

        # 2. Change Week Number
        with ce_week:
            with st.container(border=True):
                st.markdown("**Change Week Number**")
                if hier_subs:
                    e_w_sub_sel = st.selectbox("Select Subject", [s['name'] for s in hier_subs], key="e_w_sub_sel")
                    e_w_sub_id = next(s['id'] for s in hier_subs if s['name'] == e_w_sub_sel)
                    e_weeks = fetch_data("SELECT * FROM weeks WHERE subject_id=%s ORDER BY week_number ASC", (e_w_sub_id,))
                    if e_weeks:
                        e_w_sel = st.selectbox("Select Week", [w['week_number'] for w in e_weeks], key="e_w_sel")
                        e_w_id = next(w['id'] for w in e_weeks if w['week_number'] == e_w_sel)
                        with st.form("edit_week_form"):
                            new_week_num = st.number_input("New Week Number", min_value=1, max_value=100, value=e_w_sel)
                            if st.form_submit_button("Update Week", type="primary", width="stretch"):
                                if new_week_num != e_w_sel:
                                    # Update week table
                                    execute_query("UPDATE weeks SET week_number = %s WHERE id = %s", (new_week_num, e_w_id))
                                    # Cascade update to assessments table
                                    execute_query("UPDATE assessments SET week_number = %s WHERE subject_id = %s AND week_number = %s", (new_week_num, e_w_sub_id, e_w_sel))
                                    st.success(f"Updated week to {new_week_num}")
                                    st.rerun()
                    else:
                        st.info("No weeks found.")

        # 3. Rename Activity
        with ce_act:
            with st.container(border=True):
                st.markdown("**Rename Activity**")
                if hier_subs:
                    e_a_sub_sel = st.selectbox("Select Subject", [s['name'] for s in hier_subs], key="e_a_sub_sel")
                    e_a_sub_id = next(s['id'] for s in hier_subs if s['name'] == e_a_sub_sel)
                    e_a_weeks = fetch_data("SELECT DISTINCT week_number FROM assessments WHERE subject_id=%s ORDER BY week_number ASC", (e_a_sub_id,))
                    if e_a_weeks:
                        e_a_w_sel = st.selectbox("Select Week", [w['week_number'] for w in e_a_weeks], key="e_a_w_sel")
                        e_acts = fetch_data("SELECT * FROM assessments WHERE subject_id=%s AND week_number=%s ORDER BY name ASC", (e_a_sub_id, e_a_w_sel))
                        if e_acts:
                            e_a_act_sel = st.selectbox("Select Activity", [a['name'] for a in e_acts], key="e_a_act_sel")
                            e_a_act_id = next(a['id'] for a in e_acts if a['name'] == e_a_act_sel)
                            with st.form("rename_act_form"):
                                new_act_name = st.text_input("New Activity Name", value=e_a_act_sel)
                                if st.form_submit_button("Rename Activity", type="primary", width="stretch"):
                                    if new_act_name.strip() and new_act_name.strip() != e_a_act_sel:
                                        if execute_query("UPDATE assessments SET name = %s WHERE id = %s", (new_act_name.strip(), e_a_act_id)):
                                            st.success(f"Renamed to '{new_act_name}'")
                                            st.rerun()
                        else:
                            st.info("No activities found.")
    
    # ==========================================
    # TOOL 4: Content Health Inspector (NEW)
    # ==========================================
    with tab_health:
        st.markdown("##### Content Health Inspector")
        
        # We use COALESCE and TRIM to make sure we don't accidentally flag 
        # numerical questions that don't have options.
        health_filter = "WHERE LOWER(TRIM(COALESCE(q.q_type, 'mcq'))) NOT IN ('numerical', 'nat')"

        # Audit 1: MCQs with 0 options
        st.markdown("**Potential Orphaned Questions (No Options)**")
        orphans = fetch_data(f"""
            SELECT q.id, q.heading, a.name as assessment 
            FROM questions q 
            JOIN assessments a ON q.assessment_id = a.id
            {health_filter}
            AND q.id NOT IN (SELECT DISTINCT question_id FROM options)
        """)
        
        if orphans:
            st.error(f"Found {len(orphans)} Multiple Choice questions with NO options!")
            st.dataframe(pd.DataFrame(orphans), width="stretch", hide_index=True)
        else:
            st.success("Content Health: All MCQs have options.")

        # Audit 2: MCQs with NO correct answer
        st.markdown("**Unsolvable Questions (No Correct Option)**")
        unsolvable = fetch_data(f"""
            SELECT q.id, q.heading
            FROM questions q
            {health_filter}
            AND q.id NOT IN (SELECT DISTINCT question_id FROM options WHERE is_correct = TRUE)
        """)
        
        if unsolvable:
            st.warning(f"Found {len(unsolvable)} MCQs with no correct answer marked.")
            st.dataframe(pd.DataFrame(unsolvable), width="stretch", hide_index=True)

    # ==========================================
    # TOOL 7: Custom SQL Executor
    # ==========================================
    with tab_sql:
        st.markdown("#### Run Custom SQL")
        query = st.text_area("Enter SQL Query", height="content", placeholder="SELECT * FROM questions WHERE id = 1;")
        if st.button("Execute Query", type="primary"):
            if query.strip() == "":
                st.error("Please enter a query.")
            elif query.strip().upper().startswith("SELECT"):
                try:
                    res = fetch_data(query)
                    if res:
                        st.dataframe(res, width="stretch")
                        st.success(f"Returned {len(res)} rows.")
                    else:
                        st.info("Query returned no results.")
                except Exception as e:
                    st.error(f"SQL Error: {e}")
            else:
                if execute_query(query):
                    st.success("Query executed and committed successfully.")
                else:
                    st.error("Failed to execute query. Check syntax and constraints.")

# ------------------------------------------
# VIEW DATABASE (Protected Admin Area)
# ------------------------------------------
elif app_mode == "View Database":
    st.markdown("## Add")
    # Fetch global table list
    tables = fetch_data("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    table_names = [t['table_name'] for t in tables] if tables else []

    # ---------------- DATABASE TOOLS TABS ----------------
    tabs = st.tabs([
        "Explorer",
        "Table Browser", 
        "Global Search",
        "Visual Dashboard",                
        "Schema Viewer", 
        "DB Stats", 
        "Export Hub"
    ])
    tab_hier, tab_browse, tab_search, tab_viz, tab_schema, tab_stats, tab_export = tabs
    
    # ==========================================
    # TOOL 1: Hierarchy Explorer (With Option Drill-down)
    # ==========================================
    with tab_hier:
        c1, c2, c3 = st.columns(3)
        
        subs = fetch_data("SELECT id, name FROM subjects ORDER BY name ASC")
        if subs:
            s_map = {s['name']: s['id'] for s in subs}
            s_sel = c1.selectbox("Subject", list(s_map.keys()), key="hier_sub")
            
            weeks = fetch_data("SELECT DISTINCT week_number FROM assessments WHERE subject_id=%s ORDER BY week_number ASC", (s_map[s_sel],))
            if weeks:
                w_sel = c2.selectbox("Week", [w['week_number'] for w in weeks], key="hier_week")
                
                assessments = fetch_data("SELECT id, name FROM assessments WHERE subject_id=%s AND week_number=%s ORDER BY name ASC", (s_map[s_sel], w_sel))
                if assessments:
                    a_map = {a['name']: a['id'] for a in assessments}
                    a_sel = c3.selectbox("Activity", list(a_map.keys()), key="hier_act")
                    
                    st.markdown(f"###### Questions in `{a_sel}`")
                    
                    q_query = """
                        SELECT 
                            q.id as "Qid", 
                            q.heading as "Heading", 
                            q.q_type as "Q_Type", 
                            q.correct_answer as "c_ans",
                            q.media_type as "media_type", 
                            q.media_content as "media_content",
                            count(o.id) as "total_options" 
                        FROM questions q 
                        LEFT JOIN options o ON q.id = o.question_id 
                        WHERE q.assessment_id = %s 
                        GROUP BY q.id ORDER BY q.id ASC
                    """
                    questions_data = fetch_data(q_query, (a_map[a_sel],))
                    
                    if questions_data:
                        st.dataframe(questions_data, width="stretch", hide_index=False)
                        
                        st.markdown("###### Inspect Options")
                        q_ids = [q["Qid"] for q in questions_data]
                        
                        col_drill_1, col_drill_2 = st.columns([0.5, 3.5])
                        selected_q_id = col_drill_1.selectbox("Select Question ID:", [None] + q_ids, key="drill_q")
                        
                        if selected_q_id:
                            opts = fetch_data("""
                                SELECT 
                                    id as "OID", 
                                    option_text as "Text", 
                                    media_type as "media_type",
                                    media_content as "Media Content",
                                    is_correct as "Is Correct?"
                                FROM options 
                                WHERE question_id=%s ORDER BY id ASC
                            """, (selected_q_id,))
                            
                            with col_drill_2:
                                if opts:
                                    st.dataframe(opts, width="stretch", hide_index=True)
                                else:
                                    st.info("No options found. This is likely a Numerical question.")
                    else:
                        st.info("No questions found for this activity.")
                else:
                    st.warning("No activities found for this week.")
            else:
                st.warning("No weeks found for this subject.")
        else:
            st.warning("No subjects found in the database.")

    # ==========================================
    # TOOL 2: GUI Visual Dashboard (Expanded)
    # ==========================================
    with tab_viz:
        st.markdown("##### Database Analytics")
        
        v_col1, v_col2 = st.columns(2)
        
        # Graph 1: Questions per Subject
        with v_col1:
            st.markdown("**Total Questions per Subject**")
            q_per_sub = fetch_data("""
                SELECT s.name as subject, count(q.id) as question_count 
                FROM subjects s 
                LEFT JOIN assessments a ON s.id = a.subject_id 
                LEFT JOIN questions q ON a.id = q.assessment_id 
                GROUP BY s.name
            """)
            if q_per_sub:
                df_sub = pd.DataFrame(q_per_sub).set_index("subject")
                st.bar_chart(df_sub, color="#f9a01b")
                
        # Graph 2: Questions Types
        with v_col2:
            st.markdown("**Question Format Distribution**")
            q_types = fetch_data("""
                SELECT COALESCE(q_type, 'mcq') as format, COUNT(id) as count 
                FROM questions GROUP BY format
            """)
            if q_types:
                df_types = pd.DataFrame(q_types).set_index("format")
                st.bar_chart(df_types, color="#0099ff")


        # Graph 3: Area Chart of Questions Added per Week
        st.markdown("**Questions Distributed Across Weeks**")
        q_per_week = fetch_data("""
            SELECT a.week_number, count(q.id) as question_count 
            FROM assessments a 
            JOIN questions q ON a.id = q.assessment_id 
            GROUP BY a.week_number 
            ORDER BY a.week_number ASC
        """)
        if q_per_week:
            df_week = pd.DataFrame(q_per_week).set_index("week_number")
            st.area_chart(df_week, color="#00ff99")

        st.markdown("---")
        
        # Graph 4: Scatter Plot (Complexity Matrix)
        st.markdown("**Complexity Matrix (Options per Question by Week)**")
        scatter_data = fetch_data("""
            SELECT a.week_number as "Week", count(o.id) as "Options Count"
            FROM assessments a 
            JOIN questions q ON a.id = q.assessment_id 
            LEFT JOIN options o ON q.id = o.question_id
            GROUP BY a.week_number, q.id
        """)
        if scatter_data:
            df_scatter = pd.DataFrame(scatter_data)
            # Scatter chart shows density of question complexity over the weeks
            st.scatter_chart(df_scatter, x="Week", y="Options Count", color="#ff0055", size=50)

        m_col1, m_col2 = st.columns(2)
        
        with m_col1:
            st.markdown("**Media in Questions**")
            q_media = fetch_data("SELECT COALESCE(media_type, 'text-only') as media, COUNT(id) as count FROM questions GROUP BY media")
            if q_media:
                st.bar_chart(pd.DataFrame(q_media).set_index("media"), color="#8884d8")
                
        with m_col2:
            st.markdown("**Media in Options**")
            o_media = fetch_data("SELECT COALESCE(media_type, 'text-only') as media, COUNT(id) as count FROM options GROUP BY media")
            if o_media:
                st.bar_chart(pd.DataFrame(o_media).set_index("media"), color="#82ca9d")



    # ==========================================
    # TOOL 5: Global Keyword Search
    # ==========================================
    with tab_search:
        st.markdown("##### Search All Content")
        kw = st.text_input("Enter keyword to find across Questions and Options:")
        
        if st.button("Search Database", type="primary") and kw.strip():
            search_term = f"%{kw.strip()}%"
            q_res = fetch_data("SELECT id, assessment_id, heading as content, 'Question Heading' as source FROM questions WHERE heading ILIKE %s LIMIT 50", (search_term,))
            o_res = fetch_data("SELECT id, question_id, option_text as content, 'Option Text' as source FROM options WHERE option_text ILIKE %s LIMIT 50", (search_term,))
            
            if q_res:
                st.markdown("**Found in Questions:**")
                st.dataframe(q_res, width="stretch", hide_index=True)
            if o_res:
                st.markdown("**Found in Options:**")
                st.dataframe(o_res, width="stretch", hide_index=True)
            if not q_res and not o_res:
                st.info(f"No results found for '{kw}'.")

    # ==========================================
    # TOOL 6: Table Browser
    # ==========================================
    with tab_browse:
        st.markdown("#### Raw Table Browser")
        if table_names:
            selected_table = st.selectbox("Select Table to View", table_names, key="browse_tab")
            if selected_table:
                limit = st.number_input("Row Limit", min_value=10, max_value=5000, value=100, step=50)
                data = fetch_data(f"SELECT * FROM {selected_table} LIMIT {limit}")
                if data:
                    st.dataframe(data, width="stretch")
                else:
                    st.info(f"The `{selected_table}` table is currently empty.")

    

    # ==========================================
    # TOOL 8: Schema Viewer
    # ==========================================
    with tab_schema:
        st.markdown("#### Table Structures")
        if table_names:
            schema_table = st.selectbox("Select Table to Inspect", table_names, key="schema_tab")
            schema_query = """
                SELECT column_name, data_type, character_maximum_length as max_length, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = %s
            """
            schema_data = fetch_data(schema_query, (schema_table,))
            if schema_data:
                st.dataframe(schema_data, width="stretch", hide_index=True)

    # ==========================================
    # TOOL 9: Database Statistics
    # ==========================================
    with tab_stats:
        st.markdown("#### Database Overview")
        if table_names:
            stat_data = []
            total_db_records = 0
            for t in table_names:
                try:
                    count = fetch_data(f"SELECT COUNT(*) as cnt FROM {t}")[0]['cnt']
                    stat_data.append({"Table Name": t, "Total Rows": count})
                    total_db_records += count
                except: pass
            
            st.metric("Total Database Records", total_db_records)
            if stat_data:
                st.dataframe(stat_data, width="stretch", hide_index=True)

    # ==========================================
    # TOOL 10: Export Hub
    # ==========================================
    with tab_export:
        st.markdown("#### Download Table Data (CSV)")
        if table_names:
            export_table = st.selectbox("Select Table to Export", table_names, key="export_tab")
            if st.button(f"Generate CSV for {export_table}"):
                with st.spinner("Generating file..."):
                    export_data = fetch_data(f"SELECT * FROM {export_table}")
                    if export_data:
                        import csv, io
                        output = io.StringIO()
                        writer = csv.DictWriter(output, fieldnames=export_data[0].keys())
                        writer.writeheader()
                        writer.writerows(export_data)
                        st.download_button(
                            label=f"Download {export_table}.csv",
                            data=output.getvalue(),
                            file_name=f"{export_table}_backup.csv",
                            mime="text/csv",
                            type="primary"
                        )
                    else:
                        st.warning(f"`{export_table}` is empty.")


# ------------------------------------------
# VIEW VIDEOS
# ------------------------------------------
elif app_mode == "View Videos":
    st.markdown("## Add")
    # ---------------- SUBJECT / WEEK ----------------
    c0, c1, c2 = st.columns([1, 1, 1])
    
    subjects = fetch_data("SELECT * FROM subjects ORDER BY name ASC")
    if not subjects: 
        st.warning("No subjects found.")
        st.stop()
        
    s_map = {s['name']: s['id'] for s in subjects}
    s_sel = c1.selectbox("Subject", list(s_map.keys()), key="vid_sub")
    
    # Now we fetch weeks directly from the new weeks table!
    weeks = fetch_data("SELECT * FROM weeks WHERE subject_id=%s ORDER BY week_number ASC", (s_map[s_sel],))
    if not weeks: 
        st.warning(f"No weeks configured for {s_sel} yet.")
        c0.markdown("#### Video Lectures & Resources")
        st.stop()
        
    w_map = {f"Week {w['week_number']}": w['id'] for w in weeks}
    w_sel = c2.selectbox("Week", list(w_map.keys()), key="vid_week")
    
    #st.markdown("---")
    
    # ---------------- RENDER VIDEOS ----------------
    # Fetch the youtube_urls array using the week's unique ID
    week_data = fetch_data("SELECT youtube_urls FROM weeks WHERE id=%s", (w_map[w_sel],))
    week_id = w_map[w_sel]

    if week_data and week_data[0].get('youtube_urls'):
        urls = week_data[0]['youtube_urls']
        
        if isinstance(urls, list) and len(urls) > 0:
            c0.markdown(f"#### Lectures for {s_sel} - {w_sel}")
            
            state_key = f"active_vid_{week_id}"
            if state_key not in st.session_state:
                # Default to the first video in the list
                st.session_state[state_key] = urls[0]

            # 2. Create the Layout Columns (Big Left, Small Right)
            col_player, col_playlist = st.columns([2.5, .8])

            # Big Player Container
            with col_player:
                with st.container(border=True):
                    # Render whatever video URL is currently stored in the session state
                    current_url = st.session_state[state_key]
                    st.video(current_url)
            
            # Scrollable Playlist Container
            with col_playlist:
                #st.markdown("##### Playlist")
                # Using a fixed-height container so it scrolls if you have 10+ videos
                with st.container(height="content", border=True):
                    for idx, url in enumerate(urls):
                        if url and url.strip():
                            # Highlight the active video button by making its type "primary"
                            is_active = (st.session_state[state_key] == url.strip())
                            btn_type = "primary" if is_active else "secondary"
                            btn_label = f"Lecture {idx + 1}" if is_active else f"Lecture {idx + 1}"
                            
                            # If a button is clicked, update the state and instantly refresh
                            if st.button(btn_label, key=f"vid_btn_{week_id}_{idx}", type=btn_type, width="stretch"):
                                st.session_state[state_key] = url.strip()
                                st.rerun()
            with st.expander("AI Tutor: Generate Lecture Notes", expanded=False, icon=":material/model_training:"):
                # --- AI TUTOR INTEGRATION ---
                try:
                    vid_id = extract_youtube_id(current_url)
                except NameError:
                    vid_id = None
                    st.error("Error: video_ai_tutor logic not imported properly.")
                    
                if vid_id:
                    # ADD THESE LINES:
                    cached_vid = get_cached_video_notes(vid_id)
                    if cached_vid:
                        render_video_notes(cached_vid, vid_id)
                    else:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("Generate Deep-Dive Lecture Notes", key=f"gen_notes_{vid_id}", type="secondary", width="stretch"):
                            with st.spinner("Compiling elite notes..."):
                                # --- UPDATED API KEY LOGIC ---
                                # 1. Look for dedicated Video Keys first
                                if "GEMINI_VIDEO_KEYS" in st.secrets:
                                    video_api_keys = st.secrets["GEMINI_VIDEO_KEYS"]
                                elif "GEMINI_VIDEO_KEY" in st.secrets:
                                    video_api_keys = [st.secrets.get("GEMINI_VIDEO_KEY")]
                                # 2. Fall back to the standard MCQ keys if video keys aren't found
                                elif "GEMINI_KEYS" in st.secrets:
                                    video_api_keys = st.secrets["GEMINI_KEYS"]
                                else:
                                    video_api_keys = [st.secrets.get("GEMINI_KEY")]
                                
                                ai_response = ask_video_ai(s_sel, current_url, video_api_keys)
                                save_video_cache(vid_id, ai_response) # Saves to PostgreSQL
                                st.rerun()

        else:
            st.info(f"No videos are currently linked to {w_sel}.")
            c0.markdown("#### Video Lectures & Resources")
    else:
        st.info(f"No videos are currently linked to {w_sel}.")
        c0.markdown("#### Video Lectures & Resources")