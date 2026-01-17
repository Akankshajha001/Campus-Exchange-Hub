"""
Lost & Found Service - Business logic for lost and found items
"""

from datetime import datetime
from typing import List, Dict, Optional
import random
from database.lost_found_db import lost_found_items, get_next_id

def generate_verification_code() -> str:
    """Generate a unique 5-digit verification code"""
    return str(random.randint(10000, 99999))

def add_lost_item(item_name: str, category: str, location: str, 
                  description: str, reporter_name: str, reporter_contact: str,
                  image_path: str = None) -> Dict:
    """Add a new lost item to the database"""
    new_item = {
        'id': get_next_id(),
        'type': 'lost',
        'item_name': item_name,
        'category': category,
        'location': location,
        'description': description,
        'reporter_name': reporter_name,
        'reporter_contact': reporter_contact,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'status': 'open',
        'matched_with': None,
        'verification_code': generate_verification_code(),
        'image_path': image_path
    }
    lost_found_items.append(new_item)
    return new_item

def add_found_item(item_name: str, category: str, location: str,
                   description: str, reporter_name: str, reporter_contact: str,
                   image_path: str = None) -> Dict:
    """Add a new found item to the database"""
    new_item = {
        'id': get_next_id(),
        'type': 'found',
        'item_name': item_name,
        'category': category,
        'location': location,
        'description': description,
        'reporter_name': reporter_name,
        'reporter_contact': reporter_contact,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'status': 'open',
        'matched_with': None,
        'verification_code': generate_verification_code(),
        'image_path': image_path
    }
    lost_found_items.append(new_item)
    return new_item

def get_all_items() -> List[Dict]:
    """Get all lost and found items"""
    return lost_found_items.copy()

def get_lost_items() -> List[Dict]:
    """Get only lost items"""
    return [item for item in lost_found_items if item['type'] == 'lost']

def get_found_items() -> List[Dict]:
    """Get only found items"""
    return [item for item in lost_found_items if item['type'] == 'found']

def get_item_by_id(item_id: int) -> Optional[Dict]:
    """Get item by ID"""
    for item in lost_found_items:
        if item['id'] == item_id:
            return item
    return None

def find_potential_matches(item_type: str, category: str, location: str) -> List[Dict]:
    """
    Find potential matches for a lost or found item
    Match based on category and location
    """
    # If looking for matches for a lost item, search in found items and vice versa
    opposite_type = 'found' if item_type == 'lost' else 'lost'
    
    matches = []
    for item in lost_found_items:
        if item['type'] == opposite_type and item['status'] == 'open':
            # Match by category
            if item['category'].lower() == category.lower():
                # Bonus points if location also matches
                item_copy = item.copy()
                item_copy['match_score'] = 10
                if item['location'].lower() == location.lower():
                    item_copy['match_score'] = 20
                matches.append(item_copy)
    
    # Sort by match score (highest first)
    matches.sort(key=lambda x: x['match_score'], reverse=True)
    return matches

def claim_item(item_id: int, claimer_name: str, verification_detail: str = "", 
               claimer_email: str = "", claimer_contact: str = "") -> bool:
    """
    Mark an item as claimed with verification details
    
    Args:
        item_id: ID of the item being claimed
        claimer_name: Name of the person claiming (from logged-in user)
        verification_detail: Proof of ownership details
        claimer_email: Email of the claimer (from logged-in user)
        claimer_contact: Contact number for verification
    
    Returns:
        bool: True if successful, False otherwise
    """
    for item in lost_found_items:
        if item['id'] == item_id:
            item['status'] = 'claimed'
            item['claimed_by'] = claimer_name
            item['claimed_date'] = datetime.now().strftime('%Y-%m-%d')
            item['claimer_email'] = claimer_email
            item['claimer_contact'] = claimer_contact
            item['verification_detail'] = verification_detail
            return True
    return False

def get_recent_items(limit: int = 10) -> List[Dict]:
    """Get most recent items"""
    sorted_items = sorted(lost_found_items, 
                         key=lambda x: x['date'], 
                         reverse=True)
    return sorted_items[:limit]

def search_items(query: str) -> List[Dict]:
    """Search items by name, category, or location"""
    query_lower = query.lower()
    results = []
    for item in lost_found_items:
        if (query_lower in item['item_name'].lower() or 
            query_lower in item['category'].lower() or 
            query_lower in item['location'].lower() or
            query_lower in item['description'].lower()):
            results.append(item)
    return results

def get_items_by_status(status: str) -> List[Dict]:
    """Get items filtered by status"""
    return [item for item in lost_found_items if item['status'] == status]
