"""
Notes Exchange Service - Business logic for notes sharing
"""

from datetime import datetime
from typing import List, Dict, Optional
from database.notes_db import notes_data, get_next_note_id, get_all_subjects, get_all_notes

def upload_note(subject: str, topic: str, semester: str, uploaded_by: str,
                file_name: str, description: str) -> Dict:
    """Upload a new note to the database"""
    new_note = {
        'id': get_next_note_id(),
        'subject': subject,
        'topic': topic,
        'semester': semester,
        'uploaded_by': uploaded_by,
        'file_name': file_name,
        'description': description,
        'upload_date': datetime.now().strftime('%Y-%m-%d'),
        'downloads': 0,
        'rating': 0.0
    }
    
    # Add to appropriate subject list, create if doesn't exist
    if subject not in notes_data:
        notes_data[subject] = []
    
    notes_data[subject].append(new_note)
    return new_note

def get_notes_by_subject(subject: str) -> List[Dict]:
    """Get all notes for a specific subject"""
    return notes_data.get(subject, []).copy()

def get_all_notes_list() -> List[Dict]:
    """Get all notes as a flat list"""
    return get_all_notes()

def get_subjects() -> List[str]:
    """Get list of all available subjects"""
    return get_all_subjects()

def get_note_by_id(note_id: int) -> Optional[Dict]:
    """Get a specific note by ID"""
    for subject_notes in notes_data.values():
        for note in subject_notes:
            if note['id'] == note_id:
                return note
    return None

def increment_download_count(note_id: int) -> bool:
    """Increment the download count for a note"""
    for subject_notes in notes_data.values():
        for note in subject_notes:
            if note['id'] == note_id:
                note['downloads'] += 1
                return True
    return False

def get_top_contributors(limit: int = 10) -> List[Dict]:
    """Get top note contributors based on upload count"""
    contributors = {}
    
    for subject_notes in notes_data.values():
        for note in subject_notes:
            uploader = note['uploaded_by']
            if uploader not in contributors:
                contributors[uploader] = {
                    'name': uploader,
                    'uploads': 0,
                    'total_downloads': 0,
                    'subjects': set()
                }
            contributors[uploader]['uploads'] += 1
            contributors[uploader]['total_downloads'] += note['downloads']
            contributors[uploader]['subjects'].add(note['subject'])
    
    # Convert sets to lists for serialization
    contributor_list = []
    for contrib in contributors.values():
        contrib['subjects'] = list(contrib['subjects'])
        contributor_list.append(contrib)
    
    # Sort by uploads
    contributor_list.sort(key=lambda x: x['uploads'], reverse=True)
    return contributor_list[:limit]

def search_notes(query: str) -> List[Dict]:
    """Search notes by subject, topic, or description"""
    query_lower = query.lower()
    results = []
    
    for subject_notes in notes_data.values():
        for note in subject_notes:
            if (query_lower in note['subject'].lower() or
                query_lower in note['topic'].lower() or
                query_lower in note['description'].lower() or
                query_lower in note['uploaded_by'].lower()):
                results.append(note)
    
    return results

def get_notes_by_semester(semester: str) -> List[Dict]:
    """Get all notes for a specific semester"""
    results = []
    for subject_notes in notes_data.values():
        for note in subject_notes:
            if note['semester'] == semester:
                results.append(note)
    return results

def get_recent_notes(limit: int = 10) -> List[Dict]:
    """Get most recently uploaded notes"""
    all_notes = get_all_notes()
    sorted_notes = sorted(all_notes, key=lambda x: x['upload_date'], reverse=True)
    return sorted_notes[:limit]

def get_popular_notes(limit: int = 10) -> List[Dict]:
    """Get most downloaded notes"""
    all_notes = get_all_notes()
    sorted_notes = sorted(all_notes, key=lambda x: x['downloads'], reverse=True)
    return sorted_notes[:limit]
