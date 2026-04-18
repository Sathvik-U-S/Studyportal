import requests # type: ignore
import json
import re
from youtube_transcript_api import YouTubeTranscriptApi # type: ignore
from urllib.parse import urlparse, parse_qs
import streamlit as st # type: ignore
import base64
import zlib
import streamlit.components.v1 as components # type: ignore

from cache_manager import save_video_cache, delete_video_cache

def extract_youtube_id(url):
    """Extracts the video ID from various forms of YouTube URLs."""
    parsed_url = urlparse(url)
    if parsed_url.hostname in ('youtu.be', 'www.youtu.be'):
        return parsed_url.path[1:]
    if parsed_url.hostname in ('youtube.com', 'www.youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
    return None

def fetch_transcript(video_url):
    from database import fetch_data, execute_query
    video_id = extract_youtube_id(video_url)
    if not video_id: return "Error: Invalid YouTube URL."
    
    # Check local DB first
    cached = fetch_data("SELECT transcript_text FROM transcripts WHERE video_id = %s", (video_id,))
    if cached: return cached[0]['transcript_text']

    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)
        full_text = " ".join([entry['text'] for entry in transcript.to_raw_data()])
        
        execute_query("INSERT INTO transcripts (video_id, transcript_text) VALUES (%s, %s) ON CONFLICT (video_id) DO NOTHING", (video_id, full_text))
        return full_text
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

def ask_video_ai(subject, video_url, api_keys):
    if not api_keys:
        return {"executive_summary": "API Error: No personal API keys configured. Please add them in My Settings."}
        
    transcript = fetch_transcript(video_url)
    
    if transcript.startswith("Error"):
        return {"executive_summary": transcript}

    sub_l = subject.strip().lower() if subject else ""
    
    # Highly specialized guidance tailored for your core subjects
    SUBJECT_GUIDANCE = {
        "mlf": "Focus heavily on mathematical foundations, statistical theory, linear algebra, and calculus. If the professor skips a derivation step, YOU must fill in the missing mathematical proofs using LaTeX. Visualize matrix dimensional changes.",
        "mlt": "Focus on algorithms in practice, loss function optimization, hyperparameter tuning, and implementation details. Detail the mathematical formula alongside its conceptual Python/NumPy implementation. Highlight common pitfalls like data leakage or overfitting.",
        "mad 2": "Focus on full-stack architecture, API design, asynchronous execution, and component lifecycles (Vue/React). Trace data flow from the frontend, through the backend, to the database using Mermaid sequence diagrams.",
        "dbms": """
        Focus on ACID properties, relational algebra, SQL query execution plans, normalization, indexing, joins, and database state transitions.
        **DBMS SPECIAL INSTRUCTIONS FOR MERMAID DIAGRAMS:**
        - For Indexing or B+ Tree topics, use `graph TD` to draw the tree structure, showing the root, internal nodes, and leaf node pointers.
        - For Concurrency, Deadlock, or Transaction topics, use `sequenceDiagram` to plot T1 and T2 interacting with database variables over time.
        - For Normalization topics, use `graph LR` to draw the Functional Dependency graph (e.g., A --> B) to visually expose dependencies.
        - For Schema or Entity-Relationship topics, use `erDiagram` to map the tables, list Primary/Foreign Keys, and draw relationship cardinality.
        - For SQL or Relational Algebra topics, use `graph BT` (Bottom-Up) to draw the visual Execution Plan tree.
        """,
        "java": "Focus on JVM memory management, OOP architecture, inheritance trees, and multithreading behavior.",
        "pdsa": "Focus on algorithmic time/space complexity, data structure state changes, and recursion trees."
    }

    guidance = SUBJECT_GUIDANCE.get(sub_l, "Extract core concepts, underlying mechanisms, and practical applications.")

    # The upgraded prompt combining your formatting rules with the new video structure
    prompt_text = f"""
    You are an elite, highly analytical academic tutor specializing in {subject}.
    You are analyzing a raw video lecture transcript for an AIML major.
    
    RAW TRANSCRIPT:
    {transcript}
    
    SUBJECT SPECIFIC FOCUS:
    {guidance}
    
    STRICT FORMATTING & PEDAGOGY RULES:
    1. CLEVER POINT-WISE HIERARCHY: For the `choice_analysis`, `wrong_options_analysis`, `common_mistake_trigger`, and `practical_relevance` sections, you MUST use a highly structured, point-wise format. NEVER write thick, blocky paragraphs for these sections. 
       - Use main bullets (`- `) for core ideas.
       - Use indented sub-bullets (2 spaces: `  - `) for supporting details.
       - Use sub-sub-bullets (4 spaces: `    * `) for deep, clever insights.
    2. ARRAY FORMATTING (Core Concepts): For array items, output ONLY the raw text. NEVER prepend with bullets (`- `, `* `).
    3. INLINE STYLING: Apply formatting deeply INSIDE the sentences. Use standard markdown **bold** and *italics*. Use them to highlight crucial keywords.
    4. INLINE COLORS: Use standard Streamlit markdown colors strictly formatted as ` :color[plain text] `. 
       - CRITICAL COLOR RULES: 
         a) There MUST be a space before the colon. 
         b) NEVER place punctuation (commas, periods) inside the brackets. Color only the exact keywords. 
         c) NEVER nest bold or italic markdown inside the color brackets. 
         d) Valid colors: `red`, `orange`, `yellow`, `green`, `blue`, `violet`, `grey`, `gray`.
         e) Example of correct usage: The statement is :green[accurate] because it works.
    5. STEP-BY-STEP HIGHLIGHTING: In the 'step_by_step' section, explicitly label each main step using Streamlit colors and bolding like this: `**:blue[Step 1:]**`, `**:blue[Step 2:]**`. Follow each step with its corresponding logic, using indented sub-bullets for sub-points.
    6. ZERO HTML TAGS: You are strictly forbidden from using any HTML tags (NO <u>, NO <span>, NO <ul>, NO <li>).
    7. CONDITIONAL RELEVANCE: If a section is irrelevant, output EXACTLY "N/A".
    8. EXECUTION TRACE: MUST be a well-formatted Markdown Table (e.g., `| Step | Variable | State |`).
    9. MERMAID BULLETPROOF SYNTAX: You MUST use `graph TD`. 
       - CRITICAL: You are STRICTLY FORBIDDEN from using parentheses `()`, curly braces, single quotes `'`, or brackets `[]` ANYWHERE inside the node labels.
       - NO MATH/CODE SYMBOLS: You cannot use `<`, `>`, `<=`, `>=`, `==`, `!=`, or `$$`. Translate them to plain English (e.g., write "x is greater than y" instead of "x > y").
       - SHAPES: Every single node MUST be formatted as `NodeID["Plain English Text"]`. Do not use any other shape syntax.
       - SUBGRAPHS: Format as `subgraph Title` and close with `end`. DO NOT use curly braces.
    10. JSON FORMAT: Return ONLY valid JSON block. NO markdown wrapper.
    11. LATEX & COLOR SEPARATION: CRITICAL - NEVER use Streamlit color tags (like :blue[text]) near any numerical variables, formulas, or LaTeX. In fact, DO NOT use Streamlit syntax for emphasis at all. Use standard markdown bolding `**text**`. Color tags surrounding `$$` crash the renderer.
    """

    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": { 
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "executive_summary": {"type": "STRING"},
                    "core_concepts_explained": {"type": "STRING"},
                    "missing_context_and_insights": {"type": "STRING"},
                    "mathematical_proofs": {"type": "STRING"},
                    "code_architectures": {"type": "STRING"},
                    "mermaid_diagram": {"type": "STRING"},
                    "interview_prep_questions": {"type": "ARRAY", "items": {"type": "STRING"}},
                    "important_keywords": {"type": "ARRAY", "items": {"type": "STRING"}}
                },
                "required": [
                    "executive_summary", "core_concepts_explained", 
                    "missing_context_and_insights", "mathematical_proofs", 
                    "code_architectures", "mermaid_diagram", 
                    "interview_prep_questions", "important_keywords"
                ]
            }
        }
    }

    last_error_code = "Unknown Error"
    # Strictly enforce gemini-2.5-flash
    model_name = st.session_state.get('gemini_model', 'gemini-2.5-flash')
    
    for key in api_keys:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key.strip()}"
        
        try:
            response = requests.post(url, json=payload, timeout=120) 
            
            # --- 503 High Demand Fix ---
            if response.status_code == 503:
                import time
                time.sleep(2) # Wait 2 seconds and retry automatically
                response = requests.post(url, json=payload, timeout=120)

            if response.status_code == 200:
                res_json = response.json()
                if "candidates" not in res_json or not res_json["candidates"]:
                    last_error_code = "Response blocked by safety filters."
                    continue
                
                parts = res_json['candidates'][0].get('content', {}).get('parts', [])
                if not parts:
                     last_error_code = "The AI returned an empty block."
                     continue

                raw = parts[0]['text'].strip()
                clean = re.sub(r'^```json\s*|\s*```$', '', raw, flags=re.MULTILINE)
                clean = re.sub(r',\s*([\]}])', r'\1', clean) 
                
                return json.loads(clean, strict=False)
                
            else:
                last_error_code = f"HTTP {response.status_code}: {response.text}"
                continue 
                
        except Exception as e:
            last_error_code = f"Request Error: {str(e)}"
            continue 
            
    return {"executive_summary": f"API Error: All API keys exhausted. Last error: {last_error_code}"}
    

def render_video_notes(data, video_id, created_by_user="System"):
    import json
    import ast
    
    parsed_data = data
    for _ in range(3):
        if isinstance(parsed_data, str):
            try: parsed_data = json.loads(parsed_data)
            except Exception: 
                try: parsed_data = ast.literal_eval(parsed_data)
                except Exception: break
        else: break
            
    if isinstance(parsed_data, dict) and "ai_data" in parsed_data:
        parsed_data = parsed_data["ai_data"]
        for _ in range(2):
            if isinstance(parsed_data, str):
                try: parsed_data = json.loads(parsed_data)
                except: break
            else: break
            
    if not isinstance(parsed_data, dict):
        st.error(f"**Error parsing AI response from Database:**\n\n{parsed_data}")
        return
        
    data = parsed_data
    
    # 1. Fallback for legacy DB rows where the author was NULL
    if not created_by_user:
        created_by_user = "System"
        
    current_role = str(st.session_state.get("role", "")).strip().lower()
    current_user = str(st.session_state.get("username", "")).strip().lower()
    author = str(created_by_user).strip().lower()

    is_admin = (current_role == "admin")
    is_author = (current_user == author)
    can_edit = is_admin or is_author

    st.caption(f"Generated by: **{created_by_user}**")
    # --- SETUP STATE KEY ---
    edit_state_key = f"edit_mode_vid_{video_id}"
    if edit_state_key not in st.session_state:
        st.session_state[edit_state_key] = False
    
    # ==========================================
    # EDIT MODE
    # ==========================================
    if st.session_state[edit_state_key]:
        st.markdown("#### Edit AI Video Notes")
        with st.form(key=f"form_vid_{video_id}"):
            new_es = st.text_area("Executive Summary", value=data.get("executive_summary", ""), height="content")
            new_cce = st.text_area("Core Concepts Explained", value=data.get("core_concepts_explained", ""), height="content")
            new_mc = st.text_area("Missing Context & Insights", value=data.get("missing_context_and_insights", ""), height="content")
            new_mp = st.text_area("Mathematical Proofs", value=data.get("mathematical_proofs", ""), height="content")
            new_ca = st.text_area("Code Architectures", value=data.get("code_architectures", ""), height="content")
            new_md = st.text_area("Mermaid Diagram", value=data.get("mermaid_diagram", ""), height="content")

            # Handle Arrays
            iq_val = "\n".join(data.get("interview_prep_questions", [])) if isinstance(data.get("interview_prep_questions"), list) else str(data.get("interview_prep_questions", ""))
            new_iq = st.text_area("Interview Prep Questions (One per line)", value=iq_val, height="content")

            kw_val = "\n".join(data.get("important_keywords", [])) if isinstance(data.get("important_keywords"), list) else str(data.get("important_keywords", ""))
            new_kw = st.text_area("Important Keywords (One per line)", value=kw_val, height="content")

            col_save, col_cancel = st.columns([1, 1])
            save_btn = col_save.form_submit_button("Save Changes", type="primary", width="stretch")
            cancel_btn = col_cancel.form_submit_button("Cancel", width="stretch")
            
            if save_btn:
                updated_data = {
                    "executive_summary": new_es,
                    "core_concepts_explained": new_cce,
                    "missing_context_and_insights": new_mc,
                    "mathematical_proofs": new_mp,
                    "code_architectures": new_ca,
                    "mermaid_diagram": new_md,
                    "interview_prep_questions": [q.strip() for q in new_iq.split("\n") if q.strip()],
                    "important_keywords": [k.strip() for k in new_kw.split("\n") if k.strip()]
                }
                # Save to the VIDEO cache, not the MCQ cache!
                save_video_cache(video_id, updated_data, st.session_state.get("username", "System"))
                
                st.session_state[edit_state_key] = False
                st.rerun()
                
            if cancel_btn:
                st.session_state[edit_state_key] = False
                st.rerun()

    # ==========================================
    # VIEW MODE (Standard Rendering)
    # ==========================================
    else:
        # Sanitize newlines from raw JSON strings
        for key in data:
            if isinstance(data[key], str):
                data[key] = data[key].replace('\\n', '\n')
            elif isinstance(data[key], list):
                data[key] = [v.replace('\\n', '\n') if isinstance(v, str) else v for v in data[key]]            
        st.markdown("#### Deep-Dive Lecture Notes")

        # 1. Executive Summary
        if data.get("executive_summary") and data["executive_summary"] != "N/A":
            st.markdown("#### Executive Summary")
            st.markdown(f"{data['executive_summary']}")

        # 2. Keywords
        if data.get("important_keywords"):
            kws = [f"`{k}`" for k in data["important_keywords"] if str(k).strip() != "N/A"]
            if kws:
                st.markdown(f"**Keywords:** {' • '.join(kws)}")

        # 3. Core Concepts
        if data.get("core_concepts_explained") and data["core_concepts_explained"] != "N/A":
            st.markdown("#### Core Concepts Explained")
            st.markdown(data["core_concepts_explained"])

        # 4. Missing Context (The Elite Tutor feature)
        if data.get("missing_context_and_insights") and data["missing_context_and_insights"] != "N/A":
            st.markdown("#### Tutor's Missing Context & Insights:")
            st.markdown(f"{data['missing_context_and_insights']}")

        # 5. Math Proofs
        if data.get("mathematical_proofs") and data["mathematical_proofs"] != "N/A":
                st.markdown("#### Mathematical Proofs")
                st.markdown(data["mathematical_proofs"])
                
        # 6. Code Architecture
        if data.get("code_architectures") and data["code_architectures"] != "N/A":
                st.markdown("#### Code & Architecture")
                st.markdown(data["code_architectures"])

        # 7. Mermaid Diagrams
        if data.get("mermaid_diagram") and data["mermaid_diagram"] != "N/A":
            st.markdown("#### Visual Architecture")
            
            raw_mermaid = data["mermaid_diagram"].replace('```mermaid', '').replace('```', '').strip()
            clean_mermaid = raw_mermaid.replace('\xa0', ' ').replace(';', '')
            
            # 1. Universal Cleaner
            final_mermaid = clean_mermaid.replace('$$', '').replace('\\', '')
            
            # 2. STRICT FLOWCHART CLEANER (Protects ER & Sequence Diagrams)
            if final_mermaid.strip().startswith("graph ") or final_mermaid.strip().startswith("flowchart "):
                # Strip unsupported arrow labels
                final_mermaid = re.sub(r'--\s*".*?"\s*-->', '-->', final_mermaid)
                final_mermaid = re.sub(r'--\s*.*?\s*-->', '-->', final_mermaid)
                
                # Translate dangerous symbols
                final_mermaid = final_mermaid.replace('<=', ' less than or equal to ')
                final_mermaid = final_mermaid.replace('>=', ' greater than or equal to ')
                final_mermaid = final_mermaid.replace('!=', ' not equal to ')
                final_mermaid = final_mermaid.replace('==', ' equals ')
                final_mermaid = re.sub(r'(?<=\w)\s*<\s*(?=\w)', ' less than ', final_mermaid)
                final_mermaid = re.sub(r'(?<=\w)\s*>\s*(?=\w)', ' greater than ', final_mermaid)
                
                # Strip quotes and HTML breaks
                final_mermaid = final_mermaid.replace("'", "").replace('<br>', ' ').replace('<br/>', ' ')
                final_mermaid = re.sub(r'(?<!\[)"(?!\])', '', final_mermaid)
                
                # Safety Net for node shapes
                final_mermaid = re.sub(r'([A-Za-z0-9_]+)[\{\(\[]"?([^"]*?)"?[\}\)\]](?=\s*[-=\.%]|\s*$|\s*\n)', r'\1["\2"]', final_mermaid)
                # Safety Net for Subgraphs: Forcefully strips parentheses and brackets that crash the parser
                final_mermaid = re.sub(r"subgraph\s+[\"']?(.*?)[\"']?(?=\n|$)", lambda m: "subgraph " + re.sub(r'[()[\]{}]', '', m.group(1)), final_mermaid)

            try:
                compressed = zlib.compress(final_mermaid.encode('utf-8'), 9)
                b64_mermaid = base64.urlsafe_b64encode(compressed).decode('utf-8').replace('=', '')
                mermaid_url = f"https://kroki.io/mermaid/svg/{b64_mermaid}"
                
                # ... [Keep your existing components.html rendering logic exactly as it is] ...

                # --- FULLY DYNAMIC THEME-AWARE COMPONENT ---
                components.html(
                    f"""
                    <style>
                        /* Fallback default variables */
                        :root {{
                            --text-color: #31333F;
                            --bg-color: transparent;
                            --border-color: rgba(49, 51, 63, 0.2);
                            --btn-bg: rgba(49, 51, 63, 0.05);
                            --btn-hover: rgba(49, 51, 63, 0.1);
                            --container-bg: rgba(255, 255, 255, 0.5);
                        }}
                        body {{
                            margin: 0;
                            background-color: var(--bg-color);
                            color: var(--text-color);
                            font-family: sans-serif;
                        }}
                        .controls {{
                            position: sticky; 
                            top: 0; 
                            z-index: 100; 
                            display: flex; 
                            gap: 8px; 
                            background-color: transparent; 
                            padding-bottom: 10px;
                        }}
                        button {{
                            padding: 6px 12px; 
                            cursor: pointer; 
                            border-radius: 6px; 
                            border: 1px solid var(--border-color); 
                            background: var(--btn-bg); 
                            color: var(--text-color); 
                            font-weight: bold;
                            transition: background 0.2s;
                        }}
                        button:hover {{ background: var(--btn-hover); }}
                        
                        #wrapper {{
                            width: 100%; 
                            height: 500px; 
                            overflow: auto; 
                            border: 1px solid var(--border-color); 
                            border-radius: 8px; 
                            background: var(--container-bg);
                            cursor: grab; /* Shows the open hand icon */
                        }}
                        #wrapper:active {{ cursor: grabbing; /* Shows the closed hand icon */ }}
                        
                        /* Custom Scrollbars tied to dynamic variables */
                        #wrapper::-webkit-scrollbar {{ width: 10px; height: 10px; }}
                        #wrapper::-webkit-scrollbar-track {{ background: transparent; }}
                        #wrapper::-webkit-scrollbar-thumb {{
                            background-color: var(--border-color);
                            border-radius: 8px;
                        }}
                        #wrapper::-webkit-scrollbar-thumb:hover {{ background-color: var(--text-color); }}
                        
                        #container {{
                            transform-origin: 0 0; 
                            transition: transform 0.1s ease-out; 
                            display: inline-block; 
                            min-width: 100%;
                            user-select: none;
                        }}
                        #mermaid-img {{
                            display: block; 
                            width: 100%;
                            pointer-events: none; /* Stops the browser from "dragging" the raw image file */
                            transition: filter 0.3s ease; /* Smooth transition for dark mode inversion */
                        }}
                    </style>
                    
                    <div class="controls">
                        <button type="button" onclick="zoom(1.2)">Zoom In</button>
                        <button type="button" onclick="zoom(0.8)">Zoom Out</button>
                        <button type="button" onclick="resetZoom()">Reset</button>
                        <span id="zoom-level" style="margin-left: 10px; align-self: center; font-weight: 500;">100%</span>
                    </div>
                    
                    <div id="wrapper">
                        <div id="container">
                            <img id="mermaid-img" src="{mermaid_url}">
                        </div>
                    </div>

                    <script>
                        // --- DYNAMIC STREAMLIT THEME SYNC ---
                        function syncTheme() {{
                            try {{
                                // Read Streamlit's root styles directly from the parent browser window
                                const parentStyle = window.parent.getComputedStyle(window.parent.document.querySelector('.stApp') || window.parent.document.body);
                                const bgColor = parentStyle.backgroundColor;
                                const textColor = parentStyle.color;
                                
                                // Determine if Streamlit is currently in Dark Mode by checking background brightness
                                const rgb = bgColor.match(/\\d+/g);
                                let isDark = false;
                                if (rgb && rgb.length >= 3) {{
                                    const brightness = (parseInt(rgb[0]) * 299 + parseInt(rgb[1]) * 587 + parseInt(rgb[2]) * 114) / 1000;
                                    isDark = brightness < 128;
                                }}

                                // Update CSS Variables dynamically to match Streamlit exactly
                                document.documentElement.style.setProperty('--text-color', textColor);
                                
                                // Generate intelligent semi-transparent colors based on the text color
                                const textRgba = textColor.replace('rgb', 'rgba').replace(')', ', 0.2)');
                                const btnBg = textColor.replace('rgb', 'rgba').replace(')', ', 0.05)');
                                const btnHover = textColor.replace('rgb', 'rgba').replace(')', ', 0.1)');
                                const containerBg = isDark ? 'rgba(0, 0, 0, 0.2)' : 'rgba(255, 255, 255, 0.5)';

                                document.documentElement.style.setProperty('--border-color', textRgba);
                                document.documentElement.style.setProperty('--btn-bg', btnBg);
                                document.documentElement.style.setProperty('--btn-hover', btnHover);
                                document.documentElement.style.setProperty('--container-bg', containerBg);

                                // THE MAGIC TRICK: If Streamlit is in dark mode, invert the Light Mermaid SVG!
                                const img = document.getElementById('mermaid-img');
                                if (isDark) {{
                                    // Invert colors and rotate hues back to keep specific node colors mostly intact
                                    img.style.filter = 'invert(0.85) hue-rotate(180deg)';
                                }} else {{
                                    img.style.filter = 'none';
                                }}

                            }} catch (e) {{
                                console.log("Theme sync blocked by CORS or unavailable. Using fallback.");
                            }}
                        }}

                        // Sync instantly, and then check every second in case the user changes themes in the Streamlit menu
                        syncTheme();
                        setInterval(syncTheme, 1000);

                        // --- Zoom & Pan Logic ---
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

                        // --- Click and Drag to Pan ---
                        let isDown = false;
                        let startX;
                        let startY;
                        let scrollLeft;
                        let scrollTop;

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
                            wrapper.scrollLeft = scrollLeft - (x - startX) * 1.5; // Multiply by 1.5 for faster dragging
                            wrapper.scrollTop = scrollTop - (y - startY) * 1.5;
                        }});
                    </script>
                    """,
                    height=550,
                )
                with st.expander("View Diagram Code"):
                    st.code(final_mermaid, language="text")
            except Exception:
                st.code(final_mermaid, language="text")
        # 8. Interview Prep
        if data.get("interview_prep_questions") and data["interview_prep_questions"] != "N/A":
            st.markdown("#### Interview Prep Questions")
            for q in data["interview_prep_questions"]:
                if str(q).strip() != "N/A":
                    st.markdown(f"- {q}")
# --- CONTROL BUTTONS (At the very bottom) ---
        if can_edit:
            c_edit, c_del = st.columns(2)
            if c_edit.button("Edit Notes", key=f"edit_btn_{video_id}", width="stretch"):
                st.session_state[edit_state_key] = True
                st.rerun()
                
            if c_del.button("Delete Notes Cache", key=f"del_vid_{video_id}", help="Force the AI to regenerate these notes", width="stretch"):
                delete_video_cache(video_id)
                st.rerun()
