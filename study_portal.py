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
from video_quiz_tutor import *

@st.cache_data(show_spinner=False, ttl=604800) # Caches the title for a week so the app stays lightning fast
def fetch_youtube_title(url):
    """Fetches the actual video title directly from YouTube's public oEmbed API."""
    try:
        oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
        response = requests.get(oembed_url, timeout=3)
        if response.status_code == 200:
            return response.json().get('title', 'Unknown Title')
    except:
        pass
    return None
# ==========================================
# 1. ESSENTIAL CONFIG & STYLING (MUST BE FIRST)
# ==========================================
st.set_page_config(layout="wide", page_title="Academic Portal", initial_sidebar_state="collapsed")

try:
    with open("styles.css", "r") as f:
        css_content = f.read()
        
        html_payload = f"""
        <style>{css_content}</style>

        <div id="top" style="scroll-margin-top: 5rem; height: 0; visibility: hidden;"></div>

        <a href="#top" class="scroll-btn" title="Go to top">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="white">
                <path fill="white" d="M4 12l1.41 1.41L11 7.83V20h2V7.83l5.59 5.58L20 12 12 4z"/>
            </svg>
        </a>
        """
        st.html(html_payload)
except FileNotFoundError:
    pass



# ==========================================
# 0. SECURE NATIVE AUTHENTICATION
# ==========================================
# Helper function to deeply convert Streamlit's read-only secrets into a normal, editable dictionary
def make_mutable_dict(d):
    # Use hasattr instead of isinstance(dict) because Streamlit Secrets act like dicts but aren't true dicts
    if hasattr(d, 'items'):
        return {k: make_mutable_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [make_mutable_dict(v) for v in d]
    return d

# 1. Load and deeply convert credentials
credentials = make_mutable_dict(st.secrets["credentials"])
cookie_config = make_mutable_dict(st.secrets["cookie"])

# 2. Initialize the Authenticator
authenticator = stauth.Authenticate(
    credentials,
    cookie_config['name'],
    cookie_config['key'],
    cookie_config['expiry_days']
)

# 3. Gatekeeper & Login UI
if not st.session_state.get("authentication_status"):
    try:
        authenticator.login()
    except Exception as e:
        st.error(e)

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
# NAVIGATION (Smart Routing)
# ==========================================
st.sidebar.markdown(f"## Welcome, {st.session_state['name']}")
st.sidebar.markdown("### Menu")
# Base options for all students
nav_options = ["Take Assessment", "Take Test", "View Videos","AI Notes"]

# Reveal hidden tabs ONLY if the user's role in secrets is 'admin'
if current_user_role == "admin":
    nav_options.insert(4, "Edit Content")
    nav_options.insert(5, "View Database")

app_mode = st.sidebar.radio("Nav", nav_options, label_visibility="collapsed")
authenticator.logout('Log Out', 'sidebar')


# ------------------------------------------
# TAKE ASSESSMENT
# ------------------------------------------
if app_mode == "Take Assessment":    
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
                            with st.expander("View AI Tutor Analysis", expanded=False, icon=":material/model_training:"):
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
    #st.markdown("## Add")
    if 'test_state' not in st.session_state:
        st.session_state.test_state = 'setup'
        st.session_state.test_data = [] 
        st.session_state.curr_idx = 0
        st.session_state.responses = {} 

    if st.session_state.test_state == 'setup':
        st.markdown("### Configure Test")
        subs = fetch_data("SELECT * FROM subjects ORDER BY name ASC")
        if not subs: 
            st.warning("No subjects available.")
            st.stop()
        
        c1, c2 = st.columns(2)
        s_sel = c1.selectbox("Select Subject", [s['name'] for s in subs])
        s_id = next(s['id'] for s in subs if s['name'] == s_sel)
        
        weeks = fetch_data("SELECT DISTINCT week_number FROM assessments WHERE subject_id=%s ORDER BY week_number ASC", (s_id,))
        if not weeks: 
            st.warning("No weeks found for this subject.")
            st.stop()
        
        w_sel = c2.multiselect("Select Weeks (Default: All)", [w['week_number'] for w in weeks])
        w_filter = tuple(w_sel) if w_sel else tuple([w['week_number'] for w in weeks])
        if len(w_filter) == 1: w_filter = f"({w_filter[0]})"
        else: w_filter = str(w_filter)
        
        ass_types = fetch_data(f"SELECT DISTINCT name FROM assessments WHERE subject_id=%s AND week_number IN {w_filter} ORDER BY name ASC", (s_id,))
        type_opts = [a['name'] for a in ass_types]
        t_sel = st.multiselect("Types (Default: All)", type_opts)
        t_filter = tuple(t_sel) if t_sel else tuple(type_opts)
        if len(t_filter) == 1: t_filter = f"('{t_filter[0]}')"
        else: t_filter = str(t_filter)
        
        # --- THE SAFETY CHECK ---
        count_res = fetch_data(f"SELECT COUNT(*) as cnt FROM questions q JOIN assessments a ON q.assessment_id = a.id WHERE a.subject_id=%s AND a.week_number IN {w_filter} AND a.name IN {t_filter}", (s_id,))
        count = count_res[0]['cnt'] if count_res else 0

        if count == 0:
            st.error("No questions found for the selected criteria. Please change your filters.")
        else:
            st.info(f"Pool Size: {count} Questions")
            
            # The 'value' logic now has a safety floor of 1 to prevent the StreamlitValueBelowMinError
            num_q = st.number_input("Question Count", min_value=1, max_value=count, value=min(20, count))

        
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
# EDIT CONTENT (Admin Area)
# ------------------------------------------
elif app_mode == "Edit Content":
    # Renamed the second tab to reflect it handles more than just videos now
    tab_edit_q, tab_edit_w, tab_edit_hier, tab_health, tab_sql = st.tabs([
        "Edit Questions", "Edit Week Details", "Edit Hierarchy", "Content Health", "Custom SQL"
    ])
    
    # ==========================================
    # TAB 1: EDIT QUESTIONS (Upgraded with New Attributes)
    # ==========================================
    with tab_edit_q:
        c1, c2, c3 = st.columns([1, 0.5, 1.5])

        subjects = fetch_data("SELECT * FROM subjects ORDER BY name ASC")

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

                        st.markdown(f"#### Editing Question ID: `{q_id}`")

                        # ---------------- EDIT FORM ----------------
                        with st.form("edit_form"):
                            st.markdown("#### Core Details")

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
                            n_cont = c_qm2.text_area("Media Content", value=raw_media, height="content", key=f"media_edit_{q_id}")

                            # --- NEW ATTRIBUTES SECTION ---
                            st.markdown("#### Metadata & Explanations")
                            c_meta1, c_meta2 = st.columns(2)
                            curr_diff = q_data.get('difficulty') or "Medium"
                            n_diff = c_meta1.selectbox("Difficulty", ["Easy", "Medium", "Hard"], index=["Easy", "Medium", "Hard"].index(curr_diff))
                            n_pts = c_meta2.number_input("Points", min_value=1, value=int(q_data.get('points') or 1))
                            
                            n_exp = st.text_area("Manual Explanation / Tutor Note", value=q_data.get('manual_explanation') or "", height=100)

                            # ---------------- NUMERICAL LOGIC ----------------
                            if q_data.get('q_type') == 'numerical':
                                n_ans = st.text_input("Correct Answer", value=q_data.get('correct_answer') or "")

                                if st.form_submit_button("Update Question", type="primary"):
                                    final_q_mtype = n_mtype if n_mtype != "text" else None
                                    execute_query(
                                        """
                                        UPDATE questions
                                        SET heading=%s, media_type=%s, media_content=%s, correct_answer=%s,
                                            difficulty=%s, points=%s, manual_explanation=%s
                                        WHERE id=%s
                                        """,
                                        (n_head, final_q_mtype, n_cont, n_ans, n_diff, n_pts, n_exp, q_id)
                                    )
                                    st.success("Updated Successfully")
                                    st.rerun()

                            # ---------------- MCQ LOGIC ----------------
                            else:
                                st.markdown("#### Edit Options")
                                upd_opts = []

                                for opt in opts_data:
                                    c_a, c_b, c_c = st.columns([0.2, 0.7, 0.1])
                                    curr_type = opt['media_type'] if opt['media_type'] else "text"
                                    nt = c_a.selectbox("Type", ["text", "code", "image"], key=f"type_{opt['id']}", index=["text", "code", "image"].index(curr_type))
                                    raw_option = (str(opt['media_content']) if opt['media_content'] is not None else str(opt['option_text']) if opt['option_text'] is not None else "")
                                    nv = c_b.text_area("Value", value=raw_option, height="content", key=f"option_raw_{opt['id']}")
                                    nc = c_c.checkbox("Correct", value=opt['is_correct'], key=f"correct_{opt['id']}")
                                    upd_opts.append((opt['id'], nt, nv, nc))

                                if st.form_submit_button("Update Question", type="primary"):
                                    final_q_mtype = n_mtype if n_mtype != "text" else None
                                    execute_query(
                                        """
                                        UPDATE questions
                                        SET heading=%s, media_type=%s, media_content=%s,
                                            difficulty=%s, points=%s, manual_explanation=%s
                                        WHERE id=%s
                                        """,
                                        (n_head, final_q_mtype, n_cont, n_diff, n_pts, n_exp, q_id)
                                    )

                                    for oid, otype, oval, ocorr in upd_opts:
                                        if otype == "text":
                                            execute_query("UPDATE options SET option_text=%s, media_type=NULL, media_content=NULL, is_correct=%s WHERE id=%s", (oval, ocorr, oid))
                                        else:
                                            execute_query("UPDATE options SET option_text=NULL, media_type=%s, media_content=%s, is_correct=%s WHERE id=%s", (otype, oval, ocorr, oid))

                                    st.success("Updated Successfully")
                                    st.rerun()

    # ==========================================
    # TAB 2: EDIT WEEK DETAILS (Upgraded)
    # ==========================================
    with tab_edit_w:
        st.markdown("#### Manage Week Details & Videos")
        
        c1_v, c2_v = st.columns(2)
        v_subs = fetch_data("SELECT * FROM subjects ORDER BY name ASC")
        
        if not v_subs:
            st.warning("No subjects found.")
        else:
            vs_map = {s['name']: s['id'] for s in v_subs}
            vs_sel = c1_v.selectbox("Subject", list(vs_map.keys()), key="v_edit_sub")
            
            v_weeks = fetch_data("SELECT * FROM weeks WHERE subject_id=%s ORDER BY week_number ASC", (vs_map[vs_sel],))
            
            if not v_weeks:
                st.warning("No weeks configured for this subject in the weeks table.")
            else:
                vw_map = {f"Week {w['week_number']}": w['id'] for w in v_weeks}
                vw_sel = c2_v.selectbox("Week", list(vw_map.keys()), key="v_edit_week")
                
                week_id = vw_map[vw_sel]
                
                curr_vid_data = fetch_data("SELECT topic_title, youtube_urls, video_titles FROM weeks WHERE id=%s", (week_id,))
                curr_title = curr_vid_data[0].get('topic_title') if curr_vid_data else ""
                curr_urls = curr_vid_data[0].get('youtube_urls') if curr_vid_data and curr_vid_data[0].get('youtube_urls') else []
                curr_titles = curr_vid_data[0].get('video_titles') if curr_vid_data and curr_vid_data[0].get('video_titles') else []
                
                curr_urls_str = "\n".join(curr_urls)
                curr_titles_str = "\n".join(curr_titles)
                
                with st.form("edit_v_form"):
                    st.markdown("**Week Metadata**")
                    new_title = st.text_input("Overall Topic Title (e.g., 'Introduction to Python')", value=curr_title or "")
                    
                    st.markdown("**YouTube URLs & Custom Titles (Must have the same number of lines)**")
                    col_u, col_t = st.columns(2)
                    new_urls_str = col_u.text_area("YouTube URLs", value=curr_urls_str, height=150)
                    new_titles_str = col_t.text_area("Video Titles", value=curr_titles_str, height=150)
                    
                    if st.form_submit_button("Save Week Details", type="primary"):
                        new_urls_list = [u.strip() for u in new_urls_str.split("\n") if u.strip()]
                        new_titles_list = [t.strip() for t in new_titles_str.split("\n") if t.strip()]
                        
                        if len(new_urls_list) != len(new_titles_list) and len(new_urls_list) > 0:
                            st.error(f"Mismatch: You provided {len(new_urls_list)} URLs but {len(new_titles_list)} Titles.")
                        else:
                            if execute_query("UPDATE weeks SET topic_title=%s, youtube_urls=%s, video_titles=%s WHERE id=%s", (new_title, new_urls_list, new_titles_list, week_id)):
                                st.success(f"Successfully updated {vw_sel}!")
                                st.rerun()
                            else:
                                st.error("Failed to save week details.")

    # ==========================================
    # TAB 3: MANAGE STRUCTURE (Edit Hierarchy)
    # ==========================================
    with tab_edit_hier:
        st.markdown("##### Manage Database Structure")
        
        # --- ROW 1: ADD NEW STRUCTURE ---
        c_sub, c_week, c_act = st.columns(3)

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
                        else: st.warning("Please enter a name.")

        hier_subs = fetch_data("SELECT * FROM subjects ORDER BY name ASC")

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
                else: st.warning("Add a subject first.")

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
                                else: st.warning("Please enter a name.")
                    else: st.warning("Add a week to this subject first.")
                else: st.warning("Add a subject first.")

        # --- ROW 2: EDIT EXISTING STRUCTURE ---
        st.divider()
        st.markdown("##### Edit Existing Structure")
        ce_sub, ce_week, ce_act = st.columns(3)

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
                                    execute_query("UPDATE weeks SET week_number = %s WHERE id = %s", (new_week_num, e_w_id))
                                    execute_query("UPDATE assessments SET week_number = %s WHERE subject_id = %s AND week_number = %s", (new_week_num, e_w_sub_id, e_w_sel))
                                    st.success(f"Updated week to {new_week_num}")
                                    st.rerun()

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

    # ==========================================
    # TOOL 4: Content Health Inspector
    # ==========================================
    with tab_health:
        st.markdown("##### Content Health Inspector")
        health_filter = "WHERE LOWER(TRIM(COALESCE(q.q_type, 'mcq'))) NOT IN ('numerical', 'nat')"

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
        else: st.success("Content Health: All MCQs have options.")

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
            if query.strip() == "": st.error("Please enter a query.")
            elif query.strip().upper().startswith("SELECT"):
                try:
                    res = fetch_data(query)
                    if res:
                        st.dataframe(res, width="stretch")
                        st.success(f"Returned {len(res)} rows.")
                    else: st.info("Query returned no results.")
                except Exception as e: st.error(f"SQL Error: {e}")
            else:
                if execute_query(query): st.success("Query executed and committed successfully.")
                else: st.error("Failed to execute query. Check syntax and constraints.")

# ------------------------------------------
# VIEW DATABASE (Protected Admin Area)
# ------------------------------------------
elif app_mode == "View Database":
    #st.markdown("## Add")
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
    # TOOL 2: GUI Visual Dashboard (Upgraded)
    # ==========================================
    with tab_viz:
        st.markdown("##### Database Analytics")
        
        v_col1, v_col2 = st.columns(2)
        
        # 1. Questions per Subject (Kept)
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
                st.bar_chart(pd.DataFrame(q_per_sub).set_index("subject"), color="#f9a01b")
                
        # 2. Question Types (Kept)
        with v_col2:
            st.markdown("**Question Format Distribution**")
            q_types = fetch_data("""
                SELECT COALESCE(q_type, 'mcq') as format, COUNT(id) as count 
                FROM questions GROUP BY format
            """)
            if q_types:
                st.bar_chart(pd.DataFrame(q_types).set_index("format"), color="#0099ff")

        st.divider()
        m_col1, m_col2 = st.columns(2)

        # 3. NEW: Difficulty Breakdown
        with m_col1:
            st.markdown("**Difficulty Spread**")
            diff_data = fetch_data("""
                SELECT COALESCE(difficulty, 'Unassigned') as diff, count(id) as cnt 
                FROM questions GROUP BY diff
            """)
            if diff_data:
                st.bar_chart(pd.DataFrame(diff_data).set_index("diff"), color="#ff4b4b")

        # 4. NEW: Total Points Available
        with m_col2:
            st.markdown("**Total Exam Points per Subject**")
            pts_data = fetch_data("""
                SELECT s.name as subject, SUM(COALESCE(q.points, 1)) as total_points 
                FROM subjects s 
                JOIN assessments a ON s.id = a.subject_id 
                JOIN questions q ON a.id = q.assessment_id 
                GROUP BY s.name
            """)
            if pts_data:
                st.bar_chart(pd.DataFrame(pts_data).set_index("subject"), color="#00ff99")

        st.divider()

        # 5. NEW: Video Resources Allocation
        st.markdown("**Video Resources per Week**")
        vid_data = fetch_data("""
            SELECT 'Week ' || week_number as week_label, array_length(youtube_urls, 1) as vid_count 
            FROM weeks 
            WHERE youtube_urls IS NOT NULL
        """)
        if vid_data:
            st.bar_chart(pd.DataFrame(vid_data).set_index("week_label"), color="#8884d8")



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
    # TOOL 6: Supercharged Data Explorer (Dynamic Filters & JOINs)
    # ==========================================
    with tab_browse:        
        if "browse_results" not in st.session_state:
            st.session_state.browse_results = None

        # 1. Choose Data Mode (Raw vs Joined)
        c_mode, c_lim = st.columns([3, 1])
        c_mode.markdown("##### *Select Data Source*")
        source_type = c_mode.radio("Data Mode", ["Raw Tables", "Master Joined Views"], horizontal=True, label_visibility="collapsed")
        limit = c_lim.number_input("Row Limit", min_value=10, max_value=5000, value=100, step=50)

        base_query = ""
        col_info = []

        # ------------------------------------------
        # MODE A: Raw Tables
        # ------------------------------------------
        if source_type == "Raw Tables" and table_names:
            selected_table = st.selectbox("Select Table", table_names, key="raw_tbl_sel")
            if selected_table:
                base_query = f"SELECT * FROM {selected_table}"
                col_info = fetch_data("""
                    SELECT column_name as col, data_type as type 
                    FROM information_schema.columns 
                    WHERE table_name = %s
                """, (selected_table,))

        # ------------------------------------------
        # MODE B: Master Joined Views
        # ------------------------------------------
        else:
            views = {
                "Questions + Full Metadata (Context View)": {
                    "query": """
                        SELECT q.id as "Q_ID", s.name as "Subject", a.week_number as "Week", a.name as "Activity", 
                               q.heading as "Heading", q.q_type as "Format", q.difficulty as "Difficulty", 
                               q.points as "Points", q.correct_answer as "Numerical_Ans"
                        FROM questions q 
                        JOIN assessments a ON q.assessment_id = a.id 
                        JOIN subjects s ON a.subject_id = s.id
                    """,
                    "cols": [
                        {"col": "Subject", "type": "text"}, {"col": "Week", "type": "integer"}, 
                        {"col": "Activity", "type": "text"}, {"col": "Heading", "type": "text"},
                        {"col": "Format", "type": "text"}, {"col": "Difficulty", "type": "text"}
                    ]
                },
                "Options Dictionary (With Parent Question)": {
                    "query": """
                        SELECT o.id as "Opt_ID", s.name as "Subject", q.heading as "Parent_Question", 
                               o.option_text as "Option_Text", o.is_correct as "Is_Correct", o.media_type as "Media"
                        FROM options o 
                        JOIN questions q ON o.question_id = q.id 
                        JOIN assessments a ON q.assessment_id = a.id 
                        JOIN subjects s ON a.subject_id = s.id
                    """,
                    "cols": [
                        {"col": "Subject", "type": "text"}, {"col": "Parent_Question", "type": "text"},
                        {"col": "Option_Text", "type": "text"}, {"col": "Is_Correct", "type": "boolean"},
                        {"col": "Media", "type": "text"}
                    ]
                }
            }
            
            selected_view = st.selectbox("Select Pre-Built Join", list(views.keys()), key="view_sel")
            if selected_view:
                base_query = views[selected_view]["query"]
                col_info = views[selected_view]["cols"]

        # ------------------------------------------
        # DYNAMIC FILTER GENERATOR
        # ------------------------------------------
        if base_query and col_info:
            with st.expander("Auto-Generated Filters", expanded=True, icon=":material/search:"):
                filters = {}
                f_cols = st.columns(4)
                col_idx = 0

                # System columns we don't want to clutter the UI with
                ignored_cols = ['id', 'created_at', 'updated_at', 'subject_id', 'assessment_id', 
                                'question_id', 'cache_key', 'video_id', 'youtube_urls', 'media_content']

                for c in col_info:
                    col_name = c['col']
                    col_type = c['type'].lower() if c.get('type') else 'text'

                    if col_name.lower() in ignored_cols or 'array' in col_type: 
                        continue

                    # 1. Generate Boolean Filters (True/False Toggles)
                    if col_type == 'boolean':
                        sel = f_cols[col_idx % 4].selectbox(col_name.replace('_', ' ').title(), ["All", "True", "False"], key=f"f_{col_name}")
                        if sel != "All":
                            filters[col_name] = {"val": True if sel == "True" else False, "type": "bool"}
                        col_idx += 1

                    # 2. Generate Categorical Dropdowns (Only if < 25 unique values exist)
                    elif col_type in ['text', 'character varying', 'integer']:
                        # For raw tables, we dynamically check the database to see if a dropdown is appropriate
                        if source_type == "Raw Tables":
                            try:
                                dist_vals = fetch_data(f"SELECT DISTINCT {col_name} FROM {selected_table} WHERE {col_name} IS NOT NULL LIMIT 30")
                                # If there are few distinct values (like Difficulty or Week), make a multi-select
                                if dist_vals and len(dist_vals) < 25:
                                    v_list = [str(r[col_name]) for r in dist_vals]
                                    sel = f_cols[col_idx % 4].multiselect(col_name.replace('_', ' ').title(), v_list, key=f"f_{col_name}")
                                    if sel: filters[col_name] = {"val": sel, "type": "in"}
                                    col_idx += 1
                            except: pass
                        # For joined views, we build dropdowns based on the predefined structure
                        else:
                            if col_type != 'text' or col_name in ['Subject', 'Format', 'Difficulty', 'Media', 'Week']:
                                try:
                                    # Use a CTE to safely extract distinct values from the complex joined view
                                    dist_vals = fetch_data(f"WITH base AS ({base_query}) SELECT DISTINCT \"{col_name}\" FROM base WHERE \"{col_name}\" IS NOT NULL LIMIT 30")
                                    if dist_vals:
                                        v_list = [str(r[col_name]) for r in dist_vals]
                                        sel = f_cols[col_idx % 4].multiselect(col_name.replace('_', ' ').title(), v_list, key=f"f_{col_name}")
                                        if sel: filters[col_name] = {"val": sel, "type": "in"}
                                        col_idx += 1
                                except: pass

                st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
                text_search = st.text_input("Global Text Search (Scans all text columns instantly)", placeholder="Enter keyword to search...")

            # ------------------------------------------
            # QUERY EXECUTION
            # ------------------------------------------
            if st.button("Apply Filters & Fetch Data", type="primary", use_container_width=True):
                with st.spinner("Compiling dynamic query..."):
                    where_clauses = []
                    params = []

                    # Apply Dropdown and Boolean Filters
                    for k, v in filters.items():
                        # Wrap column names in double quotes to protect case-sensitive aliases in Joined Views
                        safe_col = f'"{k}"' if source_type == "Master Joined Views" else k
                        
                        if v["type"] == "in":
                            placeholders = ", ".join(["%s"] * len(v["val"]))
                            where_clauses.append(f"{safe_col} IN ({placeholders})")
                            params.extend(v["val"])
                        elif v["type"] == "bool":
                            where_clauses.append(f"{safe_col} = %s")
                            params.append(v["val"])

                    # Apply Global Text Search
                    if text_search:
                        text_cols = [c['col'] for c in col_info if c['type'] in ('text', 'character varying')]
                        if text_cols:
                            search_clauses = []
                            for c in text_cols:
                                safe_c = f'"{c}"' if source_type == "Master Joined Views" else c
                                # Cast to text ensures we don't get errors if a column behaves weirdly
                                search_clauses.append(f"CAST({safe_c} AS TEXT) ILIKE %s")
                            where_clauses.append("(" + " OR ".join(search_clauses) + ")")
                            params.extend([f"%{text_search}%"] * len(text_cols))

                    # Wrap everything in a CTE (Common Table Expression). 
                    # This guarantees that we can filter the result of ANY complex JOIN without SQL alias errors.
                    final_query = f"WITH dynamic_view AS ({base_query}) SELECT * FROM dynamic_view"
                    
                    if where_clauses:
                        final_query += " WHERE " + " AND ".join(where_clauses)

                    final_query += f" LIMIT {limit}"
                    
                    st.session_state.browse_results = fetch_data(final_query, tuple(params))

            # ------------------------------------------
            # RENDER RESULTS
            # ------------------------------------------
            if st.session_state.browse_results is not None:
                if st.session_state.browse_results:
                    st.success(f"**Showing {len(st.session_state.browse_results)} records.**")
                    st.dataframe(pd.DataFrame(st.session_state.browse_results), width="stretch", hide_index=True)
                    
                    if st.button("Clear Results"):
                        st.session_state.browse_results = None
                        st.rerun()
                else:
                    st.warning("No records found matching those filters. Try removing some restrictions.")

    

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
        st.divider()

        # --- SECTION B: EXPORT SCHEMA ---
        st.write("##### 2. Download Database Schema (.sql)")
        st.info("This will generate a single file containing the structure of all your tables.")
        
        if st.button("Generate Schema File", type="secondary"):
            with st.spinner("Mapping database structure..."):
                # Fetch all columns and types for all public tables
                schema_query = """
                    SELECT table_name, column_name, data_type, is_nullable
                    FROM information_schema.columns 
                    WHERE table_schema = 'public'
                    ORDER BY table_name, ordinal_position;
                """
                all_columns = fetch_data(schema_query)
                
                if all_columns:
                    schema_text = "-- ACADEMIC PORTAL DATABASE SCHEMA --\n"
                    schema_text += f"-- Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')} --\n\n"
                    
                    current_table = ""
                    for col in all_columns:
                        if col['table_name'] != current_table:
                            if current_table != "": schema_text += ");\n\n"
                            current_table = col['table_name']
                            schema_text += f"CREATE TABLE {current_table} (\n"
                            schema_text += f"    {col['column_name']} {col['data_type']}"
                        else:
                            schema_text += f",\n    {col['column_name']} {col['data_type']}"
                        
                        if col['is_nullable'] == "NO": schema_text += " NOT NULL"
                    
                    schema_text += "\n);"
                    
                    st.download_button(
                        label="Download full_schema.sql",
                        data=schema_text,
                        file_name="academic_portal_schema.sql",
                        mime="text/sql",
                        type="primary"
                    )
                else:
                    st.error("Could not retrieve schema information.")


# ------------------------------------------
# VIEW VIDEOS
# ------------------------------------------
elif app_mode == "View Videos":
    #st.markdown("## Add")
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
        
    # Build clean dropdown labels. Ex: "Week 1: Intro to Python" (or just "Week 1" if empty)
    w_map = {}
    for w in weeks:
        label = f"Week {w['week_number']}"
        if w.get('topic_title'):
            label += f": {w['topic_title']}"
        w_map[label] = w['id']
    w_sel = c2.selectbox("Week", list(w_map.keys()), key="vid_week")
    
    #st.markdown("---")
    
    # ---------------- RENDER VIDEOS ----------------
    week_data = fetch_data("SELECT youtube_urls, video_titles FROM weeks WHERE id=%s", (w_map[w_sel],))
    week_id = w_map[w_sel]

    if week_data and week_data[0].get('youtube_urls'):
        urls = week_data[0]['youtube_urls']
        titles = week_data[0].get('video_titles') or []
        
        if isinstance(urls, list) and len(urls) > 0:
            c0.markdown(f"#### Lectures for {s_sel} - {w_sel}")
            
            state_key = f"active_vid_{week_id}"
            if state_key not in st.session_state:
                st.session_state[state_key] = urls[0]

            col_player, col_playlist = st.columns([2.5, .8])

            with col_player:
                with st.container(border=True):
                    current_url = st.session_state[state_key]
                    st.video(current_url)
            
            with col_playlist:
                with st.container(height="content", border=True):
                    for idx, url in enumerate(urls):
                        if url and url.strip():
                            # Check what is currently in the database
                            db_title = titles[idx] if idx < len(titles) else ""
                            
                            # THE MAGIC: If the DB is empty or just says "Lecture X" from the backfill, fetch the real YouTube title!
                            if not db_title or db_title.startswith("Lecture "):
                                video_name = fetch_youtube_title(url.strip()) or f"Lecture {idx + 1}"
                            else:
                                video_name = db_title
                            
                            is_active = (st.session_state[state_key] == url.strip())
                            btn_type = "primary" if is_active else "secondary"
                            
                            if st.button(video_name, key=f"vid_btn_{week_id}_{idx}", type=btn_type, width="stretch"):
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
            
            # --- AI VIDEO QUIZ GENERATOR ---
            with st.expander("AI Tutor: Practice Quiz", expanded=False, icon=":material/quiz:"):
                try:
                    vid_id = extract_youtube_id(current_url)
                except NameError:
                    vid_id = None
                    
                if vid_id:
                    cached_quiz = get_cached_video_quiz(vid_id)
                    if cached_quiz:
                        # Render the sideways interactive UI from the new file
                        render_interactive_quiz(vid_id, cached_quiz)
                    else:
                        st.info("Test your understanding of this lecture. The AI will generate a custom quiz based on the transcript.")
                        if st.button("Generate Practice Quiz", key=f"gen_quiz_{vid_id}", type="primary", width="stretch"):
                            with st.spinner("Analyzing transcript and generating comprehensive quiz (This takes 20-30 seconds)..."):
                                # Ensure we have API keys
                                if "GEMINI_VIDEO_KEYS" in st.secrets:
                                    keys = st.secrets["GEMINI_VIDEO_KEYS"]
                                elif "GEMINI_KEYS" in st.secrets:
                                    keys = st.secrets["GEMINI_KEYS"]
                                else:
                                    keys = [st.secrets.get("GEMINI_KEY")]
                                
                                quiz_data = generate_video_quiz(s_sel, current_url, keys)
                                
                                # --- THE FIX IS HERE ---
                                if "error" not in quiz_data:
                                    try:
                                        week_num = int(w_sel.split(" ")[1].split(":")[0])
                                    except: week_num = 0
                                    
                                    topic_title = w_sel.split(": ")[1] if ": " in w_sel else ""
                                    
                                    meta = {
                                        "subject": s_sel,
                                        "week_num": week_num,
                                        "topic": topic_title,
                                        "video_title": fetch_youtube_title(current_url) or f"Video ID: {vid_id}",
                                        "url": current_url
                                    }
                                    
                                    save_video_quiz(vid_id, quiz_data, meta)
                                    
                                    # ONLY rerun if successful!
                                    st.rerun() 
                                else:
                                    # If it fails, print the error and STAY on the page so you can read it.
                                    st.error(f"Generation Failed: {quiz_data['error']}")

        else:
            st.info(f"No videos are currently linked to {w_sel}.")
            c0.markdown("#### Video Lectures & Resources")
    else:
        st.info(f"No videos are currently linked to {w_sel}.")
        c0.markdown("#### Video Lectures & Resources")

# # ------------------------------------------
# SAVED AI NOTES (Central Knowledge Hub)
# ------------------------------------------
elif app_mode == "AI Notes":
    
    # --- THE CLEVER RENDER CHECKER (UPGRADED) ---
    @st.cache_data(show_spinner=False, ttl=86400) 
    def verify_mermaid_with_kroki(mermaid_str):
        """Actually pings the Kroki rendering server. ONLY fails if Kroki explicitly rejects the syntax."""
        if not mermaid_str or str(mermaid_str).strip() in ["", "N/A", "None"]:
            return True 
        
        import zlib, base64, requests, re
        raw_mermaid = str(mermaid_str).replace('```mermaid', '').replace('```', '').strip()
        clean_mermaid = raw_mermaid.replace('\xa0', ' ').replace(';', '')
        clean_mermaid = re.sub(r'--\s*".*?"\s*-->', '-->', clean_mermaid)
        clean_mermaid = re.sub(r'--\s*.*?\s*-->', '-->', clean_mermaid)
        final_mermaid = clean_mermaid
        final_mermaid = final_mermaid.replace('$$', '').replace('\\', '')
        final_mermaid = final_mermaid.replace('<=', ' less than or equal to ')
        final_mermaid = final_mermaid.replace('>=', ' greater than or equal to ')
        final_mermaid = final_mermaid.replace('!=', ' not equal to ')
        final_mermaid = final_mermaid.replace('==', ' equals ')
        final_mermaid = re.sub(r'(?<=\w)\s*<\s*(?=\w)', ' less than ', final_mermaid)
        final_mermaid = re.sub(r'(?<=\w)\s*>\s*(?=\w)', ' greater than ', final_mermaid)
        final_mermaid = final_mermaid.replace("'", "").replace('<br>', ' ').replace('<br/>', ' ')
        final_mermaid = re.sub(r'(?<!\[)"(?!\])', '', final_mermaid)
        final_mermaid = re.sub(r'([A-Za-z0-9_]+)[\{\(\[]"?([^"]*?)"?[\}\)\]](?=\s*[-=\.%]|\s*$|\s*\n)', r'\1["\2"]', final_mermaid)
        final_mermaid = re.sub(r"subgraph\s+[\"']?(.*?)[\"']?(?=\n|$)", r"subgraph \1", final_mermaid)

        try:
            compressed = zlib.compress(final_mermaid.encode('utf-8'), 9)
            b64_mermaid = base64.urlsafe_b64encode(compressed).decode('utf-8').replace('=', '')
            mermaid_url = f"https://kroki.io/mermaid/svg/{b64_mermaid}"
            
            res = requests.get(mermaid_url, timeout=4)
            if res.status_code == 400:
                return False 
            return True 
        except:
            return True 

    def is_response_broken(ai_data):
        if not isinstance(ai_data, dict): return True 
        for val in ai_data.values():
            if isinstance(val, str) and ("API Error" in val or "Error:" in val):
                return True
        mermaid = ai_data.get("mermaid_diagram")
        if mermaid:
            if not verify_mermaid_with_kroki(mermaid):
                return True 
        return False
    
    tab_mcq, tab_vid = st.tabs(["MCQ Explanations", "Video Notes"])
    
    # ==========================================
    # TAB 1: MCQ Explanations
    # ==========================================
    with tab_mcq:
        with st.expander("Filter MCQ Scope", expanded=True, icon=":material/filter_list:"):
            c1, c2, c3 = st.columns([1, 1, 1])
            
            subjects = fetch_data("SELECT * FROM subjects ORDER BY name ASC")
            if not subjects: st.stop()
            s_map = {s['name']: s['id'] for s in subjects}
            
            # Subject Filter
            s_opts = ["All Subjects"] + list(s_map.keys())
            s_sel = c1.selectbox("Subject", s_opts, key="aimcq_sub")
            
            # Dynamic Week Filter
            w_query = "SELECT DISTINCT week_number FROM assessments"
            w_params = []
            if s_sel != "All Subjects":
                w_query += " WHERE subject_id=%s"
                w_params.append(s_map[s_sel])
            w_query += " ORDER BY week_number ASC"
            weeks = fetch_data(w_query, tuple(w_params))
            
            w_opts = ["All Weeks"] + [w['week_number'] for w in weeks]
            w_sel = c2.selectbox("Week", w_opts, key="aimcq_week")
            
            # Dynamic Activity Filter
            a_query = "SELECT id, name FROM assessments WHERE 1=1"
            a_params = []
            if s_sel != "All Subjects":
                a_query += " AND subject_id=%s"
                a_params.append(s_map[s_sel])
            if w_sel != "All Weeks":
                a_query += " AND week_number=%s"
                a_params.append(w_sel)
            a_query += " ORDER BY name ASC"
            
            assessments = fetch_data(a_query, tuple(a_params))
            a_map = {a['name']: a['id'] for a in assessments}
            
            a_opts = ["All Activities"] + list(a_map.keys())
            a_sel = c3.selectbox("Activity", a_opts, key="aimcq_act")
                
        with st.spinner("Fetching and Analyzing AI Health..."):
            # Fetch Questions based on filters (Includes Activity/Week info for context)
            q_query = "SELECT q.*, a.name as activity_name, a.week_number as w_num, s.name as sub_name FROM questions q JOIN assessments a ON q.assessment_id = a.id JOIN subjects s ON a.subject_id = s.id WHERE 1=1"
            q_params = []
            
            if a_sel != "All Activities":
                q_query += " AND q.assessment_id=%s"
                q_params.append(a_map[a_sel])
            elif assessments:
                ass_ids = tuple([a['id'] for a in assessments])
                if len(ass_ids) == 1:
                    q_query += f" AND q.assessment_id = {ass_ids[0]}"
                else:
                    q_query += f" AND q.assessment_id IN {ass_ids}"
            else:
                q_query += " AND 1=0" # Failsafe if no activities match

            q_query += " ORDER BY q.id ASC"
            questions = fetch_data(q_query, tuple(q_params))
            
            if not questions:
                st.info("No questions found for the selected filters.")
            else:
                q_ids = [q['id'] for q in questions]
                cache_map = {}
                if q_ids:
                    q_ids_str = f"({q_ids[0]})" if len(q_ids) == 1 else str(tuple(q_ids))
                    caches = fetch_data(f"SELECT * FROM mcq_cache WHERE question_id IN {q_ids_str}")
                    cache_map = {c['question_id']: c for c in caches}

                broken_qs = []
                healthy_qs = []
                
                for i, q in enumerate(questions):
                    if q['id'] in cache_map:
                        ai_data = cache_map[q['id']]['ai_data']
                        if is_response_broken(ai_data): 
                            broken_qs.append((i, q, cache_map[q['id']]))
                        else: 
                            healthy_qs.append((i, q, cache_map[q['id']]))

                def render_aimcq_question(i, q, cache_entry):
                    context_tag = f" `[{q['sub_name']} | W{q['w_num']} | {q['activity_name']}]`" if a_sel == "All Activities" else ""

                    
                    with st.expander(expanded=False, label=f"{context_tag}", icon=":material/question_answer:"):
                        # Show Context Tags if "All" is selected
                        st.markdown(f"{q['heading']}")
                        render_content(q['media_type'], q['media_content'])
                        
                        
                        if q.get('q_type') == 'numerical':
                            st.success(f"Correct Answer: {q['correct_answer']}")
                        else:
                            options = fetch_data("SELECT * FROM options WHERE question_id=%s ORDER BY id ASC", (q['id'],))
                            for idx, opt in enumerate(options):
                                status = "correct" if opt['is_correct'] else "incorrect"
                                content = opt['media_content'] if opt['media_content'] else opt['option_text']
                                render_option_card(f"OPTION {idx+1}", content, opt['media_type'], status=status)
                        render_ai_tutor_response(cache_entry['ai_data'], cache_entry['cache_key'])

                if broken_qs:
                    st.error(f"**{len(broken_qs)} Broken Responses**")
                    for i, q, cache in broken_qs:
                        render_aimcq_question(i, q, cache)
                
                if healthy_qs:
                    st.success(f"**{len(healthy_qs)} Healthy Responses**")
                    for i, q, cache in healthy_qs:
                        render_aimcq_question(i, q, cache)
                        
                if not broken_qs and not healthy_qs:
                    st.info("No AI Notes have been generated for this selection yet. Go to 'Take Assessment' to ask the AI Tutor!")

# ==========================================
    # TAB 2: Video Lecture Notes
    # ==========================================
    with tab_vid:
        with st.expander("Filter Video Scope", expanded=True, icon=":material/filter_list:"):
            c1_v, c2_v = st.columns([1, 1])
            s_opts_v = ["All Subjects"] + list(s_map.keys())
            s_sel_v = c1_v.selectbox("Subject", s_opts_v, key="aivid_sub")
            
            vw_query = "SELECT * FROM weeks WHERE 1=1"
            vw_params = []
            if s_sel_v != "All Subjects":
                vw_query += " AND subject_id=%s"
                vw_params.append(s_map[s_sel_v])
            vw_query += " ORDER BY week_number ASC"
            weeks_v = fetch_data(vw_query, tuple(vw_params))
            
            w_map_v = {f"Week {w['week_number']}: {w.get('topic_title','')}": w['id'] for w in weeks_v}
            w_opts_v = ["All Weeks"] + list(w_map_v.keys())
            w_sel_v = c2_v.selectbox("Week", w_opts_v, key="aivid_week")
        
        if not weeks_v:
            st.warning("No weeks configured for the selected filters.")
        else:
            with st.spinner("Fetching and Analyzing AI Health..."):
                # We need to map subject IDs back to Names for context tags
                reverse_s_map = {v: k for k, v in s_map.items()}

                # Compile a master list of all valid caches matching the filters
                vid_cache_list = []
                for w in weeks_v:
                    if w_sel_v != "All Weeks" and w['id'] != w_map_v[w_sel_v]:
                        continue
                    
                    if w.get('youtube_urls'):
                        # Remove duplicates while preserving order
                        seen = set()
                        unique_urls = []
                        for u in w['youtube_urls']:
                            if u not in seen:
                                unique_urls.append(u)
                                seen.add(u)
                        
                        # Safely fetch the custom titles array
                        titles = w.get('video_titles') or []

                        for idx, url in enumerate(unique_urls):
                            if url and url.strip():
                                try:
                                    vid_id = extract_youtube_id(url.strip())
                                    cached_note = get_cached_video_notes(vid_id)
                                    if cached_note:
                                        sub_name = reverse_s_map.get(w['subject_id'], "Unknown")
                                        
                                        # Check what is currently in the database
                                        db_title = titles[idx] if idx < len(titles) else ""
                                        
                                        # THE MAGIC: Auto-fetch real title if needed
                                        if not db_title or db_title.startswith("Lecture "):
                                            video_title = fetch_youtube_title(url.strip()) or f"Lecture {idx + 1}"
                                        else:
                                            video_title = db_title
                                        
                                        vid_cache_list.append({
                                            'url': url.strip(),
                                            'video_id': vid_id,
                                            'ai_data': cached_note,
                                            'sub_name': sub_name,
                                            'week_number': w['week_number'],
                                            'topic_title': w.get('topic_title', ''),
                                            'video_title': video_title, # Store the actual YouTube title
                                            'lecture_idx': idx + 1
                                        })
                                except: pass
                
                if vid_cache_list:
                    broken_vids = []
                    healthy_vids = []
                    
                    # Group them based on Mermaid/API Health
                    for item in vid_cache_list:
                        if is_response_broken(item['ai_data']):
                            broken_vids.append(item)
                        else:
                            healthy_vids.append(item)

                    # Dynamic rendering function for the expanders
                    def render_aivid_note(item):
                        context_tag = f" `[{item['sub_name']} | W{item['week_number']}]`" if (s_sel_v == "All Subjects" or w_sel_v == "All Weeks") else ""
                        
                        # Simply use the newly mapped custom video title!
                        label = f"{item['video_title']}{context_tag}"
                        
                        with st.expander(expanded=False, label=label, icon=":material/smart_display:"):
                            # Render the video player right at the top of the notes!
                            st.video(item['url'])
                            st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)
                            render_video_notes(item['ai_data'], item['video_id'])

                    # Render Broken Section
                    if broken_vids:
                        st.error(f"**{len(broken_vids)} Broken Video Notes**")
                        for item in broken_vids:
                            render_aivid_note(item)
                    
                    # Render Healthy Section
                    if healthy_vids:
                        st.success(f"**{len(healthy_vids)} Healthy Video Notes**")
                        for item in healthy_vids:
                            render_aivid_note(item)
                else:
                    st.info("No AI notes generated for this selection yet. Go to 'View Videos' to ask the AI Tutor!")