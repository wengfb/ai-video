# AI Video - Claude Code 项目指南

## 项目概述

AI 视频制作应用，使用 Claude 作为语义翻译器，将自然语言描述转换为 ComfyUI 可执行参数。

## 技术栈

- **前端**: Next.js + React + TypeScript
- **后端**: FastAPI + Python
- **数据库**: PostgreSQL
- **缓存/队列**: Redis + Celery
- **对象存储**: MinIO
- **向量搜索**: Milvus
- **AI 翻译**: Claude Code (MCP Server)
- **视频生成**: ComfyUI + AnimateDiff (端脑云)

## 项目结构

```
ai-video/
├── docs/                    # 文档
│   ├── PROJECT_PLAN.md      # 项目规划文档
│   └── DEVELOPMENT_PROGRESS.md  # 开发进度
├── backend/                 # FastAPI 后端 (待创建)
├── frontend/                # Next.js 前端 (待创建)
└── CLAUDE.md               # 本文件
```

## 核心概念

### Claude 参数翻译层
Claude 作为语义翻译器，将分镜描述转换为 ComfyUI workflow_json：
- 输入：分镜描述 + 角色资产 + 场景资产 + 工作流模板
- 输出：完整的 ComfyUI workflow_json

### 端脑云集成
使用端脑云 API 管理 ComfyUI 云端 GPU 实例：
- 创建实例: `POST /user/missions/batch`
- 查询状态: `GET /user/missions/{id}`
- 关闭实例: `POST /user/missions/close`

## 开发规范

### 代码风格
- Python: 遵循 PEP 8，使用 type hints
- TypeScript: 使用 ESLint + Prettier
- 异步优先：FastAPI 路由和服务层使用 async/await

### 命名约定
- 数据库表：snake_case (如 `generation_task`)
- API 路由：kebab-case (如 `/api/lora-training`)
- Python 类：PascalCase (如 `GenerationTask`)

### 提交规范
- feat: 新功能
- fix: 修复 bug
- docs: 文档更新
- refactor: 重构
- test: 测试相关

## 关键文档

- [项目规划](docs/PROJECT_PLAN.md) - 完整的系统设计
- [开发进度](docs/DEVELOPMENT_PROGRESS.md) - 任务跟踪

## 常用命令

```bash
# 后端 (待配置)
cd backend
uvicorn main:app --reload

# 前端 (待配置)
cd frontend
npm run dev
```
