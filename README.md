# Walter 全天候决策系统 (China Edition)

纯决策系统设计 - 数据监控 → 决策树 → 自动评分 → 每日复盘

## 系统目标

- 每日自动监测宏观、流动性、市场、企业质量
- 通过决策树判断投资环境
- 输出资产配置与风险控制
- 持续复盘修正模型

## 系统周期

- Daily monitoring
- Weekly review
- Monthly macro update
- Quarterly fundamental update

## 核心模块

| 阶段 | 名称 | 更新频率 |
|-----|------|--------|
| Stage0 | 企业质量过滤 | 季度 |
| Stage1 | 宏观周期判断 | 每月 |
| Stage2 | 全球流动性判断 | 每日 |
| Stage3 | 市场预期偏差 | 每日 |
| Stage4 | 趋势确认 | 每日 |
| Stage5 | 仓位决策 | 每日 |
| Stage6 | 每日复盘 | 每日 |

## 项目结构

```
walter-decision-maker/
├── docs/
├── src/
│   ├── data/
│   ├── stages/
│   ├── models/
│   ├── reports/
│   └── main.py
├── config/
├── tests/
├── .github/workflows/daily-report.yml
├── requirements.txt
└── README.md
```

## 数据引擎（实时抓取）

`src/data/data_monitor.py` 会优先使用 [Scrapling](https://github.com/D4Vinci/Scrapling) 抓取实时数据（若已安装），并在不可用时自动回退到 `urllib`，保证流水线对依赖变化更稳健。抓取覆盖：

- SPY（美股风险偏好）
- 2822.HK（沪深300 ETF 代理）
- US10Y（10 年期美债）
- DXY（美元指数）
- XAUUSD（黄金）
- CL（原油）
- FRED（WALCL/M2SL/BAMLH0A0HYM2）
- FMP 企业质量指标（ROE、负债结构、FCF 代理）

可选安装 Scrapling：

```bash
pip install git+https://github.com/D4Vinci/Scrapling.git
```

## DeepSeek 报告生成

流水线支持使用 DeepSeek 生成 `## DeepSeek AI Summary`：

```bash
export DEEPSEEK_API_KEY="<your-key>"
python -m src.main
```

如果没有提供 `DEEPSEEK_API_KEY`，系统会继续生成基础报告（不含 AI 段落）。

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main
```

## GitHub Action 每日任务

已提供 `.github/workflows/daily-report.yml`：

- 每天 UTC `01:00` 自动运行
- 也支持手动 `workflow_dispatch`
- 使用 `secrets.DEEPSEEK_API_KEY` 调用 DeepSeek
- 将生成的日报作为 Artifact 上传

配置步骤：

1. 进入 GitHub Repo → Settings → Secrets and variables → Actions
2. 新建 Secret：`DEEPSEEK_API_KEY`
3. 若要启用邮件发送，额外配置 Secrets：`SMTP_SERVER`、`SMTP_PORT`、`SMTP_USERNAME`、`SMTP_PASSWORD`
4. 推送代码后等待每日任务自动执行
