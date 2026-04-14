import streamlit as st # type: ignore
import json
import ast
import requests # type: ignore
import re
import time
from database import fetch_data, execute_query
from video_ai_tutor import fetch_transcript, extract_youtube_id

# ==========================================
# DATABASE CACHE FUNCTIONS
# ==========================================
def get_cached_video_quiz(video_id):
    query = "SELECT quiz_data, created_by_user FROM video_quizzes WHERE video_id = %s"
    result = fetch_data(query, (video_id,))
    return result[0] if result else None

def get_video_quiz_meta(video_id):
    """Fetches the subject and URL needed to generate MORE questions."""
    query = "SELECT subject_name, youtube_url FROM video_quizzes WHERE video_id = %s"
    result = fetch_data(query, (video_id,))
    return result[0] if result else None

def update_video_quiz_data(video_id, new_quiz_data):
    """Quickly updates the JSON data after an edit, deletion, or addition."""
    query = "UPDATE video_quizzes SET quiz_data = %s, updated_at = CURRENT_TIMESTAMP WHERE video_id = %s"
    execute_query(query, (json.dumps(new_quiz_data), video_id))

def save_video_quiz(video_id, data, meta, username):
    """Saves the quiz with the dynamic username provided from the session."""
    query = """
        INSERT INTO video_quizzes (video_id, quiz_data, subject_name, week_number, topic_title, video_title, youtube_url, created_by_user, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT (video_id) 
        DO UPDATE SET 
            quiz_data = EXCLUDED.quiz_data,
            created_by_user = EXCLUDED.created_by_user,
            updated_at = CURRENT_TIMESTAMP
    """
    execute_query(query, (
        video_id, 
        json.dumps(data), 
        meta.get('subject'), 
        meta.get('week_num'), 
        meta.get('topic'), 
        meta.get('video_title'), 
        meta.get('url'), 
        username 
    ))
    
def delete_video_quiz(video_id):
    execute_query("DELETE FROM video_quizzes WHERE video_id = %s", (video_id,))

# ==========================================
# AI GENERATION LOGIC
# ==========================================
def generate_video_quiz(subject, video_url, api_keys):
    if not api_keys:
        return {"error": "API Error: No personal API keys configured. Please add them in My Settings."}
        
    transcript = fetch_transcript(video_url)
    
    if transcript.startswith("Error"):
        return {"error": transcript}

    sub_l = subject.strip().lower() if subject else ""
    
    SUBJECT_GUIDANCE = {
        "mlf": "Test mathematical intuition, matrix dimensionality, gradient derivations, and probabilistic logic.",
        "mlt": "Test practical algorithm application, loss functions, overfitting/underfitting scenarios, and coding implementations.",
        "mad 2": "Test component lifecycles, API design, asynchronous execution states, and frontend-backend data flow.",
        "dbms": "Test ACID properties, SQL query outcomes, normal forms, and transaction anomalies.",
        "java": "Test JVM memory states, OOP polymorphism rules, threading behavior, and exact console output.",
        "pdsa": "Test algorithmic complexity (Big O), specific data structure edge cases, and recursive stack traces."
    }

    guidance = SUBJECT_GUIDANCE.get(sub_l, "Test deep conceptual understanding and logical application of the core topics.")

    prompt_text = f"""
    You are an elite academic evaluator for the subject: {subject}.
    Analyze this raw video transcript and generate a rigorous, comprehensive quiz testing the core concepts, math, and code discussed.
    Generate AS MANY high-quality questions as possible to thoroughly cover the material. Do not limit yourself.
    
    TRANSCRIPT:
    {transcript}
    
    SUBJECT SPECIFIC FOCUS:
    {guidance}
    
    RULES:
    1. Vary the question types: Use 'mcq' (Multiple Choice), 'numerical' (Math/Exact values), and 'tf' (True/False).
    2. Provide a deep, step-by-step 'explanation' for every single question. Why is the right answer right, and why are the distractors wrong?
    3. Use Markdown formatting deeply in your text and explanations (bolding, `code blocks`).
    4. For numerical questions, the correct_answer MUST be just the number (e.g., "4.5" or "1024").
    """

    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": { 
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "questions": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "q_type": {"type": "STRING", "description": "Must be 'mcq', 'numerical', or 'tf'"},
                                "question_text": {"type": "STRING"},
                                "options": {"type": "ARRAY", "items": {"type": "STRING"}, "description": "Provide 4 options for mcq. Provide ['True', 'False'] for tf. Leave empty for numerical."},
                                "correct_answer": {"type": "STRING", "description": "The exact string of the correct option, or the exact number for numerical."},
                                "explanation": {"type": "STRING", "description": "Detailed markdown explanation of the solution."}
                            },
                            "required": ["q_type", "question_text", "options", "correct_answer", "explanation"]
                        }
                    }
                },
                "required": ["questions"]
            }
        }
    }

    last_error = None
    
    # Grab the selected model from the global state, defaulting to 1.5-pro just in case
    model_name = st.session_state.get('gemini_model', 'gemini-1.5-pro')
    
    for key in api_keys:
        # Inject the dynamic model name into the URL
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key}"
        try:
            response = requests.post(url, json=payload, timeout=180)
            if response.status_code == 200:
                res_json = response.json()
                candidates = res_json.get('candidates', [])
                if not candidates:
                    last_error = "API blocked by safety filters."
                    continue 
                    
                parts = candidates[0].get('content', {}).get('parts', [])
                if parts:
                    raw = parts[0]['text'].strip()
                    clean = re.sub(r'^```json\s*|\s*```$', '', raw, flags=re.MULTILINE)
                    return json.loads(clean, strict=False)
                else:
                    last_error = "Empty response block from AI."
                    continue
            else:
                last_error = f"HTTP {response.status_code}: {response.text}"
                continue
        except Exception as e:
            last_error = f"Network Error: {str(e)}"
            continue
            
    return {"error": f"All API keys exhausted. Last error encountered: {last_error}"}

# ==========================================
# INTERACTIVE UI RENDERER (Top-Down List)
# ==========================================
def render_interactive_quiz(video_id, quiz_data, created_by_user="System"):
    # --- THE ULTIMATE UNPACKER ---
    parsed_data = quiz_data
    
    # 1. Unpack nested strings (handles both JSON and Python string-dicts)
    for _ in range(3):
        if isinstance(parsed_data, str):
            try: 
                parsed_data = json.loads(parsed_data)
            except Exception: 
                try:
                    parsed_data = ast.literal_eval(parsed_data)
                except Exception:
                    break
        else:
            break
            
    # 2. Safety check: Did it get wrapped in an extra dictionary?
    if isinstance(parsed_data, dict) and "quiz_data" in parsed_data and "questions" not in parsed_data:
        parsed_data = parsed_data["quiz_data"]
        for _ in range(2):
            if isinstance(parsed_data, str):
                try: parsed_data = json.loads(parsed_data)
                except: break
            else: break

    if not isinstance(parsed_data, dict):
        st.error(f"Error: Database returned invalid quiz formatting. Data type: {type(parsed_data)}")
        return
        
    if "error" in parsed_data:
        st.error(parsed_data["error"])
        return

    # 1. Fallback for legacy DB rows where the author was NULL
    if not created_by_user:
        created_by_user = "System"
        
    # --- THE FIX: Bulletproof Case-Insensitive Role Checking ---
    current_role = str(st.session_state.get("role", "")).strip().lower()
    current_user = str(st.session_state.get("username", "")).strip().lower()
    author = str(created_by_user).strip().lower()

    is_admin = (current_role == "admin")
    is_author = (current_user == author)
    can_edit = is_admin or is_author

    st.caption(f"Quiz Authored by: **{created_by_user}**")

    questions = parsed_data.get("questions", [])
    
    # 3. Safety check: Is the questions array itself stringified?
    if isinstance(questions, str):
        try: questions = json.loads(questions)
        except: 
            try: questions = ast.literal_eval(questions)
            except: questions = []
            
    if not questions or not isinstance(questions, list):
        st.info("No questions were generated for this video.")
        return

    # Synchronize the variable for the rest of the app's functions
    quiz_data = parsed_data 
    
    st.markdown(f"### Practice Quiz ({len(questions)} Questions)")
    # Loop through all questions and render them vertically
    # Loop through all questions and render them vertically
    for idx, q in enumerate(questions):
        
        # --- STATE MANAGEMENT PER QUESTION ---
        ans_key = f"quiz_ans_{video_id}_{idx}" 
        rev_key = f"quiz_rev_{video_id}_{idx}" 
        edit_key = f"quiz_edit_{video_id}_{idx}" 
        
        # Initialize each question's state independently
        if ans_key not in st.session_state: st.session_state[ans_key] = None
        if rev_key not in st.session_state: st.session_state[rev_key] = False
        if edit_key not in st.session_state: st.session_state[edit_key] = False

        with st.container(border=True):
            # ==========================================
            # EDIT MODE UI (Strictly Admin/Creator Only)
            # ==========================================
            if can_edit and st.session_state[edit_key]:
                st.markdown(f"#### ✏️ Edit Question {idx + 1}")
                
                e_type = st.selectbox("Question Type", ["mcq", "numerical", "tf"], index=["mcq", "numerical", "tf"].index(q['q_type']), key=f"e_type_{video_id}_{idx}")
                e_text = st.text_area("Question Text", value=q['question_text'], key=f"e_text_{video_id}_{idx}", height=100)
                
                e_opts = []
                if e_type == 'mcq':
                    st.markdown("**Options:**")
                    opts = q.get('options', [])
                    for i in range(4):
                        val = opts[i] if i < len(opts) else ""
                        e_opts.append(st.text_input(f"Option {i+1}", value=val, key=f"e_opt_{i}_{video_id}_{idx}"))
                elif e_type == 'tf':
                    e_opts = ["True", "False"]
                    
                st.markdown("**Solution:**")
                e_ans = st.text_input("Correct Answer (Must exactly match an option or a number)", value=q['correct_answer'], key=f"e_ans_{video_id}_{idx}")
                e_exp = st.text_area("Explanation", value=q['explanation'], key=f"e_exp_{video_id}_{idx}", height=150)
                
                c_save, c_cancel = st.columns([1, 5])
                
                if c_save.button("Save Changes", type="primary", key=f"save_{video_id}_{idx}"):
                    q['q_type'] = e_type
                    q['question_text'] = e_text
                    q['options'] = [o for o in e_opts if o.strip()] 
                    q['correct_answer'] = e_ans
                    q['explanation'] = e_exp
                    
                    quiz_data['questions'][idx] = q
                    update_video_quiz_data(video_id, quiz_data)
                    
                    st.session_state[edit_key] = False
                    st.success("Question updated!")
                    st.rerun()
                    
                if c_cancel.button("Cancel", key=f"cancel_{video_id}_{idx}"):
                    st.session_state[edit_key] = False
                    st.rerun()

            # ==========================================
            # NORMAL STUDY UI
            # ==========================================
            else:
                # --- THE FIX: Wider 25% column, and force buttons to fill the container ---
                c_header, c_ctrl = st.columns([0.75, 0.25])
                with c_header:
                    st.markdown(f"**Q{idx + 1}.** {q['question_text']}")
                    st.caption(f"Type: `{q['q_type'].upper()}`")
                    
                if can_edit:    
                    with c_ctrl:
                        ce1, ce2 = st.columns(2)
                        if ce1.button("✏️ Edit", key=f"btn_edit_{video_id}_{idx}", help="Edit Question", use_container_width=True):
                            st.session_state[edit_key] = True
                            st.rerun()
                        if ce2.button("🗑️ Drop", key=f"btn_drop_{video_id}_{idx}", help="Drop Question", use_container_width=True):
                            if len(quiz_data["questions"]) > 1:
                                quiz_data["questions"].pop(idx)
                                update_video_quiz_data(video_id, quiz_data)
                                st.rerun()
                            else:
                                st.error("Cannot drop the last question.")

                is_revealed = st.session_state[rev_key]
                user_choice = st.session_state[ans_key]
                c_input, c_status = st.columns([3, 1])

                with c_input:
                    if q['q_type'] in ['mcq', 'tf']:
                        opts = q.get('options', [])
                        if not opts and q['q_type'] == 'tf': opts = ['True', 'False']
                        
                        selected = st.radio(
                            "Select your answer:", 
                            options=opts, 
                            index=opts.index(user_choice) if user_choice in opts else None,
                            disabled=is_revealed,
                            key=f"rad_{video_id}_{idx}",
                            label_visibility="collapsed"
                        )
                        if selected != user_choice and not is_revealed:
                            st.session_state[ans_key] = selected
                            st.rerun()
                            
                    elif q['q_type'] == 'numerical':
                        typed_val = st.text_input(
                            "Enter numerical value:", 
                            value=user_choice if user_choice else "", 
                            disabled=is_revealed,
                            key=f"num_{video_id}_{idx}"
                        )
                        if typed_val != user_choice and not is_revealed:
                            st.session_state[ans_key] = typed_val

                if st.button("Check Answer", type="primary", disabled=is_revealed or st.session_state[ans_key] is None, key=f"chk_{video_id}_{idx}"):
                    st.session_state[rev_key] = True
                    st.rerun()

                if is_revealed:
                    correct_ans = str(q['correct_answer']).strip().lower()
                    user_ans = str(st.session_state[ans_key]).strip().lower() if st.session_state[ans_key] else ""
                    
                    is_correct = False
                    if q['q_type'] == 'numerical':
                        try:
                            is_correct = abs(float(user_ans) - float(correct_ans)) < 0.01
                        except:
                            is_correct = (user_ans == correct_ans)
                    else:
                        is_correct = (user_ans == correct_ans)

                    with c_status:
                        if is_correct:
                            st.success("✅ Correct!")
                        else:
                            st.error("❌ Incorrect.")
                            
                    st.info(f"**Correct Answer:** {q['correct_answer']}")
                    with st.container(border=True):
                        st.markdown("#### Tutor Explanation")
                        st.markdown(q['explanation'])

    # ==========================================
    # GLOBAL ADMIN / TUTOR CONTROLS
    # ==========================================
    if can_edit:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("##### ⚙️ Global Quiz Controls")
        
        ca1, ca2 = st.columns(2)
        
        with ca1:
            if not st.session_state.get("user_api_keys"):
                st.warning("Add an API key in settings to append questions.", icon=":material/vpn_key:")
            else:
                if st.button("➕ Generate & Add More Questions", width="stretch"):
                    with st.spinner("Analyzing transcript to append more questions..."):
                        meta = get_video_quiz_meta(video_id)
                        if meta:
                            new_quiz = generate_video_quiz(meta['subject_name'], meta['youtube_url'], st.session_state["user_api_keys"])
                            
                            if "error" not in new_quiz:
                                new_count = len(new_quiz['questions'])
                                quiz_data["questions"].extend(new_quiz["questions"])
                                update_video_quiz_data(video_id, quiz_data)
                                st.success(f"Successfully added {new_count} new questions to the bottom!", icon=":material/check_circle:")
                                st.rerun()
                            else:
                                st.error(new_quiz["error"], icon=":material/error:")
                        else:
                            st.error("Could not find video metadata.", icon=":material/error:")
        
        with ca2:
            if st.button("🚨 Delete Entire Quiz", width="stretch", type="primary"):
                delete_video_quiz(video_id)
                st.rerun()

