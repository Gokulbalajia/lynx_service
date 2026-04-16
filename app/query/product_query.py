from app.query.base_query import BaseQuery
from supabase import Client
from typing import Dict, Any, List, Optional
from uuid import UUID

class ProductQuery(BaseQuery):
    def __init__(self, client: Client):
        super().__init__(client, "products")

    def get_all_with_relations(self, category_id: Optional[UUID] = None) -> List[Dict[str, Any]]:
        query = self.client.table("products").select("*, details:product_details(*), variants:product_variants(*), images:product_images(*)")
        if category_id:
            query = query.eq("category_id", str(category_id))
        res = query.execute()
        return res.data

    def get_by_id_with_relations(self, id: UUID) -> Optional[Dict[str, Any]]:
        res = self.client.table("products").select("*, details:product_details(*), variants:product_variants(*), images:product_images(*)").eq("id", str(id)).execute()
        return res.data[0] if res.data else None

    def create_product(self, product_dict: Dict[str, Any], details: Optional[Dict[str, Any]], variants: Optional[List[Dict[str, Any]]], images: Optional[List[Dict[str, Any]]]):
        res = self.client.table("products").insert(product_dict).execute()
        if not res.data:
            return None
        
        product_id = res.data[0]["id"]

        if details:
            details["product_id"] = product_id
            self.client.table("product_details").insert(details).execute()
        
        if variants:
            for variant in variants:
                variant["product_id"] = product_id
                self.client.table("product_variants").insert(variant).execute()
                
        if images:
            for img in images:
                img["product_id"] = product_id
                self.client.table("product_images").insert(img).execute()

        return self.get_by_id_with_relations(product_id)

    def update_product(self, id: UUID, product_dict: Dict[str, Any], details: Optional[Dict[str, Any]], variants: Optional[List[Dict[str, Any]]], images: Optional[List[Dict[str, Any]]]):
        if product_dict:
            self.client.table("products").update(product_dict).eq("id", str(id)).execute()
        
        if details is not None:
            details["product_id"] = str(id)
            self.client.table("product_details").upsert(details, on_conflict="product_id").execute()
        
        if variants is not None:
            self.client.table("product_variants").delete().eq("product_id", str(id)).execute()
            for variant in variants:
                variant["product_id"] = str(id)
                self.client.table("product_variants").insert(variant).execute()
                
        if images is not None:
            self.client.table("product_images").delete().eq("product_id", str(id)).execute()
            for img in images:
                img["product_id"] = str(id)
                self.client.table("product_images").insert(img).execute()

        return self.get_by_id_with_relations(id)

    def delete_product(self, id: UUID):
        res = self.client.table("products").delete().eq("id", str(id)).execute()
        return res.data if res.data else None
