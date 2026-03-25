import psycopg2 # type: ignore
from psycopg2.extras import RealDictCursor # type: ignore
import streamlit as st # type: ignore
import streamlit.components.v1 as components # type: ignore
# ==========================================
# 2. DATABASE & UTILS
# ==========================================
DB_HOST = "localhost"; DB_NAME = "postgres"; DB_USER = "postgres"; DB_PASS = "123456"

@st.cache_resource
def get_db_connection():
    try: return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    except Exception as e: st.error(f"DB Error: {e}"); return None

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