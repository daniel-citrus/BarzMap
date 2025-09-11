# SupabaseAdapters package
# This package contains all Supabase adapter modules for different tables

from . import equipment_adapter
from . import user_adapter

__all__ = ["equipment_adapter", "user_adapter"]
