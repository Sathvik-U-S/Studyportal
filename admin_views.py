import streamlit as st # type: ignore
import time
import requests # type: ignore
import json
import re
import pandas as pd # type: ignore
import base64
import zlib
from database import fetch_data, execute_query
from mcq_ai_tutor import *
from cache_manager import *
from video_ai_tutor import *

def generate_traditional_er():
    """Dynamically generates a traditional ERD (Chen notation) using Mermaid Flowchart."""
    from database import fetch_data
    
    er_code = "graph TD\n"
    
    # 1. Define styling classes to match classic ERD tools like ERDPlus
    er_code += "    %% Styling\n"
    er_code += "    classDef entity fill:#BBDEFB,stroke:#0288D1,stroke-width:2px,color:#000;\n"
    er_code += "    classDef attribute fill:#FFFFFF,stroke:#757575,stroke-width:1px,color:#000;\n"
    er_code += "    classDef relation fill:#FFF9C4,stroke:#FBC02D,stroke-width:2px,color:#000;\n\n"
    
    tables = fetch_data("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    if not tables: return er_code
    
    # 2. Generate Entities (Rectangles) and Attributes (Ovals)
    for t in tables:
        t_name = str(t['table_name']).upper()
        # Create Entity Rectangle
        er_code += f"    {t_name}[\"<b>{t_name}</b>\"]:::entity\n"
        
        # Fetch columns (Limit to 5 so the diagram doesn't get overwhelmingly massive)
        cols = fetch_data("SELECT column_name FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position LIMIT 5", (t['table_name'],))
        if cols:
            for c in cols:
                c_name = c['column_name']
                node_id = f"{t_name}_{c_name}"
                
                # Underline Primary Keys for authentic ERD look
                label = f"<u>{c_name}</u>" if c_name == 'id' else c_name
                    
                # Create Attribute Oval (Stadium shape) and link it to the Entity
                er_code += f"    {node_id}([\"{label}\"]):::attribute\n"
                er_code += f"    {t_name} --- {node_id}\n"
        er_code += "\n"
                
    # 3. Generate Relationships (Diamonds) using Foreign Keys
    fk_query = """
        SELECT
            tc.table_name AS child_table, 
            ccu.table_name AS parent_table
        FROM information_schema.table_constraints AS tc
        JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY';
    """
    fks = fetch_data(fk_query)
    if fks:
        added_rels = set()
        for i, fk in enumerate(fks):
            parent = str(fk['parent_table']).upper()
            child = str(fk['child_table']).upper()
            
            # Prevent duplicate relationship diamonds between the same two tables
            rel_key = f"{parent}_{child}"
            if rel_key not in added_rels:
                rel_node = f"REL_{i}"
                
                # Create Relationship Diamond and link it (1 to N)
                er_code += f"    {rel_node}{{\"relates\"}}:::relation\n"
                er_code += f"    {parent} ---|1| {rel_node}\n"
                er_code += f"    {rel_node} ---|N| {child}\n"
                added_rels.add(rel_key)
                
    return er_code

def generate_dynamic_er():
    """Dynamically generates Mermaid ER code by querying the PostgreSQL schema."""
    from database import fetch_data
    
    # 1. Fetch Foreign Keys to draw the relationship lines
    fk_query = """
        SELECT
            tc.table_name AS child_table, 
            ccu.table_name AS parent_table
        FROM information_schema.table_constraints AS tc
        JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY';
    """
    fks = fetch_data(fk_query)
    
    er_code = "erDiagram\n"
    
    # Render Relationships
    if fks:
        added_fks = set()
        for fk in fks:
            parent = str(fk['parent_table']).upper()
            child = str(fk['child_table']).upper()
            rel = f"    {parent} ||--o{{ {child} : \"has\""
            if rel not in added_fks:
                er_code += rel + "\n"
                added_fks.add(rel)
    er_code += "\n"
    
    # 2. Fetch Tables and populate Columns
    tables = fetch_data("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    if tables:
        for t in tables:
            t_name_lower = t['table_name']
            t_name = t_name_lower.upper()
            
            # Fetch up to 6 columns per table to keep the diagram clean
            cols = fetch_data("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position LIMIT 6", (t_name_lower,))
            
            er_code += f"    {t_name} {{\n"
            if cols:
                for c in cols:
                    raw_type = str(c['data_type']).lower()
                    
                    # Simplify PostgreSQL types for visual cleanliness
                    if "int" in raw_type: c_type = "int"
                    elif "char" in raw_type or "text" in raw_type: c_type = "varchar"
                    elif "bool" in raw_type: c_type = "boolean"
                    elif "time" in raw_type or "date" in raw_type: c_type = "timestamp"
                    elif "json" in raw_type: c_type = "jsonb"
                    else: c_type = "type"
                    
                    pk_tag = " PK" if c['column_name'] == 'id' else ""
                    fk_tag = " FK" if c['column_name'].endswith('_id') else ""
                    
                    er_code += f"        {c_type} {c['column_name']}{pk_tag}{fk_tag}\n"
            er_code += "    }\n"
            
    return er_code

def render_mermaid_diagram(mermaid_code, height=600):
    """Reusable function to render Mermaid code with Zoom/Pan controls."""
    import base64
    import zlib
    import streamlit.components.v1 as components
    
    final_mermaid = mermaid_code.replace('```mermaid', '').replace('```', '').strip()
    
    try:
        compressed = zlib.compress(final_mermaid.encode('utf-8'), 9)
        b64_mermaid = base64.urlsafe_b64encode(compressed).decode('utf-8').replace('=', '')
        mermaid_url = f"https://kroki.io/mermaid/svg/{b64_mermaid}"
        
        html_content = f"""
            <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
            <style>
                :root {{ --text-color: #31333F; --bg-color: transparent; --border-color: rgba(49, 51, 63, 0.2); --btn-bg: rgba(49, 51, 63, 0.05); --btn-hover: rgba(49, 51, 63, 0.1); --container-bg: rgba(255, 255, 255, 0.5); }}
                body {{ margin: 0; background-color: var(--bg-color); color: var(--text-color); font-family: sans-serif; }}
                .controls {{ position: sticky; top: 0; z-index: 100; display: flex; gap: 12px; background-color: transparent; padding-bottom: 10px; align-items: center; }}
                button {{ display: flex; align-items: center; gap: 5px; padding: 6px 12px; cursor: pointer; border-radius: 6px; border: 1px solid var(--border-color); background: var(--btn-bg); color: var(--text-color); font-weight: bold; font-size: 13px; transition: background 0.2s; }}
                button .material-icons {{ font-size: 18px; }}
                button:hover {{ background: var(--btn-hover); }}
                #wrapper {{ width: 100%; height: {height-100}px; overflow: auto; border: 1px solid var(--border-color); border-radius: 8px; background: var(--container-bg); cursor: grab; }}
                #wrapper:active {{ cursor: grabbing; }}
                #wrapper::-webkit-scrollbar {{ width: 10px; height: 10px; }}
                #wrapper::-webkit-scrollbar-track {{ background: transparent; }}
                #wrapper::-webkit-scrollbar-thumb {{ background-color: var(--border-color); border-radius: 8px; }}
                #wrapper::-webkit-scrollbar-thumb:hover {{ background-color: var(--text-color); }}
                #container {{ transform-origin: 0 0; transition: transform 0.1s ease-out; display: inline-block; min-width: 100%; user-select: none; }}
                #mermaid-img {{ display: block; width: 100%; pointer-events: none; transition: filter 0.3s ease; }}
            </style>
            
            <div class="controls">
                <button type="button" onclick="zoom(1.2)"><span class="material-icons">zoom_in</span> Zoom In</button>
                <button type="button" onclick="zoom(0.8)"><span class="material-icons">zoom_out</span> Zoom Out</button>
                <button type="button" onclick="resetZoom()"><span class="material-icons">restart_alt</span> Reset</button>
                <span id="zoom-level" style="margin-left: 10px; align-self: center; font-weight: 500;">100%</span>
            </div>
            
            <div id="wrapper">
                <div id="container">
                    <img id="mermaid-img" src="{mermaid_url}">
                </div>
            </div>

            <script>
                function syncTheme() {{
                    try {{
                        const parentStyle = window.parent.getComputedStyle(window.parent.document.querySelector('.stApp') || window.parent.document.body);
                        const bgColor = parentStyle.backgroundColor;
                        const textColor = parentStyle.color;
                        
                        const rgb = bgColor.match(/\\d+/g);
                        let isDark = false;
                        if (rgb && rgb.length >= 3) {{
                            const brightness = (parseInt(rgb[0]) * 299 + parseInt(rgb[1]) * 587 + parseInt(rgb[2]) * 114) / 1000;
                            isDark = brightness < 128;
                        }}

                        document.documentElement.style.setProperty('--text-color', textColor);
                        const textRgba = textColor.replace('rgb', 'rgba').replace(')', ', 0.2)');
                        const btnBg = textColor.replace('rgb', 'rgba').replace(')', ', 0.05)');
                        const btnHover = textColor.replace('rgb', 'rgba').replace(')', ', 0.1)');
                        const containerBg = isDark ? 'rgba(0, 0, 0, 0.2)' : 'rgba(255, 255, 255, 0.5)';

                        document.documentElement.style.setProperty('--border-color', textRgba);
                        document.documentElement.style.setProperty('--btn-bg', btnBg);
                        document.documentElement.style.setProperty('--btn-hover', btnHover);
                        document.documentElement.style.setProperty('--container-bg', containerBg);

                        const img = document.getElementById('mermaid-img');
                        if (isDark) {{ img.style.filter = 'invert(0.85) hue-rotate(180deg)'; }} 
                        else {{ img.style.filter = 'none'; }}
                    }} catch (e) {{}}
                }}

                syncTheme();
                setInterval(syncTheme, 1000);

                let scale = 1.0;
                const container = document.getElementById('container');
                const zoomLevel = document.getElementById('zoom-level');
                const wrapper = document.getElementById('wrapper');

                function zoom(factor) {{
                    scale *= factor;
                    if (scale < 0.2) scale = 0.2;
                    if (scale > 10.0) scale = 10.0;
                    container.style.transform = `scale(${{scale}})`;
                    zoomLevel.innerText = Math.round(scale * 100) + "%";
                }}

                function resetZoom() {{
                    scale = 1.0;
                    container.style.transform = 'scale(1)';
                    zoomLevel.innerText = "100%";
                }}

                let isDown = false;
                let startX, startY, scrollLeft, scrollTop;

                wrapper.addEventListener('mousedown', (e) => {{
                    isDown = true;
                    startX = e.pageX - wrapper.offsetLeft;
                    startY = e.pageY - wrapper.offsetTop;
                    scrollLeft = wrapper.scrollLeft;
                    scrollTop = wrapper.scrollTop;
                }});
                wrapper.addEventListener('mouseleave', () => {{ isDown = false; }});
                wrapper.addEventListener('mouseup', () => {{ isDown = false; }});
                wrapper.addEventListener('mousemove', (e) => {{
                    if (!isDown) return;
                    e.preventDefault();
                    const x = e.pageX - wrapper.offsetLeft;
                    const y = e.pageY - wrapper.offsetTop;
                    wrapper.scrollLeft = scrollLeft - (x - startX) * 1.5; 
                    wrapper.scrollTop = scrollTop - (y - startY) * 1.5;
                }});

                wrapper.addEventListener('touchstart', (e) => {{
                    isDown = true;
                    startX = e.touches[0].pageX - wrapper.offsetLeft;
                    startY = e.touches[0].pageY - wrapper.offsetTop;
                    scrollLeft = wrapper.scrollLeft;
                    scrollTop = wrapper.scrollTop;
                }});
                wrapper.addEventListener('touchend', () => {{ isDown = false; }});
                wrapper.addEventListener('touchmove', (e) => {{
                    if (!isDown) return;
                    e.preventDefault(); 
                    const x = e.touches[0].pageX - wrapper.offsetLeft;
                    const y = e.touches[0].pageY - wrapper.offsetTop;
                    wrapper.scrollLeft = scrollLeft - (x - startX) * 1.5;
                    wrapper.scrollTop = scrollTop - (y - startY) * 1.5;
                }}, {{ passive: false }});
            </script>
        """
        components.html(html_content, height=height)
    except Exception as e:
        st.error(f"Diagram failed to render. {e}")
        st.code(final_mermaid, language="text")

@st.cache_data(show_spinner=False, ttl=604800) 
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

def render_edit_content():
    """
    Renders the Edit Content view for modifying questions, weeks, and structure.
    """
    # Renamed the second tab to reflect it handles more than just videos now
    tab_edit_q, tab_flag_q, tab_edit_w, tab_edit_hier, tab_health, tab_overview, tab_sql = st.tabs([
        "Edit Questions", "Flagged Questions", "Edit Week Details", "Edit Hierarchy", "Content Health", "Content Overview", "Custom SQL"
    ])
    
    # TAB 1: EDIT QUESTIONS (Upgraded Bulk Editor + Add/Delete)
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
                    act_id = a_map[a_sel]

                    # ---------- BULK QUESTION VIEWER ----------------
                    questions = fetch_data(
                        "SELECT * FROM questions WHERE assessment_id = %s ORDER BY id ASC",
                        (act_id,)
                    )

                    if not questions:
                        st.info("No questions found for this activity. Add one below!", icon=":material/info:")
                    else:
                        st.markdown(f"#### Managing {len(questions)} Questions in `{a_sel}`")
                        
                        # OPTIMIZATION: Isolate every question into its own micro-environment
                        @st.fragment
                        def render_question_editor_fragment(idx, q_data, act_id, s_sel):
                            q_id = q_data['id']
                            short_head = str(q_data['heading'])[:60] + ("..." if len(str(q_data['heading'])) > 60 else "")
                            
                            with st.expander(f"Q{idx} | ID: {q_id} | {short_head}", expanded=False, icon=":material/edit_document:"):
                                opts_data = fetch_data("SELECT * FROM options WHERE question_id = %s ORDER BY id ASC", (q_id,))

                                # ---------- EDIT FORM ----------------
                                with st.form(f"edit_form_{q_id}"):
                                    st.markdown("#### :material/info: Core Details")

                                    raw_heading = str(q_data['heading']) if q_data['heading'] is not None else ""
                                    n_head = st.text_area("Heading (Raw DB Value)", value=raw_heading, height="content", key=f"heading_raw_{q_id}")

                                    c_qm1, c_qm2 = st.columns([1, 4])
                                    curr_q_mtype = q_data['media_type'] if q_data['media_type'] else "text"
                                    n_mtype = c_qm1.selectbox("Media Type", ["text", "code", "image"], index=["text", "code", "image"].index(curr_q_mtype), key=f"mtype_{q_id}")
                                    raw_media = str(q_data['media_content']) if q_data['media_content'] is not None else ""
                                    n_cont = c_qm2.text_area("Media Content", value=raw_media, height="content", key=f"media_edit_{q_id}")

                                    # Metadata Section
                                    st.markdown("#### :material/notes: Metadata & Explanations")
                                    c_meta1, c_meta2 = st.columns(2)
                                    curr_diff = q_data.get('difficulty') or "Medium"
                                    n_diff = c_meta1.selectbox("Difficulty", ["Easy", "Medium", "Hard"], index=["Easy", "Medium", "Hard"].index(curr_diff), key=f"diff_{q_id}")
                                    n_pts = c_meta2.number_input("Points", min_value=1, value=int(q_data.get('points') or 1), key=f"pts_{q_id}")
                                    n_exp = st.text_area("Manual Explanation / Tutor Note", value=q_data.get('manual_explanation') or "", height=100, key=f"exp_{q_id}")

                                    # NUMERICAL LOGIC
                                    if q_data.get('q_type') == 'numerical' or str(q_data.get('q_type')).lower() == 'nat':
                                        n_ans = st.text_input("Correct Answer", value=q_data.get('correct_answer') or "", icon=":material/check:", key=f"ans_{q_id}")

                                        if st.form_submit_button("Update Question", type="primary", icon=":material/save:"):
                                            final_q_mtype = n_mtype if n_mtype != "text" else None
                                            execute_query("UPDATE questions SET heading=%s, media_type=%s, media_content=%s, correct_answer=%s, difficulty=%s, points=%s, manual_explanation=%s WHERE id=%s", (n_head, final_q_mtype, n_cont, n_ans, n_diff, n_pts, n_exp, q_id))
                                            st.success("Updated Successfully", icon=":material/check_circle:")
                                            st.rerun(scope="fragment") # Instantly reloads just this box!

                                    # MCQ LOGIC
                                    else:
                                        st.markdown("#### :material/list: Edit Options")
                                        upd_opts = []

                                        for opt in opts_data:
                                            c_a, c_b, c_c, c_d = st.columns([0.2, 0.55, 0.15, 0.1])
                                            curr_type = opt['media_type'] if opt['media_type'] else "text"
                                            nt = c_a.selectbox("Type", ["text", "code", "image"], key=f"type_{opt['id']}", index=["text", "code", "image"].index(curr_type))
                                            raw_option = (str(opt['media_content']) if opt['media_content'] is not None else str(opt['option_text']) if opt['option_text'] is not None else "")
                                            nv = c_b.text_area("Value", value=raw_option, height="content", key=f"option_raw_{opt['id']}")
                                            nc = c_c.checkbox("Correct", value=opt['is_correct'], key=f"correct_{opt['id']}")
                                            ndel = c_d.checkbox("Delete", value=False, key=f"del_opt_{opt['id']}") 
                                            upd_opts.append((opt['id'], nt, nv, nc, ndel))

                                        if st.form_submit_button("Update Question", type="primary", icon=":material/save:"):
                                            final_q_mtype = n_mtype if n_mtype != "text" else None
                                            execute_query("UPDATE questions SET heading=%s, media_type=%s, media_content=%s, difficulty=%s, points=%s, manual_explanation=%s WHERE id=%s", (n_head, final_q_mtype, n_cont, n_diff, n_pts, n_exp, q_id))

                                            for oid, otype, oval, ocorr, odel in upd_opts:
                                                if odel: execute_query("DELETE FROM options WHERE id=%s", (oid,))
                                                else:
                                                    if otype == "text": execute_query("UPDATE options SET option_text=%s, media_type=NULL, media_content=NULL, is_correct=%s WHERE id=%s", (oval, ocorr, oid))
                                                    else: execute_query("UPDATE options SET option_text=NULL, media_type=%s, media_content=%s, is_correct=%s WHERE id=%s", (otype, oval, ocorr, oid))

                                            st.success("Updated Successfully", icon=":material/check_circle:")
                                            st.rerun(scope="fragment")

                                # ADD BLANK OPTION BUTTON
                                if q_data.get('q_type') != 'numerical' and str(q_data.get('q_type')).lower() != 'nat':
                                    if st.button(f"➕ Add Blank Option to Q{idx}", key=f"add_opt_btn_{q_id}", use_container_width=True):
                                        execute_query("INSERT INTO options (question_id, option_text, is_correct, subject_name) VALUES (%s, %s, %s, %s)", (q_id, "New Option", False, s_sel))
                                        st.success("Option Added!", icon=":material/check_circle:")
                                        st.rerun(scope="fragment")

                        # Execute the fragment for each question
                        for idx, q_data in enumerate(questions, start=1):
                            render_question_editor_fragment(idx, q_data, act_id, s_sel)

                    # ---------- ADD NEW QUESTION TOOL ----------------
                    st.divider()
                    st.markdown("#### :material/add_circle: Add New Question")
                    with st.form(f"add_q_form_{act_id}"):
                        st.info("When adding an MCQ, the system will automatically create 4 blank options for you to edit above.", icon=":material/info:")
                        new_heading = st.text_area("Question Heading", height=100, placeholder="Enter your question here...")
                        
                        col_t1, col_t2 = st.columns(2)
                        new_type = col_t1.selectbox("Question Format", ["mcq", "numerical"])
                        new_diff = col_t2.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
                        
                        if st.form_submit_button("Create Question", type="primary", icon=":material/add:"):
                            if new_heading.strip():
                                # 1. Insert the Question
                                execute_query(
                                    "INSERT INTO questions (assessment_id, heading, q_type, difficulty, points, created_at, subject_name) VALUES (%s, %s, %s, %s, 1, CURRENT_TIMESTAMP, %s)", 
                                    (act_id, new_heading.strip(), new_type, new_diff, s_sel)
                                )
                                
                                # 2. If it is an MCQ, seed 4 blank options so the user can easily edit them
                                if new_type == "mcq":
                                    new_q_data = fetch_data("SELECT id FROM questions WHERE assessment_id=%s ORDER BY id DESC LIMIT 1", (act_id,))
                                    if new_q_data:
                                        new_q_id = new_q_data[0]['id']
                                        for _ in range(4):
                                            execute_query("INSERT INTO options (question_id, option_text, is_correct, subject_name) VALUES (%s, %s, %s, %s)", (new_q_id, "New Option", False, s_sel))
                                
                                st.success("Question created! It now appears in the list above for you to edit.")
                                st.rerun()
                            else:
                                st.error("Heading cannot be blank.", icon=":material/error:")
    
    # NEW TAB: FLAGGED QUESTIONS DATA
    with tab_flag_q:
        st.markdown("#### :material/flag: Flagged Question Data")
        st.info("These questions were flagged by admins during Study Mode due to bad data, missing options, or typos.", icon=":material/info:")
        
        # CRITICAL FIX: Fetch all the necessary question and metadata columns to render the Full Editor
        flags = fetch_data("""
            SELECT qi.id as flag_id, qi.issue_description, qi.reported_by, qi.created_at, 
                   q.id as q_id, q.heading, q.q_type, q.media_type, q.media_content, q.difficulty, q.points, q.correct_answer, q.manual_explanation,
                   s.name as sub_name, a.week_number, a.name as act_name
            FROM question_issues qi
            JOIN questions q ON qi.question_id = q.id
            JOIN assessments a ON q.assessment_id = a.id
            JOIN subjects s ON a.subject_id = s.id
            ORDER BY qi.created_at DESC
        """)
        
        if not flags:
            st.success("No flagged questions! Great job.", icon=":material/check_circle:")
        else:
            @st.fragment
            def render_flagged_question_editor(idx, f):
                q_id = f['q_id']
                flag_id = f['flag_id']
                short_head = str(f['heading'])[:60] + ("..." if len(str(f['heading'])) > 60 else "")
                
                with st.expander(f"FLAGGED: {f['sub_name']} (W{f['week_number']}) | Q_ID: {q_id} | {short_head}", expanded=False, icon=":material/flag:"):
                    st.error(f"**Admin Note (by {f['reported_by']}):** {f['issue_description']}", icon=":material/error:")
                    
                    c_dis1, c_dis2 = st.columns([4, 1])
                    if c_dis2.button("Dismiss Flag (No Changes)", key=f"res_flag_{flag_id}", type="secondary", use_container_width=True):
                        execute_query("DELETE FROM question_issues WHERE id=%s", (flag_id,))
                        st.success("Flag resolved!", icon=":material/check_circle:")
                        st.rerun() 

                    st.divider()
                    
                    opts_data = fetch_data("SELECT * FROM options WHERE question_id = %s ORDER BY id ASC", (q_id,))
                    
                    # --- THE FULL EDITOR UI ---
                    with st.form(f"flag_edit_form_{q_id}"):
                        st.markdown("#### :material/info: Core Details")

                        raw_heading = str(f['heading']) if f['heading'] is not None else ""
                        n_head = st.text_area("Heading (Raw DB Value)", value=raw_heading, height="content", key=f"fq_head_{q_id}")

                        c_qm1, c_qm2 = st.columns([1, 4])
                        curr_q_mtype = f['media_type'] if f['media_type'] else "text"
                        n_mtype = c_qm1.selectbox("Media Type", ["text", "code", "image"], index=["text", "code", "image"].index(curr_q_mtype), key=f"fq_mtype_{q_id}")
                        raw_media = str(f['media_content']) if f['media_content'] is not None else ""
                        n_cont = c_qm2.text_area("Media Content", value=raw_media, height="content", key=f"fq_media_{q_id}")

                        st.markdown("#### :material/notes: Metadata & Explanations")
                        c_meta1, c_meta2 = st.columns(2)
                        curr_diff = f.get('difficulty') or "Medium"
                        n_diff = c_meta1.selectbox("Difficulty", ["Easy", "Medium", "Hard"], index=["Easy", "Medium", "Hard"].index(curr_diff), key=f"fq_diff_{q_id}")
                        n_pts = c_meta2.number_input("Points", min_value=1, value=int(f.get('points') or 1), key=f"fq_pts_{q_id}")
                        n_exp = st.text_area("Manual Explanation / Tutor Note", value=f.get('manual_explanation') or "", height=100, key=f"fq_exp_{q_id}")

                        # NUMERICAL LOGIC
                        if f.get('q_type') == 'numerical' or str(f.get('q_type')).lower() == 'nat':
                            n_ans = st.text_input("Correct Answer", value=f.get('correct_answer') or "", icon=":material/check:", key=f"fq_ans_{q_id}")

                            if st.form_submit_button("Update Question & Resolve Flag", type="primary", icon=":material/save:"):
                                final_q_mtype = n_mtype if n_mtype != "text" else None
                                execute_query("UPDATE questions SET heading=%s, media_type=%s, media_content=%s, correct_answer=%s, difficulty=%s, points=%s, manual_explanation=%s WHERE id=%s", (n_head, final_q_mtype, n_cont, n_ans, n_diff, n_pts, n_exp, q_id))
                                execute_query("DELETE FROM question_issues WHERE id=%s", (flag_id,))
                                st.success("Updated Successfully and Flag Dismissed", icon=":material/check_circle:")
                                st.rerun() 

                        # MCQ LOGIC
                        else:
                            st.markdown("#### :material/list: Edit Options")
                            upd_opts = []

                            for opt in opts_data:
                                c_a, c_b, c_c, c_d = st.columns([0.2, 0.55, 0.15, 0.1])
                                curr_type = opt['media_type'] if opt['media_type'] else "text"
                                nt = c_a.selectbox("Type", ["text", "code", "image"], key=f"fq_type_{opt['id']}", index=["text", "code", "image"].index(curr_type))
                                raw_option = (str(opt['media_content']) if opt['media_content'] is not None else str(opt['option_text']) if opt['option_text'] is not None else "")
                                nv = c_b.text_area("Value", value=raw_option, height="content", key=f"fq_option_raw_{opt['id']}")
                                nc = c_c.checkbox("Correct", value=opt['is_correct'], key=f"fq_correct_{opt['id']}")
                                ndel = c_d.checkbox("Delete", value=False, key=f"fq_del_opt_{opt['id']}") 
                                upd_opts.append((opt['id'], nt, nv, nc, ndel))

                            if st.form_submit_button("Update Question & Resolve Flag", type="primary", icon=":material/save:"):
                                final_q_mtype = n_mtype if n_mtype != "text" else None
                                execute_query("UPDATE questions SET heading=%s, media_type=%s, media_content=%s, difficulty=%s, points=%s, manual_explanation=%s WHERE id=%s", (n_head, final_q_mtype, n_cont, n_diff, n_pts, n_exp, q_id))

                                for oid, otype, oval, ocorr, odel in upd_opts:
                                    if odel: execute_query("DELETE FROM options WHERE id=%s", (oid,))
                                    else:
                                        if otype == "text": execute_query("UPDATE options SET option_text=%s, media_type=NULL, media_content=NULL, is_correct=%s WHERE id=%s", (oval, ocorr, oid))
                                        else: execute_query("UPDATE options SET option_text=NULL, media_type=%s, media_content=%s, is_correct=%s WHERE id=%s", (otype, oval, ocorr, oid))
                                
                                execute_query("DELETE FROM question_issues WHERE id=%s", (flag_id,))
                                st.success("Updated Successfully and Flag Dismissed", icon=":material/check_circle:")
                                st.rerun()

                    # ADD BLANK OPTION BUTTON
                    if f.get('q_type') != 'numerical' and str(f.get('q_type')).lower() != 'nat':
                        if st.button(f"Add Blank Option to Q{idx}", key=f"fq_add_opt_btn_{q_id}", use_container_width=True, icon=":material/add:"):
                            execute_query("INSERT INTO options (question_id, option_text, is_correct, subject_name) VALUES (%s, %s, %s, %s)", (q_id, "New Option", False, f['sub_name']))
                            st.success("Option Added!", icon=":material/check_circle:")
                            st.rerun(scope="fragment")

            # Execute the fragment for each flagged question
            for idx, f in enumerate(flags, start=1):
                render_flagged_question_editor(idx, f)
    
    # TAB 2: EDIT WEEK DETAILS (Upgraded with Auto-Title Fetch)
    with tab_edit_w:
        st.markdown("#### :material/play_lesson: Manage Week Details & Videos")
        
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
                    new_title = st.text_input("Overall Topic Title (e.g., 'Introduction to Python')", value=curr_title or "", icon=":material/title:")
                    
                    st.markdown("**YouTube URLs & Video Titles**")
                    st.info("You can leave the Video Titles box completely empty. The app will automatically fetch the real titles directly from YouTube!", icon=":material/auto_awesome:")
                    col_u, col_t = st.columns(2)
                    new_urls_str = col_u.text_area("YouTube URLs", value=curr_urls_str, height=150)
                    new_titles_str = col_t.text_area("Video Titles (Optional Override)", value=curr_titles_str, height=150)
                    
                    if st.form_submit_button("Save Week Details", type="primary", icon=":material/save:"):
                        new_urls_list = [u.strip() for u in new_urls_str.split("\n") if u.strip()]
                        new_titles_list = [t.strip() for t in new_titles_str.split("\n") if t.strip()]
                        
                        final_titles = []
                        with st.spinner("Processing URLs and automatically fetching YouTube titles..."):
                            for i, url in enumerate(new_urls_list):
                                # If you typed a manual title, keep it. Otherwise, fetch it.
                                if i < len(new_titles_list) and new_titles_list[i]:
                                    final_titles.append(new_titles_list[i])
                                else:
                                    fetched_title = fetch_youtube_title(url)
                                    final_titles.append(fetched_title if fetched_title else f"Lecture {i+1}")
                                    
                            if execute_query("UPDATE weeks SET topic_title=%s, youtube_urls=%s, video_titles=%s WHERE id=%s", (new_title, new_urls_list, final_titles, week_id)):
                                st.success(f"Successfully updated {vw_sel}!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Failed to save week details.")

        # ==========================================
        # THE GLOBAL BACKFILL TOOL (Fixes old videos)
        # ==========================================
        st.divider()
        st.markdown("##### :material/build: Auto-Fix Missing Titles (Global)")
        st.info("Did you previously add URLs without titles? Click below to scan the entire database and automatically fetch titles for any videos that are missing them.")
        
        if st.button("Auto-Fill Missing Titles for ALL Weeks", type="secondary", icon=":material/autorenew:"):
            with st.spinner("Scanning database and fetching titles from YouTube... This may take a minute."):
                all_weeks = fetch_data("SELECT id, youtube_urls, video_titles FROM weeks WHERE youtube_urls IS NOT NULL")
                fixed_count = 0
                
                for w in all_weeks:
                    urls = w['youtube_urls']
                    if not urls: continue
                    titles = w['video_titles'] or []
                    
                    needs_update = False
                    new_titles = []
                    
                    for i, u in enumerate(urls):
                        # Keep existing valid titles
                        if i < len(titles) and titles[i] and not titles[i].startswith("Lecture "):
                            new_titles.append(titles[i])
                        else:
                            # Fetch the missing title
                            fetched = fetch_youtube_title(u)
                            new_titles.append(fetched if fetched else f"Lecture {i+1}")
                            needs_update = True
                            
                    # Update database if changes were made or arrays were misaligned
                    if needs_update or len(new_titles) != len(urls):
                        execute_query("UPDATE weeks SET video_titles=%s WHERE id=%s", (new_titles, w['id']))
                        fixed_count += 1
                
                if fixed_count > 0:
                    st.success(f"✅ Successfully fetched and updated titles for {fixed_count} weeks!")
                else:
                    st.success("✅ All videos in the database already have titles!")
                    
                time.sleep(2)
                st.rerun()
                
    # TAB 3: MANAGE STRUCTURE (Edit Hierarchy)
    with tab_edit_hier:
        st.markdown("##### :material/account_tree: Manage Database Structure")
        
        # ROW 1: ADD NEW STRUCTURE
        c_sub, c_week, c_act = st.columns(3)

        with c_sub:
            with st.container(border=True):
                st.markdown("**Add Subject**")
                with st.form("add_sub_form"):
                    new_sub_name = st.text_input("Subject Name", icon=":material/bookmark:")
                    if st.form_submit_button("Add Subject", type="primary", width="stretch", icon=":material/add:"):
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
                        new_week_num = st.number_input("Week Number", min_value=1, max_value=50, step=1, icon=":material/calendar_today:")
                        if st.form_submit_button("Add Week", type="primary", width="stretch", icon=":material/add:"):
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
                            new_act_name = st.text_input("Activity Name", icon=":material/local_activity:")
                            if st.form_submit_button("Add Activity", type="primary", width="stretch", icon=":material/add:"):
                                if new_act_name.strip():
                                    if execute_query("INSERT INTO assessments (subject_id, week_number, name) VALUES (%s, %s, %s)", (sub_id_a, week_sel_a, new_act_name.strip())):
                                        st.success(f"Added '{new_act_name}'")
                                        st.rerun()
                                else: st.warning("Please enter a name.")
                    else: st.warning("Add a week to this subject first.")
                else: st.warning("Add a subject first.")

        # ROW 2: EDIT EXISTING STRUCTURE
        st.divider()
        st.markdown("##### :material/edit_document: Edit Existing Structure")
        ce_sub, ce_week, ce_act = st.columns(3)

        with ce_sub:
            with st.container(border=True):
                st.markdown("**Rename Subject**")
                if hier_subs:
                    edit_sub_sel = st.selectbox("Select Subject to Rename", [s['name'] for s in hier_subs], key="edit_sub_sel")
                    edit_sub_id = next(s['id'] for s in hier_subs if s['name'] == edit_sub_sel)
                    with st.form("rename_sub_form"):
                        new_sub_name = st.text_input("New Name", value=edit_sub_sel, icon=":material/edit:")
                        if st.form_submit_button("Rename Subject", type="primary", width="stretch", icon=":material/drive_file_rename_outline:"):
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
                            new_week_num = st.number_input("New Week Number", min_value=1, max_value=100, value=e_w_sel, icon=":material/edit:")
                            if st.form_submit_button("Update Week", type="primary", width="stretch", icon=":material/update:"):
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
                                new_act_name = st.text_input("New Activity Name", value=e_a_act_sel, icon=":material/edit:")
                                if st.form_submit_button("Rename Activity", type="primary", width="stretch", icon=":material/drive_file_rename_outline:"):
                                    if new_act_name.strip() and new_act_name.strip() != e_a_act_sel:
                                        if execute_query("UPDATE assessments SET name = %s WHERE id = %s", (new_act_name.strip(), e_a_act_id)):
                                            st.success(f"Renamed to '{new_act_name}'")
                                            st.rerun()

    # TOOL 4: Content Health Inspector
    with tab_health:
        st.markdown("##### :material/health_and_safety: Content Health Inspector")
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

    # TAB: CONTENT OVERVIEW
    with tab_overview:
        st.markdown("#### :material/account_tree: Content Overview")

        subjects = fetch_data("SELECT * FROM subjects ORDER BY name ASC")
        if subjects:
            s_map = {s['name']: s['id'] for s in subjects}
            s_sel = st.selectbox("Select Subject", list(s_map.keys()), key="overview_sub")

            if s_sel:
                s_id = s_map[s_sel]

                # 1. Fetch all weeks and activities in TWO lightning-fast queries
                weeks_data = fetch_data("SELECT week_number, topic_title FROM weeks WHERE subject_id=%s ORDER BY week_number ASC", (s_id,))
                
                # The "Magic" Query: Gets activities and counts their questions instantly
                act_query = """
                    SELECT a.week_number, a.name AS activity_name, COUNT(q.id) as question_count
                    FROM assessments a
                    LEFT JOIN questions q ON a.id = q.assessment_id
                    WHERE a.subject_id = %s
                    GROUP BY a.week_number, a.name
                    ORDER BY a.week_number ASC, a.name ASC
                """
                act_data = fetch_data(act_query, (s_id,))

                # 2. Organize data in Python memory so we don't spam the database inside the UI loop!
                act_by_week = {}
                if act_data:
                    for row in act_data:
                        wn = row['week_number']
                        if wn not in act_by_week:
                            act_by_week[wn] = []
                        act_by_week[wn].append({
                            'name': row['activity_name'],
                            'count': row['question_count']
                        })

                # Merge week numbers from both the weeks table and any orphaned activities
                all_week_nums = set([w['week_number'] for w in weeks_data]) if weeks_data else set()
                if act_data:
                    all_week_nums.update([row['week_number'] for row in act_data])
                
                w_title_map = {w['week_number']: w.get('topic_title', '') for w in weeks_data} if weeks_data else {}

                # 3. Render the Collapsibles
                if not all_week_nums:
                    st.warning(f"No weeks or activities found for {s_sel}.", icon=":material/warning:")
                else:
                    for wn in sorted(list(all_week_nums)):
                        title = w_title_map.get(wn, "")
                        label = f"Week {wn}" + (f": {title}" if title else "")
                        
                        week_acts = act_by_week.get(wn, [])
                        total_acts = len(week_acts)
                        total_qs = sum(a['count'] for a in week_acts)

                        # Provide a rich summary right on the collapsible header!
                        with st.expander(f"{label} — ({total_acts} Activities, {total_qs} Questions)", icon=":material/folder:"):
                            if week_acts:
                                for act in week_acts:
                                    st.markdown(f"- **{act['name']}**: `{act['count']} Questions`")
                            else:
                                st.info("No activities added for this week yet.", icon=":material/info:")

    # TAB: CUSTOM SQL
    with tab_sql:
        st.markdown("#### :material/terminal: Run Custom SQL")
        
        # 1. Wrap in a form to stop laggy reloads while typing
        with st.form("custom_sql_form", clear_on_submit=False):
            query = st.text_area("Enter SQL Query", height=200, placeholder="SELECT * FROM questions WHERE id = 1;")
            
            # 2. Form submit button handles the loading state and prevents double-clicks
            submitted = st.form_submit_button("Execute Query", type="primary", icon=":material/play_circle:")
            
            if submitted:
                if query.strip() == "":
                    st.error("Please enter a query.", icon=":material/error:")
                else:
                    import datetime
                    # 3. Precise timestamp for feedback (Hour:Minute:Second AM/PM)
                    now = datetime.datetime.now().strftime("%I:%M:%S %p")
                    
                    with st.spinner("Executing..."):
                        # Use same text and logic as your original snippet
                        if query.strip().upper().startswith("SELECT"):
                            try:
                                res = fetch_data(query) #
                                if res:
                                    st.dataframe(res, use_container_width=True)
                                    st.success(f"**[{now}]** Returned {len(res)} rows.", icon=":material/check_circle:")
                                else:
                                    st.info(f"**[{now}]** Query returned no results.", icon=":material/info:")
                            except Exception as e:
                                st.error(f"**[{now}]** SQL Error: {e}", icon=":material/error:")
                        else:
                            if execute_query(query): #
                                st.success(f"**[{now}]** Query executed and committed successfully.", icon=":material/check_circle:")
                            else:
                                st.error(f"**[{now}]** Failed to execute query. Check syntax and constraints.", icon=":material/error:")


def render_view_database():
    """
    Renders the View Database tool for inspecting tables, hierarchy, and health.
    """
    # Fetch global table list
    tables = fetch_data("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    table_names = [t['table_name'] for t in tables] if tables else []

    # ---------- DATABASE TOOLS TABS ----------------
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
    
    # TOOL 1: Hierarchy Explorer (With Option Drill-down)
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
                                    st.info("No options found. This is likely a Numerical question.", icon=":material/info:")
                    else:
                        st.info("No questions found for this activity.", icon=":material/info:")
                else:
                    st.warning("No activities found for this week.")
            else:
                st.warning("No weeks found for this subject.")
        else:
            st.warning("No subjects found in the database.")

    # TOOL 2: GUI Visual Dashboard (Upgraded)
    with tab_viz:
        st.markdown("##### :material/analytics: Database Analytics")
        
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



    # TOOL 5: Global Keyword Search
    with tab_search:
        st.markdown("##### :material/manage_search: Search All Content")
        kw = st.text_input("Enter keyword to find across Questions and Options:", icon=":material/search:")
        
        if st.button("Search Database", type="primary", icon=":material/search:") and kw.strip():
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
                st.info(f"No results found for '{kw}'.", icon=":material/info:")

    # TOOL 6: Supercharged Data Explorer (Dynamic Filters & JOINs)
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

        # MODE A: Raw Tables
        if source_type == "Raw Tables" and table_names:
            selected_table = st.selectbox("Select Table", table_names, key="raw_tbl_sel")
            if selected_table:
                base_query = f"SELECT * FROM {selected_table}"
                col_info = fetch_data("""
                    SELECT column_name as col, data_type as type 
                    FROM information_schema.columns 
                    WHERE table_name = %s
                """, (selected_table,))

        # MODE B: Master Joined Views
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

        # Dynamic Filter Generator
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
                text_search = st.text_input("Global Text Search (Scans all text columns instantly)", placeholder="Enter keyword to search...", icon=":material/search:")

            # Query Execution
            if st.button("Apply Filters & Fetch Data", type="primary", use_container_width=True, icon=":material/filter_alt:"):
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

            # Render Results
            if st.session_state.browse_results is not None:
                if st.session_state.browse_results:
                    st.success(f"**Showing {len(st.session_state.browse_results)} records.**")
                    st.dataframe(pd.DataFrame(st.session_state.browse_results), width="stretch", hide_index=True)
                    
                    if st.button("Clear Results", icon=":material/clear_all:"):
                        st.session_state.browse_results = None
                        st.rerun()
                else:
                    st.warning("No records found matching those filters. Try removing some restrictions.")

    

    # TOOL 8: Schema Viewer
    with tab_schema:
        st.markdown("#### :material/table: Table Structures")
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

    # TOOL 9: Database Statistics
    with tab_stats:
        st.markdown("#### :material/dashboard: Database Overview")
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

    # TOOL 10: Export Hub & Architecture
    with tab_export:
        st.markdown("#### :material/database: Architecture & Export Hub")
        #st.info("Manage data backups and view live system architecture rules directly from the database engine.", icon=":material/info:")

        t_data, t_er, t_rel, t_chk, t_trg, t_sql = st.tabs([
            ":material/table_view: Data Backup",
            ":material/account_tree: ER Diagram",
            ":material/link: Relations",
            ":material/security: Constraints",
            ":material/bolt: Triggers",
            ":material/code: Schema Export"
        ])

        # ==========================================
        # TAB 1: CSV DATA BACKUP
        # ==========================================
        with t_data:
            st.markdown("##### :material/downloading: Download Table Data (CSV)")
            if table_names:
                export_table = st.selectbox("Select Table to Export", table_names, key="export_tab")
                if st.button(f"Generate CSV for {export_table}", icon=":material/download:"):
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
                                type="primary",
                                icon=":material/save_alt:"
                            )
                        else:
                            st.warning(f"`{export_table}` is empty.", icon=":material/warning:")

        # ==========================================
        # TAB 2: ER DIAGRAMS (DUAL MODE)
        # ==========================================
        with t_er:
            st.markdown("##### :material/schema: Database Visualizations")
            st.info("These diagrams are generated live directly from your PostgreSQL structure.", icon=":material/info:")
            
            # Create sub-tabs so you can keep the original one and view the new one!
            sub_tab_schema, sub_tab_chen = st.tabs([
                "Relational Schema (Tables)", 
                "Traditional ERD (Chen Notation)"
            ])
            
            with sub_tab_schema:
                with st.spinner("Mapping relational schema..."):
                    schema_code = generate_dynamic_er()
                render_mermaid_diagram(schema_code, height=700)
                
                with st.expander("View/Copy Schema Code", icon=":material/code:"):
                    st.code(schema_code, language="mermaid")
                    
            with sub_tab_chen:
                with st.spinner("Drawing traditional ERD..."):
                    erd_code = generate_traditional_er()
                render_mermaid_diagram(erd_code, height=700)
                
                with st.expander("View/Copy Traditional ERD Code", icon=":material/code:"):
                    st.code(erd_code, language="mermaid")

        # ==========================================
        # TAB 3: RELATIONS (FOREIGN KEYS)
        # ==========================================
        with t_rel:
            st.markdown("##### :material/account_tree: Active Foreign Keys (Cascades)")
            st.write("These rules ensure Referential Integrity. If a parent is deleted, children are safely cascaded.")
            fk_query = """
                SELECT
                    tc.table_name AS "Child Table", 
                    kcu.column_name AS "Foreign Key",
                    ccu.table_name AS "Parent Table",
                    ccu.column_name AS "Target Key",
                    rc.delete_rule AS "On Delete"
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name
                JOIN information_schema.referential_constraints AS rc ON tc.constraint_name = rc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY';
            """
            fks = fetch_data(fk_query)
            if fks: st.dataframe(fks, use_container_width=True, hide_index=True)
            else: st.warning("No foreign keys detected.", icon=":material/warning:")

        # ==========================================
        # TAB 4: DOMAIN INTEGRITY (CONSTRAINTS)
        # ==========================================
        with t_chk:
            st.markdown("##### :material/gpp_good: Domain Integrity Constraints")
            st.write("These rules prevent invalid logic (like negative scores) from entering the database.")
            chk_query = """
                SELECT 
                    conrelid::regclass AS "Table Name", 
                    conname AS "Constraint Name", 
                    pg_get_constraintdef(c.oid) AS "Rule Definition"
                FROM pg_constraint c
                WHERE contype IN ('c', 'u') AND connamespace = 'public'::regnamespace;
            """
            chks = fetch_data(chk_query)
            if chks: st.dataframe(chks, use_container_width=True, hide_index=True)
            else: st.warning("No constraints detected.", icon=":material/warning:")

        # ==========================================
        # TAB 5: TRIGGERS (MAGIC FUNCTIONS)
        # ==========================================
        with t_trg:
            st.markdown("##### :material/memory: Active Database Triggers")
            st.write("These 'Magic Functions' automatically execute during INSERTS/UPDATES to sync metadata.")
            trg_query = """
                SELECT 
                    event_object_table AS "Target Table", 
                    trigger_name AS "Trigger Name", 
                    event_manipulation AS "Action Event", 
                    action_statement AS "Function Call"
                FROM information_schema.triggers
                WHERE trigger_schema = 'public';
            """
            trgs = fetch_data(trg_query)
            if trgs: st.dataframe(trgs, use_container_width=True, hide_index=True)
            else: st.warning("No triggers detected.", icon=":material/warning:")

        # ==========================================
        # TAB 6: UPGRADED SCHEMA EXPORT
        # ==========================================
        with t_sql:
            st.markdown("##### :material/description: Download Database Schema (.sql)")
            st.info("This generates a file containing the structure of all tables, plus your professional constraints.", icon=":material/info:")
            
            if st.button("Generate Schema File", type="secondary", icon=":material/code:"):
                with st.spinner("Mapping database structure..."):
                    # Fetch basic columns
                    schema_query = """
                        SELECT table_name, column_name, data_type, is_nullable, column_default
                        FROM information_schema.columns 
                        WHERE table_schema = 'public'
                        ORDER BY table_name, ordinal_position;
                    """
                    all_columns = fetch_data(schema_query)
                    
                    # Fetch advanced constraints to append
                    constraint_query = """
                        SELECT 'ALTER TABLE ' || conrelid::regclass || ' ADD CONSTRAINT ' || conname || ' ' || pg_get_constraintdef(c.oid) || ';' AS def
                        FROM pg_constraint c
                        WHERE connamespace = 'public'::regnamespace;
                    """
                    all_constraints = fetch_data(constraint_query)
                    
                    if all_columns:
                        import time
                        schema_text = "-- ACADEMIC PORTAL DATABASE SCHEMA (V2) --\n"
                        schema_text += f"-- Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')} --\n\n"
                        
                        # Build Tables
                        current_table = ""
                        for col in all_columns:
                            if col['table_name'] != current_table:
                                if current_table != "": schema_text += "\n);\n\n"
                                current_table = col['table_name']
                                schema_text += f"CREATE TABLE {current_table} (\n"
                                schema_text += f"    {col['column_name']} {col['data_type']}"
                            else:
                                schema_text += f",\n    {col['column_name']} {col['data_type']}"
                            
                            if col['is_nullable'] == "NO": schema_text += " NOT NULL"
                            if col['column_default']: schema_text += f" DEFAULT {col['column_default']}"
                        schema_text += "\n);\n\n"
                        
                        # Append Constraints (PKs, FKs, CHECKs)
                        schema_text += "-- SYSTEM CONSTRAINTS & FOREIGN KEYS --\n"
                        if all_constraints:
                            for con in all_constraints:
                                schema_text += f"{con['def']}\n"
                        
                        st.download_button(
                            label="Download full_schema.sql",
                            data=schema_text,
                            file_name="academic_portal_schema.sql",
                            mime="text/sql",
                            type="primary",
                            icon=":material/download:"
                        )
                    else:
                        st.error("Could not retrieve schema information.", icon=":material/error:")

def render_ai_notes():
    """
    Renders the AI Notes view to view generated notes.
    """
    
    # THE CLEVER RENDER CHECKER (UPGRADED)
    @st.cache_data(show_spinner=False, ttl=86400) 
    def verify_mermaid_with_kroki(mermaid_str):
        """Actually pings the Kroki rendering server. ONLY fails if Kroki explicitly rejects the syntax."""
        if not mermaid_str or str(mermaid_str).strip() in ["", "N/A", "None"]:
            return True 
        
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
    
    # TAB 1: MCQ Explanations
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
                st.info("No questions found for the selected filters.", icon=":material/info:")
            else:
                # Workaround: Fetch ALL caches and extract the ID directly from the cache_key string
                # This bypasses the empty question_id column in the database entirely!
                caches = fetch_data("SELECT * FROM mcq_cache")
                cache_map = {}
                for c in caches:
                    if c.get('cache_key'):
                        parts = c['cache_key'].split('_')
                        if len(parts) >= 2 and parts[1].isdigit():
                            q_id = int(parts[1])
                            cache_map[q_id] = c

                broken_qs = []
                healthy_qs = []
                flagged_qs = []

                for i, q in enumerate(questions):
                    if q['id'] in cache_map:
                        c_row = cache_map[q['id']]
                        # Check for flags first!
                        if c_row.get('needs_attention'): 
                            flagged_qs.append((i, q, c_row))
                        elif c_row['is_healthy']: 
                            healthy_qs.append((i, q, c_row))
                        else: 
                            broken_qs.append((i, q, c_row))

                # OPTIMIZATION: Fragmenting AI MCQ rendering prevents whole-page reload on edits/dismissals
                @st.fragment
                def render_aimcq_question(i, q, cache_entry, is_flagged=False):
                    context_tag = f" `[{q['sub_name']} | W{q['w_num']} | {q['activity_name']}]`" if a_sel == "All Activities" else ""
                    
                    icon = ":material/warning:" if is_flagged else ":material/question_answer:"
                    label = f"FLAGGED {context_tag}" if is_flagged else f"{context_tag}"
                    
                    # STRICT FIX: Set expanded to False for all items
                    with st.expander(expanded=False, label=label, icon=icon):
                        if is_flagged:
                            st.error(f"**Admin Note:** {cache_entry.get('attention_note', 'No details provided.')}", icon=":material/error:")
                            
                        st.markdown(f"{q['heading']}")
                        render_content(q['media_type'], q['media_content'])
                        
                        if q.get('q_type') == 'numerical':
                            st.success(f"Correct Answer: {q['correct_answer']}", icon=":material/check_circle:")
                        else:
                            options = fetch_data("SELECT * FROM options WHERE question_id=%s ORDER BY id ASC", (q['id'],))
                            for idx, opt in enumerate(options):
                                status = "correct" if opt['is_correct'] else "incorrect"
                                content = opt['media_content'] if opt['media_content'] else opt['option_text']
                                render_option_card(f"OPTION {idx+1}", content, opt['media_type'], status=status)
                                
                        render_ai_tutor_response(cache_entry['ai_data'], cache_entry['cache_key'], cache_entry.get('created_by_user', 'System'))
                        
                        if is_flagged:
                            if st.button("Dismiss Flag (Without Editing)", key=f"unflag_{cache_entry['cache_key']}"):
                                execute_query("UPDATE mcq_cache SET needs_attention=FALSE, attention_note=NULL WHERE cache_key=%s", (cache_entry['cache_key'],))
                                # CRITICAL FIX: Changed to a full rerun so the list actually updates and removes the dismissed item!
                                st.rerun()

                # Render Flagged Items FIRST at the top!
                if flagged_qs:
                    st.warning(f"**{len(flagged_qs)} Flagged AI Responses (Needs Review)**", icon=":material/warning:")
                    for i, q, cache in flagged_qs:
                        render_aimcq_question(i, q, cache, is_flagged=True)

                if broken_qs:
                    st.error(f"**{len(broken_qs)} Broken Responses**")
                    for i, q, cache in broken_qs:
                        render_aimcq_question(i, q, cache)
                
                if healthy_qs:
                    st.success(f"**{len(healthy_qs)} Healthy Responses**")
                    for i, q, cache in healthy_qs:
                        render_aimcq_question(i, q, cache)
                        
                if not broken_qs and not healthy_qs and not flagged_qs:
                    st.info("No AI Notes have been generated for this selection yet.", icon=":material/info:")

    # TAB 2: Video Lecture Notes
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
                                        
                                        # Auto-resolution Logic: Auto-fetch real title if needed
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
                        # Workaround: Extract the actual JSON from the database row dictionary
                        actual_ai_json = item['ai_data'].get('ai_data', item['ai_data'])
                        
                        if is_response_broken(actual_ai_json):
                            broken_vids.append(item)
                        else:
                            healthy_vids.append(item)

                    # Dynamic rendering function for the expanders
                    # OPTIMIZATION: Fragmenting Video Notes editing
                    @st.fragment
                    def render_aivid_note(item):
                        context_tag = f" `[{item['sub_name']} | W{item['week_number']}]`" if (s_sel_v == "All Subjects" or w_sel_v == "All Weeks") else ""
                        
                        label = f"{item['video_title']}{context_tag}"
                        
                        with st.expander(expanded=False, label=label, icon=":material/smart_display:"):
                            st.video(item['url'])
                            st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)
                            
                            actual_ai_json = item['ai_data'].get('ai_data', item['ai_data'])
                            author = item['ai_data'].get('created_by_user', 'System')
                            
                            render_video_notes(actual_ai_json, item['video_id'], author)

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
                    st.info("No AI notes generated for this selection yet. Go to 'View Videos' to ask the AI Tutor!", icon=":material/info:")
