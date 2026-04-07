from typing import Any, List, Optional, Dict
from supabase import Client
from uuid import UUID

class BaseService:
    def __init__(self, client: Client, table_name: str):
        self.client = client
        self.table_name = table_name

    def get_all(self, query_params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        query = self.client.table(self.table_name).select("*")
        if query_params:
            for key, value in query_params.items():
                query = query.eq(key, value)
        response = query.execute()
        return response.data

    def get_by_id(self, id: UUID) -> Optional[Dict[str, Any]]:
        response = self.client.table(self.table_name).select("*").eq("id", str(id)).execute()
        return response.data[0] if response.data else None

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self.client.table(self.table_name).insert(data).execute()
        return response.data[0]

    def update(self, id: UUID, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self.client.table(self.table_name).update(data).eq("id", str(id)).execute()
        return response.data[0]

    def delete(self, id: UUID) -> bool:
        self.client.table(self.table_name).delete().eq("id", str(id)).execute()
        return True
