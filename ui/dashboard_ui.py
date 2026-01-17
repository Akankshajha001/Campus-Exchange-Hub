"""
Dashboard UI - Home page and analytics dashboard
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from services.analytics_service import (
    get_lost_found_stats,
    get_notes_stats,
    get_category_distribution,
    get_location_distribution,
    get_subject_wise_stats
)
from utils.helpers import format_number

def render_dashboard():
    """Render the main dashboard with statistics and charts"""
    
    # Hero Section
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='color: #1E88E5; font-size: 3rem; margin-bottom: 0.5rem;'>
                🎓 Campus Exchange Hub
            </h1>
            <p style='font-size: 1.2rem; color: #666; margin-bottom: 2rem;'>
                Your One-Stop Platform for Lost Items & Academic Notes
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 2rem; border-radius: 15px; color: white; 
                        box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 1rem;'>
                <h2 style='margin: 0; font-size: 1.8rem;'>🔍 Lost & Found</h2>
                <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>
                    Report lost items or help others find their belongings
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 2rem; border-radius: 15px; color: white; 
                        box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 1rem;'>
                <h2 style='margin: 0; font-size: 1.8rem;'>📚 Notes Exchange</h2>
                <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>
                    Share and access academic notes with your peers
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Statistics Section
    st.markdown("""
        <h2 style='color: #1E88E5; text-align: center; margin: 2rem 0;'>
            📊 Platform Statistics
        </h2>
    """, unsafe_allow_html=True)
    
    # Get statistics
    lf_stats = get_lost_found_stats()
    notes_stats = get_notes_stats()
    
    # Metrics Row 1 - Lost & Found
    st.markdown("### 🔍 Lost & Found Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Items",
            value=lf_stats['total_items'],
            delta=None
        )
    
    with col2:
        st.metric(
            label="Lost Items",
            value=lf_stats['lost_count'],
            delta=None
        )
    
    with col3:
        st.metric(
            label="Found Items",
            value=lf_stats['found_count'],
            delta=None
        )
    
    with col4:
        st.metric(
            label="Success Rate",
            value=f"{lf_stats['match_rate']}%",
            delta=None
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Metrics Row 2 - Notes Exchange
    st.markdown("### 📚 Notes Exchange Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Notes",
            value=notes_stats['total_notes'],
            delta=None
        )
    
    with col2:
        st.metric(
            label="Subjects",
            value=notes_stats['total_subjects'],
            delta=None
        )
    
    with col3:
        st.metric(
            label="Total Downloads",
            value=format_number(notes_stats['total_downloads']),
            delta=None
        )
    
    with col4:
        st.metric(
            label="Contributors",
            value=notes_stats['contributors'],
            delta=None
        )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Charts Section
    st.markdown("""
        <h2 style='color: #1E88E5; text-align: center; margin: 2rem 0;'>
            📈 Visual Analytics
        </h2>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Category Distribution Chart
        category_dist = get_category_distribution()
        if category_dist:
            fig = go.Figure(data=[go.Pie(
                labels=list(category_dist.keys()),
                values=list(category_dist.values()),
                hole=0.4,
                marker=dict(colors=px.colors.qualitative.Set3)
            )])
            fig.update_layout(
                title="Lost & Found Items by Category",
                height=400,
                showlegend=True
            )
            st.plotly_chart(fig, width='stretch')
    
    with col2:
        # Location Distribution Chart
        location_dist = get_location_distribution()
        if location_dist:
            fig = go.Figure(data=[go.Bar(
                x=list(location_dist.values()),
                y=list(location_dist.keys()),
                orientation='h',
                marker=dict(
                    color=list(location_dist.values()),
                    colorscale='Viridis'
                )
            )])
            fig.update_layout(
                title="Items by Location",
                xaxis_title="Count",
                yaxis_title="Location",
                height=400
            )
            st.plotly_chart(fig, width='stretch')
    
    # Subject-wise Notes Chart
    subject_stats = get_subject_wise_stats()
    if subject_stats:
        subjects = list(subject_stats.keys())
        notes_count = [stats['total_notes'] for stats in subject_stats.values()]
        downloads = [stats['total_downloads'] for stats in subject_stats.values()]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Notes Count',
            x=subjects,
            y=notes_count,
            marker_color='#667eea'
        ))
        fig.add_trace(go.Bar(
            name='Downloads',
            x=subjects,
            y=downloads,
            marker_color='#f5576c'
        ))
        
        fig.update_layout(
            title="Subject-wise Notes Statistics",
            xaxis_title="Subject",
            yaxis_title="Count",
            barmode='group',
            height=400
        )
        st.plotly_chart(fig, width='stretch')
    
    # Quick Actions
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <h2 style='color: #1E88E5; text-align: center; margin: 2rem 0;'>
            🚀 Quick Actions
        </h2>
    """, unsafe_allow_html=True)
    
    # Check if user is logged in
    from database.users_db import is_logged_in
    
    if not is_logged_in():
        st.warning("⚠️ Please login from the sidebar to access Lost & Found and Notes Exchange features.")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📢 Report Lost Item", width='stretch', disabled=not is_logged_in()):
            st.session_state.page = 'lost_found'
            st.session_state.lf_action = 'report_lost'
            st.rerun()
    
    with col2:
        if st.button("✅ Report Found Item", width='stretch', disabled=not is_logged_in()):
            st.session_state.page = 'lost_found'
            st.session_state.lf_action = 'report_found'
            st.rerun()
    
    with col3:
        if st.button("📤 Upload Notes", width='stretch', disabled=not is_logged_in()):
            st.session_state.page = 'notes'
            st.session_state.notes_action = 'upload'
            st.rerun()
    
    with col4:
        if st.button("📥 Browse Notes", width='stretch', disabled=not is_logged_in()):
            st.session_state.page = 'notes'
            st.session_state.notes_action = 'browse'
            st.rerun()
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; padding: 2rem; background: #f8f9fa; 
                    border-radius: 10px; margin-top: 2rem;'>
            <p style='color: #666; margin: 0;'>
                💡 <strong>Campus Exchange Hub</strong> - Making campus life easier, one connection at a time
            </p>
            <p style='color: #999; margin: 0.5rem 0 0 0; font-size: 0.9rem;'>
                Built with ❤️ for students, by students
            </p>
        </div>
    """, unsafe_allow_html=True)
