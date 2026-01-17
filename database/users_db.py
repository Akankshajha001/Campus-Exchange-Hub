"""
User and Session Database - Simple in-memory user tracking
"""

from typing import Dict, Optional

# Current user session data
current_user: Dict[str, Optional[str]] = {
    'name': None,
    'roll_no': None,
    'email': None,
    'session_id': None
}

# User activity sessions
user_sessions: Dict[str, Dict] = {}

def set_current_user(name: str, roll_no: str, email: str):
    """Set the current user information"""
    current_user['name'] = name
    current_user['roll_no'] = roll_no
    current_user['email'] = email
    current_user['session_id'] = f"{roll_no}_{name.replace(' ', '_')}"
    
    # Track in user sessions
    if current_user['session_id'] not in user_sessions:
        user_sessions[current_user['session_id']] = {
            'name': name,
            'roll_no': roll_no,
            'email': email,
            'items_reported': 0,
            'notes_uploaded': 0,
            'notes_downloaded': 0
        }

def get_current_user() -> Dict:
    """Get current user information"""
    return current_user.copy()

def is_logged_in() -> bool:
    """Check if a user is logged in"""
    return current_user['name'] is not None

def logout():
    """Logout current user"""
    current_user['name'] = None
    current_user['roll_no'] = None
    current_user['email'] = None
    current_user['session_id'] = None

def update_user_activity(activity_type: str):
    """Update user activity count"""
    if current_user['session_id'] and current_user['session_id'] in user_sessions:
        if activity_type == 'item_reported':
            user_sessions[current_user['session_id']]['items_reported'] += 1
        elif activity_type == 'note_uploaded':
            user_sessions[current_user['session_id']]['notes_uploaded'] += 1
        elif activity_type == 'note_downloaded':
            user_sessions[current_user['session_id']]['notes_downloaded'] += 1

def get_all_users() -> Dict:
    """Get all user sessions"""
    return user_sessions.copy()
