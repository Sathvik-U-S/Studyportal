import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 2. DATABASE & UTILS
# ==========================================

@st.cache_resource(ttl=600)
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
    if not conn: return []
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()
    except psycopg2.OperationalError:
        # THE FIX: If Neon dropped the connection, clear the cache and try exactly once more!
        st.cache_resource.clear()
        conn = get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                return cur.fetchall()
        except Exception as e:
            st.error(f"Retry Fetch Error: {e}")
            return []
    except Exception as e:
        st.error(f"Fetch Error: {e}")
        return []

def execute_query(query, params=None):
    conn = get_db_connection()
    if not conn: return False
    
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()
        return True
    except psycopg2.OperationalError:
        # THE FIX: If Neon dropped the connection, clear the cache and retry the save!
        st.cache_resource.clear()
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()
            return True
        except Exception as e: 
            st.error(f"Retry Execute Error: {e}")
            return False
    except Exception as e: 
        st.error(f"Execute Error: {e}")
        return False