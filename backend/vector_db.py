from typing import Dict, List, Optional
from datetime import datetime
from utils import get_logger
from exceptions import VectorDBError
from config import settings

logger = get_logger(__name__)


class PromptMemory:
    """In-memory vector DB simulation for storing prompts and metadata"""
    
    def __init__(self):
        self.prompts: List[Dict[str, str]] = []
    
    def store_prompt(self, prompt: str, metadata: Optional[Dict] = None) -> None:
        """Store a prompt with optional metadata"""
        try:
            entry = {"prompt": prompt, "metadata": metadata or {}}
            self.prompts.append(entry)
            logger.info(f"Stored prompt: {prompt[:30]}...")
        except Exception as e:
            logger.error(f"Failed to store prompt: {e}")
            raise VectorDBError(f"Failed to store prompt: {str(e)}")
    
    def get_last_prompt(self) -> str:
        """Get the last stored prompt"""
        try:
            if len(self.prompts) > 0:
                return self.prompts[-1]["prompt"]
            return ""
        except Exception as e:
            logger.error(f"Failed to retrieve last prompt: {e}")
            raise VectorDBError(f"Failed to retrieve prompt: {str(e)}")
    
    def get_all_prompts(self) -> List[str]:
        """Get all stored prompts"""
        try:
            return [entry["prompt"] for entry in self.prompts]
        except Exception as e:
            logger.error(f"Failed to retrieve prompts: {e}")
            raise VectorDBError(f"Failed to retrieve prompts: {str(e)}")
    
    def clear(self) -> None:
        """Clear all prompts"""
        self.prompts.clear()
        logger.info("Prompt memory cleared")


class SupabaseDB:
    """Supabase PostgreSQL vector DB for storing prompts"""
    
    def __init__(self):
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            raise VectorDBError("Supabase credentials not configured")
        
        try:
            from supabase import create_client
            self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            self.table_name = "prompts"
            self._create_table()
            logger.info("Connected to Supabase database")
        except Exception as e:
            logger.error(f"Failed to connect to Supabase: {e}")
            raise VectorDBError(f"Supabase connection failed: {str(e)}")
    
    def _create_table(self) -> None:
        """Create prompts table if it doesn't exist"""
        try:
            self.client.table(self.table_name).select("id").limit(1).execute()
        except Exception:
            logger.info(f"Creating table: {self.table_name}")
    
    def store_prompt(self, prompt: str, metadata: Optional[Dict] = None) -> None:
        """Store a prompt in Supabase"""
        try:
            data = {
                "prompt_text": prompt,
                "metadata": metadata or {},
                "created_at": datetime.utcnow().isoformat()
            }
            self.client.table(self.table_name).insert(data).execute()
            logger.info(f"Stored prompt in Supabase: {prompt[:30]}...")
        except Exception as e:
            logger.error(f"Failed to store prompt in Supabase: {e}")
            raise VectorDBError(f"Failed to store prompt: {str(e)}")
    
    def get_last_prompt(self) -> str:
        """Get the last stored prompt from Supabase"""
        try:
            response = self.client.table(self.table_name).select("prompt_text").order(
                "created_at", desc=True
            ).limit(1).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]["prompt_text"]
            return ""
        except Exception as e:
            logger.error(f"Failed to retrieve last prompt from Supabase: {e}")
            raise VectorDBError(f"Failed to retrieve prompt: {str(e)}")
    
    def get_all_prompts(self) -> List[str]:
        """Get all stored prompts from Supabase"""
        try:
            response = self.client.table(self.table_name).select("prompt_text").order(
                "created_at", desc=True
            ).execute()
            return [entry["prompt_text"] for entry in response.data]
        except Exception as e:
            logger.error(f"Failed to retrieve prompts from Supabase: {e}")
            raise VectorDBError(f"Failed to retrieve prompts: {str(e)}")
    
    def clear(self) -> None:
        """Clear all prompts from Supabase"""
        try:
            self.client.table(self.table_name).delete().neq("id", 0).execute()
            logger.info("Cleared all prompts from Supabase")
        except Exception as e:
            logger.error(f"Failed to clear prompts: {e}")
            raise VectorDBError(f"Failed to clear prompts: {str(e)}")


# Initialize appropriate database based on config
if settings.USE_SUPABASE and settings.SUPABASE_URL and settings.SUPABASE_KEY:
    try:
        db = SupabaseDB()
        logger.info("Using Supabase as primary database")
    except Exception as e:
        logger.warning(f"Supabase initialization failed, falling back to in-memory: {e}")
        db = PromptMemory()
else:
    db = PromptMemory()
    logger.info("Using in-memory database")


def store_prompt(prompt: str, metadata: Optional[Dict] = None) -> None:
    """Store a prompt"""
    db.store_prompt(prompt, metadata)


def get_last_prompt() -> str:
    """Get the last stored prompt"""
    return db.get_last_prompt()


def get_all_prompts() -> List[str]:
    """Get all stored prompts"""
    return db.get_all_prompts()


def clear_memory() -> None:
    """Clear all prompts"""
    db.clear()