from app.query.base_query import BaseQuery
from supabase import Client
from uuid import UUID
from typing import Any, Dict, List

class CategoryQuery(BaseQuery):
    def __init__(self, client: Client):
        super().__init__(client, "categories")

    def get_all_categories(self, query_params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Get all categories.
        """
        return self.get_all(query_params)

    def get_category_by_id(self, id: UUID) -> Any:
        """
        Get category by ID.
        """
        return self.get_by_id(id)

    def create_category(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new category.
        """
        return self.create(data)

    def update_category(self, id: UUID, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update category name and description.
        """
        return self.update(id, data)

    def delete_category(self, id: UUID) -> bool:
        """
        Delete category by id.
        """
        return self.delete(id)
