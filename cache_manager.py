import streamlit as st # type: ignore
from database import fetch_data, execute_query
import json
import requests # type: ignore
import re
import zlib
import base64

# --- HEALTH CHECK LOGIC (Moved here to run ONCE during save) ---
def verify_mermaid_with_kroki(mermaid_str):
    if not mermaid_str or str(mermaid_str).strip() in ["", "N/A", "None"]: return True 
    raw_mermaid = str(mermaid_str).replace('```mermaid', '').replace('```', '').strip()
    clean_mermaid = raw_mermaid.replace('\xa0', ' ').replace(';', '')
    clean_mermaid = re.sub(r'--\s*".*?"\s*-->', '-->', clean_mermaid)
    clean_mermaid = re.sub(r'--\s*.*?\s*-->', '-->', clean_mermaid)
    
    # Kroki supports a lot, so we just remove double dollar signs and HTML which clash with simple string definitions.
    final_mermaid = clean_mermaid.replace('$$', '').replace('<br>', ' ').replace('<br/>', ' ')
    
    try:
        compressed = zlib.compress(final_mermaid.encode('utf-8'), 9)
        b64_mermaid = base64.urlsafe_b64encode(compressed).decode('utf-8').replace('=', '')
        mermaid_url = f"https://kroki.io/mermaid/svg/{b64_mermaid}"
        res = requests.get(mermaid_url, timeout=4)
        if res.status_code == 400: return False 
        return True 
    except: return True 

def is_response_broken(ai_data):
    if not isinstance(ai_data, dict): return True 
    for val in ai_data.values():
        if isinstance(val, str) and ("API Error" in val or "Error:" in val): return True
    mermaid = ai_data.get("mermaid_diagram")
    if mermaid:
        if not verify_mermaid_with_kroki(mermaid): return True 
    return False

# --- CACHE RETRIEVAL & SAVING ---

def get_cached_ai_response(ai_key):
    """Returns a dict containing data, creator, and health status."""
    # CRITICAL FIX: Added needs_attention and attention_note to the SELECT statement
    query = "SELECT ai_data, created_by_user, is_healthy, needs_attention, attention_note FROM mcq_cache WHERE cache_key = %s"
    result = fetch_data(query, (ai_key,))
    return result[0] if result else None

def save_ai_cache(ai_key, data, username, metadata=None):
    """Saves MCQ notes with full metadata and automatically resolves any active flags."""
    is_healthy = not is_response_broken(data)
    m = metadata if metadata else {}
    query = """
        INSERT INTO mcq_cache (
            cache_key, ai_data, created_by_user, is_healthy, 
            question_id, subject_name, question_heading, week_number, assessment_name, updated_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT (cache_key) 
        DO UPDATE SET 
            ai_data = EXCLUDED.ai_data, 
            is_healthy = EXCLUDED.is_healthy,
            needs_attention = FALSE, 
            attention_note = NULL,
            updated_at = CURRENT_TIMESTAMP
    """
    execute_query(query, (
        ai_key, json.dumps(data), username, is_healthy,
        m.get('q_id'), m.get('sub'), m.get('heading'), m.get('week'), m.get('ass_name')
    ))

def get_cached_video_notes(video_id):
    query = "SELECT ai_data, created_by_user, is_healthy FROM video_cache WHERE video_id = %s"
    result = fetch_data(query, (video_id,))
    return result[0] if result else None

def save_video_cache(video_id, data, username, metadata=None):
    """Saves Video notes with full metadata."""
    is_healthy = not is_response_broken(data)
    m = metadata if metadata else {}
    query = """
        INSERT INTO video_cache (
            video_id, ai_data, created_by_user, is_healthy, 
            subject_name, week_number, youtube_url, updated_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT (video_id) 
        DO UPDATE SET ai_data = EXCLUDED.ai_data, is_healthy = EXCLUDED.is_healthy, updated_at = CURRENT_TIMESTAMP
    """
    execute_query(query, (
        video_id, json.dumps(data), username, is_healthy,
        m.get('sub'), m.get('week'), m.get('url')
    ))
        
def delete_video_cache(video_id):
    execute_query("DELETE FROM video_cache WHERE video_id = %s", (video_id,))

def delete_ai_cache(ai_key):
    execute_query("DELETE FROM mcq_cache WHERE cache_key = %s", (ai_key,))