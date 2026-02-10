from __future__ import annotations

from typing import TYPE_CHECKING, cast

from pydantic import TypeAdapter
from redis.asyncio import Redis
from sqlalchemy import select

from app.constants import REDIS_KEY_MODELS_LIST
from app.core.config import get_settings
from app.models.db_models import AIModel, ModelProvider
from app.services.base import BaseDbService, SessionFactoryType

if TYPE_CHECKING:
    from app.models.schemas import AIModelResponse

settings = get_settings()


class AIModelService(BaseDbService[AIModel]):
    def __init__(self, session_factory: SessionFactoryType | None = None) -> None:
        super().__init__(session_factory)

    async def get_models(
        self, active_only: bool = True, redis: Redis[str] | None = None
    ) -> list[AIModelResponse] | list[AIModel]:
        from app.models.schemas import AIModelResponse

        cache_key = REDIS_KEY_MODELS_LIST.format(active_only=active_only)

        if redis:
            cached = await redis.get(cache_key)
            if cached:
                adapter = TypeAdapter(list[AIModelResponse])
                return cast(list[AIModelResponse], adapter.validate_json(cached))

        async with self.session_factory() as db:
            query = select(AIModel).order_by(AIModel.sort_order, AIModel.name)
            if active_only:
                query = query.filter(AIModel.is_active.is_(True))
            result = await db.execute(query)
            models = list(result.scalars().all())

        if redis:
            responses = [AIModelResponse.model_validate(m) for m in models]
            adapter = TypeAdapter(list[AIModelResponse])
            await redis.setex(
                cache_key,
                settings.MODELS_CACHE_TTL_SECONDS,
                adapter.dump_json(responses),
            )

        return models

    async def get_model_by_model_id(self, model_id: str) -> AIModel | None:
        async with self.session_factory() as db:
            result = await db.execute(
                select(AIModel).filter(AIModel.model_id == model_id)
            )
            return cast(AIModel | None, result.scalar_one_or_none())

    async def get_model_provider(self, model_id: str) -> ModelProvider | None:
        model = await self.get_model_by_model_id(model_id)
        return model.provider if model else None
