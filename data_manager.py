import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class PromptManager:
    def __init__(self):
        self.data_dir = Path.home() / ".prompt_manager"
        self.data_file = self.data_dir / "prompts.json"
        self.api_docs_file = self.data_dir / "api_docs.json"
        self.api_keys_file = self.data_dir / "api_keys.json"
        self.config_file = self.data_dir / "config.json"
        self._ensure_data_dir()
        self.prompts = self._load_prompts()
        self.api_docs = self._load_api_docs()
        self.api_keys = self._load_api_keys()
        self.config = self._load_config()
    
    def _ensure_data_dir(self):
        self.data_dir.mkdir(exist_ok=True)
    
    def _load_prompts(self) -> List[Dict]:
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 确保返回的是列表
                    if isinstance(data, list):
                        return data
                    else:
                        return []
            except Exception as e:
                print(f"Error loading prompts: {e}")
                return []
        return []
    
    def _save_prompts(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.prompts, f, ensure_ascii=False, indent=2)
    
    def _load_api_docs(self) -> List[Dict]:
        if self.api_docs_file.exists():
            try:
                with open(self.api_docs_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
                    else:
                        return []
            except Exception as e:
                print(f"Error loading api_docs: {e}")
                return []
        return []
    
    def _save_api_docs(self):
        with open(self.api_docs_file, 'w', encoding='utf-8') as f:
            json.dump(self.api_docs, f, ensure_ascii=False, indent=2)
    
    def _load_api_keys(self) -> List[Dict]:
        if self.api_keys_file.exists():
            try:
                with open(self.api_keys_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
                    else:
                        return []
            except Exception as e:
                print(f"Error loading api_keys: {e}")
                return []
        return []
    
    def _save_api_keys(self):
        with open(self.api_keys_file, 'w', encoding='utf-8') as f:
            json.dump(self.api_keys, f, ensure_ascii=False, indent=2)
    
    def _load_config(self) -> Dict:
        default_config = {
            "window_size": "normal",
            "opacity": 0.95,
            "always_on_top": True,
            "position_locked": False,
            "auto_collapse": True,
            "window_position": None,
            "window_geometry": None,
            "first_run": True,
            "gemini_api_key": ""
        }
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    default_config.update(loaded)
            except:
                pass
        return default_config
    
    def save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def add_prompt(self, name: str, category: str, tags: List[str], content: str) -> Dict:
        prompt = {
            "id": self._generate_id(),
            "name": name,
            "category": category,
            "tags": tags,
            "content": content,
            "usage_count": 0,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.prompts.append(prompt)
        self._save_prompts()
        return prompt
    
    def update_prompt(self, prompt_id: str, name: str, category: str, tags: List[str], content: str):
        for prompt in self.prompts:
            if prompt["id"] == prompt_id:
                prompt["name"] = name
                prompt["category"] = category
                prompt["tags"] = tags
                prompt["content"] = content
                prompt["updated_at"] = datetime.now().isoformat()
                self._save_prompts()
                return True
        return False
    
    def delete_prompt(self, prompt_id: str) -> bool:
        original_len = len(self.prompts)
        self.prompts = [p for p in self.prompts if p["id"] != prompt_id]
        if len(self.prompts) < original_len:
            self._save_prompts()
            return True
        return False
    
    def get_prompt(self, prompt_id: str) -> Optional[Dict]:
        for prompt in self.prompts:
            if prompt["id"] == prompt_id:
                return prompt
        return None
    
    def increment_usage(self, prompt_id: str):
        for prompt in self.prompts:
            if prompt["id"] == prompt_id:
                prompt["usage_count"] = prompt.get("usage_count", 0) + 1
                self._save_prompts()
                break
    
    def get_all_prompts(self) -> List[Dict]:
        return self.prompts
    
    def get_categories(self) -> List[str]:
        categories = set()
        for prompt in self.prompts:
            if prompt.get("category"):
                categories.add(prompt["category"])
        return sorted(list(categories))
    
    def get_all_tags(self) -> List[str]:
        tags = set()
        for prompt in self.prompts:
            for tag in prompt.get("tags", []):
                tags.add(tag)
        return sorted(list(tags))
    
    def search_prompts(self, query: str, category: Optional[str] = None) -> List[Dict]:
        results = []
        query_lower = query.lower()
        
        for prompt in self.prompts:
            if category and prompt.get("category") != category:
                continue
            
            if not query:
                results.append(prompt)
                continue
            
            if (query_lower in prompt["name"].lower() or
                query_lower in prompt.get("category", "").lower() or
                query_lower in prompt.get("content", "").lower() or
                any(query_lower in tag.lower() for tag in prompt.get("tags", []))):
                results.append(prompt)
        
        return results
    
    def get_category_stats(self) -> Dict[str, int]:
        stats = {}
        for prompt in self.prompts:
            category = prompt.get("category", "未分类")
            stats[category] = stats.get(category, 0) + 1
        return stats
    
    def get_top_prompts(self, limit: int = 5) -> List[Dict]:
        sorted_prompts = sorted(self.prompts, key=lambda p: p.get("usage_count", 0), reverse=True)
        return sorted_prompts[:limit]
    
    def import_prompts(self, file_path: str) -> tuple[int, int]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_prompts = json.load(f)
            
            if not isinstance(imported_prompts, list):
                return 0, 0
            
            existing_names = {p["name"] for p in self.prompts}
            added = 0
            skipped = 0
            
            for prompt in imported_prompts:
                if prompt.get("name") in existing_names:
                    skipped += 1
                    continue
                
                if "id" not in prompt:
                    prompt["id"] = self._generate_id()
                if "usage_count" not in prompt:
                    prompt["usage_count"] = 0
                if "created_at" not in prompt:
                    prompt["created_at"] = datetime.now().isoformat()
                if "updated_at" not in prompt:
                    prompt["updated_at"] = datetime.now().isoformat()
                
                self.prompts.append(prompt)
                added += 1
            
            if added > 0:
                self._save_prompts()
            
            return added, skipped
        except Exception as e:
            print(f"Import error: {e}")
            return 0, 0
    
    def export_prompts(self, file_path: str) -> bool:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.prompts, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False
    
    def _generate_id(self) -> str:
        import uuid
        return str(uuid.uuid4())
    
    # ==================== API 文档相关方法 ====================
    
    def add_api_doc(self, name: str, category: str, tags: List[str], content: str) -> Dict:
        doc = {
            "id": self._generate_id(),
            "name": name,
            "category": category,
            "tags": tags,
            "content": content,
            "usage_count": 0,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.api_docs.append(doc)
        self._save_api_docs()
        return doc
    
    def update_api_doc(self, doc_id: str, name: str, category: str, tags: List[str], content: str):
        for doc in self.api_docs:
            if doc["id"] == doc_id:
                doc["name"] = name
                doc["category"] = category
                doc["tags"] = tags
                doc["content"] = content
                doc["updated_at"] = datetime.now().isoformat()
                self._save_api_docs()
                return True
        return False
    
    def delete_api_doc(self, doc_id: str) -> bool:
        original_len = len(self.api_docs)
        self.api_docs = [d for d in self.api_docs if d["id"] != doc_id]
        if len(self.api_docs) < original_len:
            self._save_api_docs()
            return True
        return False
    
    def get_api_doc(self, doc_id: str) -> Optional[Dict]:
        for doc in self.api_docs:
            if doc["id"] == doc_id:
                return doc
        return None
    
    def increment_api_doc_usage(self, doc_id: str):
        for doc in self.api_docs:
            if doc["id"] == doc_id:
                doc["usage_count"] = doc.get("usage_count", 0) + 1
                self._save_api_docs()
                break
    
    def get_all_api_docs(self) -> List[Dict]:
        return self.api_docs
    
    def get_api_doc_categories(self) -> List[str]:
        categories = set()
        for doc in self.api_docs:
            if doc.get("category"):
                categories.add(doc["category"])
        return sorted(list(categories))
    
    def search_api_docs(self, query: str, category: Optional[str] = None) -> List[Dict]:
        results = []
        query_lower = query.lower()
        
        for doc in self.api_docs:
            if category and doc.get("category") != category:
                continue
            
            if not query:
                results.append(doc)
                continue
            
            if (query_lower in doc["name"].lower() or
                query_lower in doc.get("category", "").lower() or
                query_lower in doc.get("content", "").lower() or
                any(query_lower in tag.lower() for tag in doc.get("tags", []))):
                results.append(doc)
        
        return results
    
    # ==================== API 密钥相关方法 ====================
    
    def add_api_key(self, name: str, key: str, category: str = "") -> Dict:
        """添加 API 密钥（只需名称和密钥）"""
        api_key = {
            "id": self._generate_id(),
            "name": name,
            "key": key,
            "category": category,
            "usage_count": 0,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.api_keys.append(api_key)
        self._save_api_keys()
        return api_key
    
    def update_api_key(self, key_id: str, name: str, key: str, category: str = ""):
        for api_key in self.api_keys:
            if api_key["id"] == key_id:
                api_key["name"] = name
                api_key["key"] = key
                api_key["category"] = category
                api_key["updated_at"] = datetime.now().isoformat()
                self._save_api_keys()
                return True
        return False
    
    def delete_api_key(self, key_id: str) -> bool:
        original_len = len(self.api_keys)
        self.api_keys = [k for k in self.api_keys if k["id"] != key_id]
        if len(self.api_keys) < original_len:
            self._save_api_keys()
            return True
        return False
    
    def get_api_key(self, key_id: str) -> Optional[Dict]:
        for api_key in self.api_keys:
            if api_key["id"] == key_id:
                return api_key
        return None
    
    def increment_api_key_usage(self, key_id: str):
        for api_key in self.api_keys:
            if api_key["id"] == key_id:
                api_key["usage_count"] = api_key.get("usage_count", 0) + 1
                self._save_api_keys()
                break
    
    def get_all_api_keys(self) -> List[Dict]:
        return self.api_keys
    
    def get_api_key_categories(self) -> List[str]:
        categories = set()
        for api_key in self.api_keys:
            if api_key.get("category"):
                categories.add(api_key["category"])
        return sorted(list(categories))
    
    def search_api_keys(self, query: str, category: Optional[str] = None) -> List[Dict]:
        results = []
        query_lower = query.lower()
        
        for api_key in self.api_keys:
            if category and api_key.get("category") != category:
                continue
            
            if not query:
                results.append(api_key)
                continue
            
            if (query_lower in api_key["name"].lower() or
                query_lower in api_key.get("category", "").lower() or
                query_lower in api_key.get("key", "").lower()):
                results.append(api_key)
        
        return results
