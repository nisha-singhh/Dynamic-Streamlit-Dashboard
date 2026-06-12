📊 Dynamic Superstore Analytics Dashboard (v2.0)
A full‑stack, multipage business intelligence application built with Streamlit, Plotly, and SQLite.
This dashboard provides secure authentication and real‑time insights into retail sales, profit margins, and regional performance.
It’s designed to be production‑ready yet simple enough for students to learn from and replicate.

🚀 Live Demo
[https://nisha-dynamic-dashboard.streamlit.app/]

✨ Key Features
🛡️ Secure Authentication
Custom Login/Signup using SQLite database.

Google OAuth 2.0 integration for one‑click enterprise login.

Session Persistence with CSRF protection and state‑aware navigation.

Modern glassmorphism login page with personalized greetings.

📈 Advanced Data Visualization
Real‑time KPIs: Total Sales, Profit, Orders.

Treemaps: Region → Category → Sub‑Category breakdown.

Time Series Forecasting: Interactive line charts for sales trends.

Scatter Plots: Sales vs Profit correlation.

Cross‑Filtering: Category‑wise and region‑wise analysis.

🛠️ Interactive Functionality
Dynamic Filters for Region, State, City, and Date ranges.

File Uploads: CSV, XLSX, XLS, TXT (up to 200MB).

Export Options: Download filtered data as CSV.

Multi‑tab Layouts with side navigation toggles.

🛠️ Technology Stack
Component	Technology	Purpose
Frontend	Streamlit v1.35.0	Interactive UI, routing, state handling
Backend	Python	Core logic
Database	SQLite3 / Supabase	User profiles, metadata
Security	google-auth-oauthlib	OAuth tokens, identity verification
Visualization	Plotly v5.22.0	Interactive charts
Data Processing	Pandas, Openpyxl, SciPy	Cleaning, transformations
Styling	Custom CSS	Dark theme, glassmorphism
Deployment	Streamlit Cloud	Continuous deployment via GitHub


📁 Project Structure
Code
├── main.py                # Entry point (Login, Signup, Google OAuth)
├── pages/
│   ├── dashboard.py       # Analytics dashboard
│   ├── User_Profile.py    # User settings
│   └── Admin_Panel.py     # Admin console
├── assets/
│   ├── style.css          # Custom styling
│   └── login_bg.png       # Background asset
├── database.db            # SQLite database
├── Superstore.csv         # Sample dataset
├── requirements.txt       # Dependencies
└── README.md              # Documentation
🔄 Application Workflow
Initiation → App boots via main.py, sets up database and loads CSS.

Authentication → User logs in via credentials or Google OAuth.

Redirection → Successful login routes to dashboard.py.

Data Injection → Uploaded files processed with Pandas.

Visualization → Plotly renders interactive charts with filters applied.

🧩 Development Challenges & Solutions
OAuth Conflicts

Problem: Legacy authenticators caused 403 errors.

Solution: Refactored to use JSON configs via st.secrets, added CSRF validation keys.

Asset Compilation Errors

Problem: Precompiled asset paths broke Plotly imports.

Solution: Reorganized dependency tree, pinned stable versions (streamlit==1.35.0, plotly==5.22.0).

🏃 How to Run Locally
bash
# Clone repository
git clone <your-repository-url>
cd sales-analytics-dashboard

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run main.py
🎯 Why This Project is Great for Students
Teaches real‑world project structure.

Covers authentication, data visualization, and interactivity.

Perfect for adding to your portfolio or resume.

Helps you practice Python + Streamlit + Plotly in one project.