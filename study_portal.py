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
import streamlit_authenticator as stauth # type: ignore
import yaml # type: ignore
from yaml.loader import SafeLoader # type: ignore
from video_quiz_tutor import *
from cryptography.fernet import Fernet # type: ignore
from student_views import *
from admin_views import *
import urllib.parse

# 1. ESSENTIAL CONFIG & STYLING 
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

# --- FOOLPROOF JAVASCRIPT: Aggressively kills mobile keyboard on ALL dropdowns ---
js_killer = """
    <script>
    function lockDropdowns() {
        const inputs = window.parent.document.querySelectorAll('div[data-baseweb="select"] input');
        inputs.forEach(function(input) {
            // Setting readonly prevents the phone keyboard from ever popping up, but allows clicks!
            if (!input.hasAttribute('readonly')) {
                input.setAttribute('readonly', 'readonly');
                input.setAttribute('inputmode', 'none');
            }
        });
    }

    // 1. Run immediately for dropdowns already on the screen (Subject, Week)
    lockDropdowns();

    // 2. Run aggressively on a loop to catch anything Streamlit renders late
    setInterval(lockDropdowns, 200);

    // 3. Watch for dynamic changes (Activity, Mode)
    const observer = new MutationObserver(lockDropdowns);
    observer.observe(window.parent.document.body, { childList: true, subtree: true });
    </script>
"""
# EXACT REPLACEMENT: Uses iframe with a data URI to bypass deprecation
components.iframe(f"data:text/html;charset=utf-8,{urllib.parse.quote(js_killer)}", height=0, width=0)
# Create a fully mutable deep-copy of secrets
def to_dict(obj):
    if hasattr(obj, 'items'):
        return {k: to_dict(v) for k, v in obj.items()}
    return obj

config = to_dict(st.secrets)

# 1. INITIALIZE AUTHENTICATOR
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# 2. RENDER LOGIN FORM
authenticator.login(location='main')

# --- THE STREAMLIT CLOUD "COOKIE LATENCY" HACK ---
# Bypasses the network delay that causes random logouts on refresh
if st.session_state.get("authentication_status") is None:
    if "cloud_cookie_sync" not in st.session_state:
        st.session_state["cloud_cookie_sync"] = True
        time.sleep(0.3) 
        st.rerun()

# 3. HANDLE LOGIN STATES
if st.session_state.get("authentication_status") is False:
    st.error('Username/password is incorrect', icon=":material/error:")
    st.stop()
    
elif st.session_state.get("authentication_status") is None:
    st.warning('Please enter your username and password', icon=":material/warning:")
    st.stop()
    
elif st.session_state.get("authentication_status"):
    current_username = st.session_state["username"]
    
    # Setup session user info
    user_config_name = config['credentials']['usernames'][current_username].get('name', 'Sathvik')
    st.session_state["name"] = user_config_name 
    st.session_state["role"] = config['credentials']['usernames'][current_username].get('role', 'user')
    current_user_role = st.session_state["role"]

    # ==========================================
    # "CURIOUS" API KEY SYNC & CROSS-ACCOUNT LEAK FIX
    # ==========================================
    # We check if the list is empty OR if the logged-in user changed (Session Leakage Fix)
    if not st.session_state.get("user_api_keys") or st.session_state.get("api_key_owner") != current_username:
        
        # 1. Instantly clear any inherited keys from a previous logout and lock the owner
        st.session_state["user_api_keys"] = []
        st.session_state["api_key_owner"] = current_username
        
        # 2. Fetch the raw encrypted data from the database
        res = fetch_data("SELECT api_key FROM user_settings WHERE username = %s", (current_username,))
        
        if res and res[0]['api_key']:
            try:
                # Initialize the decryptor
                enc_secret = st.secrets.get("ENCRYPTION_KEY")
                f = Fernet(enc_secret.encode())
                raw_db_value = res[0]['api_key']
                
                # Handle JSON vs Python Literals (single quotes)
                import ast
                try:
                    saved_list = json.loads(raw_db_value)
                except (json.JSONDecodeError, TypeError):
                    try:
                        saved_list = ast.literal_eval(raw_db_value)
                    except Exception:
                        saved_list = [raw_db_value]

                if not isinstance(saved_list, list):
                    saved_list = [saved_list]

                # Decryption Mismatch Handshake & Raw Fallback
                decrypted_list = []
                for entry in saved_list:
                    if not entry or not isinstance(entry, str):
                        continue
                    
                    clean_entry = entry.strip()
                    try:
                        decrypted_val = f.decrypt(clean_entry.encode()).decode()
                        decrypted_list.append(decrypted_val)
                    except Exception:
                        # Rescue raw keys if decryption fails
                        if clean_entry.startswith("AIza"):
                            decrypted_list.append(clean_entry)
                
                # Final Cleanup: Purge any remaining empty strings or duplicates
                final_keys = list(dict.fromkeys([k for k in decrypted_list if k and k.strip()]))
                st.session_state["user_api_keys"] = final_keys
                
            except Exception as e:
                print(f"API Sync Error: {e}")

    # SIDEBAR & NAVIGATION
    st.sidebar.markdown(f"## :material/account_circle: Welcome, {st.session_state['name']}")
    st.sidebar.markdown("### :material/menu: Menu")

    nav_options = ["Take Assessment", "Take Test", "View Videos", "My Settings"]

    if current_user_role == "admin":
        nav_options.append("AI Notes")
        nav_options.append("Edit Content")
        nav_options.append("View Database")
        
    app_mode = st.sidebar.radio("Nav", nav_options, label_visibility="collapsed")
    
    if "gemini_model" not in st.session_state:
        st.session_state.gemini_model = "gemini-2.5-flash"

    authenticator.logout('Log Out', 'sidebar')

    # Routing
    if app_mode == "Take Assessment":
        render_take_assessment() # Argument removed
        
    elif app_mode == "Take Test":
        render_take_test()
        
    elif app_mode == "Edit Content":
        render_edit_content()
        
    elif app_mode == "View Database":
        render_view_database()
        
    elif app_mode == "View Videos":
        render_view_videos()
        
    elif app_mode == "AI Notes":
        render_ai_notes()
        
    elif app_mode == "My Settings":
        st.markdown("### :material/settings: My Settings")

        # --- AI MODEL SELECTION (ADMIN ONLY) ---
        if current_user_role == "admin":
            st.markdown("#### :material/smart_toy: AI Model Configuration")
            
            # Initialize widget states so they don't reset when changing tabs
            if "dd_model" not in st.session_state:
                st.session_state.dd_model = "gemini-2.5-flash"
            if "cust_model" not in st.session_state:
                st.session_state.cust_model = ""

            with st.container(border=True):
                c1, c2 = st.columns(2)
                
                with c1:
                    available_models = ["gemini-2.5-flash", "gemini-3.1-pro-preview", "gemini-2.5-pro", "gemini-1.5-pro", "gemini-1.5-flash"]
                    idx = available_models.index(st.session_state.dd_model) if st.session_state.dd_model in available_models else 0
                    selected_dd = st.selectbox("Select Standard Model", available_models, index=idx)
                    
                with c2:
                    typed_cust = st.text_input("Or Type Custom Model", value=st.session_state.cust_model, placeholder="e.g. gemini-exp-123", icon=":material/edit:")

                # Track user interactions
                st.session_state.dd_model = selected_dd
                st.session_state.cust_model = typed_cust

                # Core Override Logic & Visual Indication
                if typed_cust.strip():
                    st.session_state.gemini_model = typed_cust.strip()
                    st.warning(f"**CUSTOM OVERRIDE:** Currently using ` {typed_cust.strip()} ` (Dropdown is disabled)", icon=":material/warning:")
                else:
                    st.session_state.gemini_model = selected_dd
                    st.success(f"**ACTIVE MODEL:** Currently using ` {selected_dd} `", icon=":material/check_circle:")
            

        # --- ENCRYPTED API KEYS ---
        st.markdown("#### :material/vpn_key: Google Gemini API Keys")
        st.info("Your API keys are heavily encrypted. If you add multiple keys, the system will automatically fall back to the next key if one hits a rate limit or fails.", icon=":material/info:")

        def get_fernet():
            key = st.secrets.get("ENCRYPTION_KEY")
            if not key:
                st.error("SYSTEM ERROR: ENCRYPTION_KEY missing from secrets.toml. Contact Administrator.", icon=":material/error:")
                st.stop()
            return Fernet(key.encode())

        current_user = st.session_state["username"]
        res = fetch_data("SELECT api_key FROM user_settings WHERE username = %s", (current_user,))
        
        saved_keys = []
        if res and res[0]['api_key']:
            raw_data = res[0]['api_key']
            try:
                saved_keys = json.loads(raw_data)
                if not isinstance(saved_keys, list):
                    saved_keys = [raw_data] 
            except:
                saved_keys = [raw_data]

        f = get_fernet()

        if saved_keys:
            st.markdown("#### :material/key: Your Active Keys")
            for i, enc_key in enumerate(saved_keys):
                try:
                    dec_key = f.decrypt(enc_key.encode()).decode()
                    masked_key = f"{dec_key[:8]}...{dec_key[-4:]}"
                except:
                    masked_key = "Invalid/Corrupted Key"
                    
                col_key, col_del = st.columns([3, 1])
                with col_key:
                    st.code(f"Key {i+1}: {masked_key}")
                with col_del:
                    if st.button("Remove", key=f"del_key_{i}", use_container_width=True, icon=":material/delete:"):
                        saved_keys.pop(i)
                        new_data = json.dumps(saved_keys) if saved_keys else None
                        
                        if new_data:
                            execute_query("UPDATE user_settings SET api_key = %s WHERE username = %s", (new_data, current_user))
                        else:
                            execute_query("DELETE FROM user_settings WHERE username = %s", (current_user,))
                            
                        st.success(f"Key {i+1} removed!", icon=":material/check_circle:")
                        time.sleep(1)
                        
                        # --- ADD THIS LINE TO RESET THE CACHE ---
                        if "user_api_keys" in st.session_state:
                            del st.session_state["user_api_keys"]
                            
                        st.rerun()
        else:
            st.warning("No API keys saved. You are currently using the shared global pool.", icon=":material/warning:")

        st.markdown("---")
        st.markdown("#### :material/add_box: Add a New Key")
        with st.form("api_key_form", clear_on_submit=True):
            new_key = st.text_input("Enter new Gemini API Key:", type="password", placeholder="AIzaSy...", icon=":material/vpn_key:")
            submitted = st.form_submit_button("Encrypt & Add Key", type="primary", icon=":material/lock:")

            if submitted:
                if new_key.strip():
                    try:
                        encrypted_key = f.encrypt(new_key.strip().encode()).decode()
                        saved_keys.append(encrypted_key)
                        
                        query = """
                            INSERT INTO user_settings (username, api_key)
                            VALUES (%s, %s)
                            ON CONFLICT (username)
                            DO UPDATE SET api_key = EXCLUDED.api_key;
                        """
                        success = execute_query(query, (current_user, json.dumps(saved_keys)))

                        if success:
                            st.success("API Key encrypted and added successfully!", icon=":material/check_circle:")
                            time.sleep(1)
                            
                            # --- ADD THIS LINE TO RESET THE CACHE ---
                            if "user_api_keys" in st.session_state:
                                del st.session_state["user_api_keys"]
                                
                            st.rerun()
                        else:
                            st.error("Failed to save to database. Check database connection.", icon=":material/error:")
                    except Exception as e:
                        st.error(f"Encryption error: {e}", icon=":material/error:")
                else:
                    st.error("Please enter a valid key before saving.", icon=":material/error:")
