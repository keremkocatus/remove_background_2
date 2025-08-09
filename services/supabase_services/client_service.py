import asyncio
from supabase import AsyncClient, create_async_client
from core import config

SUPABASE_URL = config.SUPABASE_URL
SUPABASE_ANON_KEY = config.SUPABASE_ANON_KEY

# Lazy-initialized Supabase client
_supabase_client: AsyncClient | None = None
_supabase_lock = asyncio.Lock()

async def get_supabase_client() -> AsyncClient:
    global _supabase_client
    if _supabase_client is None:
        async with _supabase_lock:
            if _supabase_client is None:
                _supabase_client = await create_async_client(
                    SUPABASE_URL, SUPABASE_ANON_KEY
                )
    return _supabase_client
