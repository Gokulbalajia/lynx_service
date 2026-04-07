# Database Migrations

Run the following SQL in your Supabase SQL Editor to support the current backend version.

## 1. Role-Based Access Control (RBAC)

Create the `roles` table and seed it with default shop roles.

```sql
-- Create roles table
CREATE TABLE IF NOT EXISTS public.roles (
    id BIGSERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Seed roles
INSERT INTO public.roles (name) VALUES ('admin'), ('user') 
ON CONFLICT (name) DO NOTHING;

-- Add role_id to users if it doesn't exist
-- ALTER TABLE public.users ADD COLUMN IF NOT EXISTS role_id BIGINT REFERENCES public.roles(id);
```

## 2. Stock Management RPC

Create a function to atomically decrement product stock during checkout.

```sql
-- Function to decrement product variant stock
CREATE OR REPLACE FUNCTION public.decrement_product_stock(variant_id UUID, qty INT)
RETURNS VOID AS $$
BEGIN
    UPDATE public.product_variants
    SET stock = stock - qty,
        updated_at = NOW()
    WHERE id = variant_id AND stock >= qty;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Insufficient stock or variant not found';
    END IF;
END;
$$ LANGUAGE plpgsql;
```

## 3. Storage Buckets (Optional)

If using pictures for pets or products:

```sql
-- Ensure storage buckets exist
INSERT INTO storage.buckets (id, name, public) 
VALUES ('products', 'products', true), 
       ('pets', 'pets', true)
ON CONFLICT (id) DO NOTHING;
```
