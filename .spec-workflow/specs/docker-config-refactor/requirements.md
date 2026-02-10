# Requirements Document

## Introduction

本规格文档旨在消除 `preview_base_url` 配置的重复定义，将 Docker 沙箱的预览基础 URL 配置统一管理到全局配置中。目前该配置在 `DockerConfig` 数据类和 `Settings` 配置类中重复存在，违反了 DRY (Don't Repeat Yourself) 原则，增加了维护成本和出错风险。

## Alignment with Product Vision

本项目遵循最佳工程实践，配置管理应遵循单一数据源（Single Source of Truth）原则。通过统一配置管理，提高代码的可维护性和一致性。

## Requirements

### Requirement 1: 统一配置管理

**User Story:** 作为开发者，我需要 `preview_base_url` 配置只有一个权威来源，以便于维护和修改，避免配置不一致的问题。

#### Acceptance Criteria

1. WHEN 系统启动时 THEN `DockerConfig` 应从 `Settings.DOCKER_PREVIEW_BASE_URL` 读取 `preview_base_url`
2. IF `DockerConfig` 被实例化 THEN 其 `preview_base_url` 字段应使用全局配置的值
3. WHEN 开发者修改 `.env` 中的 `DOCKER_PREVIEW_BASE_URL` THEN Docker 沙箱提供商应使用新值
4. IF 代码中需要访问预览基础 URL THEN 应通过 `Settings` 类访问，而非硬编码

### Requirement 2: 移除重复默认值

**User Story:** 作为代码维护者，我希望消除重复的默认值定义，以遵循 DRY 原则。

#### Acceptance Criteria

1. WHEN 重构完成后 THEN `DockerConfig` 数据类中的 `preview_base_url` 不应有默认值
2. IF `DockerConfig` 需要默认值 THEN 应通过参数传递从 `Settings` 获取
3. WHEN 查看代码时 THEN 任何给定的配置项应只有一个定义源

### Requirement 3: 保持向后兼容性

**User Story:** 作为现有系统的使用者，我希望重构不会破坏现有的 Docker 沙箱功能。

#### Acceptance Criteria

1. WHEN 重构完成后 THEN 所有现有的 Docker 沙箱功能应继续正常工作
2. IF 环境变量 `DOCKER_PREVIEW_BASE_URL` 未设置 THEN 应使用合理的默认值
3. WHEN 代码创建 `DockerConfig` 实例时 THEN 应能正确获取配置值

## Non-Functional Requirements

### Code Architecture and Modularity

- **Single Responsibility Principle**: `Settings` 类负责所有环境配置，`DockerConfig` 仅负责沙箱特定的运行时配置
- **Modular Design**: 配置与使用分离，通过依赖注入传递配置值
- **DRY Principle**: 任何配置值只定义一次，其他地方通过引用获取
- **Clear Interfaces**: `DockerConfig` 的构造应清晰表明它需要从外部获取 `preview_base_url`

### Performance

- 配置读取在启动时完成一次，对运行时性能无影响

### Security

- 配置值通过环境变量管理，不暴露敏感信息

### Reliability

- 确保配置加载失败时有明确的错误提示
- 使用 Pydantic 的验证机制确保配置值有效性

### Usability

- 开发者只需在一个地方（`.env` 或 `Settings`）修改配置
- 配置变更后只需重启应用即可生效
