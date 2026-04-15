import streamlit as st # type: ignore
import time
import requests # type: ignore
import pandas as pd # type: ignore
from database import fetch_data, execute_query
from video_ai_tutor import *
from mcq_ai_tutor import *
from cache_manager import *
from video_quiz_tutor import *
import streamlit.components.v1 as components # type: ignore

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


def render_take_assessment():
    """
    Renders the Take Assessment view where students can practice questions.
    Utilizes st.fragment for micro-reloading and st.form for batching.
    """
    # 1. Base Setup
    c1, c2, c3, c4 = st.columns([.6, 1.2, 1, 0.8])
    
    subjects = fetch_data("SELECT * FROM subjects ORDER BY name ASC")
    if not subjects: st.stop()
    s_map = {s['name']: s['id'] for s in subjects}
    s_sel = c1.selectbox("Subject", list(s_map.keys()), key="assess_sub")
    
    week_details = fetch_data("SELECT week_number, topic_title FROM weeks WHERE subject_id=%s", (s_map[s_sel],))
    w_title_map = {w['week_number']: w.get('topic_title', '') for w in week_details} if week_details else {}

    weeks = fetch_data("SELECT DISTINCT week_number FROM assessments WHERE subject_id=%s ORDER BY week_number ASC", (s_map[s_sel],))
    if not weeks: st.stop()
    
    # 2. Build clean dropdown labels
    w_opts = []
    w_val_map = {}
    for w in weeks:
        wn = w['week_number']
        title = w_title_map.get(wn, '')
        label = f"Week {wn}" + (f": {title}" if title else "")
        w_opts.append(label)
        w_val_map[label] = wn
        
    w_sel_label = c2.selectbox("Week", w_opts, key="assess_week")
    w_sel = w_val_map[w_sel_label] 
    
    assessments = fetch_data("SELECT * FROM assessments WHERE subject_id=%s AND week_number=%s ORDER BY name ASC", (s_map[s_sel], w_sel))
    if not assessments: st.stop()
    a_map = {a['name']: a['id'] for a in assessments}
    a_sel = c3.selectbox("Activity", list(a_map.keys()), key="assess_act")
    
    mode = c4.selectbox("Mode", ["Study Mode", "Exam Mode"])

    questions = fetch_data("SELECT * FROM questions WHERE assessment_id=%s ORDER BY id ASC", (a_map[a_sel],))
    if not questions:
        st.info("No questions found for this activity.")
        return

    # =========================================================================
    # OPTIMIZATION 1: BULK FETCH ALL OPTIONS (Kills the infinite loading bug)
    # =========================================================================
    q_ids = tuple([q['id'] for q in questions])
    opts_by_q = {}
    if q_ids:
        options_data = fetch_data("SELECT * FROM options WHERE question_id IN %s ORDER BY id ASC", (q_ids,))
        if options_data:
            for opt in options_data:
                opts_by_q.setdefault(opt['question_id'], []).append(opt)

    # =========================================================================
    # MICRO-RELOADING STRATEGY (Isolates logic so only 1 question reloads at a time)
    # =========================================================================
    @st.fragment
    def render_study_question(i, q, options, s_sel, w_sel, a_sel):
        with st.container(border=True):
            st.markdown(f"Q{i+1}. {q['heading']}")    
            render_content(q['media_type'], q['media_content'])
            
            # NUMERICAL LOGIC
            if q.get('q_type') == 'numerical':
                val = st.text_input(f"Answer Q{i+1}", key=f"num_{q['id']}")
                
                if val:
                    if check_numerical_answer(val, q['correct_answer']): st.success("Correct")
                    else: st.error(f"Incorrect. Answer: {q['correct_answer']}")
                
                ai_key = f"num_{q['id']}" 
                cached_res = get_cached_ai_response(ai_key)
                
                if cached_res:
                    with st.expander("View AI Tutor Analysis", expanded=False, icon=":material/model_training:"):
                        render_ai_tutor_response(cached_res.get('ai_data', cached_res), ai_key, cached_res.get('created_by_user', 'System'))
                else:
                    if not st.session_state.get("user_api_keys"):
                        st.warning("Please add your Gemini API Key in 'My Settings' to unlock the AI Tutor.", icon=":material/vpn_key:")
                    else:
                        if st.button(f"Ask AI Tutor for Q{i+1}", key=f"ai_btn_{q['id']}", width="stretch", type="secondary", icon=":material/smart_toy:"):
                            with st.spinner("Consulting AI Tutor..."):
                                opt_texts = [] 
                                c_ans = q['correct_answer']
                                explanation = ask_ai_tutor(s_sel, q['heading'], q['media_type'], q['media_content'], opt_texts, c_ans, st.session_state["user_api_keys"])
                                meta = {'q_id': q['id'], 'sub': s_sel, 'heading': q['heading'], 'week': w_sel, 'ass_name': a_sel}
                                save_ai_cache(ai_key, explanation, st.session_state["name"], metadata=meta)
                                st.rerun(scope="fragment") # Only reruns this specific question!

            # MCQ LOGIC
            else:
                is_multi = len([o for o in options if o['is_correct']]) > 1
                c_disp, c_sel = st.columns([0.90, 0.10])
                
                with c_disp:
                    for idx, opt in enumerate(options):
                        content = opt['media_content'] if (opt['media_content']) else opt['option_text']
                        status = None
                        
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

                # AI Tutor Logic
                has_selection = (is_multi and len(sel_idxs) > 0) or (not is_multi and choice is not None)
                if has_selection:
                    ai_key = f"mcq_{q['id']}"
                    cached_res = get_cached_ai_response(ai_key)
                    
                    if cached_res:
                        with st.expander("View AI Tutor Analysis", expanded=False, icon=":material/model_training:"):
                            render_ai_tutor_response(cached_res.get('ai_data', cached_res), ai_key, cached_res.get('created_by_user', 'System'))
                    else:
                        if not st.session_state.get("user_api_keys"):
                            st.warning("Please add your Gemini API Key in 'My Settings' to unlock the AI Tutor.", icon=":material/vpn_key:")
                        else:
                            if st.button(f"Ask AI Tutor for Q{i+1}", key=f"ai_btn_{q['id']}", width="stretch", type="secondary", icon=":material/smart_toy:"):
                                with st.spinner("Consulting AI Tutor..."):
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
                                    
                                    explanation = ask_ai_tutor(s_sel, q['heading'], q['media_type'], q['media_content'], opt_texts, c_ans, st.session_state["user_api_keys"])
                                    meta = {'q_id': q['id'], 'sub': s_sel, 'heading': q['heading'], 'week': w_sel, 'ass_name': a_sel}
                                    save_ai_cache(ai_key, explanation, st.session_state["name"], metadata=meta) 
                                    st.rerun(scope="fragment") # Micro-reload!

            # ADMIN CONTROLS
            if st.session_state.get("role") == "admin":
                c_flag1, c_flag2 = st.columns(2)
                
                if c_flag1.toggle("Flag Question Data", key=f"tog_q_{q['id']}"):
                    q_note = st.text_area("Describe the issue with the Question or Options:", key=f"txt_q_{q['id']}")
                    if st.button("Save Question Flag", key=f"save_q_{q['id']}", type="primary"):
                        execute_query("INSERT INTO question_issues (question_id, issue_description, reported_by) VALUES (%s, %s, %s)", (q['id'], q_note, st.session_state.get("name")))
                        st.success("Question Data flagged successfully!", icon=":material/check_circle:")
                        st.rerun(scope="fragment")
                
                if c_flag2.toggle("Flag AI Response", key=f"tog_ai_{q['id']}"):
                    ai_note = st.text_area("Describe the issue with the AI explanation:", key=f"txt_ai_{q['id']}")
                    if st.button("Save AI Flag", key=f"save_ai_{q['id']}", type="primary"):
                        a_key = f"num_{q['id']}" if q.get('q_type') == 'numerical' else f"mcq_{q['id']}"
                        execute_query("UPDATE mcq_cache SET needs_attention=TRUE, attention_note=%s WHERE cache_key=%s", (ai_note, a_key))
                        st.success("AI Response flagged successfully!", icon=":material/check_circle:")
                        st.rerun(scope="fragment")


    # =========================================================================
    # EXAM MODE (Batching Strategy - Zero Loading - Wrapped in a Form)
    # =========================================================================
    if mode == "Exam Mode":
        st.info("**Exam Mode Active:** Click options below with zero loading. Click 'Lock Answers' at the bottom when finished, then switch to Study Mode to instantly see your results.", icon=":material/speed:")
        
        with st.form("exam_form", clear_on_submit=False):
            for i, q in enumerate(questions):
                with st.container(border=True):
                    st.markdown(f"Q{i+1}. {q['heading']}")    
                    render_content(q['media_type'], q['media_content'])
                    
                    if q.get('q_type') == 'numerical':
                        st.text_input(f"Answer Q{i+1}", key=f"num_{q['id']}")
                    else:
                        options = opts_by_q.get(q['id'], [])
                        is_multi = len([o for o in options if o['is_correct']]) > 1
                        
                        c_disp, c_sel = st.columns([0.90, 0.10])
                        with c_disp:
                            for idx, opt in enumerate(options):
                                content = opt['media_content'] if (opt['media_content']) else opt['option_text']
                                render_option_card(f"OPTION {idx+1}", content, opt['media_type'], status=None)
                        
                        with c_sel:
                            st.markdown('<span class="option-label">SELECT</span>', unsafe_allow_html=True)
                            if is_multi:
                                for idx, opt in enumerate(options):
                                    st.checkbox(f"{idx+1}", key=f"chk_{q['id']}_{opt['id']}")
                            else:
                                r_opts = [f"{x+1}" for x in range(len(options))]
                                st.radio(f"Rad_{i}", r_opts, index=None, label_visibility="collapsed", key=f"rad_{q['id']}")
                                
            st.form_submit_button("Lock Answers & Save State", type="primary", use_container_width=True)

    # =========================================================================
    # STUDY MODE (Micro-Reloading Execution)
    # =========================================================================
    else:
        for i, q in enumerate(questions):
            options = opts_by_q.get(q['id'], [])
            # Call the fragment function for each question independently!
            render_study_question(i, q, options, s_sel, w_sel, a_sel)

def render_take_test():
    """
    Renders the Take Test view for a timed, graded test.
    """
    if 'test_state' not in st.session_state:
        st.session_state.test_state = 'setup'
        st.session_state.test_data = [] 
        st.session_state.curr_idx = 0
        st.session_state.responses = {} 

    if st.session_state.test_state == 'setup':
        st.markdown("#### :material/settings: Configure Test")
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
        
        # The Safety Check
        count_res = fetch_data(f"SELECT COUNT(*) as cnt FROM questions q JOIN assessments a ON q.assessment_id = a.id WHERE a.subject_id=%s AND a.week_number IN {w_filter} AND a.name IN {t_filter}", (s_id,))
        count = count_res[0]['cnt'] if count_res else 0

        if count == 0:
            st.error("No questions found for the selected criteria. Please change your filters.")
        else:
            st.info(f"Pool Size: {count} Questions", icon=":material/info:")
            
            # The 'value' logic now has a safety floor of 1 to prevent the StreamlitValueBelowMinError
            num_q = st.number_input("Question Count", min_value=1, max_value=count, value=min(20, count))

        
            if st.button("Start Test", type="secondary", icon=":material/play_arrow:"):
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
                
        if q.get('q_type') == 'numerical':
            col_q, col_a = st.columns([0.6, 0.4])
            with col_q: st.write("Numerical Answer")
            with col_a:
                val = st.text_input("Value:", key=f"t_num_{q['id']}", icon=":material/edit:")
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

        if st.button("Submit", type="primary", icon=":material/send:"):
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
        st.markdown("### :material/emoji_events: Results")
        
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

    # EDIT CONTENT (Admin Area)


def render_view_videos():
    """
    Renders the View Videos view for lectures and quizzes.
    """
    # ---------- SUBJECT / WEEK ----------------
    c0, c1, c2 = st.columns([2, .7, 1])
    
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
    
    
    # ---------- RENDER VIDEOS ----------------
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
                    
                    # 1. Add a Continuous Play toggle
                    c_vid1, c_vid2 = st.columns([3, 1])
                    use_playlist = c_vid2.toggle("Autoplay", value=False, help="Autoplays all videos in this week. Note: You must still manually select a video from the list to use the AI features.")
                    
                    if use_playlist and len(urls) > 1:
                        # 2. Extract all IDs and build a YouTube Playlist URL
                        try:
                            all_ids = [extract_youtube_id(u) for u in urls if extract_youtube_id(u)]
                            if all_ids:
                                first_id = all_ids[0]
                                remaining_ids = ",".join(all_ids[1:])
                                playlist_url = f"https://www.youtube.com/embed/{first_id}?playlist={remaining_ids}&autoplay=1&rel=0"
                                
                                components.html(
                                    f'<iframe width="100%" height="450" src="{playlist_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
                                    height=460
                                )
                            else:
                                st.video(current_url)
                        except:
                            st.video(current_url)
                    else:
                        # Standard single-video player
                        st.video(current_url)
            
            with col_playlist:
                with st.container(height="content", border=True):
                    for idx, url in enumerate(urls):
                        if url and url.strip():
                            # Check what is currently in the database
                            db_title = titles[idx] if idx < len(titles) else ""
                            
                            # Auto-resolution Logic: If the DB is empty or just says "Lecture X" from the backfill, fetch the real YouTube title!
                            if not db_title or db_title.startswith("Lecture "):
                                video_name = fetch_youtube_title(url.strip()) or f"Lecture {idx + 1}"
                            else:
                                video_name = db_title
                            
                            is_active = (st.session_state[state_key] == url.strip())
                            btn_type = "primary" if is_active else "secondary"
                            
                            if st.button(video_name, key=f"vid_btn_{week_id}_{idx}", type=btn_type, width="stretch", icon=":material/play_circle:"):
                                st.session_state[state_key] = url.strip()
                                st.rerun()
            with st.expander("AI Tutor: Generate Lecture Notes", expanded=False, icon=":material/model_training:"):
                if vid_id:
                    cached_vid = get_cached_video_notes(vid_id)
                    if cached_vid:
                        render_video_notes(cached_vid.get('ai_data', cached_vid), vid_id, cached_vid.get('created_by_user', 'System'))
                    else:
                        # STRICT FIX: Hide button if no keys
                        if not st.session_state.get("user_api_keys"):
                            st.warning("Please add your Gemini API Key in 'My Settings' to generate AI notes.", icon=":material/vpn_key:")
                        else:
                            if st.button("Generate Deep-Dive Lecture Notes", key=f"gen_notes_{vid_id}", type="secondary", width="stretch", icon=":material/auto_awesome:"):
                                with st.spinner("Compiling elite notes..."):
                                    ai_response = ask_video_ai(s_sel, current_url, st.session_state["user_api_keys"])
                                    save_video_cache(vid_id, ai_response, st.session_state["name"]) 
                                    st.rerun()
            
            # Ai Video Quiz Generator
            with st.expander("AI Tutor: Practice Quiz", expanded=False, icon=":material/quiz:"):
                if vid_id:
                    cached_quiz = get_cached_video_quiz(vid_id)
                    if cached_quiz:
                        render_interactive_quiz(vid_id, cached_quiz)
                    else:
                        st.info("Test your understanding of this lecture. The AI will generate a custom quiz based on the transcript.", icon=":material/info:")
                        # STRICT FIX: Hide button if no keys
                        if not st.session_state.get("user_api_keys"):
                            st.warning("Please add your Gemini API Key in 'My Settings' to generate quizzes.", icon=":material/vpn_key:")
                        else:
                            if st.button("Generate Practice Quiz", key=f"gen_quiz_{vid_id}", type="primary", width="stretch", icon=":material/quiz:"):
                                with st.spinner("Analyzing transcript and generating comprehensive quiz..."):
                                    quiz_data = generate_video_quiz(s_sel, current_url, st.session_state["user_api_keys"])
                                    # ... (keep your existing save logic here)
                                
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
                                    
                                    save_video_quiz(vid_id, quiz_data, meta, st.session_state["name"])
                                    
                                    # ONLY rerun if successful!
                                    st.rerun() 
                                else:
                                    # If it fails, print the error and STAY on the page so you can read it.
                                    st.error(f"Generation Failed: {quiz_data['error']}")

        else:
            st.info(f"No videos are currently linked to {w_sel}.", icon=":material/info:")
            c0.markdown("#### Video Lectures & Resources")
    else:
        st.info(f"No videos are currently linked to {w_sel}.", icon=":material/info:")
        c0.markdown("#### Video Lectures & Resources")

    # # ------------------------------------

