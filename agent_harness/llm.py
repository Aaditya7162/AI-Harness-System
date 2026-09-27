import os
from groq import Groq
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Global state for multi-provider routing
current_provider_index = 0
current_key_index = 0

class ProviderRouter:
    def __init__(self, custom_provider=None, custom_key=None):
        # Force reload from .env file every single time so the user can change keys on the fly!
        load_dotenv(override=True)
        
        global current_provider_index
        global current_key_index
        
        self.providers = []
        
        # 0. Check for Custom Key from UI (Takes Top Priority)
        if custom_provider and custom_key and custom_key.strip():
            prov_name = custom_provider.lower()
            custom_entry = {
                "name": prov_name,
                "keys": [custom_key.strip()]
            }
            if prov_name == "groq":
                custom_entry["model"] = "openai/gpt-oss-120b"
                custom_entry["fallback_model"] = "openai/gpt-oss-20b"
            elif prov_name == "deepseek":
                custom_entry["model"] = "deepseek-coder"
                custom_entry["base_url"] = "https://api.deepseek.com"
            elif prov_name == "qwen":
                custom_entry["model"] = "qwen2.5-coder-32b-instruct"
                custom_entry["base_url"] = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
            elif prov_name == "gemini":
                custom_entry["model"] = "gemini-3.8-flash"
                custom_entry["base_url"] = "https://generativelanguage.googleapis.com/v1beta/openai/"
            elif prov_name == "requesty":
                custom_entry["model"] = "meta-llama/llama-3.1-70b-instruct"
                custom_entry["base_url"] = "https://router.requesty.ai/v1"
                
            self.providers.append(custom_entry)
        
        # 1. Check for Groq (.env)
        keys_str = os.getenv("GROQ_API_KEYS")
        groq_keys = [k.strip() for k in keys_str.split(",")] if keys_str else []
        single_groq = os.getenv("GROQ_API_KEY")
        if single_groq and single_groq not in groq_keys:
            groq_keys.append(single_groq)
            
        if groq_keys:
            self.providers.append({
                "name": "groq",
                "keys": [k for k in groq_keys if k],
                "model": "openai/gpt-oss-120b",
                "fallback_model": "openai/gpt-oss-20b" 
            })
            
        # 2. Check for DeepSeek
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        if deepseek_key:
            self.providers.append({
                "name": "deepseek",
                "keys": [deepseek_key],
                "model": "deepseek-coder",
                "base_url": "https://api.deepseek.com"
            })
            
        # 3. Check for Qwen (Native Alibaba DashScope)
        qwen_key = os.getenv("QWEN_API_KEY")
        if qwen_key:
            self.providers.append({
                "name": "qwen",
                "keys": [qwen_key],
                "model": "qwen2.5-coder-32b-instruct",
                "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
            })
            
        # 4. Check for Gemini
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            self.providers.append({
                "name": "gemini",
                "keys": [gemini_key],
                "model": "gemini-3.8-flash",
                "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/"
            })
            
        # 5. Check for Requesty AI
        requesty_key = os.getenv("REQUESTY_API_KEY")
        if requesty_key:
            self.providers.append({
                "name": "requesty",
                "keys": [requesty_key],
                "model": os.getenv("REQUESTY_MODEL", "meta-llama/llama-3.1-70b-instruct"), 
                "base_url": "https://router.requesty.ai/v1"
            })
            
        # 6. Check for Local Hosted AI (Ollama, LM Studio, vLLM)
        local_url = os.getenv("LOCAL_API_BASE_URL")
        if local_url:
            self.providers.append({
                "name": "local",
                "keys": [os.getenv("LOCAL_API_KEY", "local-key-ignored")],
                "model": os.getenv("LOCAL_MODEL_NAME", "gemma2-9b-it"),
                "base_url": local_url
            })
            
        if not self.providers:
            raise ValueError("No API keys found! Please set GROQ_API_KEYS, DEEPSEEK_API_KEY, QWEN_API_KEY, GEMINI_API_KEY, REQUESTY_API_KEY, or LOCAL_API_BASE_URL in .env")
            
        # Ensure indices are valid
        if current_provider_index >= len(self.providers):
            current_provider_index = 0
            current_key_index = 0
            
        self._initialize_active_client()

    def _initialize_active_client(self):
        """Dynamically re-initializes the active client based on the current global indices."""
        global current_provider_index
        global current_key_index
        
        self.active_provider = self.providers[current_provider_index]
        self.active_key = self.active_provider["keys"][current_key_index]
        self.model = self.active_provider.get("current_active_model", self.active_provider["model"])
        
        if self.active_provider["name"] == "groq":
            self.client = Groq(api_key=self.active_key, max_retries=0)
        else:
            self.client = OpenAI(
                api_key=self.active_key,
                base_url=self.active_provider["base_url"],
                max_retries=0
            )

    def chat_completion(self, messages, tools=None):
        # ALWAYS sync the client with the global state in case it was hot-swapped!
        self._initialize_active_client()
        
        try:
            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.6,
            }
            # Only send max_tokens if not DeepSeek (DeepSeek sometimes rejects it depending on endpoint)
            if self.active_provider["name"] != "deepseek":
                kwargs["max_tokens"] = 4096
                
            if tools:
                kwargs["tools"] = tools
                kwargs["tool_choice"] = "auto"

            response = self.client.chat.completions.create(**kwargs)
            return response
        except Exception as e:
            error_str = str(e)
            global current_provider_index
            global current_key_index
            
            # AGGRESSIVE FALLBACK: Trigger on ANY error (Rate Limit, Server Down 500, Invalid Key 401, etc)
            # This ensures "whichever is available it should work" is 100% true!
            
            # 1. Try rotating keys within the current provider
            if current_key_index < len(self.active_provider["keys"]) - 1:
                current_key_index += 1
                return f"API_KEY_ROTATED_{self.active_provider['name'].upper()}"
                
            # 2. Try routing to the next provider completely (e.g. Groq -> DeepSeek -> Qwen)
            if current_provider_index < len(self.providers) - 1:
                current_provider_index += 1
                current_key_index = 0
                next_provider = self.providers[current_provider_index]["name"]
                return f"PROVIDER_FALLBACK_{next_provider.upper()}"
                
            # 3. If out of providers, try the Groq OSS fallback model as an absolute last resort
            if self.active_provider["name"] == "groq" and "fallback_model" in self.active_provider:
                current_active = self.active_provider.get("current_active_model", self.active_provider["model"])
                if current_active != self.active_provider["fallback_model"]:
                    self.active_provider["current_active_model"] = self.active_provider["fallback_model"]
                    return "MODEL_FALLBACK_OSS"
                    
            return f"Error: {error_str}"

# For backwards compatibility with app.py
GroqClient = ProviderRouter
