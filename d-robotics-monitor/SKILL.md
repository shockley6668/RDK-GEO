---
name: d-robotics-monitor
description: 专门用于地瓜机器人 (D-Robotics) RDK、X3、X5、S100、TROS 系列产品的开发者生态监控、搜索趋势分析及周报生成。
---

# D-Robotics Monitor: 地瓜机器人开发者生态监控工具

本 Skill 用于自动化收集地瓜机器人 (D-Robotics) 相关产品的市场声量、搜索趋势及开发者反馈，并生成结构化的周报。

## 核心功能

1.  **多平台趋势分析**：利用 `opencli` 抓取 B站、YouTube、知乎、CSDN、Reddit、HackerNews 的最新数据。
2.  **搜索指数追踪**：对比核心关键词 (RDK, X3, X5, S100, TROS) 的周度搜索波动。
3.  **传播效果评估**：分析热门 Demo 视频的传播量、互动率及开发者自发评论。
4.  **自动化报告生成**：输出包含搜索趋势、热点内容分析及内容营销建议的 Markdown 周报。

## 推荐工作流

### 第一步：收集数据
使用内置脚本抓取数据并存入 CSV：
```bash
python3 scripts/monitor_d_robotics.py
```

### 第二步：分析 Demo 传播
针对 B 站和 YouTube 上的热门内容进行深度检索：
- `opencli bilibili search "RDK X5 demo" -f json`
- `opencli youtube search "D-Robotics X3" -f json`

### 第三步：生成周报
按照以下结构汇总数据：
1. **搜索指数周报**：量化趋势变化（本周 vs 上周）。
2. **热点内容分析**：附上爆款文章/视频链接（从 CSV 或搜索结果中提取）。
3. **内容营销评估**：给出下周内容铺设的具体建议。

## 注意事项
- **关键词去噪**：过滤 BMW X5、RDKit 等干扰项。
- **数据存档**：数据会自动追加至 `d_robotics_keyword_monitor.csv`。
