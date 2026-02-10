# CLAUDE.md 改进建议

以下是对现有 CLAUDE.md 的改进建议,您可以手动合并这些内容:

## 1. 项目概述部分更新

**当前内容:**
```
Full-stack Claude AI chat interface with sandbox code execution. Frontend (React/TypeScript/Vite) on port 3000, Backend (FastAPI/Python) on port 8080, PostgreSQL 13, Redis 7.
```

**建议改为:**
```
Full-stack Claude AI chat interface with sandbox code execution. Frontend (React 19/TypeScript/Vite) on port 3000, Backend (FastAPI/Python 3.13) on port 8080, PostgreSQL 13, Redis 7, Celery workers for background tasks.

**Tech Stack:**
- Frontend: React 19, TypeScript, Vite, TailwindCSS, Zustand, React Query, Monaco Editor, XTerm.js
- Backend: FastAPI, SQLAlchemy 2.0, Celery, Redis, Granian ASGI server
- Sandbox: Docker (local) or E2B (cloud) for isolated code execution
```

## 2. Docker Compose 部分更新

**在 "docker compose logs -f backend" 后添加:**
```bash
docker compose up -d              # Start all services (postgres, redis, api, celery-worker, celery-beat, frontend)
```

这样可以让用户了解启动的所有服务。

## 3. 架构部分增强

### Backend 部分 - 添加更多细节:

```
- **Entry:** `main.py` - FastAPI app factory with `create_application()`, includes all routers, admin panel, middleware
- **API Layer:** `api/endpoints/` - Route handlers (chat, auth, sandbox, websocket, agents, skills, commands, attachments, permissions, scheduling, ai_models)
- **Service Layer:** `services/` - Business logic (`ChatService`, `ClaudeAgentService`, `SandboxService`, `PermissionManager`, `AgentService`, `SkillService`)
- **Models:** `models/db_models/` - SQLAlchemy ORM models, `models/schemas/` - Pydantic schemas for request/response validation
- **Background Tasks:** `tasks/` - Celery tasks (`chat_processor.py` for streaming responses, `scheduler.py` for scheduled tasks)
- **Dependencies:** `core/deps.py` - FastAPI dependency injection for sessions, auth, services
- **Streaming:** `services/streaming/` - SSE event handling, Redis pub/sub for cross-worker communication
```

### Frontend 部分 - 添加更多细节:

```
- **Entry:** `main.tsx` → `App.tsx` with React Router
- **Pages:** `pages/` - Route containers (ChatPage, SettingsPage, etc.)
- **Components:** `components/` - Feature folders organized by domain:
  - `chat/` - Message display, input, tools, thinking mode selector
  - `editor/` - Monaco editor, file tree, terminal, web/mobile preview
  - `settings/` - Settings tabs and dialogs
  - `layout/` - Header, sidebar, routing
  - `ui/` - Reusable UI components
- **State:** `store/` - Zustand stores:
  - `authStore` - User authentication state
  - `chatStore` - Chat list and current chat state
  - `streamStore` - SSE connection and streaming state
  - `modelStore` - AI model selection and provider settings
  - `permissionStore` - Tool permission requests
  - `uiStore` - UI state (modals, panels, etc.)
- **API:** `services/` - API client functions for each backend endpoint
- **Custom Hooks:** `hooks/` - 30+ hooks for chat streaming, file handling, message actions, xterm, drag-and-drop
```

### Key Patterns 部分 - 扩展说明:

**Backend:**
- Async SQLAlchemy with separate session factories for API (`SessionLocal`) and Celery (`CelerySessionLocal`)
- All services inherit from `BaseDbService[T]` for common CRUD operations
- Real-time chat via SSE streaming with Redis pub/sub for cross-worker communication
- Celery tasks handle long-running AI responses; workers publish events to Redis streams
- Pydantic schemas for all API requests/responses (no bare dicts)
- FastAPI dependency injection via `core/deps.py` for service initialization

**Frontend:**
- Zustand for client state, React Query (`@tanstack/react-query`) for server state
- All API calls go through service functions in `services/` (no direct fetch)
- Components organized by feature, not by type (e.g., `components/chat/` not `components/ChatMessage.tsx`)
- Custom hooks encapsulate complex logic (streaming, file handling, permissions)

**Sandbox System:**
- Provider pattern: `SandboxProvider` interface with `DockerProvider` and `E2BProvider` implementations
- Created via `create_sandbox_provider(provider_type, api_key)` factory function
- `SandboxService` provides high-level operations (execute code, manage files, start terminals)
- User settings determine which provider to use (Docker for local, E2B for cloud)
- Docker containers mount `/var/run/docker.sock` for sandbox creation

**Permission Management:**
- `PermissionManager` service tracks tool usage and approval status
- Frontend `permissionStore` manages user approval UI flow
- Tools can require explicit user approval before execution (configurable per tool type)
- Permissions stored in Redis for fast access during streaming

## 4. 数据库部分增强

**在现有内容后添加:**

```
**Models in `/backend/app/models/db_models/`:**
- `User` - User accounts and authentication
- `Chat` - Chat sessions (sandbox_id, model provider, title)
- `Message` - Chat messages (role, content, status, attachments)
- `MessageAttachment` - File attachments to messages
- `AIModel` - Available AI models and providers
- `UserSettings` - User preferences (sandbox provider, API keys)
- `RefreshToken` - JWT refresh tokens for auth
- `ScheduledTask` - Recurring tasks managed by Celery Beat
```

## 5. 新增流式响应架构部分

**在 "Database" 部分后添加新的 "Streaming Architecture" 部分:**

```
### Streaming Architecture

Chat responses stream in real-time via SSE (Server-Sent Events):

1. Frontend sends chat request → Backend creates `Chat` and `Message` records
2. Backend enqueues Celery task with `process_chat.apply_async()`
3. Celery worker processes chat with Claude API, publishes events to Redis stream:
   - `content_block_delta` - Streaming text content
   - `tool_use` - AI wants to use a tool
   - `tool_result` - Tool execution result
   - `content_block_stop` - Message complete
4. Backend `/chat/{id}/stream` endpoint reads from Redis stream and forwards to frontend via SSE
5. Frontend `useChatStreaming` hook parses SSE events and updates UI in real-time
6. Redis stream max 10,000 events (`STREAM_MAX_LEN`), trimmed automatically

**Key constants in `app/constants/`:**
- `REDIS_KEY_CHAT_STREAM` - Redis stream key pattern
- `REDIS_KEY_CHAT_TASK` - Celery task ID tracking
- `REDIS_KEY_CHAT_REVOKED` - Cancellation signal
```

## 6. 环境变量部分扩展

**在现有内容后添加:**

```
**Additional env vars:**
- `ZAI_API_KEY` - Z.AI coding plan key
- `OPENROUTER_API_KEY` - OpenRouter key
- `BASE_URL` - Backend URL for tunneling (required for E2B sandbox)
- `CELERY_CONCURRENCY` - Number of Celery worker processes (default: 25)
- `CELERY_WORKER_REPLICAS` - Number of Celery worker replicas (default: 8)

**For E2B sandbox (remote execution):**
- E2B cannot reach `localhost`, so expose backend via tunnel (ngrok, cloudflared)
- Set `BASE_URL` to tunnel URL: `BASE_URL=https://your-tunnel.ngrok.io docker compose up -d`
- Docker sandbox works fine with `BASE_URL=http://localhost:8080`
```

## 7. 新增开发工作流程部分

**在文件末尾添加新的 "Development Workflow" 部分:**

```
## Development Workflow

**Adding a new API endpoint:**
1. Create Pydantic schemas in `backend/app/models/schemas/`
2. Add route handler in `backend/app/api/endpoints/`
3. Add service methods in `backend/app/services/`
4. Register router in `backend/app/main.py`
5. Create frontend service in `frontend/src/services/`
6. Create React Query hook in `frontend/src/hooks/queries/` (optional)
7. Add to admin panel in `backend/app/admin/views/` if needed

**Adding a new UI component:**
1. Create component in appropriate feature folder (e.g., `components/chat/`)
2. Define prop interfaces locally in the component file
3. Use existing UI primitives from `components/ui/primitives/`
4. Follow existing component patterns (layout, hooks, state management)
5. Export via feature index if used across multiple features

**Database changes:**
1. Modify model in `backend/app/models/db_models/`
2. Run `alembic revision --autogenerate -m "description"`
3. Review generated migration in `backend/migrations/versions/`
4. Run `python migrate.py` to apply
5. Update Pydantic schemas in `backend/app/models/schemas/` if API changes
```

---

## 改进总结

以上改进主要增加了:

1. ✅ **技术栈详细信息** - 明确列出了所有主要技术
2. ✅ **Docker 服务列表** - 说明启动的所有服务组件
3. ✅ **架构细节** - 更详细的目录结构和职责说明
4. ✅ **Sandbox 系统说明** - Provider 模式和集成方式
5. ✅ **权限管理系统** - 工具权限审批流程
6. ✅ **流式响应架构** - SSE + Redis 的完整流程
7. ✅ **开发工作流程** - 添加新功能的标准步骤
8. ✅ **环境变量详细说明** - 包括 E2B 配置和 Celery 参数

这些改进将帮助未来的 Claude Code 实例更快地理解代码库架构和开发模式。
