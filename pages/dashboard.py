import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import plotly.figure_factory as ff
import sqlite3  
import base64   

# ================= 1. PAGE CONFIG =================
st.set_page_config(
    page_title="Superstore Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)

# ================= 2. SECURITY CHECK =================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.info("Please login to access the dashboard.")
    st.switch_page("main.py")
    st.stop()

# ================= 3. DATABASE INITIALIZATION (CRITICAL FIX) =================
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# ================= SIDEBAR PROFILE SECTION =================
with st.sidebar:
    # 1. Check karein ki username session mein hai
    if "username" in st.session_state and st.session_state.username:
        try:
            # Database se image fetch karein
            cursor.execute("SELECT profile_pic FROM users WHERE username = ?", (st.session_state.username,))
            res = cursor.fetchone()
        except Exception as e:
            res = None
        # Circular Profile Pic ke liye CSS (Refined)
        st.markdown("""
            <style>
                .profile-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    margin-bottom: 20px;
                }
                .circular-img {
                    width: 120px;
                    height: 120px;
                    border-radius: 50%;
                    object-fit: cover;
                    border: 3px solid #00d4ff;
                    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
                }
                .user-name {
                    text-align: center;
                    font-size: 20px;
                    font-weight: bold;
                    color: white;
                    margin-top: 10px;
                }
            </style>
        """, unsafe_allow_html=True)

        # Avatar dikhane ka Logic
        if res and res[0]:
            try:
                base64_img = base64.b64encode(res[0]).decode()
                img_html = f'<div class="profile-container"><img src="data:image/png;base64,{base64_img}" class="circular-img"></div>'
            except:
                img_html = f'<div class="profile-container"><img src="https://www.w3schools.com/howto/img_avatar.png" class="circular-img"></div>'
        else:
            img_html = f'<div class="profile-container"><img src="https://www.w3schools.com/howto/img_avatar.png" class="circular-img"></div>'
        
        st.markdown(img_html, unsafe_allow_html=True)
        st.markdown(f'<p class="user-name">Welcome, {st.session_state.username}!</p>', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#00ff00; font-size:14px;'>● Online</p>", unsafe_allow_html=True)
        
        st.markdown("---")

        # Logout Button
        if st.button("Logout", use_container_width=True, type="primary"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun() 
    else:
        st.warning("Please log in.")
        if st.button("Go to Login Page"):
            st.switch_page("main.py")

# ================= 4. LOAD CSS & PAGE CONTENT (Unchanged) =================
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# Ignore warnings
import warnings
warnings.filterwarnings('ignore')

# Dashboard title
st.markdown("""
<h1 style='text-align:center; font-size:55px; font-weight:bold; color:white; margin-bottom:10px;'>
📊 SuperStore Analytics Dashboard
</h1>
""", unsafe_allow_html=True)

# Remove top padding
st.markdown("<style>div.block-container {padding-top: 1rem;}</style>", unsafe_allow_html=True)

# File uploader logic (Same as yours)
fl = st.file_uploader(":file_folder: Upload a file", type=["csv", "txt", "xlsx", "xls"])

if fl is not None:
    filename = fl.name
    st.write("Uploaded File:", filename)
    if filename.endswith(".csv") or filename.endswith(".txt"):
        df = pd.read_csv(fl, encoding="ISO-8859-1")
    elif filename.endswith(".xlsx") or filename.endswith(".xls"):
        df = pd.read_excel(fl)
else:
    # Make sure you have this file in your root folder
    try:
        df = pd.read_csv("Superstore.csv", encoding="ISO-8859-1")
    except:
        st.error("Superstore.csv not found. Please upload a file.")
        st.stop()

# Create columns
col1, col2 = st.columns(2)
df.columns = df.columns.str.strip()
# Find Order Date column automatically
order_date_col = None

for col in df.columns:
    if "order" in col.lower() and "date" in col.lower():
        order_date_col = col
        break

# Check if Order Date column exists
if order_date_col is not None:

    # Convert into datetime
    df[order_date_col] = pd.to_datetime(df[order_date_col],format="mixed",errors="coerce"
)

    # Getting min and max date
    startDate = df[order_date_col].min()
    endDate = df[order_date_col].max()

    # Date input
    with col1:
        date1 = pd.to_datetime(
            st.date_input("Start Date", startDate)
        )

    with col2:
        date2 = pd.to_datetime(
            st.date_input("End Date", endDate)
        )

    # Filter dataframe
    df = df[
        (df[order_date_col] >= date1) &
        (df[order_date_col] <= date2)
    ].copy()

# Sidebar filter
st.sidebar.header("Choose Your Filter:")

# Region Filter
region = st.sidebar.multiselect(
    "Pick Your Region",
    df["Region"].unique()
)

if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]

# State Filter
state = st.sidebar.multiselect(
    "Pick the State",
    df2["State"].unique()
)

if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)]

# City Filter
city = st.sidebar.multiselect(
    "Pick the City",
    df3["City"].unique()
)
# Filter the data based on Region, State and City

if not region and not state and not city:
    filtered_df = df

elif region and not state and not city:
    filtered_df = df[df["Region"].isin(region)]

elif state and not region and not city:
    filtered_df = df[df["State"].isin(state)]

elif city and not region and not state:
    
    filtered_df = df[df["City"].isin(city)]

elif state and city:
    filtered_df = df3[
        df3["State"].isin(state) &
        df3["City"].isin(city)
    ]

elif region and city:
    filtered_df = df3[
        df3["Region"].isin(region) &
        df3["City"].isin(city)
    ]

elif region and state:
    filtered_df = df3[
        df3["Region"].isin(region) &
        df3["State"].isin(state)
    ]

else:
    filtered_df = df3[
        df3["Region"].isin(region) &
        df3["State"].isin(state) &
        df3["City"].isin(city)
    ]

# ================= KPI =================

total_sales = int(filtered_df["Sales"].sum())

total_profit = int(filtered_df["Profit"].sum())

total_orders = filtered_df.shape[0]

k1,k2,k3 = st.columns(3)

k1.metric("Total Sales", f"${total_sales:,}")

k2.metric("Total Profit", f"${total_profit:,}")

k3.metric("Total Orders", total_orders)

# Category wise sales dataframe
category_df = filtered_df.groupby(
    by=["Category"],
    as_index=False
)["Sales"].sum()


# Category Wise Sales Chart
with col1:

    st.subheader("Category Wise Sales")

    fig = px.bar(
        category_df,
        x="Category",
        y="Sales",

        # Show sales value on bars
        text=['${:,.2f}'.format(x) for x in category_df["Sales"]],

        template="plotly_dark"
    )

    # Text position on bars
    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        height=200
    )


# Region Wise Sales Chart
with col2:

    st.subheader("Region Wise Sales")

    fig = px.pie(
        filtered_df,
        values="Sales",
        names="Region",
        hole=0.5
    )

    # Update text position
    fig.update_traces(
        textposition="outside",
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
# Create two columns
cl1, cl2 = st.columns(2)


# =========================
# Category View Data
# =========================
with cl1:

    with st.expander("Category_ViewData"):

        # Show dataframe with color gradient
        st.write(
            category_df.style.background_gradient(cmap="Blues")
        )

        # Convert dataframe to CSV
        csv = category_df.to_csv(index=False).encode('utf-8')

        # Download button
        st.download_button(
            "Download Data",
            data=csv,
            file_name="Category.csv",
            mime="text/csv",
            help='Click here to download the data as a CSV file'
        )


# =========================
# Region View Data
# =========================
with cl2:

    with st.expander("Region_ViewData"):

        # Group region wise sales
        region_df = filtered_df.groupby(
            by="Region",
            as_index=False
        )["Sales"].sum()

        # Display dataframe
        st.write(
            region_df.style.background_gradient(cmap="Oranges")
        )

        # Convert dataframe to CSV
        csv = region_df.to_csv(index=False).encode('utf-8')

        # Download button
        st.download_button(
            "Download Data",
            data=csv,
            file_name="Region.csv",
            mime="text/csv",
            help='Click here to download the data as a CSV file'
        )


# =========================
# Time Series Analysis
# =========================

# Create month-year column
filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")

# Subheader
st.subheader('Time Series Analysis')

# Create line chart dataframe
linechart = pd.DataFrame(
    filtered_df.groupby(
        filtered_df["month_year"].dt.strftime("%Y : %b")
    )["Sales"].sum()
).reset_index()

# Line chart
fig2 = px.line(
    linechart,
    x="month_year",
    y="Sales",
    labels={"Sales": "Amount"},
    height=500,
    width=1000,
    template="plotly_dark"
)

# Display chart
st.plotly_chart(
    fig2,
    use_container_width=True
)


# =========================
# View Time Series Data
# =========================
with st.expander("View Data of TimeSeries"):

    st.write(
        linechart.T.style.background_gradient(cmap="Blues")
    )

    csv = linechart.to_csv(index=False).encode("utf-8")

    st.download_button(
        'Download Data',
        data=csv,
        file_name="TimeSeries.csv",
        mime='text/csv'
    )


# =========================
# TreeMap Chart
# =========================
st.subheader("Hierarchical View of Sales using TreeMap")

fig3 = px.treemap(
    filtered_df,
    path=["Region", "Category", "Sub-Category"],
    values="Sales",
    hover_data=["Sales"],
    color="Sub-Category"
)

# Update chart size
fig3.update_layout(
    width=800,
    height=650
)

# Display chart
st.plotly_chart(
    fig3,
    use_container_width=True
)


# =========================
# Pie Charts
# =========================
chart1, chart2 = st.columns(2)


# Segment Wise Sales
with chart1:

    st.subheader('Segment Wise Sales')

    fig = px.pie(
        filtered_df,
        values="Sales",
        names="Segment",
        template="plotly_dark"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# Category Wise Sales
with chart2:

    st.subheader('Category Wise Sales')

    fig = px.pie(
        filtered_df,
        values="Sales",
        names="Category",
        template="plotly_dark"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================
# Summary Table
# =========================

st.subheader(":point_right: Month Wise Sub-Category Sales Summary")

with st.expander("Summary_Table"):

    # Sample dataframe
    df_sample = df[0:5][
        ["Region", "State", "City",
         "Category", "Sales",
         "Profit", "Quantity"]
    ]

    # Create table
    fig = ff.create_table(
        df_sample,
        colorscale="Cividis"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Subheader
    st.markdown("### Month Wise Sub-Category Table")

    # Create month column
    filtered_df["month"] = filtered_df["Order Date"].dt.month_name()

    # Pivot table
    sub_category_year = pd.pivot_table(
        data=filtered_df,
        values="Sales",
        index=["Sub-Category"],
        columns="month"
    )

    # Display pivot table
    st.write(
        sub_category_year.style.background_gradient(cmap="Blues")
    )

# =========================
# Scatter Plot
# =========================

# Create scatter plot
data1 = px.scatter(
    filtered_df,
    x="Sales",
    y="Profit",
    size="Quantity",
    color="Category",
    hover_data=["Sub-Category"],
    title="Relationship between Sales and Profit using Scatter Plot"
)

# Update layout
data1.update_layout(

    # Chart title
    title=dict(
        text="Relationship between Sales and Profit using Scatter Plot",
        font=dict(size=20)
    ),

    # X-axis settings
    xaxis=dict(
        title="Sales",
        title_font=dict(size=19)
    ),

    # Y-axis settings
    yaxis=dict(
        title="Profit",
        title_font=dict(size=19)
    ),

    template="plotly_dark")

# Display chart
st.plotly_chart(
    data1,
    use_container_width=True
)


# =========================
# View Data Expander
# =========================
with st.expander("View Data"):

    st.write(
        filtered_df.iloc[:500, 1:20:2]
        .style.background_gradient(cmap="Oranges")
    )


# =========================
# Download Original Dataset
# =========================

# Convert dataframe to CSV
csv = df.to_csv(index=False).encode('utf-8')

# Download button
st.download_button(
    'Download Data',
    data=csv,
    file_name="Data.csv",
    mime="text/csv"
)