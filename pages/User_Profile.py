import streamlit as st
import sqlite3
from PIL import Image
import io

# Database connection
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# --- SIDEBAR START (Aapka original logic) ---
with st.sidebar:
    if "username" in st.session_state and st.session_state.username:
        cursor.execute("SELECT profile_pic FROM users WHERE username = ?", (st.session_state.username,))
        res = cursor.fetchone()
        
        if res and res[0]:
            st.image(res[0], width=100)
        else:
            st.image("https://www.w3schools.com/howto/img_avatar.png", width=100)
            
        st.write(f"Logged in as: **{st.session_state.username}**")
        
        if st.button("Logout", type="primary"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun() 
    else:
        st.write("Please log in.")
# --- SIDEBAR END ---

st.title("👤 User Profile")
st.markdown("---") # Ek line separation ke liye

if st.session_state.logged_in:
    user = st.session_state.username
    st.subheader(f"Welcome, {user}!")

    # --- ENHANCED LAYOUT (Columns for better look) ---
    col1, col2 = st.columns([1, 1.5]) # Left mein current photo, Right mein upload

    with col1:
        # --- DISPLAY SECTION (Aapka logic col1 mein) ---
        cursor.execute("SELECT profile_pic FROM users WHERE username = ?", (user,))
        data = cursor.fetchone()
        
        if data and data[0]:
            st.markdown("### Your Current Photo")
            st.image(data[0], width=200) # Thoda bada size preview ke liye
        else:
            st.info("No profile picture uploaded yet.")
            st.image("https://www.w3schools.com/howto/img_avatar.png", width=150)

    with col2:
        # --- UPLOAD SECTION (Aapka logic col2 mein) ---
        st.subheader("Update Your Profile")
        uploaded_file = st.file_uploader("Choose a profile picture", type=['jpg', 'jpeg', 'png'])

        if uploaded_file is not None:
            # Image ko display karein
            img = Image.open(uploaded_file)
            st.image(img, width=150, caption="Preview of New Photo")

            if st.button("Save Profile Picture", use_container_width=True):
                # Image ko binary format mein convert karein
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format=img.format if img.format else "PNG")
                img_blob = img_byte_arr.getvalue()

                # Database mein save karein
                cursor.execute("UPDATE users SET profile_pic = ? WHERE username = ?", (img_blob, user))
                conn.commit()
                st.success("✅ Profile picture updated successfully!")
                st.rerun() # Isse sidebar turant update ho jayega

else:
    st.warning("Please login first.")
    if st.button("Go to Login"):
        st.switch_page("main.py")