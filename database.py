import psycopg2 # type: ignore
from psycopg2.extras import RealDictCursor # type: ignore
from psycopg2.pool import ThreadedConnectionPool # type: ignore
import streamlit as st # type: ignore

@st.cache_resource(ttl=600)
def get_db_pool():
    db_url = st.secrets.get("DATABASE_URL")
    if not db_url:
        st.error("Missing DATABASE_URL in Streamlit Secrets!")
        return None
        
    try: 
        return ThreadedConnectionPool(1, 20, db_url)
    except Exception as e: 
        st.error(f"Neon Connection Error: {e}")
        return None

def fetch_data(query, params=None):
    pool = get_db_pool()
    if not pool: return []
    
    try:
        conn = pool.getconn()
    except Exception as e:
        st.cache_resource.clear()
        pool = get_db_pool()
        if not pool: return []
        conn = pool.getconn()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()
    except Exception as e:
        if conn and conn.closed == 0:
            try: conn.rollback()
            except: pass
        if isinstance(e, (psycopg2.OperationalError, psycopg2.InterfaceError)):
            try:
                pool.putconn(conn, close=True) 
                conn = pool.getconn()
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(query, params)
                    return cur.fetchall()
            except Exception as retry_e:
                if conn and conn.closed == 0:
                    try: conn.rollback()
                    except: pass
                st.error(f"Retry Fetch Error: {retry_e}")
                return []
        
        st.error(f"Database Fetch Error: {e}")
        return []
    finally:
        if conn:
            try: conn.rollback() # CRITICAL FIX: Clears transaction state before pooling so custom SQL doesn't lock!
            except: pass
            pool.putconn(conn)

def execute_query(query, params=None):
    pool = get_db_pool()
    if not pool: return False
    
    try:
        conn = pool.getconn()
    except Exception as e:
        st.cache_resource.clear()
        pool = get_db_pool()
        if not pool: return False
        conn = pool.getconn()

    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()
        return True
    except Exception as e:
        if conn and conn.closed == 0:
            try: conn.rollback()
            except: pass
        
        if isinstance(e, (psycopg2.OperationalError, psycopg2.InterfaceError)):
            try:
                pool.putconn(conn, close=True)
                conn = pool.getconn()
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    conn.commit()
                return True
            except Exception as retry_e:
                if conn and conn.closed == 0:
                    try: conn.rollback()
                    except: pass
                st.error(f"Retry Execute Error: {retry_e}")
                return False
        
        st.error(f"Database Execute Error: {e}")
        return False
    finally:
        if conn:
            try: conn.rollback() # CRITICAL FIX: Ensure clean slate
            except: pass
            pool.putconn(conn)