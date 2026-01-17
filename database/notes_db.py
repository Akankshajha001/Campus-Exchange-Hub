"""
Notes Exchange Database - In-memory storage using dictionaries and lists
"""

from datetime import datetime
from typing import Dict, List

# Main data structure: Dictionary of lists
# Key = Subject name
# Value = List of notes metadata
notes_data: Dict[str, List[Dict]] = {
    'Data Structures': [
        {
            'id': 1,
            'subject': 'Data Structures',
            'topic': 'Arrays and Linked Lists',
            'semester': 'Semester 3',
            'uploaded_by': 'Ankit Verma',
            'file_name': 'DS_Arrays_LinkedLists.pdf',
            'description': 'Comprehensive notes on arrays and linked lists with examples',
            'upload_date': '2026-01-05',
            'downloads': 45,
            'rating': 4.5
        },
        {
            'id': 2,
            'subject': 'Data Structures',
            'topic': 'Trees and Graphs',
            'semester': 'Semester 3',
            'uploaded_by': 'Priya Gupta',
            'file_name': 'DS_Trees_Graphs.pdf',
            'description': 'Detailed explanation of tree and graph algorithms',
            'upload_date': '2026-01-07',
            'downloads': 32,
            'rating': 4.8
        }
    ],
    'Database Management': [
        {
            'id': 3,
            'subject': 'Database Management',
            'topic': 'SQL Queries',
            'semester': 'Semester 4',
            'uploaded_by': 'Rohan Mehta',
            'file_name': 'DBMS_SQL_Queries.pdf',
            'description': 'Complete SQL query reference with practice problems',
            'upload_date': '2026-01-06',
            'downloads': 67,
            'rating': 4.7
        }
    ],
    'Operating Systems': [
        {
            'id': 4,
            'subject': 'Operating Systems',
            'topic': 'Process Scheduling',
            'semester': 'Semester 4',
            'uploaded_by': 'Neha Sharma',
            'file_name': 'OS_Process_Scheduling.pdf',
            'description': 'Process scheduling algorithms with diagrams',
            'upload_date': '2026-01-08',
            'downloads': 28,
            'rating': 4.3
        }
    ],
    'Web Development': [
        {
            'id': 5,
            'subject': 'Web Development',
            'topic': 'JavaScript Fundamentals',
            'semester': 'Semester 5',
            'uploaded_by': 'Karan Singh',
            'file_name': 'WebDev_JavaScript.pdf',
            'description': 'JavaScript basics to advanced concepts',
            'upload_date': '2026-01-09',
            'downloads': 53,
            'rating': 4.6
        }
    ]
}

# Counter for generating new IDs
note_id_counter = 6

def get_next_note_id() -> int:
    """Generate next unique ID for notes"""
    global note_id_counter
    current_id = note_id_counter
    note_id_counter += 1
    return current_id

def get_all_subjects() -> List[str]:
    """Get list of all subjects"""
    return list(notes_data.keys())

def get_all_notes() -> List[Dict]:
    """Get all notes as a flat list"""
    all_notes = []
    for subject_notes in notes_data.values():
        all_notes.extend(subject_notes)
    return all_notes

def reset_database():
    """Reset database to initial state"""
    global notes_data, note_id_counter
    notes_data.clear()
    note_id_counter = 1
