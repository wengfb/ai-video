# AI 视频制作应用 - 项目规划

## 一、项目概述

| 项目名称 | ai-video（暂定） |
|---------|-----------------|
| 目标用户 | 自己 + 独立创作者/自媒体 |
| 视频类型 | 短视频、AI生成视频、短剧、新闻解读、科普 |
| 核心特点 | Claude 语义翻译 + 确定性任务编排 + ComfyUI 生成后端 |

## 二、系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        前端 (Next.js/React)                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ 项目管理  │ │ 资产管理  │ │ 剧本编辑  │ │ 视频预览  │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────────┐            │
│  │ 工作流管理│ │ AI 对话  │ │ 分镜/时间线编辑器     │            │
│  └──────────┘ └──────────┘ └──────────────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      后端 API (FastAPI/Python)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ 项目服务      │  │ 剧本服务      │  │ 生成任务服务  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ 资产服务      │  │ 工作流服务    │  │ 视频合成服务  │          │
│  │ (含 LoRA)    │  │              │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              Claude 参数翻译层 (Semantic Translator)             │
│                                                                 │
│  分镜描述 + 角色/场景资产 + 工作流模板 → ComfyUI workflow_json   │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ 语义理解      │  │ 工作流选择    │  │ 参数生成      │          │
│  │ (自然语言)    │  │ (匹配最优)    │  │ (填充节点)    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    任务编排层 (Task Orchestrator)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ DAG 调度器    │  │ 资源管理器    │  │ 状态机管理    │          │
│  │ (依赖解析)    │  │ (GPU/内存)   │  │ (重试/恢复)   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│   Asset Hub      │ │ ComfyUI 云服务   │ │   音频服务 API    │
│   (本地)         │ │   (端脑云)       │ │                  │
└──────────────────┘ └──────────────────┘ └──────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        基础设施（本地）                           │
│  PostgreSQL │ Redis │ MinIO │ Milvus │ Celery Workers           │
└─────────────────────────────────────────────────────────────────┘
```

## 三、核心模块划分

### 1. 项目管理模块
```
功能：
- 项目 CRUD（创建、复制、归档）
- 项目配置（风格、一致性参数）
- 项目进度追踪
- 项目资产关联
```

### 2. 内容创作模块
```
功能：
- 世界观设定编辑
- 角色设定管理
- 场景设定管理
- 剧本/大纲编辑
- 分镜脚本生成
- AI 辅助创作（Claude）
```

### 3. 资产管理模块（复用 asset-hub）
```
功能：
- 角色图片管理
- 场景图片管理
- 参考图管理
- LoRA 模型管理
- 音频素材管理
- 智能搜索（向量检索）
```

### 4. ComfyUI 工作流模块
```
功能：
- 工作流模板管理
- 工作流参数配置
- 工作流执行调度
- 执行结果管理
```

### 5. 任务编排模块 (Task Orchestrator)
```
功能：
- DAG 任务图管理（创建、执行、取消）
- 任务依赖解析与拓扑排序
- 资源调度（GPU 内存、并发控制）
- 任务状态机管理
- 失败重试与恢复
- 人工干预入口

核心组件：
- DAGScheduler: 解析依赖，调度就绪任务
- ResourceManager: GPU/内存资源分配
- TaskExecutor: 任务执行与监控
- RetryHandler: 重试策略与指数退避
```

### 6. 视频生成模块
```
功能：
- 分镜到视频片段生成
- 一致性控制（IP-Adapter/LoRA/ControlNet）
- 视频片段合成
- 字幕叠加
- 音频合成
```

### 7. Claude 参数翻译模块
```
核心理念：Claude 作为语义翻译器，将自然语言描述转换为 ComfyUI 可执行参数

功能：
- 理解分镜描述的语义（情绪、氛围、风格）
- 自动选择最合适的工作流模板
- 生成优化的 prompt（正向/负向提示词）
- 配置 LoRA/ControlNet 参数
- 辅助创作（剧本、分镜生成）

输入：
- 分镜描述（自然语言）
- 角色资产（LoRA、参考图）
- 场景资产（参考图）
- 可用工作流模板列表

输出：
- 完整的 ComfyUI workflow_json（可直接执行）
```

## 四、数据模型设计

### 核心实体

#### Project (项目)
```
├── id: UUID
├── name: string
├── description: text
├── status: enum (draft/in_progress/completed/archived)
├── settings: JSONB
│   ├── style_preset: string (视觉风格预设)
│   ├── color_palette: string[] (配色方案)
│   ├── subtitle_style: object (字幕样式)
│   └── music_style: string (音乐风格)
├── created_at, updated_at
└── 关联: WorldSetting, Characters[], Scenes[], Episodes[]
```

#### WorldSetting (世界观设定)
```
├── id: UUID
├── project_id: FK
├── content: text (世界观描述)
├── keywords: string[] (关键词)
└── created_at, updated_at
```

#### Character (角色)
```
├── id: UUID
├── project_id: FK
├── name: string
├── description: text
├── appearance: text (外貌描述)
├── personality: text (性格描述)
├── reference_assets: UUID[] (参考图片，关联 asset-hub)
├── lora_model_id: UUID (可选，训练的 LoRA)
├── consistency_config: JSONB
│   ├── method: enum (ip_adapter/lora/controlnet)
│   └── parameters: object
└── created_at, updated_at
```

#### Scene (场景)
```
├── id: UUID
├── project_id: FK
├── name: string
├── description: text
├── reference_assets: UUID[]
├── style_config: JSONB
└── created_at, updated_at
```

#### Episode (分集/章节)
```
├── id: UUID
├── project_id: FK
├── title: string
├── synopsis: text (概要)
├── order: integer
├── status: enum
└── 关联: Script, Storyboard[], GeneratedVideos[]
```

#### Script (剧本)
```
├── id: UUID
├── episode_id: FK
├── content: text (剧本内容)
├── structured_content: JSONB (结构化剧本)
└── version: integer
```

#### Storyboard (分镜)
```
├── id: UUID
├── episode_id: FK
├── scene_number: integer
├── description: text (镜头描述)
├── duration: float (时长，秒)
├── camera_movement: string (镜头运动)
├── characters: UUID[] (出场角色)
├── scene_id: FK (场景)
├── dialogue: text (台词)
├── notes: text (备注)
├── thumbnail_asset_id: UUID (分镜缩略图)
└── generation_config: JSONB (生成配置)
```

#### ComfyWorkflow (工作流模板)
```
├── id: UUID
├── name: string
├── description: text
├── category: enum (image/video/animation)
├── workflow_json: JSONB (ComfyUI 工作流定义)
├── input_schema: JSONB (输入参数定义)
├── tags: string[]
└── created_at, updated_at
```

#### GenerationTask (生成任务)
```
├── id: UUID
├── dag_id: FK (所属 DAG)
├── storyboard_id: FK (可选)
├── workflow_id: FK
├── task_type: enum (image/video/audio/composite)
├── status: enum (见下方状态机)
├── priority: integer (0-100, 默认 50)
├── input_params: JSONB
├── output_assets: UUID[]
├── error_message: text
├── retry_count: integer (当前重试次数)
├── max_retries: integer (最大重试次数, 默认 3)
├── retry_delay: integer (重试延迟秒数)
├── timeout: integer (超时秒数)
├── resource_requirements: JSONB
│   ├── gpu_memory_mb: integer (所需显存)
│   ├── estimated_duration: integer (预估耗时秒)
│   └── priority_boost: boolean (是否优先调度)
├── version: integer (乐观锁)
├── created_at, started_at, completed_at
└── parent_task_ids: UUID[] (依赖的前置任务)

状态机定义：
┌─────────┐
│ pending │ ──────────────────────────────────────┐
└────┬────┘                                       │
     │ (依赖完成 & 资源可用)                        │
     ▼                                            │
┌─────────┐    (超时/错误)    ┌─────────┐         │
│ running │ ───────────────► │ failed  │         │
└────┬────┘                  └────┬────┘         │
     │                            │              │
     │ (成功)                     │ (retry < max)│
     ▼                            ▼              │
┌───────────┐              ┌─────────────┐       │
│ completed │              │retry_pending│───────┘
└───────────┘              └─────────────┘
                                 │
                                 │ (retry >= max)
                                 ▼
                          ┌──────────────┐
                          │manual_review │
                          └──────────────┘

状态说明：
- pending: 等待依赖完成或资源分配
- running: 正在执行
- completed: 执行成功
- failed: 执行失败（可重试）
- retry_pending: 等待重试
- manual_review: 超过重试次数，需人工干预
```

#### GeneratedVideo (生成的视频)
```
├── id: UUID
├── episode_id: FK
├── asset_id: FK (关联 asset-hub)
├── version: integer
├── composition_config: JSONB (合成配置)
└── created_at
```

#### LoraAsset (LoRA 资产)
```
├── id: UUID
├── name: string (LoRA 名称)
├── description: text (描述)
├── type: enum (character/style/concept/object)
│   - character: 角色 LoRA，用于保持人物一致性
│   - style: 风格 LoRA，用于特定画风
│   - concept: 概念 LoRA，用于特定概念/IP
│   - object: 物体 LoRA，用于特定物品
├── status: enum (pending/training/ready/failed/archived)
├── base_model: string (适配的基础模型，如 "SDXL 1.0")
├── base_model_hash: string (基础模型哈希，确保兼容性)
├── trigger_words: string[] (触发词列表)
├── recommended_weight: float (推荐权重，默认 0.8)
├── weight_range: JSONB {min: 0.3, max: 1.0} (有效权重范围)
├── file_path: string (模型文件路径，MinIO)
├── file_size: bigint (文件大小，字节)
├── file_hash: string (文件 MD5，用于校验)
├── preview_images: UUID[] (效果预览图，关联 asset-hub)
├── training_task_id: UUID (关联的训练任务，可选)
├── metadata: JSONB
│   ├── rank: integer (LoRA rank，如 32/64/128)
│   ├── alpha: float (LoRA alpha)
│   ├── network_type: string (如 "lora", "locon", "loha")
│   └── training_steps: integer (训练步数)
├── tags: string[] (标签，便于搜索)
├── usage_count: integer (使用次数统计)
├── project_id: UUID (所属项目，可选，null 表示全局可用)
├── created_by: string (创建者)
├── created_at, updated_at
└── 索引: (project_id, type), (base_model), (tags)
```

#### LoraTrainingTask (LoRA 训练任务)
```
├── id: UUID
├── name: string (任务名称)
├── lora_asset_id: UUID (关联的 LoRA 资产，训练完成后更新)
├── status: enum (preparing/queued/training/completed/failed/cancelled)
├── type: enum (character/style/concept/object)
├── base_model: string (基础模型)
├── training_images: UUID[] (训练图片，关联 asset-hub)
├── training_config: JSONB
│   ├── network_type: string ("lora"/"locon"/"loha")
│   ├── network_rank: integer (8/16/32/64/128)
│   ├── network_alpha: float
│   ├── learning_rate: float (如 1e-4)
│   ├── unet_lr: float
│   ├── text_encoder_lr: float
│   ├── max_train_steps: integer
│   ├── save_every_n_steps: integer
│   ├── batch_size: integer
│   ├── resolution: integer (如 512/768/1024)
│   ├── enable_bucket: boolean (是否启用分桶)
│   ├── caption_extension: string (".txt"/".caption")
│   └── optimizer: string ("AdamW8bit"/"Lion"等)
├── regularization_images: UUID[] (正则化图片，可选)
├── trigger_word: string (训练时使用的触发词)
├── progress: JSONB
│   ├── current_step: integer
│   ├── total_steps: integer
│   ├── current_epoch: integer
│   ├── loss: float
│   └── sample_images: string[] (训练过程中的采样图)
├── resource_usage: JSONB
│   ├── gpu_id: string
│   ├── gpu_memory_mb: integer
│   └── estimated_time_minutes: integer
├── error_message: text
├── started_at, completed_at
├── created_by: string
└── created_at, updated_at
```

#### TaskDAG (任务有向无环图)
```
├── id: UUID
├── name: string
├── episode_id: FK (可选，关联的分集)
├── status: enum (pending/running/completed/failed/cancelled)
├── trigger_type: enum (manual/scheduled/api)
├── created_by: string (创建者，user/claude_agent)
├── total_tasks: integer
├── completed_tasks: integer
├── failed_tasks: integer
├── started_at, completed_at
└── created_at, updated_at
```

## 五、技术选型建议

| 层级 | 技术选择 | 部署位置 | 理由 |
|-----|---------|---------|-----|
| 前端 | Next.js + React + TypeScript | 本地/云 | 与 asset-hub 一致 |
| 后端 | FastAPI + Python | 本地 | 与 asset-hub 一致，AI 生态好 |
| 数据库 | PostgreSQL | 本地 | 已有部署，JSONB 支持好 |
| 缓存/队列 | Redis + Celery | 本地 | 与 asset-hub 一致 |
| 对象存储 | MinIO | 本地 | 与 asset-hub 一致 |
| 向量搜索 | Milvus | 本地 | 与 asset-hub 一致 |
| AI 翻译 | Claude Code | 本地 | 复用已配置的 API 和模型 |
| 视频生成 | ComfyUI + AnimateDiff | **云端 GPU** | 端脑云 |
| LoRA 训练 | ComfyUI 训练节点 | **云端 GPU** | 端脑云 |
| 音频 | Edge-TTS / GPT-SoVITS | 本地/云 | TTS 方案 |

### ComfyUI 云服务方案（端脑云）

#### 端脑云简介

端脑云（Cephalon Cloud）是国内算力平台，通过 API 提供 ComfyUI 等 AIGC 应用的云端 GPU 资源。

#### API 能力

| API | 功能 | 端点 |
|-----|------|-----|
| 批量创建应用 | 启动 ComfyUI 实例 | POST /user/missions/batch |
| 查询应用信息 | 获取实例状态和访问地址 | GET /user/missions/{id} |
| 批量关闭应用 | 停止实例 | POST /user/missions/close |
| 负载均衡 | 多实例管理 | /load-balancer/* |

#### 任务类型

| 类型 | 参数值 | 说明 |
|-----|-------|-----|
| ComfyUI 标准版 | `comfyui_time` | 基础版本 |
| ComfyUI 高级版 | `comfyui_advance_time` | 预装更多节点 |

#### 任务状态

```
waiting → doing → suppyling → succeed
   ↓                           ↓
canceled                    failed
```

- `suppyling`：实例运行中，开始计费
- `failed`：失败不计费

## 六、MVP 实现路径

### 阶段 1：基础框架
```
- 项目结构搭建（前后端）
- 数据库模型设计与迁移
- 基础 API 框架
- 前端路由和布局
```

### 阶段 2：项目管理 + 资产集成
```
- 项目 CRUD
- 集成 asset-hub API（或直接复用代码）
- 角色/场景管理
- 资产关联
```

### 阶段 3：Claude 集成
```
- Claude Code SDK 集成
- 对话界面
- 脚本生成功能
- 分镜生成功能（结构化 JSON 输出）
```

### 阶段 4：ComfyUI 集成
```
- ComfyUI API 对接
- 工作流模板管理
- 图片生成任务
- 一致性控制（IP-Adapter 优先）
```

### 阶段 5：视频生成
```
- AnimateDiff 工作流
- 视频片段生成
- FFmpeg 合成
- 字幕叠加
```

### 阶段 6：智能决策
```
- Claude 自动选择资产
- Claude 自动选择工作流
- 参数优化
- 结果评估与重试
```

## 七、关键技术点

### 1. 端脑云集成设计

#### 1.1 集成架构

```
┌─────────────────────────────────────────┐
│         ai-video 后端                    │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │     CephalonCloudService        │   │
│  │  ├── create_instance()          │   │
│  │  ├── get_instance_status()      │   │
│  │  ├── get_comfyui_url()          │   │
│  │  └── close_instance()           │   │
│  └─────────────────────────────────┘   │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│           端脑云 API                     │
│  POST /user/missions/batch  (创建实例)  │
│  GET  /user/missions/{id}   (查询状态)  │
│  POST /user/missions/close  (关闭实例)  │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│        ComfyUI 实例 (云端 GPU)          │
│  通过返回的 URL 调用 ComfyUI API        │
└─────────────────────────────────────────┘
```

#### 1.2 工作流程

```
1. 创建实例
   POST /user/missions/batch
   {type: "comfyui_advance_time", gpu_version: "RTX4090", gpu_num: 1}
   → 返回 mission_id

2. 轮询状态
   GET /user/missions/{mission_id}
   → 等待状态变为 "suppyling"
   → 获取 ComfyUI 访问 URL

3. 提交任务
   POST {comfyui_url}/prompt
   → 提交 workflow_json

4. 获取结果
   GET {comfyui_url}/history/{prompt_id}
   → 下载生成的图片/视频

5. 关闭实例
   POST /user/missions/close
   → 停止计费
```

#### 1.3 实例管理策略

| 策略 | 说明 | 适用场景 |
|-----|------|---------|
| 按需创建 | 每次任务创建新实例 | 任务稀疏 |
| 实例池 | 预创建多个实例复用 | 任务密集 |
| 混合模式 | 保持最小实例 + 动态扩展 | 生产环境 |

### 2. 一致性控制方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|-----|-----|-----|---------|
| IP-Adapter | 无需训练，即插即用 | 相似度有限，时序一致性差 | 快速原型，单角色短片段 |
| LoRA | 高度一致 | 需要训练数据和时间 | 固定主角，长期项目 |
| ControlNet | 姿态控制精确 | 需要额外输入 | 特定动作场景 |
| 组合方案 | 综合优势 | 复杂度高 | 生产级项目 |

#### IP-Adapter 局限性警告

> **重要提示**：IP-Adapter 在视频生成中存在以下已知局限，用户需知悉：

| 局限性 | 具体表现 | 影响程度 |
|-------|---------|---------|
| 时序一致性差 | 视频帧间角色面部会漂移，几秒后可能偏离参考图 | 高 |
| 细节丢失 | 服装、配饰、体型等非面部特征难以保持 | 高 |
| 多角色困难 | 多角色场景易出现"角色克隆"或混淆 | 高 |
| 强度敏感 | 参数太高限制场景变化，太低丢失特征 | 中 |
| 分辨率影响 | 低分辨率时面部易变形 | 中 |

#### 一致性等级设计

为管理用户预期，系统提供三个一致性等级：

```
┌─────────────┬──────────────────┬─────────────────────────────┐
│ 等级        │ 技术方案          │ 适用场景                     │
├─────────────┼──────────────────┼─────────────────────────────┤
│ 低 (快速)   │ IP-Adapter only  │ 概念验证、草稿预览            │
│ 中 (标准)   │ IP-Adapter +     │ 短视频、单角色内容            │
│             │ ControlNet       │                             │
│ 高 (精确)   │ LoRA + ControlNet│ 正式作品、多集连续剧          │
│             │ + FaceSwap后处理  │                             │
└─────────────┴──────────────────┴─────────────────────────────┘
```

**建议**：MVP 阶段实现"低"和"中"等级，"高"等级需要 LoRA 训练流程支持。

### 3. LoRA 管理模块详细设计

#### 2.1 LoRA 管理 API

```
LoRA 资产 API
─────────────────────────────────────────────────
POST   /api/loras                    创建 LoRA 资产（上传已有模型）
GET    /api/loras                    列出 LoRA 资产（支持筛选）
GET    /api/loras/{id}               获取 LoRA 详情
PUT    /api/loras/{id}               更新 LoRA 信息
DELETE /api/loras/{id}               删除 LoRA
POST   /api/loras/{id}/preview       上传预览图
GET    /api/loras/{id}/download      下载 LoRA 文件

LoRA 训练 API
─────────────────────────────────────────────────
POST   /api/lora-training            创建训练任务
GET    /api/lora-training            列出训练任务
GET    /api/lora-training/{id}       获取训练任务详情
POST   /api/lora-training/{id}/start 开始训练
POST   /api/lora-training/{id}/cancel 取消训练
GET    /api/lora-training/{id}/logs  获取训练日志
GET    /api/lora-training/{id}/samples 获取训练采样图

查询参数示例
─────────────────────────────────────────────────
GET /api/loras?type=character&base_model=SDXL&project_id=xxx
GET /api/loras?tags=anime,female&status=ready
```

#### 2.2 LoRA 相关 MCP 工具

```python
# Claude Agent 可用的 LoRA 相关工具

Tool(
    name="list_loras",
    description="列出可用的 LoRA 资产",
    inputSchema={
        "type": "object",
        "properties": {
            "project_id": {"type": "string", "description": "项目ID，可选"},
            "type": {"type": "string", "enum": ["character", "style", "concept", "object"]},
            "base_model": {"type": "string", "description": "基础模型名称"},
            "tags": {"type": "array", "items": {"type": "string"}}
        }
    }
)

Tool(
    name="get_lora_info",
    description="获取 LoRA 详细信息，包括触发词和推荐权重",
    inputSchema={
        "type": "object",
        "properties": {
            "lora_id": {"type": "string", "description": "LoRA ID"}
        },
        "required": ["lora_id"]
    }
)

Tool(
    name="select_lora_for_character",
    description="为角色自动选择合适的 LoRA",
    inputSchema={
        "type": "object",
        "properties": {
            "character_id": {"type": "string"},
            "base_model": {"type": "string"}
        },
        "required": ["character_id", "base_model"]
    }
)

Tool(
    name="start_lora_training",
    description="启动 LoRA 训练任务",
    inputSchema={
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "type": {"type": "string", "enum": ["character", "style", "concept", "object"]},
            "training_images": {"type": "array", "items": {"type": "string"}},
            "trigger_word": {"type": "string"},
            "base_model": {"type": "string"},
            "config": {"type": "object", "description": "训练配置参数"}
        },
        "required": ["name", "type", "training_images", "trigger_word", "base_model"]
    }
)

Tool(
    name="get_training_status",
    description="获取 LoRA 训练任务状态",
    inputSchema={
        "type": "object",
        "properties": {
            "task_id": {"type": "string"}
        },
        "required": ["task_id"]
    }
)
```

#### 2.3 LoRA 训练流程（通过 ComfyUI 云服务）

```
用户上传训练图片
        │
        ▼
┌─────────────────┐
│ 1. 图片预处理    │  ← 本地执行
│  - 裁剪/缩放     │
│  - 质量检查      │
│  - 自动打标签    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. 上传到云端    │
│  - 图片 → MinIO │
│  - 同步到云 GPU  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. ComfyUI 训练 │  ← 云端执行 (RunPod/Modal)
│  - 训练节点执行  │
│  - 进度回调      │
│  - 采样图生成    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. 训练完成     │
│  - 下载 LoRA    │
│  - 存入 MinIO   │
│  - 创建资产记录  │
└─────────────────┘
```

> **说明**：使用 ComfyUI 训练节点（如 ComfyUI-TrainTools）统一处理，
> 与图片/视频生成共用云端 GPU 资源。

#### 2.4 LoRA 训练预设配置

| 预设名称 | 适用场景 | rank | 训练步数 | 显存需求 |
|---------|---------|------|---------|---------|
| 快速训练 | 测试/原型 | 16 | 500 | 8GB |
| 标准训练 | 一般角色 | 32 | 1500 | 12GB |
| 高质量训练 | 主要角色 | 64 | 3000 | 16GB |
| 精细训练 | 复杂风格 | 128 | 5000 | 24GB |

### 4. Claude 参数翻译层详细设计

Claude 作为**语义翻译器**，将自然语言分镜描述转换为 ComfyUI 可执行的 workflow_json。

#### 3.1 核心价值

| 传统方案 | Claude 翻译方案 |
|---------|---------------|
| 每个工作流需手动配置映射规则 | 无需预配置，Claude 理解工作流结构 |
| 机械的参数填充 | 语义理解，智能参数生成 |
| 无法理解"忧郁""电影感"等描述 | 能将抽象描述转为具体参数 |
| 新增工作流需开发适配 | 新增工作流只需让 Claude 读取 |

#### 3.2 翻译流程

```
输入
├── 分镜描述: "小明站在雨中，忧郁地看着远方，电影感"
├── 角色资产: {lora_id, reference_images}
├── 场景资产: {reference_images}
└── 工作流模板列表: [{id, name, workflow_json, description}]
        │
        ▼
┌─────────────────────────────────────────┐
│           Claude 参数翻译               │
│                                         │
│  1. 理解语义                            │
│     - "忧郁" → 冷色调、低饱和度          │
│     - "电影感" → 2.35:1、景深、柔光      │
│     - "雨中" → 雨天氛围、湿润质感        │
│                                         │
│  2. 选择工作流                          │
│     - 分析需求 → 选择 image2video       │
│                                         │
│  3. 生成参数                            │
│     - positive_prompt: 优化后的提示词    │
│     - negative_prompt: 排除项           │
│     - lora_name + weight               │
│     - controlnet 配置                   │
│     - 其他节点参数                       │
└─────────────────────────────────────────┘
        │
        ▼
输出: 完整的 workflow_json（可直接提交 ComfyUI）
```

#### 4.3 Claude Code 集成方式

通过 Claude Code 的 MCP Server 暴露参数翻译能力，后端通过 MCP 协议调用。

```python
# MCP Server 实现 - 参数翻译工具
from mcp.server import Server
from mcp.types import Tool, TextContent
import json

server = Server("ai-video-translator")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="translate_storyboard",
            description="将分镜描述翻译为 ComfyUI workflow_json",
            inputSchema={
                "type": "object",
                "properties": {
                    "storyboard": {"type": "object"},
                    "character_assets": {"type": "array"},
                    "scene_assets": {"type": "array"},
                    "available_workflows": {"type": "array"}
                },
                "required": ["storyboard", "available_workflows"]
            }
        )
    ]
```

#### 4.4 调用流程

```
后端任务服务
    │
    ▼
MCP Client 调用 translate_storyboard
    │
    ▼
Claude Code (使用已配置的 API/模型)
    │
    ▼
返回 workflow_json
```

> **优势**：复用 Claude Code 已配置的 API Key 和模型，无需在后端单独管理。

### 5. Celery 异步兼容性方案

> **问题**：FastAPI 是全异步框架，但 Celery 不原生支持 async/await。

#### 解决方案

```python
import asyncio
from celery import Celery

celery_app = Celery('ai_video')

def run_async(coro):
    """在 Celery Worker 中安全执行异步代码"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

@celery_app.task(bind=True, max_retries=3)
def execute_comfyui_task(self, task_id: str):
    """Celery 任务：执行 ComfyUI 工作流"""
    try:
        result = run_async(_async_execute(task_id))
        return result
    except Exception as e:
        # 指数退避重试
        raise self.retry(exc=e, countdown=2 ** self.request.retries)

async def _async_execute(task_id: str):
    """实际的异步执行逻辑"""
    task = await db.get_task(task_id)
    workflow_json = await param_mapper.map_params(
        task.workflow_id, task.input_params
    )
    return await comfyui_client.execute(workflow_json)
```

#### 架构规范

| 层级 | 同步/异步 | 说明 |
|-----|----------|-----|
| FastAPI 路由 | async | 处理 HTTP 请求 |
| 服务层 | async | 业务逻辑 |
| Celery Task | sync | 包装异步调用 |
| 底层客户端 | async | ComfyUI/DB 调用 |

### 6. 错误处理与恢复机制

#### 错误分类

| 错误类型 | 示例 | 处理策略 |
|---------|-----|---------|
| 临时错误 | 网络超时、GPU 繁忙 | 自动重试 |
| 资源错误 | GPU OOM、磁盘满 | 等待资源释放后重试 |
| 配置错误 | 模型文件缺失、参数无效 | 标记失败，人工干预 |
| 系统错误 | ComfyUI 崩溃 | 重启服务后重试 |

#### 重试策略

```python
class RetryPolicy:
    """重试策略配置"""
    max_retries: int = 3
    base_delay: int = 5  # 秒
    max_delay: int = 300  # 最大延迟 5 分钟
    exponential_base: float = 2.0

    def get_delay(self, retry_count: int) -> int:
        """指数退避计算"""
        delay = self.base_delay * (self.exponential_base ** retry_count)
        return min(delay, self.max_delay)
```

#### 资源预检查

```python
async def pre_check_resources(task: GenerationTask) -> bool:
    """执行前资源检查"""
    requirements = task.resource_requirements

    # 检查 GPU 内存
    if requirements.get("gpu_memory_mb"):
        available = await gpu_monitor.get_available_memory()
        if available < requirements["gpu_memory_mb"]:
            return False

    # 检查模型文件
    workflow = await get_workflow(task.workflow_id)
    for model in workflow.required_models:
        if not await storage.exists(model):
            raise ConfigurationError(f"模型文件缺失: {model}")

    return True
```

## 八、待确认/探索的问题

1. **Claude Code SDK 的具体 API 和限制** - 需要深入研究文档
2. **ComfyUI 云端部署方案** - RunPod vs 自建
3. **视频生成质量与速度的平衡** - AnimateDiff 参数调优
4. **音频方案选择** - Edge-TTS vs GPT-SoVITS vs 其他
