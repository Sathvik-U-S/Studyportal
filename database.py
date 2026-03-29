import psycopg2 # type: ignore
from psycopg2.extras import RealDictCursor # type: ignore
import streamlit as st # type: ignore

# ==========================================
# 2. DATABASE & UTILS
# ==========================================

@st.cache_resource(ttl=600)
def get_db_connection():
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
    if not conn: return []
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()
    except Exception as e:
        # THE FIX: Always rollback on an error to prevent the "Transaction Aborted" lockout
        if conn: conn.rollback()
        
        # If it's a dropped connection error, clear cache and retry exactly once
        if isinstance(e, psycopg2.OperationalError):
            st.cache_resource.clear()
            conn = get_db_connection()
            if conn:
                try:
                    with conn.cursor(cursor_factory=RealDictCursor) as cur:
                        cur.execute(query, params)
                        return cur.fetchall()
                except Exception as retry_e:
                    conn.rollback()
                    st.error(f"Retry Fetch Error: {retry_e}")
                    return []
        
        st.error(f"Database Fetch Error: {e}")
        return []

def execute_query(query, params=None):
    conn = get_db_connection()
    if not conn: return False
    
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()
        return True
    except Exception as e:
        # THE FIX: Rollback failed transactions immediately
        if conn: conn.rollback()
        
        if isinstance(e, psycopg2.OperationalError):
            st.cache_resource.clear()
            conn = get_db_connection()
            if conn:
                try:
                    with conn.cursor() as cur:
                        cur.execute(query, params)
                        conn.commit()
                    return True
                except Exception as retry_e:
                    conn.rollback()
                    st.error(f"Retry Execute Error: {retry_e}")
                    return False
        
        st.error(f"Database Execute Error: {e}")
        return False