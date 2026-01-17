"""
Analytics Service - Statistics and charts logic
"""

from typing import Dict, List
from database.lost_found_db import lost_found_items
from database.notes_db import notes_data, get_all_notes
from database.users_db import user_sessions

def get_lost_found_stats() -> Dict:
    """Get statistics for lost & found items"""
    total_items = len(lost_found_items)
    lost_count = len([item for item in lost_found_items if item['type'] == 'lost'])
    found_count = len([item for item in lost_found_items if item['type'] == 'found'])
    open_count = len([item for item in lost_found_items if item['status'] == 'open'])
    claimed_count = len([item for item in lost_found_items if item['status'] == 'claimed'])
    
    return {
        'total_items': total_items,
        'lost_count': lost_count,
        'found_count': found_count,
        'open_count': open_count,
        'claimed_count': claimed_count,
        'match_rate': round((claimed_count / total_items * 100) if total_items > 0 else 0, 2)
    }

def get_notes_stats() -> Dict:
    """Get statistics for notes exchange"""
    all_notes = get_all_notes()
    total_notes = len(all_notes)
    total_downloads = sum(note['downloads'] for note in all_notes)
    total_subjects = len(notes_data.keys())
    
    avg_downloads = round(total_downloads / total_notes, 2) if total_notes > 0 else 0
    
    return {
        'total_notes': total_notes,
        'total_subjects': total_subjects,
        'total_downloads': total_downloads,
        'avg_downloads': avg_downloads,
        'contributors': len(set(note['uploaded_by'] for note in all_notes))
    }

def get_category_distribution() -> Dict[str, int]:
    """Get distribution of items by category"""
    categories = {}
    for item in lost_found_items:
        category = item['category']
        categories[category] = categories.get(category, 0) + 1
    
    # Sort by count
    sorted_categories = dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))
    return sorted_categories

def get_location_distribution() -> Dict[str, int]:
    """Get distribution of items by location"""
    locations = {}
    for item in lost_found_items:
        location = item['location']
        locations[location] = locations.get(location, 0) + 1
    
    # Sort by count
    sorted_locations = dict(sorted(locations.items(), key=lambda x: x[1], reverse=True))
    return sorted_locations

def get_top_downloaded_notes(limit: int = 10) -> List[Dict]:
    """Get top downloaded notes"""
    all_notes = get_all_notes()
    sorted_notes = sorted(all_notes, key=lambda x: x['downloads'], reverse=True)
    return sorted_notes[:limit]

def get_subject_wise_stats() -> Dict[str, Dict]:
    """Get statistics for each subject"""
    subject_stats = {}
    
    for subject, notes_list in notes_data.items():
        total_notes = len(notes_list)
        total_downloads = sum(note['downloads'] for note in notes_list)
        
        subject_stats[subject] = {
            'total_notes': total_notes,
            'total_downloads': total_downloads,
            'avg_downloads': round(total_downloads / total_notes, 2) if total_notes > 0 else 0
        }
    
    return subject_stats

def get_user_activity_stats() -> List[Dict]:
    """Get user activity statistics"""
    activity_list = []
    
    for session_id, user_data in user_sessions.items():
        activity_list.append({
            'name': user_data['name'],
            'roll_no': user_data['roll_no'],
            'items_reported': user_data['items_reported'],
            'notes_uploaded': user_data['notes_uploaded'],
            'notes_downloaded': user_data['notes_downloaded'],
            'total_activity': (user_data['items_reported'] + 
                             user_data['notes_uploaded'] + 
                             user_data['notes_downloaded'])
        })
    
    # Sort by total activity
    activity_list.sort(key=lambda x: x['total_activity'], reverse=True)
    return activity_list

def get_daily_activity() -> Dict[str, int]:
    """Get item reports by date"""
    daily_counts = {}
    
    for item in lost_found_items:
        date = item['date']
        daily_counts[date] = daily_counts.get(date, 0) + 1
    
    # Sort by date
    sorted_daily = dict(sorted(daily_counts.items()))
    return sorted_daily

def get_semester_wise_notes() -> Dict[str, int]:
    """Get notes distribution by semester"""
    semester_counts = {}
    
    for note in get_all_notes():
        semester = note['semester']
        semester_counts[semester] = semester_counts.get(semester, 0) + 1
    
    return semester_counts
