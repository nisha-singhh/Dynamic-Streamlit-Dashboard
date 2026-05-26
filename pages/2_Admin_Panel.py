import streamlit as st
import sqlite3
import pandas as pd
import base64

# 1. Page Config
st.set_page_config(page_title="Admin Panel", page_icon="🛡️", layout="wide")

# 2. Database Connection
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Helper for current user
current_user = st.session_state.get("username", "User")

# ================= SIDEBAR LOGIC (Refined & Matching) =================
with st.sidebar:
    if "logged_in" in st.session_state and st.session_state.logged_in:
        # Profile Pic Fetch
        cursor.execute("SELECT profile_pic FROM users WHERE username = ?", (current_user,))
        res = cursor.fetchone()
        
        # Circular CSS
        st.markdown("""
            <style>
                .side-img {
                    width: 100px; height: 100px;
                    border-radius: 50%; object-fit: cover;
                    border: 2px solid #ff4b4b; margin-bottom: 10px;
                }
            </style>
        """, unsafe_allow_html=True)

        if res and res[0]:
            img_base64 = base64.b64encode(res[0]).decode()
            st.markdown(f'<img src="data:image/png;base64,{img_base64}" class="side-img">', unsafe_allow_html=True)
        else:
            st.image("https://www.w3schools.com/howto/img_avatar.png", width=100)
            
        st.write(f"Logged in as: **{current_user}**")
        st.caption("🛡️ Admin Access")
        
        if st.button("Logout", type="primary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun() 
    else:
        st.write("Please log in.")

# ================= SECURITY CHECK =================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in to access this page.")
    if st.button("Go to Login"):
        st.switch_page("main.py")
    st.stop()

# Verify Admin Status from DB
cursor.execute("SELECT is_admin FROM users WHERE username = ?", (current_user,))
admin_check = cursor.fetchone()
is_admin = admin_check[0] if admin_check else 0

if not is_admin:
    st.error("⛔ Access Denied: Admin privileges required.")
    st.stop()

# ================= MAIN UI CONTENT =================
st.title("🛡️ Admin Control Center")
st.info("Manage user permissions, roles, and account statuses from this central panel.")
st.markdown("---")

# 3. User Overview Table
st.subheader("👥 All Registered Users")
df_users = pd.read_sql("SELECT username, is_admin FROM users", conn)

# Table Styling
df_users['Role'] = df_users['is_admin'].apply(lambda x: "⭐ Admin" if x == 1 else "👤 User")
df_users['Password Status'] = "🔒 Encrypted/Hidden"
st.dataframe(df_users[['username', 'Password Status', 'Role']], use_container_width=True)

st.markdown("---")

# 4. Management Section (3 Columns Layout)
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🚀 Promote")
    regular_users = df_users[df_users['is_admin'] == 0]['username'].tolist()
    if regular_users:
        user_to_promote = st.selectbox("Grant Admin Status:", regular_users, key="promote_box")
        if st.button("Make Admin", use_container_width=True):
            cursor.execute("UPDATE users SET is_admin = 1 WHERE username = ?", (user_to_promote,))
            conn.commit()
            st.success(f"Done! {user_to_promote} promoted.")
            st.rerun()
    else:
        st.info("No regular users found.")

with col2:
    st.subheader("📉 Demote")
    # Hum 'nisha' (aap) ko demote hone se bacha rahe hain safety ke liye
    admins = df_users[(df_users['is_admin'] == 1) & (df_users['username'] != current_user)]['username'].tolist()
    if admins:
        user_to_demote = st.selectbox("Remove Admin Status:", admins, key="demote_box")
        if st.button("Revoke Access", use_container_width=True):
            cursor.execute("UPDATE users SET is_admin = 0 WHERE username = ?", (user_to_demote,))
            conn.commit()
            st.success(f"{user_to_demote} demoted.")
            st.rerun()
    else:
        st.info("No other admins to demote.")

with col3:
    st.subheader("🗑️ Remove")
    all_users = df_users['username'].tolist()
    user_to_delete = st.selectbox("Permanently Delete User:", all_users, key="delete_box")
    if st.button("Delete Account", type="primary", use_container_width=True):
        if user_to_delete == current_user:
            st.warning("⚠️ Safety Lock: You cannot delete yourself.")
        else:
            cursor.execute("DELETE FROM users WHERE username = ?", (user_to_delete,))
            conn.commit()
            st.success(f"User {user_to_delete} removed.")
            st.rerun()

conn.close()