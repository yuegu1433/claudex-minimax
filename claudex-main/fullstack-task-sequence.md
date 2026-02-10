# 全栈页面任务编写时序图

## 完整的全栈开发任务流程

```mermaid
sequenceDiagram
    participant U as 用户界面 (React)
    participant F as 前端服务
    participant A as API网关
    participant CS as 聊天服务
    participant AS as AI代理服务
    participant SS as 沙盒服务
    participant DP as Docker提供商
    participant E2B as E2B提供商
    participant C as Celery Worker
    participant AI as Claude AI
    participant SB as 沙盒容器
    participant IDE as Monaco编辑器
    participant WS as WebSocket
    participant FS as 文件系统

    Note over U, FS: 1. 用户提出全栈开发任务
    U->>F: 输入任务需求
    Note right of U: "创建一个React + FastAPI的待办事项应用"
    F->>F: 解析任务类型 (全栈开发)
    F->>F: 生成任务ID

    Note over U, FS: 2. AI任务理解与规划
    F->>A: POST /api/v1/chat/chats/{id}/stream
    A->>CS: 启动流式聊天
    CS->>C: 提交AI处理任务
    C->>AI: 发送完整任务上下文
    AI-->>C: 返回任务分析结果

    Note over U, FS: 3. AI生成开发计划
    loop 规划生成
        AI->>AI: 分析需求
        AI->>AI: 生成任务分解
        AI->>AI: 确定技术栈
        C->>F: 流式输出计划 (SSE)
        F->>U: 实时显示规划进度
    end

    Note over U, FS: 4. 创建沙盒环境
    C->>SS: 创建开发环境
    SS->>SS: 检查沙盒配置
    alt 使用Docker沙盒
        SS->>DP: 创建Docker沙盒
        DP->>SB: 启动开发容器
        DP->>SB: 安装必要工具 (Node.js, Python等)
        SB-->>DP: 返回环境就绪
        DP-->>SS: 返回沙盒ID
    else 使用E2B云端
        SS->>E2B: 创建云端沙盒
        E2B-->>SS: 返回访问令牌
    end

    Note over U, FS: 5. 前端开发阶段
    C->>AI: 请求前端代码生成
    AI-->>C: 返回React组件代码
    C->>SB: 写入前端文件
    Note right of C: src/App.tsx, src/components/, src/hooks/

    loop 前端文件生成
        C->>SB: 创建组件文件
        SB->>SB: 写入代码
        SB->>FS: 保存到工作目录
        C->>F: 推送文件更新事件 (WebSocket)
        F->>IDE: 更新编辑器内容
        F->>U: 实时显示代码
    end

    Note over U, FS: 6. 后端API开发
    C->>AI: 请求后端API生成
    AI-->>C: 返回FastAPI代码
    C->>SB: 写入后端文件
    Note right of C: app/main.py, app/api/endpoints/, app/models/

    loop 后端文件生成
        C->>SB: 创建API文件
        SB->>SB: 写入代码
        SB->>FS: 保存到工作目录
        C->>F: 推送文件更新
        F->>IDE: 更新编辑器视图
    end

    Note over U, FS: 7. 数据库模型创建
    C->>AI: 请求数据库模型
    AI-->>C: 返回SQLAlchemy模型
    C->>SB: 写入模型文件
    Note right of C: models.py, migrations/

    Note over U, FS: 8. 代码执行与测试
    C->>SB: 执行后端测试
    SB->>SB: 运行pytest
    SB->>SB: 生成测试报告
    C->>F: 返回测试结果 (SSE)
    F->>U: 显示测试状态

    Note over U, FS: 9. 前端构建与运行
    C->>SB: 执行npm install
    SB->>SB: 安装依赖
    C->>SB: 执行npm run build
    SB->>SB: 构建生产版本
    SB->>SB: 启动开发服务器

    Note over U, FS: 10. 实时预览生成
    C->>SS: 生成预览链接
    SS->>SB: 启动预览服务
    SB->>SS: 返回预览URL
    SS->>F: 返回预览链接
    F->>U: 显示实时预览
    Note right of F: http://192.168.1.44:32808

    Note over U, FS: 11. 交互式调试
    U->>IDE: 编辑代码
    IDE->>C: 触发重新编译 (WebSocket)
    C->>SB: 执行热重载
    SB->>SB: 重新构建
    SB->>F: 推送更新事件
    F->>U: 实时预览更新

    Note over U, FS: 12. API集成测试
    C->>SB: 调用前端API
    SB->>SB: 发送HTTP请求
    SB->>SB: 接收API响应
    C->>F: 返回API测试结果
    F->>U: 显示集成状态

    Note over U, FS: 13. 任务完成与打包
    AI->>AI: 生成最终报告
    C->>SB: 创建项目打包
    SB->>FS: 生成ZIP文件
    C->>F: 返回下载链接
    F->>U: 提供项目下载

    Note over U, FS: 14. 资源清理
    C->>SS: 清理沙盒环境
    SS->>SB: 停止容器
    SS->>SB: 清理临时文件
    SB-->>SS: 环境已清理
    SS-->>C: 返回清理确认

    Note over U, FS: 15. 持久化存储
    C->>FS: 保存最终代码
    FS->>FS: 归档到存储目录
    C->>F: 推送完成事件
    F->>U: 显示任务完成
```

## 代码编辑与实时协作时序图

```mermaid
sequenceDiagram
    participant U as 用户
    participant IDE as Monaco编辑器
    participant F as 前端服务
    participant WS as WebSocket
    participant C as Celery Worker
    participant SB as 沙盒容器
    participant AI as AI助手
    participant FS as 文件系统

    Note over U, FS: 用户开始编辑代码
    U->>IDE: 输入代码
    IDE->>IDE: 语法高亮
    IDE->>IDE: 自动补全

    Note over U, FS: 实时同步到沙盒
    IDE->>F: 文件变更事件
    F->>WS: 广播文件更新
    WS->>C: 接收文件变更
    C->>SB: 写入沙盒文件系统
    SB->>FS: 更新文件

    Note over U, FS: 代码执行
    U->>IDE: 点击运行按钮
    IDE->>F: 发送执行请求
    F->>C: 触发代码执行
    C->>SB: 执行代码
    SB->>SB: 运行命令
    SB->>C: 返回执行结果

    Note over U, FS: 实时反馈
    C->>WS: 推送执行输出
    WS->>F: 广播结果
    F->>IDE: 更新输出面板
    IDE->>U: 显示执行结果

    Note over U, FS: AI辅助编程
    U->>IDE: 选择代码片段
    IDE->>F: 发送AI请求
    F->>C: 调用AI助手
    C->>AI: 生成建议
    AI--代码建议
    C>>C: 返回->>F: 推送AI建议
    F->>IDE: 显示建议
    IDE->>U: 展示AI建议
```

## 多文件项目管理时序图

```mermaid
sequenceDiagram
    participant U as 用户
    participant FS as 文件浏览器
    participant IDE as 代码编辑器
    participant F as 前端服务
    participant C as Celery Worker
    participant SB as 沙盒容器
    participant AI as 代码分析器
    participant VCS as 版本控制

    Note over U, VCS: 文件管理操作
    U->>FS: 创建新文件
    FS->>F: 文件操作请求
    F->>C: 验证文件操作
    C->>SB: 创建文件
    SB->>FS: 返回文件列表
    FS->>U: 更新文件树

    Note over U, VCS: 文件依赖分析
    U->>IDE: 打开文件
    IDE->>F: 请求文件内容
    F->>C: 获取文件数据
    C->>SB: 读取文件
    SB->>C: 返回文件内容
    C->>AI: 分析依赖关系
    AI-->>C: 返回依赖图
    C->>F: 推送分析结果
    F->>IDE: 显示依赖提示

    Note over U, VCS: 批量操作
    U->>FS: 选择多个文件
    FS->>F: 批量操作请求
    F->>C: 执行批量操作
    C->>SB: 批量文件系统操作
    SB->>C: 返回操作结果
    C->>F: 推送更新事件
    F->>FS: 更新文件状态

    Note over U, VCS: 版本控制
    C->>VCS: 创建提交
    VCS->>VCS: 生成diff
    VCS->>C: 返回版本信息
    C->>F: 推送版本历史
    F->>U: 显示提交记录
```

## 错误处理与调试时序图

```mermaid
sequenceDiagram
    participant U as 用户
    participant IDE as 编辑器
    participant F as 前端服务
    participant C as Celery Worker
    participant SB as 沙盒容器
    participant AI as 调试助手
    participant LOG as 日志系统

    Note over U, LOG: 错误检测
    C->>SB: 执行代码
    SB->>SB: 检测到错误
    SB->>C: 返回错误信息
    C->>LOG: 记录错误日志

    Note over U, LOG: 错误分析
    C->>AI: 发送错误上下文
    AI->>AI: 分析错误原因
    AI->>AI: 生成解决方案
    AI-->>C: 返回调试建议
    C->>F: 推送错误信息

    Note over U, LOG: 错误展示
    F->>IDE: 显示错误面板
    IDE->>U: 高亮错误行
    IDE->>U: 显示错误信息

    Note over U, LOG: 智能修复
    U->>IDE: 请求自动修复
    IDE->>F: 发送修复请求
    F->>C: 调用修复助手
    C->>AI: 生成修复代码
    AI-->>C: 返回修复建议
    C->>F: 推送修复方案
    F->>IDE: 显示修复选项
    IDE->>U: 应用修复

    Note over U, LOG: 重新执行
    C->>SB: 重新运行代码
    SB->>SB: 验证修复结果
    SB->>C: 返回执行状态
    C->>F: 推送成功消息
    F->>IDE: 清除错误标记
    IDE->>U: 显示成功状态
```

## 部署与发布时序图

```mermaid
sequenceDiagram
    participant U as 用户
    participant F as 前端服务
    participant C as Celery Worker
    participant SB as 沙盒容器
    participant CI as CI/CD系统
    participant REG as 容器镜像仓库
    participant PROD as 生产环境

    Note over U, PROD: 开始部署流程
    U->>F: 点击部署按钮
    F->>C: 启动部署任务
    C->>SB: 构建项目

    Note over U, PROD: 构建阶段
    SB->>SB: 安装依赖
    SB->>SB: 运行测试
    SB->>SB: 编译代码
    SB->>SB: 生成构建产物

    Note over U, PROD: 容器化
    C->>SB: 创建Dockerfile
    SB->>SB: 构建镜像
    SB->>REG: 推送镜像
    REG-->>SB: 返回镜像标签

    Note over U, PROD: 部署到生产
    C->>CI: 触发部署流水线
    CI->>PROD: 拉取镜像
    CI->>PROD: 启动容器
    CI->>PROD: 配置负载均衡
    CI->>PROD: 运行健康检查

    Note over U, PROD: 部署验证
    PROD->>CI: 返回健康状态
    CI->>C: 推送部署状态
    C->>F: 更新部署状态
    F->>U: 显示部署结果

    Note over U, PROD: 回滚机制
    alt 部署失败
        CI->>PROD: 自动回滚
        PROD->>CI: 回滚完成
        CI->>C: 推送回滚状态
        C->>F: 通知失败
        F->>U: 显示错误信息
    else 部署成功
        CI->>C: 推送成功状态
        C->>F: 更新状态
        F->>U: 显示成功
    end
```

## 性能监控与分析时序图

```mermaid
sequenceDiagram
    participant U as 用户
    participant F as 前端服务
    participant C as Celery Worker
    participant SB as 沙盒容器
    participant MON as 监控系统
    participant AI as 性能分析器

    Note over U, MON: 性能数据收集
    SB->>MON: 收集性能指标
    MON->>MON: 存储监控数据
    SB->>C: 推送实时指标

    Note over U, MON: 性能分析
    C->>AI: 发送性能数据
    AI->>AI: 分析瓶颈
    AI->>AI: 生成优化建议
    AI-->>C: 返回分析报告
    C->>F: 推送性能报告

    Note over U, MON: 实时监控面板
    F->>U: 显示性能仪表盘
    Note right of F: CPU、内存、响应时间

    Note over U, MON: 告警机制
    MON->>MON: 检测异常
    MON->>C: 发送告警
    C->>F: 推送告警信息
    F->>U: 显示告警通知

    Note over U, MON: 优化建议
    C->>AI: 请求优化建议
    AI-->>C: 生成代码优化
    C->>F: 推送优化方案
    F->>IDE: 建议代码修改
    IDE->>U: 显示优化提示
```

## 关键流程说明

### 1. 任务理解阶段
- AI分析用户需求
- 生成技术选型
- 分解开发任务
- 估算开发时间

### 2. 环境准备阶段
- 选择沙盒提供商
- 创建隔离环境
- 安装必要工具
- 配置开发依赖

### 3. 代码编写阶段
- 前端组件生成
- 后端API开发
- 数据库模型创建
- 业务逻辑实现

### 4. 测试验证阶段
- 单元测试执行
- 集成测试验证
- 端到端测试
- 性能测试

### 5. 部署发布阶段
- 代码构建
- 容器化
- CI/CD流水线
- 生产部署

### 6. 监控维护阶段
- 性能监控
- 错误追踪
- 日志分析
- 自动扩容

---

*全栈任务时序图生成时间: 2025-12-26 10:02:57*