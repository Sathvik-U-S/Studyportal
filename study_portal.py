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
from cryptography.fernet import Fernet
from student_views import *
from admin_views import *

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

# --- FOOLPROOF JAVASCRIPT: Kills mobile keyboard on dropdowns without breaking clicks ---
components.html(
    """
    <script>
    setInterval(function() {
        const inputs = window.parent.document.querySelectorAll('div[data-baseweb="select"] input');
        inputs.forEach(function(input) {
            // Setting readonly prevents the phone keyboard from ever popping up
            if (!input.hasAttribute('readonly')) {
                input.setAttribute('readonly', 'readonly');
                input.setAttribute('inputmode', 'none');
            }
        });
    }, 500); // Runs in the background to catch newly loaded tabs
    </script>
    """,
    height=0, width=0
)


# Create a fully mutable deep-copy of secrets
def to_dict(obj):
    if hasattr(obj, 'items'):
        return {k: to_dict(v) for k, v in obj.items()}
    return obj

config = to_dict(st.secrets)

# Initialize Authenticator 
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Render the Login Form 
authenticator.login(location='main')

# --- THE STREAMLIT CLOUD "COOKIE LATENCY" HACK ---
# Bypasses the network delay that causes random logouts on refresh
if st.session_state.get("authentication_status") is None:
    if "cloud_cookie_sync" not in st.session_state:
        st.session_state["cloud_cookie_sync"] = True
        import time
        time.sleep(0.3) # Give the browser 300ms to send the cookie over the internet
        st.rerun()

# Handle Login States
if st.session_state.get("authentication_status") is False:
    st.error('Username/password is incorrect', icon=":material/error:")
    st.stop()
    
elif st.session_state.get("authentication_status") is None:
    st.warning('Please enter your username and password', icon=":material/warning:")
    st.stop()
    
elif st.session_state.get("authentication_status"):
    current_username = st.session_state["username"]
    
# Render the Login Form
try:
    authenticator.login()
except Exception as e:
    pass

# Handle Login States
if st.session_state.get("authentication_status") is False:
    st.error('Username/password is incorrect', icon=":material/error:")
    st.stop()
    
elif st.session_state.get("authentication_status") is None:
    st.warning('Please enter your username and password', icon=":material/warning:")
    st.stop()
    
elif st.session_state.get("authentication_status"):
    current_username = st.session_state["username"]
    
    user_config_name = config['credentials']['usernames'][current_username].get('name', 'Sathvik')
    st.session_state["name"] = user_config_name 
    st.session_state["role"] = config['credentials']['usernames'][current_username].get('role', 'user')
    current_user_role = st.session_state["role"]

    # OPTIMIZATION: Pre-fetch and decrypt the user's API keys ONCE per session
    if "user_api_keys" not in st.session_state:
        st.session_state["user_api_keys"] = []
        res = fetch_data("SELECT api_key FROM user_settings WHERE username = %s", (current_username,))
        
        if res and res[0]['api_key']:
            try:
                key = st.secrets.get("ENCRYPTION_KEY")
                f = Fernet(key.encode())
                raw_data = res[0]['api_key']
                
                # 1. BULLETPROOF PARSING: Catches single quotes, malformed JSON, and bare strings
                import ast
                try:
                    saved_keys = json.loads(raw_data)
                except:
                    try:
                        saved_keys = ast.literal_eval(raw_data)
                    except:
                        saved_keys = [raw_data]
                        
                if not isinstance(saved_keys, list):
                    saved_keys = [saved_keys]
                
                # 2. BULLETPROOF DECRYPTION: Rescues old unencrypted keys
                decrypted_keys = []
                for enc_key in saved_keys:
                    if not enc_key or not isinstance(enc_key, str): 
                        continue
                    enc_key = enc_key.strip()
                    try:
                        decrypted_keys.append(f.decrypt(enc_key.encode()).decode())
                    except: 
                        # FALLBACK: If decryption fails, check if it is an old unencrypted API key!
                        if enc_key.startswith("AIza") or enc_key.startswith("gsk_"):
                            decrypted_keys.append(enc_key)
                
                if len(saved_keys) > 0 and len(decrypted_keys) == 0:
                    st.error("CRITICAL ERROR: Keys are saved but cannot be decrypted. Please remove and re-add them in 'My Settings'.", icon=":material/lock_open:")
                else:
                    # STRICT FIX: Purge any empty strings or blank spaces from the list
                    valid_keys = [k for k in decrypted_keys if k and str(k).strip()]
                    st.session_state["user_api_keys"] = valid_keys

            except Exception as e:
                st.error(f"Failed to initialize encryption: {e}", icon=":material/error:")

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
