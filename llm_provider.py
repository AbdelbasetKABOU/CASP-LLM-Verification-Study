import os
import logging
from typing import Optional

class LLMProvider:
    @staticmethod
    def _get_api_key(provider: str) -> str:
        provider = provider.lower()
        mapping = {
            "openai": "OPENAI_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
            "openrouter": "OPENROUTER_API_KEY",
            "perplexity": "PERPLEXITY_API_KEY",
            "together": "TOGETHER_API_KEY",
            "anyscale": "ANYSCALE_API_KEY",
        }
        key_env = mapping.get(provider, "")
        api_key = (os.getenv(key_env, "") or "").strip()

        # fallback to OPENAI_API_KEY for OpenAI-compatible providers if desired
        if not api_key and provider in mapping and provider != "openai":
            api_key = (os.getenv("OPENAI_API_KEY", "") or "").strip()

        return api_key

    @staticmethod
    def _get_base_url(provider: str) -> Optional[str]:
        provider = provider.lower()

        # IMPORTANT:
        # - For real OpenAI, do NOT use OPENAI_BASE_URL (yours points to deepseek)
        # - For OpenAI-compatible backends (deepseek/openrouter/etc), do use OPENAI_BASE_URL
        if provider == "openai":
            # If you ever need a custom OpenAI proxy, set OPENAI_BASE_URL_OPENAI
            v = (os.getenv("OPENAI_BASE_URL_OPENAI", "") or "").strip()
            return v or None

        v = (os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_BASE") or "").strip()
        return v or None

    @staticmethod
    def load(provider: str, model: str, temperature: float = 0.0):
        provider = provider.lower()

        if provider in ("openai", "deepseek", "openrouter", "perplexity", "together", "anyscale"):
            from langchain_openai import ChatOpenAI

            api_key = LLMProvider._get_api_key(provider)
            if not api_key:
                raise RuntimeError(
                    "Missing API key. Set provider-specific key "
                    "(e.g., DEEPSEEK_API_KEY) or OPENAI_API_KEY."
                )

            base_url = LLMProvider._get_base_url(provider)

            logging.info("LLM init: provider=%s model=%s base_url=%s", provider, model, base_url)

            kwargs = dict(model=model, temperature=temperature, api_key=api_key)
            if base_url:
                kwargs["base_url"] = base_url

            return ChatOpenAI(**kwargs)

        if provider == "mistral":
            from langchain_mistralai import ChatMistralAI
            api_key = (os.getenv("MISTRAL_API_KEY", "") or "").strip()
            if not api_key:
                raise RuntimeError("MISTRAL_API_KEY is missing.")
            return ChatMistralAI(model=model, temperature=temperature, api_key=api_key)

        if provider == "groq":
            from langchain_groq import ChatGroq
            api_key = (os.getenv("GROQ_API_KEY", "") or "").strip()
            if not api_key:
                raise RuntimeError("GROQ_API_KEY is missing.")
            return ChatGroq(model=model, temperature=temperature, api_key=api_key)

        if provider == "gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI
            api_key = (os.getenv("GOOGLE_API_KEY", "") or "").strip()
            if not api_key:
                raise RuntimeError("GOOGLE_API_KEY is missing.")
            return ChatGoogleGenerativeAI(model=model, api_key=api_key, temperature=temperature)

        raise ValueError("Unknown provider: {}".format(provider))