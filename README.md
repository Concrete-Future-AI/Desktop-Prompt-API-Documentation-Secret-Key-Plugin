# Prompt Manager

一个优雅的 Prompt、API 文档和密钥管理工具，支持浮动球快速访问。

## 安装

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 配置 AI 分析功能（可选）

如果需要使用 AI 智能分析功能，请设置豆包 API 密钥：

```bash
export DOUBAO_API_KEY="your_api_key_here"
```

或复制 `.env.example` 为 `.env` 并填入密钥。

## 启动方式

双击 `start.command` 即可启动，或命令行运行：

```bash
source venv/bin/activate
python main_with_ball.py
```

## 功能特性

- **三分区管理**：
  - 💡 提示词 - 管理各种 Prompt 模板
  - 📄 API文档 - 存储 API 文档片段
  - 🔑 密钥 - 安全存储 API 密钥（显示时自动遮蔽）
- **浮动球**：点击浮动球快速调出管理窗口
- **AI 智能分析**：快速添加时自动分析生成名称、分类、标签（豆包 API）
- **双击复制**：双击列表项即可复制内容到剪贴板

## 核心文件

| 文件 | 说明 |
|------|------|
| `main_with_ball.py` | 主入口（带浮动球） |
| `main_window.py` | 主窗口 UI |
| `data_manager.py` | 数据存储管理 |
| `floating_ball.py` | 浮动球组件 |
| `ai_analyzer.py` | AI 分析器（豆包 API） |
| `style_manager.py` | UI 风格管理 |

## 数据存储

数据保存在 `~/.prompt_manager/` 目录：
- `prompts.json` - 提示词数据
- `api_docs.json` - API 文档数据
- `api_keys.json` - API 密钥数据
- `config.json` - 配置文件
