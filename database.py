import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 2. DATABASE & UTILS
# ==========================================

@st.cache_resource
def get_db_connection():
    # Force it to use the Secret URL
    db_url = st.secrets.get("DATABASE_URL")
    
    if not db_url:
        st.error("Missing DATABASE_URL in Streamlit Secrets!")
        return None
        
    try: 
        return psycopg2.connect(db_url)
    except Exception as e: 
        st.error(f"Neon Connection Error: {e}")
        return None


def fetch_data(query, params=None):
    conn = get_db_connection()
    if conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()
    return []

def execute_query(query, params=None):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()
            return True
        except: return False
    return False