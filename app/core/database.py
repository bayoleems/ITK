from abc import ABC, abstractmethod
from typing import Dict, Optional, List

class Database(ABC):
    """Abstract base class defining database interface"""

    @abstractmethod
    async def save_item(self, item: Dict) -> Dict:
        """Save an item to the database"""
        pass

    @abstractmethod 
    async def get_item(self, item_id: str) -> Optional[Dict]:
        """Get an item from the database by ID"""
        pass

    @abstractmethod
    async def list_items(self) -> List[Dict]:
        """List all items in the collection"""
        pass

    @abstractmethod
    async def delete_item(self, item_id: str) -> None:
        """Delete an item from the database"""
        pass

    @abstractmethod
    async def update_item(self, item_id: str, updates: Dict) -> Dict:
        """Update an item in the database"""
        pass

    


