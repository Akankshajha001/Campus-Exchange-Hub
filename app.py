"""
Campus Exchange Hub - Main Application Entry Point
A Streamlit-based platform for Lost & Found and Notes Exchange

Author: Gaurav Pathak
Description: Campus utility platform using in-memory Python data structures
"""

import streamlit as st
from database.users_db import set_current_user, get_current_user, is_logged_in, logout
from ui.dashboard_ui import render_dashboard
from ui.lost_found_ui import render_lost_found
from ui.notes_ui import render_notes_exchange
from utils.validators import validate_name, validate_email, validate_roll_no

# Page Configuration
st.set_page_config(
    page_title="Campus Exchange Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for attractive UI
def load_custom_css():
    st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Global Styles */
        .stApp {
            font-family: 'Inter', sans-serif;
        }
        
        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Button Styling */
        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
            border: none;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }
        
        /* Input Styling */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            transition: border-color 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #1E88E5;
            box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.1);
        }
        
        /* Sidebar Styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }
        
        [data-testid="stSidebar"] .stMarkdown {
            color: white;
        }
        
        /* Metric Styling */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
        }
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px 10px 0 0;
            padding: 10px 20px;
            font-weight: 600;
        }
        
        /* Card Hover Effect */
        div[style*="box-shadow"]:hover {
            transform: translateY(-5px);
            transition: transform 0.3s ease;
        }
        
        /* Success/Error Messages */
        .stSuccess, .stError, .stWarning, .stInfo {
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* Form Styling */
        .stForm {
            background: #f8f9fa;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.05);
        }
        
        /* Expander Styling */
        .streamlit-expanderHeader {
            border-radius: 10px;
            font-weight: 600;
        }
        
        /* Scrollbar Styling */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
        </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with navigation and user info"""
    with st.sidebar:
        # Logo and Title
        st.markdown("""
            <div style='text-align: center; padding: 1rem 0; color: white;'>
                <h1 style='font-size: 2.5rem; margin: 0;'>🎓</h1>
                <h2 style='margin: 0.5rem 0; font-size: 1.5rem;'>Campus Hub</h2>
                <p style='margin: 0; opacity: 0.8; font-size: 0.9rem;'>Exchange • Connect • Succeed</p>
            </div>
            <hr style='border: 1px solid rgba(255,255,255,0.3); margin: 1rem 0;'>
        """, unsafe_allow_html=True)
        
        # User Login Section
        if not is_logged_in():
            st.markdown("""
                <div style='color: white; padding: 1rem 0;'>
                    <h3 style='margin: 0; font-size: 1.2rem;'>👤 User Login</h3>
                    <p style='margin: 0.5rem 0 0 0; opacity: 0.8; font-size: 0.9rem;'>
                        Sign in to access all features
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("login_form"):
                name = st.text_input("Name", placeholder="Enter your name")
                roll_no = st.text_input("Roll Number", placeholder="e.g., 2021-CS-001")
                email = st.text_input("Email", placeholder="your.email@example.com")
                
                login_btn = st.form_submit_button("🚀 Sign In", width='stretch')
                
                if login_btn:
                    # Validate inputs
                    name_valid, name_error = validate_name(name)
                    roll_valid, roll_error = validate_roll_no(roll_no)
                    email_valid, email_error = validate_email(email)
                    
                    if not name_valid:
                        st.error(name_error)
                    elif not roll_valid:
                        st.error(roll_error)
                    elif not email_valid:
                        st.error(email_error)
                    else:
                        set_current_user(name, roll_no, email)
                        st.success(f"Welcome, {name}! 🎉")
                        st.rerun()
        else:
            # User Info Display
            user = get_current_user()
            st.markdown(f"""
                <div style='background: rgba(255,255,255,0.1); padding: 1rem; 
                            border-radius: 10px; color: white; margin-bottom: 1rem;'>
                    <h3 style='margin: 0; font-size: 1.2rem;'>👤 {user['name']}</h3>
                    <p style='margin: 0.5rem 0 0 0; opacity: 0.8; font-size: 0.9rem;'>
                        Roll: {user['roll_no']}<br>
                        Email: {user['email']}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚪 Logout", width='stretch'):
                logout()
                st.success("Logged out successfully!")
                st.rerun()
        
        st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.3); margin: 1.5rem 0;'>", unsafe_allow_html=True)
        
        # Navigation
        st.markdown("""
            <div style='color: white; padding: 0.5rem 0;'>
                <h3 style='margin: 0; font-size: 1.2rem;'>📍 Navigation</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Initialize page state if not exists
        if 'page' not in st.session_state:
            st.session_state.page = 'dashboard'
        
        # Navigation Buttons with custom styling
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🏠", help="Dashboard", width='stretch'):
                st.session_state.page = 'dashboard'
                st.rerun()
        
        with col2:
            if st.button("🔍", help="Lost & Found", width='stretch'):
                st.session_state.page = 'lost_found'
                st.rerun()
        
        with col3:
            if st.button("📚", help="Notes", width='stretch'):
                st.session_state.page = 'notes'
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Full width navigation buttons
        if st.button("🏠 Dashboard", width='stretch', 
                     type="primary" if st.session_state.page == 'dashboard' else "secondary"):
            st.session_state.page = 'dashboard'
            st.rerun()
        
        if st.button("🔍 Lost & Found", width='stretch',
                     type="primary" if st.session_state.page == 'lost_found' else "secondary"):
            st.session_state.page = 'lost_found'
            st.rerun()
        
        if st.button("📚 Notes Exchange", width='stretch',
                     type="primary" if st.session_state.page == 'notes' else "secondary"):
            st.session_state.page = 'notes'
            st.rerun()
        
        st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.3); margin: 1.5rem 0;'>", unsafe_allow_html=True)
        
        # Quick Stats
        from services.analytics_service import get_lost_found_stats, get_notes_stats
        lf_stats = get_lost_found_stats()
        notes_stats = get_notes_stats()
        
        st.markdown("""
            <div style='color: white; padding: 0.5rem 0;'>
                <h3 style='margin: 0; font-size: 1.2rem;'>📊 Quick Stats</h3>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style='background: rgba(255,255,255,0.1); padding: 1rem; 
                        border-radius: 10px; color: white;'>
                <p style='margin: 0.3rem 0;'>🔍 Lost Items: <strong>{lf_stats['lost_count']}</strong></p>
                <p style='margin: 0.3rem 0;'>✅ Found Items: <strong>{lf_stats['found_count']}</strong></p>
                <p style='margin: 0.3rem 0;'>📚 Total Notes: <strong>{notes_stats['total_notes']}</strong></p>
                <p style='margin: 0.3rem 0;'>📥 Downloads: <strong>{notes_stats['total_downloads']}</strong></p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
            <div style='text-align: center; color: white; opacity: 0.6; 
                        font-size: 0.8rem; padding: 1rem 0;'>
                <p style='margin: 0;'>Campus Exchange Hub v1.0</p>
                <p style='margin: 0;'>Made with ❤️ using Streamlit</p>
                <p style='margin: 0;'>© 2026 - All rights reserved</p>
            </div>
        """, unsafe_allow_html=True)

def main():
    """Main application logic"""
    
    # Load custom CSS
    load_custom_css()
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    # Get current page from session state
    current_page = st.session_state.get('page', 'dashboard')
    
    # Render appropriate page
    if current_page == 'dashboard':
        render_dashboard()
    elif current_page == 'lost_found':
        render_lost_found()
    elif current_page == 'notes':
        render_notes_exchange()
    else:
        # Default to dashboard
        render_dashboard()

if __name__ == "__main__":
    main()
