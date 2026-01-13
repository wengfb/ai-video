# Claude Agent SDK 文档

> 注意：Claude Code SDK 已更名为 Claude Agent SDK，反映了该 SDK 在构建 AI 代理方面的更广泛能力。

## 一、概述

Claude Agent SDK 允许你构建能够自主执行任务的 AI 代理，包括：
- 读取文件
- 执行命令
- 搜索网络
- 编辑代码

SDK 提供了与 Claude Code 相同的核心功能、代理循环和上下文管理，支持 Python 和 TypeScript。

## 二、安装

```bash
# Python (需要 Python 3.10+)
pip install claude-agent-sdk

# TypeScript/Node.js
npm install @anthropic-ai/claude-agent-sdk
```

SDK 安装包含 Claude Code CLI，无需单独安装。

## 三、基础用法

### 3.1 简单查询

```python
import anyio
from claude_agent_sdk import query, AssistantMessage, TextBlock

async def simple_query():
    async for message in query(prompt="What is 2 + 2?"):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)

anyio.run(simple_query)
```

### 3.2 带配置选项的查询

```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    system_prompt="You are a Python expert",
    allowed_tools=["Read", "Write", "Bash"],
    permission_mode="acceptEdits",
    cwd="/path/to/project",
    max_turns=5
)

async for message in query(
    prompt="Create a hello.py file",
    options=options
):
    print(message)
```

### 3.3 会话管理（多轮对话）

```python
from claude_agent_sdk import ClaudeSDKClient, AssistantMessage, TextBlock

async def conversation():
    async with ClaudeSDKClient() as client:
        # 第一个问题
        await client.query("What's the capital of France?")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

        # 后续问题 - Claude 记住上下文
        await client.query("What's the population of that city?")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")
```

## 四、配置选项 (ClaudeAgentOptions)

### 4.1 主要参数

| 参数 | 类型 | 说明 |
|-----|------|-----|
| `allowed_tools` | list[str] | 允许使用的工具列表 |
| `disallowed_tools` | list[str] | 禁止使用的工具列表 |
| `system_prompt` | str | 自定义系统提示词 |
| `max_turns` | int | 最大对话轮数 |
| `permission_mode` | str | 权限模式 |
| `model` | str | 使用的模型 |
| `cwd` | str | 工作目录 |
| `output_format` | dict | 结构化输出格式 |
| `mcp_servers` | dict | MCP 服务器配置 |

### 4.2 权限模式 (PermissionMode)

| 模式 | 说明 |
|-----|------|
| `default` | 标准权限行为 |
| `acceptEdits` | 自动接受文件编辑 |
| `plan` | 规划模式，不执行 |
| `bypassPermissions` | 绕过所有权限检查（谨慎使用） |

## 五、内置工具

| 工具 | 说明 |
|-----|------|
| `Read` | 读取工作目录中的文件 |
| `Write` | 创建新文件 |
| `Edit` | 精确编辑现有文件 |
| `Bash` | 运行终端命令、脚本、git 操作 |
| `Glob` | 按模式查找文件 (`**/*.ts`, `src/**/*.py`) |
| `Grep` | 使用正则搜索文件内容 |
| `WebSearch` | 搜索网络获取最新信息 |
| `WebFetch` | 获取和解析网页内容 |

### 工具使用示例

```python
from claude_agent_sdk import query, ClaudeAgentOptions

# 只读分析
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Grep"]
)

# 代码分析和修改
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Edit", "Glob"]
)

# 完全自动化
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Edit", "Bash", "Glob", "Grep"]
)
```

## 六、自定义工具 (MCP Server)

### 6.1 定义自定义工具

```python
from claude_agent_sdk import tool, create_sdk_mcp_server
from typing import Any

@tool("calculate", "Perform calculations", {"expression": str})
async def calculate(args: dict[str, Any]) -> dict[str, Any]:
    result = eval(args["expression"])
    return {
        "content": [{"type": "text", "text": f"Result: {result}"}]
    }

@tool("get_time", "Get current time", {})
async def get_time(args: dict[str, Any]) -> dict[str, Any]:
    from datetime import datetime
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "content": [{"type": "text", "text": f"Current time: {current_time}"}]
    }
```

### 6.2 创建 MCP Server 并使用

```python
# 创建 MCP Server
my_server = create_sdk_mcp_server(
    name="utilities",
    version="1.0.0",
    tools=[calculate, get_time]
)

# 配置并使用
options = ClaudeAgentOptions(
    mcp_servers={"utils": my_server},
    allowed_tools=[
        "mcp__utils__calculate",
        "mcp__utils__get_time"
    ]
)
```

## 七、结构化输出

使用 JSON Schema 定义输出格式，确保返回结构化数据。

```python
from claude_agent_sdk import query

schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "scenes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "scene_number": {"type": "integer"},
                    "description": {"type": "string"},
                    "duration": {"type": "number"}
                }
            }
        }
    },
    "required": ["title", "scenes"]
}

async for message in query(
    prompt="为一个30秒的产品广告生成分镜脚本",
    options={
        "output_format": {
            "type": "json_schema",
            "schema": schema
        }
    }
):
    if hasattr(message, 'structured_output'):
        print(message.structured_output)
```

## 八、消息类型

| 类型 | 说明 |
|-----|------|
| `UserMessage` | 用户消息 |
| `AssistantMessage` | Claude 的回复 |
| `SystemMessage` | 系统消息 |
| `ResultMessage` | 最终结果，包含统计信息 |

### ResultMessage 包含的信息

- `duration_ms`: 执行时长
- `num_turns`: 对话轮数
- `total_cost_usd`: 总费用
- `session_id`: 会话 ID
- `result`: 文本结果
- `structured_output`: 结构化输出（如果配置了）

## 九、在 ai-video 项目中的应用

### 9.1 剧本生成服务

```python
from claude_agent_sdk import query, ClaudeAgentOptions

SCRIPT_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "synopsis": {"type": "string"},
        "scenes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "scene_number": {"type": "integer"},
                    "location": {"type": "string"},
                    "description": {"type": "string"},
                    "characters": {"type": "array", "items": {"type": "string"}},
                    "dialogue": {"type": "array", "items": {"type": "object"}}
                }
            }
        }
    },
    "required": ["title", "scenes"]
}

async def generate_script(project_context: dict) -> dict:
    """根据项目上下文生成剧本"""
    prompt = f"""
    根据以下设定生成视频剧本：
    - 世界观：{project_context['world_setting']}
    - 角色：{project_context['characters']}
    - 风格：{project_context['style']}
    """

    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            output_format={"type": "json_schema", "schema": SCRIPT_SCHEMA},
            max_turns=3
        )
    ):
        if hasattr(message, 'structured_output'):
            return message.structured_output
```

### 9.2 分镜生成服务

```python
STORYBOARD_SCHEMA = {
    "type": "object",
    "properties": {
        "shots": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "shot_number": {"type": "integer"},
                    "description": {"type": "string"},
                    "duration": {"type": "number"},
                    "camera": {"type": "string"},
                    "characters": {"type": "array"},
                    "dialogue": {"type": "string"}
                }
            }
        }
    }
}

async def generate_storyboard(script: dict) -> dict:
    """根据剧本生成分镜"""
    async for message in query(
        prompt=f"将以下剧本转换为详细分镜：{script}",
        options=ClaudeAgentOptions(
            output_format={"type": "json_schema", "schema": STORYBOARD_SCHEMA}
        )
    ):
        if hasattr(message, 'structured_output'):
            return message.structured_output
```

### 9.3 自主视频生成服务（核心）

Claude Agent 作为自主执行者，直接调用工具完成整个生成流程。

#### MCP 工具定义

```python
from claude_agent_sdk import tool, create_sdk_mcp_server
import json

@tool("get_project_info", "获取项目完整信息", {"project_id": str})
async def get_project_info(args):
    project = await db.get_project(args["project_id"])
    return {"content": [{"type": "text", "text": json.dumps(project.to_dict())}]}

@tool("get_storyboard", "获取分镜脚本", {"episode_id": str})
async def get_storyboard(args):
    storyboard = await db.get_storyboard(args["episode_id"])
    return {"content": [{"type": "text", "text": json.dumps(storyboard)}]}

@tool("get_character_assets", "获取角色参考图", {"character_id": str})
async def get_character_assets(args):
    assets = await asset_hub.get_character_assets(args["character_id"])
    return {"content": [{"type": "text", "text": json.dumps(assets)}]}

@tool("list_workflows", "列出可用工作流", {"category": str})
async def list_workflows(args):
    workflows = await db.list_workflows(category=args.get("category"))
    return {"content": [{"type": "text", "text": json.dumps(workflows)}]}

@tool("execute_workflow", "执行 ComfyUI 工作流", {
    "workflow_id": str,
    "params": dict
})
async def execute_workflow(args):
    result = await comfyui_client.execute(
        args["workflow_id"],
        args["params"]
    )
    return {"content": [{"type": "text", "text": json.dumps(result)}]}

@tool("save_generated_asset", "保存生成结果", {
    "storyboard_id": str,
    "asset_url": str,
    "asset_type": str
})
async def save_generated_asset(args):
    asset = await asset_hub.save(
        url=args["asset_url"],
        type=args["asset_type"],
        metadata={"storyboard_id": args["storyboard_id"]}
    )
    return {"content": [{"type": "text", "text": f"已保存，资产ID: {asset.id}"}]}

#### 创建 MCP Server

```python
ai_video_server = create_sdk_mcp_server(
    name="ai-video",
    version="1.0.0",
    tools=[
        get_project_info,
        get_storyboard,
        get_character_assets,
        list_workflows,
        execute_workflow,
        save_generated_asset
    ]
)
```

#### 启动自主生成任务

```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    mcp_servers={"ai-video": ai_video_server},
    allowed_tools=[
        "mcp__ai-video__get_project_info",
        "mcp__ai-video__get_storyboard",
        "mcp__ai-video__get_character_assets",
        "mcp__ai-video__list_workflows",
        "mcp__ai-video__execute_workflow",
        "mcp__ai-video__save_generated_asset"
    ],
    permission_mode="acceptEdits",
    max_turns=50
)

async def start_video_generation(project_id: str, episode_id: str):
    """启动自主视频生成任务"""
    prompt = f"""
    你是视频制作助手，请完成以下任务：

    1. 获取项目 {project_id} 的完整信息
    2. 获取第 {episode_id} 集的分镜脚本
    3. 对于每个分镜：
       - 分析需要的角色和场景
       - 获取角色参考图
       - 选择合适的工作流
       - 执行生成
       - 保存结果

    注意：保持角色一致性，使用 IP-Adapter
    """

    async for message in query(prompt=prompt, options=options):
        print(message)  # Claude 自动完成整个流程
```

#### 工作流程示意

```
Claude 收到任务
    │
    ├─► 调用 get_project_info("proj_123")
    │   └─► 获得项目设定、角色列表
    │
    ├─► 调用 get_storyboard("ep_001")
    │   └─► 获得 10 个分镜
    │
    └─► 遍历每个分镜：
        ├─► 调用 get_character_assets("char_A")
        ├─► 调用 list_workflows("image")
        ├─► 自主决策：使用 "sd_ipadapter" 工作流
        ├─► 调用 execute_workflow(...)
        └─► 调用 save_generated_asset(...)
```

## 十、注意事项

1. **API Key**: 需要设置 `ANTHROPIC_API_KEY` 环境变量
2. **费用控制**: 使用 `max_turns` 限制对话轮数
3. **权限管理**: 生产环境谨慎使用 `bypassPermissions`
4. **异步编程**: SDK 基于异步，需要使用 `async/await`
5. **错误处理**: 检查 `ResultMessage.is_error` 处理错误情况
