import streamlit as st # type: ignore
import os
import requests # type: ignore
import json
import re
import base64
import zlib
import streamlit.components.v1 as components # type: ignore
from cache_manager import save_ai_cache, delete_ai_cache
import mimetypes

def detect_language(code_str):
    """A heuristic text classifier to auto-detect the programming language for syntax highlighting."""
    if not code_str: return "python"
    
    c = code_str.strip()
    c_lower = c.lower()
    
    # HTML
    if re.search(r'^<!doctype html>|<html|<div|<p>|<script', c_lower): return 'html'
    # SQL
    if re.search(r'^\s*(select\s+.*?\s+from|insert\s+into|update\s+.*?\s+set|delete\s+from|create\s+table)', c_lower): return 'sql'
    # Java
    if re.search(r'public\s+class\s+\w+|public\s+static\s+void\s+main|system\.out\.print|import\s+java\.', c_lower): return 'java'
    # C / C++
    if re.search(r'#include\s*<|int\s+main\s*\(|std::cout|printf\(', c_lower): return 'cpp'
    # CSS
    if re.search(r'^[.#a-z0-9\s,\-_]+\s*\{[^}]+\}', c_lower) and ':' in c_lower and ';' in c_lower: return 'css'
    # JSON
    if (c.startswith('{') and c.endswith('}')) or (c.startswith('[') and c.endswith(']')):
        if '"' in c and ':' in c: return 'json'
    # JavaScript / TypeScript / Vue
    if re.search(
        r'console\.log|document\.|const\s+\w+\s*=|let\s+\w+\s*=|var\s+\w+\s*=|'
        r'=>|export\s+const|\w+\s*\([^)]*\)\s*\{|\.push\(|\.map\(|\.filter\(|'
        r'v-(if|else|else-if|for|on|bind|model)\s*[:=]',
        c_lower
    ):
        return 'javascript'
    # Markdown
    if re.search(r'^#+\s+[a-zA-Z]|^\*\*[a-zA-Z]', c): return 'markdown'
    
    # Default fallback to Python
    return 'python'

def render_content(media_type, content):
    if not content or str(content).strip() == "": return
    
    if media_type == 'code':
        # Bulletproof regex split for code blocks
        blocks = re.split(r'\\?u[eE]000', str(content))
        for block in blocks:
            if block.strip():
                lang = detect_language(block)
                st.caption(f"_{lang.upper()}_", text_alignment="right")
                st.code(block.strip(), language=lang, line_numbers=True)
                
    elif media_type == 'image':
        # --- BULLETPROOF MULTIPLE IMAGE SPLIT ---
        # This regex catches 'uE000', 'ue000', '\uE000', '\ue000' and any spacing
        image_filenames = [img.strip() for img in re.split(r'\\?u[eE]000', str(content)) if img.strip()]
        
        for img_name in image_filenames:
            img_path = f"pic/{img_name}" if not img_name.startswith("pic/") else img_name
            if os.path.exists(img_path): 
                st.image(img_path)
            else: 
                st.warning(f"Image not found: {img_path}")
    else: 
        st.markdown(content)

def render_option_card(label, content, media_type, status=None):
    """Renders an option. If a status is provided, it changes color to success or error."""
    if media_type == 'image':
        # --- BULLETPROOF MULTIPLE IMAGE SPLIT ---
        image_filenames = [img.strip() for img in re.split(r'\\?u[eE]000', str(content)) if img.strip()]
        
        if status == 'correct': st.success("Selected Image(s) Correct")
        elif status == 'incorrect': st.error("Selected Image(s) Incorrect")
        
        for img_name in image_filenames:
            img_path = f"pic/{img_name}" if not img_name.startswith("pic/") else img_name
            if os.path.exists(img_path): 
                st.image(img_path)
            else: 
                st.warning(f"Image missing: {img_path}")
                
    elif media_type == 'code':
        blocks = re.split(r'\\?u[eE]000', str(content))
        for block in blocks:
            if block.strip():
                lang = detect_language(block)
                st.caption(f"_{lang.upper()}_", text_alignment="right")
                if status == 'correct': st.success(f"```{lang}\n{block.strip()}\n```")
                elif status == 'incorrect': st.error(f"```{lang}\n{block.strip()}\n```")
                else: st.code(block.strip(), language=lang, line_numbers=True)
    else:
        if status == 'correct': st.success(content)
        elif status == 'incorrect': st.error(content)
        else: st.info(content)

def check_numerical_answer(user_val, correct_key):
    try:
        u = float(user_val)
        if ',' in correct_key:
            l, h = map(float, correct_key.split(','))
            return l <= u <= h
        return abs(u - float(correct_key)) < 0.001
    except: return False

def ask_ai_tutor(subject, question, media_type, media_content, all_options, correct_answer, retry_count=0):
    if "GEMINI_KEYS" in st.secrets:
        api_keys = st.secrets["GEMINI_KEYS"]
    else:
        api_keys = [st.secrets.get("GEMINI_KEY")]
        
    media_context = ""
    image_parts = [] 

    def extract_and_encode_images(image_string):
        raw_media = str(image_string).replace('\\uE000', 'uE000').replace('\ue000', 'uE000')
        filenames = [img.strip() for img in raw_media.split('uE000') if img.strip()]
        for img_name in filenames:
            img_path = f"pic/{img_name}" if not img_name.startswith("pic/") else img_name
            if os.path.exists(img_path):
                import mimetypes
                mime_type, _ = mimetypes.guess_type(img_path)
                if not mime_type: mime_type = "image/png"
                with open(img_path, "rb") as f:
                    encoded_img = base64.b64encode(f.read()).decode('utf-8')
                image_parts.append({
                    "inlineData": {"mimeType": mime_type, "data": encoded_img}
                })

    # 1. Process Question Images
    if media_content:
        if media_type == 'code':
            media_context = f"\nCode Provided:\n```\n{media_content}\n```\n"
        elif media_type == 'text':
            media_context = f"\nContextual Text:\n{media_content}\n"
        elif media_type == 'image':
            media_context = f"\n[Please physically analyze the attached image(s) to answer this question.]\n"
            extract_and_encode_images(media_content)

    # 2. Process Option Images (Extracted via Regex from the tags we added in study_portal.py)
    all_options_str = str(all_options)
    option_images = re.findall(r'\[IMAGE:\s*(.*?)\]', all_options_str)
    for opt_img in option_images:
        extract_and_encode_images(opt_img)

    sub_l = subject.strip().lower() if subject else ""
    SUBJECT_GUIDANCE = {
        "dbms": "Focus on ACID properties, relational algebra, SQL query execution plans, normalization, indexing, joins, and database state transitions.",
        "mad 1": "Simulate execution step-by-step. Track variable scope, control flow, function calls, memory state, and edge cases.",
        "mad 2": "Simulate execution step-by-step. Focus on asynchronous execution, event loop behavior, callbacks, promises, and UI lifecycle.",
        "java": "Trace object creation, OOP principles, inheritance, polymorphism, memory allocation, and runtime execution order.",
        "python": "Trace variable binding, recursion, list/dictionary operations, mutable vs immutable behavior, and execution flow.",
        "pdsa": "Focus on algorithm complexity, recursion trees, data structure state changes, stack/queue behavior, and edge cases.",
        "mlf": "Provide full mathematical derivations using LaTeX delimiters ($ for inline, $$ for block equations). Show matrix operations, probability reasoning, and optimization steps clearly.",
        "mlt": "Provide step-by-step ML algorithm derivations using LaTeX. Explain loss functions, gradients, matrix math, and probabilistic reasoning."
    }

    guidance = SUBJECT_GUIDANCE.get(sub_l, "Break down the core concepts using strict logical reasoning and eliminate incorrect options step-by-step.")

    prompt_text = f"""
    You are a precise, highly analytical academic tutor for the subject: {subject}.
    Question: {question} {media_context}
    Options: {all_options}
    Correct Answer: {correct_answer}
    
    SUBJECT SPECIFIC FOCUS: {guidance}
    
    STRICT FORMATTING & PEDAGOGY RULES:
    1. STRICT MULTIPLE BULLETS: Format EVERY textual section as a bulleted list using `- `. CRITICAL: You MUST insert a newline (`\\n`) before EVERY single bullet point so they render on separate lines. NEVER smash points together. Limit to 1-2 sentences per point.
    2. ARRAY FORMATTING (Core Concepts): For array items, output ONLY the raw text. NEVER prepend with bullets (`- `, `* `).
    3. INLINE STYLING: Apply formatting deeply INSIDE the sentences. Use standard markdown **bold** and *italics*. Use them to highlight crucial keywords.
    4. INLINE COLORS: Use standard Streamlit markdown colors for both text and background. Text color format: `:color[text]`. Background color format: `:color-background[text]`. Supported colors: `red`, `orange`, `yellow`, `green`, `blue`, `violet`, `grey`, `gray`. Example text color: `:orange[crucial concept]`. Example background color: `:blue-background[important definition]`. Use them often to make the explanation more visually engaging and to highlight key insights.
    5. ZERO HTML TAGS: You are strictly forbidden from using any HTML tags (NO <u>, NO <span>, NO <ul>, NO <li>).
    6. CONDITIONAL RELEVANCE: If a section is irrelevant, output EXACTLY "N/A".
    7. EXECUTION TRACE: MUST be a well-formatted Markdown Table (e.g., `| Step | Variable | State |`).
    8. MERMAID BULLETPROOF SYNTAX: You MUST use `graph TD`. 
       - CRITICAL: You are STRICTLY FORBIDDEN from using parentheses `()`, curly braces, single quotes `'`, or brackets `[]` ANYWHERE inside the node labels.
       - NO MATH/CODE SYMBOLS: You cannot use `<`, `>`, `<=`, `>=`, `==`, `!=`, or `$$`. Translate them to plain English (e.g., write "x is greater than y" instead of "x > y").
       - SHAPES: Every single node MUST be formatted as `NodeID["Plain English Text"]`. Do not use any other shape syntax.
       - SUBGRAPHS: Format as `subgraph Title` and close with `end`. DO NOT use curly braces.
    9. JSON SAFETY: Escape internal double quotes with \\". Use \\n for newlines.
    """
    api_parts = [{"text": prompt_text}]
    
    # Send all encoded images (from questions and options) dynamically to Gemini
    if image_parts:
        api_parts.extend(image_parts)
        
    payload = {
        "contents": [{"parts": api_parts}],
        "generationConfig": { 
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "choice_analysis": {"type": "STRING"},
                    "wrong_options_analysis": {"type": "STRING"},
                    "common_mistake_trigger": {"type": "STRING"},
                    "step_by_step": {"type": "STRING"},
                    "code_trace": {"type": "STRING"},
                    "math_steps": {"type": "STRING"},
                    "mermaid_diagram": {"type": "STRING"},
                    "core_concepts": {"type": "ARRAY", "items": {"type": "STRING"}},
                    "practical_relevance": {"type": "STRING"}
                },
                "required": [
                    "choice_analysis", "wrong_options_analysis", 
                    "common_mistake_trigger", "step_by_step", "code_trace", "math_steps", 
                    "mermaid_diagram", "core_concepts", "practical_relevance"
                ]
            }
        }
    }
    
    last_error_code = None

    for key in api_keys:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code == 200:
                res_json = response.json()
                if "candidates" not in res_json or not res_json["candidates"]:
                    return {"choice_analysis": "API Error: Response blocked by safety filters."}
                parts = res_json['candidates'][0].get('content', {}).get('parts', [])
                if not parts:
                     return {"choice_analysis": "API Error: The AI returned an empty block."}

                raw = parts[0]['text'].strip()
                clean = re.sub(r'^```json\s*|\s*```$', '', raw, flags=re.MULTILINE)
                clean = re.sub(r',\s*([\]}])', r'\1', clean) 
                
                return json.loads(clean, strict=False)
                
            elif response.status_code == 429:
                last_error_code = 429
                continue
            else:
                return {"choice_analysis": f"API Error: {response.status_code}. Request failed."}
                
        except Exception as e:
            return {"choice_analysis": f"Request Error: {str(e)}"}
            
    return {"choice_analysis": f"API Error: {last_error_code}. All API keys exhausted."}

def render_ai_tutor_response(data, ai_key):
    """Dynamically renders the structured JSON from the AI Tutor into beautiful UI components."""
    if not isinstance(data, dict):
        clean_text = data.replace('\\n', '\n') if isinstance(data, str) else data
        st.error(f"**Error:**\n\n{clean_text}") 
        return
    with st.expander("View AI Tutor Analysis", expanded=False, icon=":material/model_training:"):
        edit_state_key = f"edit_mode_{ai_key}"
        if edit_state_key not in st.session_state:
            st.session_state[edit_state_key] = False
        #edit mode
        if st.session_state[edit_state_key]:
            st.markdown("### Edit AI Response (Raw JSON)")
            with st.form(key=f"form_{ai_key}"):
                new_ca = st.text_area("Choice Analysis", value=data.get("choice_analysis", ""), height="content")
                new_wo = st.text_area("Wrong Options Analysis", value=data.get("wrong_options_analysis", ""), height="content")
                new_cm = st.text_area("Common Mistake Trigger", value=data.get("common_mistake_trigger", ""), height="content")
                new_sbs = st.text_area("Step-by-Step Reasoning", value=data.get("step_by_step", ""), height="content")
                new_ms = st.text_area("Mathematical Derivation", value=data.get("math_steps", ""), height="content")
                new_ct = st.text_area("Execution Trace", value=data.get("code_trace", ""), height="content")
                new_md = st.text_area("Mermaid Diagram", value=data.get("mermaid_diagram", ""), height="content")

                cc_val = "\n".join(data.get("core_concepts", [])) if isinstance(data.get("core_concepts"), list) else str(data.get("core_concepts", ""))
                new_cc = st.text_area("Core Concepts (One per line)", value=cc_val, height="content")
                new_pr = st.text_area("Practical Relevance", value=data.get("practical_relevance", ""), height="content")

                col_save, col_cancel = st.columns([1, 1])
                save_btn = col_save.form_submit_button("Save Changes", type="primary", width="stretch")
                cancel_btn = col_cancel.form_submit_button("Cancel", width="stretch")
                
                if save_btn:
                    updated_data = {
                        "choice_analysis": new_ca,
                        "wrong_options_analysis": new_wo,
                        "common_mistake_trigger": new_cm,
                        "step_by_step": new_sbs,
                        "math_steps": new_ms,
                        "code_trace": new_ct,
                        "mermaid_diagram": new_md,
                        "core_concepts": [c.strip() for c in new_cc.split("\n") if c.strip()],
                        "practical_relevance": new_pr
                    }
                    
                    save_ai_cache(ai_key, updated_data)
                    st.session_state[edit_state_key] = False
                    st.rerun()
                if cancel_btn:
                    st.session_state[edit_state_key] = False
                    st.rerun()
        else:
            # VIEW MODE (Standard Rendering)
            for key in data:
                if isinstance(data[key], str):
                    data[key] = data[key].replace('\\n', '\n')
                elif isinstance(data[key], list):
                    data[key] = [v.replace('\\n', '\n') if isinstance(v, str) else v for v in data[key]]

            def is_valid(val):
                if not val: return False
                v_str = str(val).strip()
                clean_str = re.sub(r'[^A-Za-z0-9]', '', v_str).upper()
                if clean_str in ["", "NULL", "NONE", "NA", "NOTAPPLICABLE"]: 
                    return False
                return True

            # PYTHON AUTO-CORRECTOR: Fixes smashed bullet points
            def format_bullets(val):
                if not val: return ""
                v_str = str(val).strip()
                # Finds periods/punctuation followed by a hyphen and forces a double line break
                v_str = re.sub(r'([.?!])\s*-\s+', r'\1\n\n- ', v_str)
                return v_str

            
            # 1. Choice Analysis
            ca = format_bullets(data.get("choice_analysis"))
            if is_valid(ca):
                st.markdown("#### Choice Analysis:")
                st.markdown(ca)

            # 2. Wrong Options Analysis
            wo = format_bullets(data.get("wrong_options_analysis"))
            if is_valid(wo):
                st.markdown("#### Wrong Options Analysis:")
                st.markdown(wo)
                
            # 3. Common Mistake Trigger
            cm = format_bullets(data.get("common_mistake_trigger"))
            if is_valid(cm):
                st.markdown("#### Common Mistake Trap:")
                st.markdown(cm)

            # 4. Reasoning & Math
            sbs = format_bullets(data.get("step_by_step"))
            if is_valid(sbs):
                st.markdown("#### Step-by-Step Reasoning")
                st.markdown(sbs)

            ms = str(data.get("math_steps", "")).strip()
            if is_valid(ms):
                st.markdown("#### Mathematical Derivation")
                st.markdown(ms)

            # 5. Execution Trace 
            ct = str(data.get("code_trace", "")).strip()
            if is_valid(ct):
                st.markdown("#### Execution Trace")
                ct = re.sub(r'^```[a-zA-Z]*\n?', '', ct)
                ct = re.sub(r'\n?```$', '', ct)
                st.markdown(ct)

            # 6. Mermaid Flowchart
            # 7. Mermaid Diagrams
            if data.get("mermaid_diagram") and data["mermaid_diagram"] != "N/A":
                st.markdown("#### Visual Architecture")
                # 1. Clean up markdown wrappers
                # 1. Clean up markdown wrappers and invisible characters
                # 1. Clean up markdown wrappers and invisible characters
            # 1. Clean up markdown wrappers and invisible characters
                raw_mermaid = data["mermaid_diagram"].replace('```mermaid', '').replace('```', '').strip()
                clean_mermaid = raw_mermaid.replace('\xa0', ' ').replace(';', '')
                
                # 2. Strip unsupported arrow labels (Kroki/Mermaid fix)
                clean_mermaid = re.sub(r'--\s*".*?"\s*-->', '-->', clean_mermaid)
                clean_mermaid = re.sub(r'--\s*.*?\s*-->', '-->', clean_mermaid)
                
                final_mermaid = clean_mermaid
                
                # --- THE UNIVERSAL MASTER CLEANER ---
                # Remove LaTeX and math backslashes (Crucial for MATHS 2 / MLF)
                # --- THE UNIVERSAL MASTER CLEANER (V3 - MATH FIX) ---
                # Remove LaTeX and math backslashes
                final_mermaid = final_mermaid.replace('$$', '').replace('\\', '')
                
                # Translate dangerous symbols to English
                final_mermaid = final_mermaid.replace('<=', ' less than or equal to ')
                final_mermaid = final_mermaid.replace('>=', ' greater than or equal to ')
                final_mermaid = final_mermaid.replace('!=', ' not equal to ')
                final_mermaid = final_mermaid.replace('==', ' equals ')
                
                # Safe replacement for isolated < and >
                final_mermaid = re.sub(r'(?<=\w)\s*<\s*(?=\w)', ' less than ', final_mermaid)
                final_mermaid = re.sub(r'(?<=\w)\s*>\s*(?=\w)', ' greater than ', final_mermaid)
                
                # Strip single quotes and HTML breaks
                final_mermaid = final_mermaid.replace("'", "").replace('<br>', ' ').replace('<br/>', ' ')

                # 1. THE QUOTE STRIPPER: Runs FIRST to clear out rogue internal quotes.
                # Safely turns A{"Text"} into A{Text} so the Safety Net can process it cleanly.
                final_mermaid = re.sub(r'(?<!\[)"(?!\])', '', final_mermaid)
                
                # 2. THE SAFETY NET: Convert Diamond {}, Round (), and Square [] nodes into ID["Text"]
                # The new lookahead (?=\s*[-=\.%]|\s*$|\s*\n) guarantees it won't aggressively chop internal parentheses like (A*)
                final_mermaid = re.sub(r'([A-Za-z0-9_]+)[\{\(\[]"?([^"]*?)"?[\}\)\]](?=\s*[-=\.%]|\s*$|\s*\n)', r'\1["\2"]', final_mermaid)
                
                # 3. Fix Subgraph syntax
                final_mermaid = re.sub(r"subgraph\s+[\"']?(.*?)[\"']?(?=\n|$)", r"subgraph \1", final_mermaid)

                try:
                    compressed = zlib.compress(final_mermaid.encode('utf-8'), 9)
                    b64_mermaid = base64.urlsafe_b64encode(compressed).decode('utf-8').replace('=', '')
                    mermaid_url = f"https://kroki.io/mermaid/svg/{b64_mermaid}"
                    
                    # --- FULLY DYNAMIC THEME-AWARE COMPONENT ---
                    components.html(
                        f"""
                        <style>
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
                                cursor: grab;
                            }}
                            #wrapper:active {{ cursor: grabbing; }}
                            
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
                                pointer-events: none;
                                transition: filter 0.3s ease;
                            }}
                        </style>
                        
                        <div class="controls">
                            <button type="button" onclick="zoom(1.2)">➕ Zoom In</button>
                            <button type="button" onclick="zoom(0.8)">➖ Zoom Out</button>
                            <button type="button" onclick="resetZoom()">🔄 Reset</button>
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
                                    if (isDark) {{
                                        img.style.filter = 'invert(0.85) hue-rotate(180deg)';
                                    }} else {{
                                        img.style.filter = 'none';
                                    }}
                                }} catch (e) {{
                                    console.log("Theme sync fallback.");
                                }}
                            }}

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

                            // --- Desktop Mouse Events ---
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

                            // --- Mobile Touch Events ---
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
                        """,
                        height=600,
                    )

                    with st.expander("View Diagram Code"):
                        st.code(final_mermaid, language="text")
                except Exception:
                    st.code(final_mermaid, language="text")

            # 7. Summary Info
            col1, col2 = st.columns(2)
            cc = data.get("core_concepts")
            if is_valid(cc):
                with col1:
                    st.markdown("#### Core Concepts")
                    for c in cc:
                        clean_c = re.sub(r'^[\-\*\•\s]+', '', str(c)).strip()
                        st.markdown(f"- {clean_c}")

            pr = format_bullets(data.get("practical_relevance"))
            if is_valid(pr):
                with col2:
                    st.markdown("#### Practical Relevance")
                    st.markdown(pr)

            
            st.divider()
            c_edit, c_del = st.columns(2)

            if c_edit.button("Edit AI Response", key=f"edit_{ai_key}", help="Manually correct or enhance the AI's analysis", width="stretch"):
                st.session_state[edit_state_key] = True
                st.rerun()

            if c_del.button("Delete Cache for this Question", key=f"del_{ai_key}", help="Clear the saved AI response", width="stretch"):
                delete_ai_cache(ai_key)
                st.rerun()
