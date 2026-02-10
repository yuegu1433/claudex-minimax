# Tasks Document

- [x] 1. 修改 DockerConfig 数据类，移除 preview_base_url 默认值
  - File: backend/app/services/sandbox_providers/types.py
  - 将 `preview_base_url: str = "http://192.168.1.44"` 改为 `preview_base_url: str`
  - 添加文档注释说明该参数为必需参数
  - Purpose: 消除配置重复定义，强制使用单一配置源
  - _Leverage: backend/app/core/config.py (Settings.DOCKER_PREVIEW_BASE_URL), backend/app/services/sandbox_providers/factory.py (create_docker_config)_
  - _Requirements: 1, 2, 3_
  - _Prompt: |
      Implement the task for spec docker-config-refactor, first run spec-workflow-guide to get the workflow guide then implement the task:

      Role: Python Backend Developer specializing in dataclasses and configuration management
      Task: Remove the default value from DockerConfig.preview_base_url field in backend/app/services/sandbox_providers/types.py, changing it from `preview_base_url: str = "http://192.168.1.44"` to `preview_base_url: str` (required parameter), and add a docstring comment explaining this parameter is required and should be obtained from Settings.DOCKER_PREVIEW_BASE_URL via the create_docker_config() factory function
      Restrictions: Do not modify any other fields in DockerConfig, do not change the dataclass decorator, maintain existing type annotations, verify that create_docker_config() in factory.py already passes this parameter correctly (no changes needed to factory.py)
      Success: The preview_base_url field has no default value, proper documentation added, code maintains backward compatibility through the factory function, all existing code using create_docker_config() continues to work
      Instructions: Start by editing tasks.md to change this task from [ ] to [-], then implement the changes, test that existing code still works, log the implementation using log-implementation tool with full artifacts details, and finally change this task from [-] to [x]

- [x] 2. 查找并更新测试文件中的 DockerConfig 实例化
  - File: backend/tests/conftest.py, backend/tests/**/*test*.py
  - 查找所有直接实例化 `DockerConfig()` 的地方
  - 更新为显式传入 `preview_base_url` 参数，或使用 `create_docker_config()` 工厂函数
  - Purpose: 确保测试代码与新的必需参数兼容
  - _Leverage: backend/app/services/sandbox_providers/factory.py (create_docker_config), backend/app/core/config.py (get_settings)_
  - _Requirements: 3_
  - _Prompt: |
      Implement the task for spec docker-config-refactor, first run spec-workflow-guide to get the workflow guide then implement the task:

      Role: QA Engineer and Python Developer with expertise in test fixture management
      Task: Search for all DockerConfig instantiations in test files (using grep/ripgrep), and update them to either explicitly pass the preview_base_url parameter or use the create_docker_config() factory function from backend/app/services/sandbox_providers/factory.py, particularly check and update backend/tests/conftest.py if it contains a docker_config fixture
      Restrictions: Do not modify production code (only test files), ensure all tests can create DockerConfig instances, use factory function where possible for consistency, maintain test isolation
      Success: All test files can instantiate DockerConfig without errors, tests use consistent configuration approach, no test failures due to missing preview_base_url parameter, pytest runs successfully
      Instructions: Start by editing tasks.md to change this task from [ ] to [-], then search for DockerConfig usage in tests, update each instance, run tests to verify, log the implementation using log-implementation tool with full artifacts details, and finally change this task from [-] to [x]

- [x] 3. 验证配置流程并运行测试
  - File: backend/tests/
  - 运行相关测试验证修改正确性
  - 验证配置从 .env → Settings → create_docker_config() → DockerConfig → Provider 的流程
  - Purpose: 确保重构后系统正常工作
  - _Leverage: docker compose -f docker-compose.test.yml, pytest, backend/app/core/config.py (get_settings)_
  - _Requirements: 3_
  - _Prompt: |
      Implement the task for spec docker-config-refactor, first run spec-workflow-guide to get the workflow guide then implement the task:

      Role: QA Engineer with expertise in integration testing and Docker-based testing
      Task: Run the full test suite using docker compose -f docker-compose.test.yml or pytest directly, verify that all Docker-related tests pass, confirm the configuration flow works correctly from environment variables through Settings to DockerConfig to LocalDockerProvider, and test the get_preview_links() method to ensure it uses the correct preview_base_url
      Restrictions: Must run all sandbox provider tests, do not skip failing tests, verify in a clean environment, document any test failures with specific error messages
      Success: All tests pass, configuration flow is verified end-to-end, get_preview_links() returns correct URLs with DOCKER_PREVIEW_BASE_URL, no regressions in Docker sandbox functionality
      Instructions: Start by editing tasks.md to change this task from [ ] to [-], then run tests, investigate any failures, fix issues if needed, log the implementation using log-implementation tool with full artifacts details, and finally change this task from [-] to [x]
