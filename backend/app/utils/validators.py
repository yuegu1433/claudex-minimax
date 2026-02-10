from __future__ import annotations

from typing import TYPE_CHECKING, cast

from app.models.db_models.enums import ModelProvider
from app.models.types import JSONList, JSONValue
from app.services.ai_model import AIModelService

if TYPE_CHECKING:
    from app.models.db_models import UserSettings
    from app.services.base import SessionFactoryType


class APIKeyValidationError(ValueError):
    pass


def normalize_json_list(value: JSONValue | None) -> JSONList:
    """
    Normalize JSON values to a list format.

    Handles legacy data formats where dicts were stored instead of lists.
    Returns empty list for None, dict, or already valid lists.
    """
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        # Handle legacy dict format - convert to empty list
        return []
    raise ValueError(f"Expected list, dict, or None, got {type(value).__name__}")


def validate_e2b_api_key(user_settings: UserSettings) -> str:
    if not user_settings.e2b_api_key:
        raise APIKeyValidationError(
            "E2B API key is required. Please configure your E2B API key in Settings."
        )
    return cast(str, user_settings.e2b_api_key)


async def validate_model_api_keys(
    user_settings: UserSettings,
    model_id: str,
    session_factory: "SessionFactoryType | None" = None,
) -> None:
    ai_model_service = AIModelService(session_factory=session_factory)
    provider = await ai_model_service.get_model_provider(model_id)

    if provider == ModelProvider.ZAI:
        if not user_settings.z_ai_api_key:
            raise APIKeyValidationError(
                f"Z.AI API key is required for model '{model_id}'. "
                "Please configure your Z.AI API key in Settings."
            )
    elif provider == ModelProvider.OPENROUTER:
        if not user_settings.openrouter_api_key:
            raise APIKeyValidationError(
                f"OpenRouter API key is required for model '{model_id}'. "
                "Please configure your OpenRouter API key in Settings."
            )
    elif provider == ModelProvider.MINIMAX:
        if not user_settings.minimax_api_key:
            raise APIKeyValidationError(
                f"MiniMax API key is required for model '{model_id}'. "
                "Please configure your MiniMax API key in Settings."
            )
    else:
        if not user_settings.claude_code_oauth_token:
            raise APIKeyValidationError(
                f"Claude Code Auth Token is required for model '{model_id}'. "
                "Please configure your Claude Code Auth Token in Settings."
            )
