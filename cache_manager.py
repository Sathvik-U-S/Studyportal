import streamlit as st # type: ignore
from database import fetch_data, execute_query
import json

# --- MCQ CACHE FUNCTIONS ---

def get_cached_ai_response(ai_key):
    """Fetches a single specific response from the DB."""
    query = "SELECT ai_data FROM mcq_cache WHERE cache_key = %s"
    result = fetch_data(query, (ai_key,))
    return result[0]['ai_data'] if result else None

def save_ai_cache(ai_key, data):
    """Saves or updates a single response in the DB."""
    query = """
        INSERT INTO mcq_cache (cache_key, ai_data, updated_at)
        VALUES (%s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT (cache_key) 
        DO UPDATE SET ai_data = EXCLUDED.ai_data, updated_at = CURRENT_TIMESTAMP
    """
    # psycopg2 handles dict -> jsonb conversion automatically
    execute_query(query, (ai_key, json.dumps(data)))

# --- VIDEO CACHE FUNCTIONS ---

def get_cached_video_notes(video_id):
    """Fetches a single specific video note from the DB."""
    query = "SELECT ai_data FROM video_cache WHERE video_id = %s"
    result = fetch_data(query, (video_id,))
    return result[0]['ai_data'] if result else None

def save_video_cache(video_id, data):
    """Saves or updates a single video note in the DB."""
    query = """
        INSERT INTO video_cache (video_id, ai_data, updated_at)
        VALUES (%s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT (video_id) 
        DO UPDATE SET ai_data = EXCLUDED.ai_data, updated_at = CURRENT_TIMESTAMP
    """
    execute_query(query, (video_id, json.dumps(data)))

def delete_video_cache(video_id):
    """Removes a specific video from the cache."""
    execute_query("DELETE FROM video_cache WHERE video_id = %s", (video_id,))

def delete_ai_cache(ai_key):
    """Removes a specific MCQ response from the cache."""
    execute_query("DELETE FROM mcq_cache WHERE cache_key = %s", (ai_key,))