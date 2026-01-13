# AI 视频制作应用 - 开发进度管理

## 项目状态总览

| 阶段 | 状态 | 进度 |
|-----|------|-----|
| 阶段 1：基础框架 | 未开始 | 0% |
| 阶段 2：项目管理 + 资产集成 | 未开始 | 0% |
| 阶段 3：Claude 集成 | 未开始 | 0% |
| 阶段 4：ComfyUI 集成 | 未开始 | 0% |
| 阶段 5：视频生成 | 未开始 | 0% |
| 阶段 6：智能决策 | 未开始 | 0% |

---

## 阶段 1：基础框架

### 1.1 后端框架搭建
- [ ] FastAPI 项目初始化
- [ ] 目录结构规划
- [ ] 配置管理（环境变量、配置文件）
- [ ] 日志系统配置
- [ ] 异常处理框架

### 1.2 数据库设计与迁移
- [ ] PostgreSQL 连接配置
- [ ] SQLAlchemy 模型定义
- [ ] Alembic 迁移脚本
- [ ] 基础表创建（Project, Episode, Script 等）

### 1.3 前端框架搭建
- [ ] Next.js 项目初始化
- [ ] 路由结构规划
- [ ] 布局组件
- [ ] UI 组件库选择与配置

### 1.4 基础设施
- [ ] Redis 连接配置
- [ ] Celery Worker 配置
- [ ] MinIO 对象存储配置

---

## 阶段 2：项目管理 + 资产集成

### 2.1 项目管理模块
- [ ] Project CRUD API
- [ ] 项目配置管理
- [ ] 项目状态流转

### 2.2 内容创作模块
- [ ] 世界观设定 CRUD
- [ ] 角色管理 CRUD
- [ ] 场景管理 CRUD
- [ ] 剧本编辑功能

### 2.3 资产管理模块
- [ ] 集成 asset-hub API（或复用代码）
- [ ] 资产上传与管理
- [ ] 资产与项目关联

### 2.4 LoRA 管理模块
- [ ] LoraAsset 数据模型
- [ ] LoRA 资产 CRUD API
- [ ] LoRA 文件上传与存储
- [ ] LoRA 预览图管理

---

## 阶段 3：Claude 集成

### 3.1 MCP Server 开发
- [ ] MCP Server 框架搭建
- [ ] translate_storyboard 工具实现
- [ ] list_loras 工具实现
- [ ] select_lora_for_character 工具实现

### 3.2 对话界面
- [ ] AI 对话组件
- [ ] 对话历史管理
- [ ] 流式响应支持

### 3.3 内容生成功能
- [ ] 剧本生成
- [ ] 分镜生成（结构化 JSON 输出）

---

## 阶段 4：ComfyUI 集成

### 4.1 端脑云服务集成
- [ ] CephalonCloudService 实现
- [ ] 实例创建与管理
- [ ] 状态轮询机制
- [ ] 实例池管理策略

### 4.2 工作流管理
- [ ] ComfyWorkflow 数据模型
- [ ] 工作流模板 CRUD
- [ ] 工作流参数配置

### 4.3 任务执行
- [ ] GenerationTask 数据模型
- [ ] 任务提交与执行
- [ ] 结果获取与存储

---

## 阶段 5：视频生成

### 5.1 分镜到视频
- [ ] AnimateDiff 工作流集成
- [ ] 视频片段生成
- [ ] 一致性控制（IP-Adapter）

### 5.2 视频合成
- [ ] FFmpeg 集成
- [ ] 视频片段拼接
- [ ] 字幕叠加
- [ ] 音频合成

### 5.3 LoRA 训练（可选）
- [ ] LoraTrainingTask 数据模型
- [ ] 训练任务创建与管理
- [ ] 训练进度监控
- [ ] 训练结果处理

---

## 阶段 6：智能决策

### 6.1 Claude 参数翻译层
- [ ] 语义理解优化
- [ ] 工作流自动选择
- [ ] 参数生成优化

### 6.2 任务编排
- [ ] TaskDAG 数据模型
- [ ] DAG 调度器实现
- [ ] 资源管理器
- [ ] 重试与恢复机制

---

## 开发日志

### 2026-01-13
- 完成项目规划文档 (`PROJECT_PLAN.md`)
- 设计 LoRA 资产管理模块
- 集成端脑云 GPU 服务方案
- 确定 Claude Code MCP 集成方式
- 创建开发进度管理文档
- 项目上传至 GitHub: https://github.com/wengfb/ai-video
- 完成 Claude Agent SDK 调研（见下方技术参考）

---

## 技术债务 & 待办事项

| 优先级 | 事项 | 状态 |
|-------|-----|------|
| 高 | ~~确认 Claude Code SDK 具体 API~~ | ✅ 已完成 |
| 中 | 音频方案选择（Edge-TTS vs GPT-SoVITS） | 待决定 |
| 中 | AnimateDiff 参数调优 | 待研究 |

---

## 里程碑

| 里程碑 | 目标 | 状态 |
|-------|-----|------|
| M1 | 基础框架可运行 | 未开始 |
| M2 | 项目管理功能完成 | 未开始 |
| M3 | 单张图片生成可用 | 未开始 |
| M4 | 视频片段生成可用 | 未开始 |
| M5 | 完整视频生成流程 | 未开始 |

---

## 技术参考

### Claude Agent SDK (Python)

**仓库**: https://github.com/anthropics/claude-agent-sdk-python

**安装**:
```bash
pip install claude-agent-sdk
```

**核心 API**:

#### 1. query() - 简单查询
```python
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(prompt="Hello Claude"):
    print(message)
```

#### 2. ClaudeSDKClient - 交互式对话
```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

async with ClaudeSDKClient(options=options) as client:
    await client.query("Your prompt")
    async for msg in client.receive_response():
        print(msg)
```

#### 3. 自定义工具 (SDK MCP Server)
```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("greet", "Greet a user", {"name": str})
async def greet_user(args):
    return {"content": [{"type": "text", "text": f"Hello, {args['name']}!"}]}

server = create_sdk_mcp_server(name="my-tools", tools=[greet_user])
```

#### 4. Hooks - 钩子函数
```python
options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [HookMatcher(matcher="Bash", hooks=[check_bash_command])],
    }
)
```

**关键配置项 (ClaudeAgentOptions)**:
- `system_prompt`: 系统提示词
- `max_turns`: 最大对话轮数
- `allowed_tools`: 允许的工具列表
- `permission_mode`: 权限模式 (`acceptEdits` 等)
- `cwd`: 工作目录
- `mcp_servers`: MCP 服务器配置
