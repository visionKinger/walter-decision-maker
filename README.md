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
│   ├── system_design.md
│   ├── decision_tree.md
│   ├── scoring_model.md
│   └── review_system.md
├── src/
│   ├── stages/
│   ├── data/
│   ├── models/
│   ├── reports/
│   └── main.py
├── data/
│   ├── monitored_assets.json
│   ├── decision_log.csv
│   └── daily_report/
├── config/
│   └── settings.json
├── tests/
├── requirements.txt
└── README.md
```

## 数据引擎（Dalio + Druckenmiller + Jiang）

当前实现内置了可离线运行的数据快照与指标映射，便于先跑通流程：

- **Macro Dashboard**：CPI/PCE、ISM、2s10s、Debt proxy
- **Liquidity Dashboard**：Fed Balance Sheet trend、M2、HY Spread、政策鹰鸽评分
- **Game Theory Matrix**：关键参与方、激励与可能动作

后续可把 `src/data/sources.py` 替换为 Wind / Bloomberg / Reuters / FRED 的实时拉取。

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main
```

## 每日自动输出

**Walter Daily Decision Report** 包含：

- Macro Regime（宏观环境）
- Liquidity Status（流动性状态）
- Trend Status（趋势状态）
- Opportunity Score（机会评分）
- Portfolio Allocation（仓位配置）
- Risk Alert（风险预警）
- Dalio/Druckenmiller/Jiang 三模块摘要

## 系统运行时间

```
06:00 - 数据抓取
07:00 - 指标计算
08:00 - 决策树运行
09:00 - 生成报告
```

## 监控资产

**中国市场：**
- 000300 (沪深300)
- 000905 (中证500)
- 399006 (创业板指)

**全球资产：**
- SPY (S&P 500)
- GLD (黄金)
- USO (原油)

**宏观指标：**
- 美元指数
- 美债收益率
- 黄金
- 原油
