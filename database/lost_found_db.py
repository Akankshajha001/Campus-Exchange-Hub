"""
Lost & Found Database - In-memory storage using lists and dictionaries
"""

from datetime import datetime
from typing import List, Dict

# Main data structure: List of dictionaries
# Each dictionary represents one lost or found item
lost_found_items: List[Dict] = [
    {
        'id': 1,
        'type': 'lost',  # 'lost' or 'found'
        'item_name': 'Black Water Bottle',
        'category': 'Bottle',
        'location': 'Library Ground Floor',
        'description': 'Black steel water bottle with university logo',
        'reporter_name': 'Rahul Kumar',
        'reporter_contact': 'rahul@example.com',
        'date': '2026-01-08',
        'status': 'open',  # 'open', 'matched', 'claimed'
        'matched_with': None,
        'verification_code': '12345',
        'image_path': None
    },
    {
        'id': 2,
        'type': 'found',
        'item_name': 'Student ID Card',
        'category': 'ID Card',
        'location': 'Cafeteria',
        'description': 'Student ID card - Name: Priya Sharma',
        'reporter_name': 'Amit Singh',
        'reporter_contact': 'amit@example.com',
        'date': '2026-01-09',
        'status': 'open',
        'matched_with': None,
        'verification_code': '67890',
        'image_path': None
    },
    {
        'id': 3,
        'type': 'lost',
        'item_name': 'Laptop Charger',
        'category': 'Charger',
        'location': 'Computer Lab',
        'description': 'Dell laptop charger, 65W',
        'reporter_name': 'Sneha Patel',
        'reporter_contact': 'sneha@example.com',
        'date': '2026-01-10',
        'status': 'open',
        'matched_with': None,
        'verification_code': '54321',
        'image_path': None
    }
]

# Counter for generating new IDs
item_id_counter = 4

def get_next_id() -> int:
    """Generate next unique ID for items"""
    global item_id_counter
    current_id = item_id_counter
    item_id_counter += 1
    return current_id

def reset_database():
    """Reset database to initial state (useful for testing)"""
    global lost_found_items, item_id_counter
    lost_found_items.clear()
    item_id_counter = 1
