# 搜索协议引擎 Search Protocol Engine
## 53个ARU的精确搜索查询模板

> 使用规则：
> - `{INDUSTRY}` = 替换为目标行业（中英文均可）
> - `{COMPANY}` = 替换为目标公司
> - `{YEAR}` = 当前年份或目标年份
> - `{REGION}` = 地区（China/Global/US/Europe等）
> - 每轮搜索后，基于结果用「下钻查询」深入具体线索

---

## M系列查询模板

### M01：行业边界勘测

**第1轮 — 定义边界**
```
"{INDUSTRY} industry definition scope value chain {YEAR}"
"{INDUSTRY} 行业定义 上下游 产业链 范围"
"{INDUSTRY} market segmentation breakdown categories"
"what is included in {INDUSTRY} industry SIC NAICS code"
```

**第2轮 — 上下游测绘**
```
"{INDUSTRY} upstream downstream suppliers buyers"
"{INDUSTRY} adjacent industries related markets"
"{INDUSTRY} value chain map stages"
```

**第3轮 — 国内外对比**
```
"{INDUSTRY} China market definition vs global"
"{INDUSTRY} 中国标准 GB 行业分类"
```

**提取目标**：行业定义边界、上游投入品类别、下游应用场景、监管分类代码

---

### M02：市场规模测算

**第1轮 — 权威规模数据**
```
"{INDUSTRY} market size {YEAR} billion USD revenue"
"{INDUSTRY} 市场规模 {YEAR} 亿元 亿美元"
"{INDUSTRY} global market size CAGR forecast 2025 2030"
"{INDUSTRY} market size McKinsey BCG Gartner IDC report"
```

**第2轮 — 多机构交叉验证**
```
"{INDUSTRY} market size Grand View Research MarketsandMarkets"
"{INDUSTRY} TAM SAM addressable market size"
"{INDUSTRY} revenue forecast {REGION} {YEAR}"
```

**第3轮 — 底部向上验证**
```
"{INDUSTRY} total units shipped volume {YEAR}"
"{INDUSTRY} average selling price ASP trend"
"number of {INDUSTRY} companies revenue per company"
```

**第4轮 — 增速驱动**
```
"{INDUSTRY} growth drivers market expansion factors"
"{INDUSTRY} market contraction headwinds decline reasons"
```

**提取目标**：规模数字（注明机构来源）、CAGR（注明预测时间段）、测算方法

---

### M03：市场分层解剖

```
"{INDUSTRY} market segments breakdown by product type"
"{INDUSTRY} market segments by geography end user"
"{INDUSTRY} high end mid range low end market split"
"{INDUSTRY} B2B B2C enterprise SMB market breakdown"
"{INDUSTRY} premium vs commodity segment size share"
"{INDUSTRY} 细分市场 子行业 分类 规模"
```

---

### M04：价值链解剖

```
"{INDUSTRY} value chain analysis profit pool"
"{INDUSTRY} gross margin by segment layer stage"
"{INDUSTRY} who captures value where is profit"
"{INDUSTRY} value chain disruption where AI eating margin"
"{INDUSTRY} 价值链 利润分配 各环节毛利率"
```

---

### M05：生命周期定位

```
"{INDUSTRY} industry lifecycle stage maturity growth"
"{INDUSTRY} industry consolidation consolidating phase"
"{INDUSTRY} aging industry declining market"
"{INDUSTRY} nascent emerging industry early stage"
"{INDUSTRY} market saturation penetration rate"
"S-curve {INDUSTRY} adoption growth"
```

---

### M06：市场集中度

```
"{INDUSTRY} market share top 5 10 companies concentration"
"{INDUSTRY} CR3 CR5 market concentration ratio"
"{INDUSTRY} HHI Herfindahl Hirschman index"
"{INDUSTRY} fragmented vs consolidated competitive landscape"
"{INDUSTRY} market share ranking {YEAR}"
"{INDUSTRY} 市场集中度 CR3 前五 前十 份额"
```

---

### M07：定价机制解析

```
"{INDUSTRY} pricing model structure how priced"
"{INDUSTRY} pricing power who sets price"
"{INDUSTRY} price elasticity demand sensitivity"
"{INDUSTRY} pricing trends inflation pass through"
"{INDUSTRY} value based cost plus pricing strategy"
"{INDUSTRY} 定价机制 定价权 价格体系"
```

---

### M08：渠道矩阵分析

```
"{INDUSTRY} distribution channels breakdown percentage"
"{INDUSTRY} direct vs indirect sales channel"
"{INDUSTRY} online offline channel mix {YEAR}"
"{INDUSTRY} go-to-market channel strategy"
"{INDUSTRY} channel partners distributors resellers"
"{INDUSTRY} 渠道结构 线上线下 直营 经销"
```

---

### M09：需求驱动因子

```
"{INDUSTRY} demand drivers growth catalysts"
"{INDUSTRY} demand forecast model assumptions"
"{INDUSTRY} correlation GDP income demographics demand"
"{INDUSTRY} demand sensitivity macro factors"
"{INDUSTRY} secular tailwinds structural growth drivers"
"{INDUSTRY} 需求驱动因素 增长逻辑 宏观相关性"
```

---

### M10：供给结构分析

```
"{INDUSTRY} production capacity utilization rate"
"{INDUSTRY} supply structure manufacturers producers"
"{INDUSTRY} capacity expansion new plants capex"
"{INDUSTRY} supply shortage surplus balance"
"{INDUSTRY} 产能 开工率 在建项目 扩产"
```

---

## C系列查询模板

### C01：竞争格局雷达

```
"{INDUSTRY} competitive landscape major players {YEAR}"
"{INDUSTRY} market share ranking top companies"
"{INDUSTRY} who are the leaders challengers niche players"
"{INDUSTRY} competitive dynamics oligopoly monopoly"
"{INDUSTRY} 竞争格局 市场份额 主要玩家 排名"
```

---

### C02：头部玩家深度画像

> 针对每家目标公司单独执行

```
"{COMPANY} revenue EBITDA margin net income {YEAR} annual report"
"{COMPANY} business model strategy competitive advantage moat"
"{COMPANY} market share growth rate segment breakdown"
"{COMPANY} investor presentation annual report 10-K"
"{COMPANY} CEO strategy keynote competitive positioning"
"{COMPANY} 年报 营收 毛利率 战略 竞争优势"
"{COMPANY} analyst day presentation long term targets"
```

---

### C03：战略群组映射

```
"{INDUSTRY} competitive strategy types differentiation cost leadership"
"{INDUSTRY} strategic groups positioning map"
"{INDUSTRY} premium vs value players strategy"
"{INDUSTRY} integrated vs specialized players"
"{INDUSTRY} platform vs product company strategy"
```

---

### C04：M&A活动扫描

```
"{INDUSTRY} merger acquisition {YEAR} {YEAR-1} {YEAR-2}"
"{INDUSTRY} M&A deal value EV EBITDA multiple"
"{INDUSTRY} strategic rationale acquisition target"
"{INDUSTRY} consolidation wave buyout private equity"
"{INDUSTRY} 并购 收购 战略整合 估值倍数"
```

---

### C05：融资动态情报

```
"{INDUSTRY} venture capital investment funding {YEAR}"
"{INDUSTRY} startup funding round Series A B C"
"{INDUSTRY} IPO listing valuation {YEAR}"
"{INDUSTRY} private equity investment buyout"
"{INDUSTRY} unicorn valuation funding latest"
"{INDUSTRY} 融资 VC PE 投资 估值 融资轮次"
```

---

### C06：人才与高管信号

```
"{COMPANY} key executives leadership team background"
"{INDUSTRY} talent war hiring war for talent"
"{COMPANY} executive departure hire LinkedIn"
"{INDUSTRY} talent flow from Google Amazon Microsoft"
"site:linkedin.com {COMPANY} {INDUSTRY} VP Director hiring"
```

---

### C07：专利与IP格局

```
"{INDUSTRY} patent landscape key patents holder"
"{INDUSTRY} patent filings trend {YEAR}"
"{COMPANY} patent portfolio core IP"
"{INDUSTRY} patent litigation disputes"
"{INDUSTRY} open source vs proprietary IP strategy"
"{INDUSTRY} 专利 知识产权 核心技术壁垒"
```

---

### C08：品牌认知对比

```
"{INDUSTRY} brand ranking perception survey NPS"
"{INDUSTRY} consumer preference brand loyalty survey"
"{COMPANY} brand value Interbrand BrandZ"
"{INDUSTRY} brand equity comparison"
"{INDUSTRY} customer satisfaction index score"
```

---

### C09：新进入者雷达

```
"{INDUSTRY} new entrants threat disruption"
"who is entering {INDUSTRY} market crossover"
"tech companies entering {INDUSTRY}"
"{INDUSTRY} barriers to entry overcome"
"startup disrupting {INDUSTRY} {YEAR}"
"{INDUSTRY} 跨界进入 新玩家 颠覆者"
```

---

## T系列查询模板

### T01：技术前沿测绘

```
"{INDUSTRY} technology trends {YEAR} emerging"
"{INDUSTRY} Gartner hype cycle technology"
"key technologies transforming {INDUSTRY}"
"{INDUSTRY} technology roadmap next 5 years"
"{INDUSTRY} 技术趋势 前沿技术 技术路线图"
```

---

### T02：颠覆向量分析

```
"{INDUSTRY} disruptive technology threat"
"what will disrupt {INDUSTRY} next decade"
"{INDUSTRY} digital disruption transformation"
"{INDUSTRY} Innovator's Dilemma disruption case"
"technology killing {INDUSTRY} obsolete"
"{INDUSTRY} 颠覆性技术 破坏式创新"
```

---

### T03：R&D投入基准

```
"{INDUSTRY} R&D spending intensity revenue ratio"
"{COMPANY} research development expenditure {YEAR}"
"{INDUSTRY} innovation investment benchmark"
"{INDUSTRY} R&D to revenue ratio comparison"
```

---

### T04：平台与生态分析

```
"{INDUSTRY} platform business model ecosystem"
"{INDUSTRY} network effects competitive moat"
"{INDUSTRY} marketplace dynamics two-sided"
"{INDUSTRY} API ecosystem developer platform"
"{INDUSTRY} 平台效应 生态系统 网络效应"
```

---

### T05：AI渗透程度扫描

```
"AI artificial intelligence impact on {INDUSTRY}"
"{INDUSTRY} AI automation use case ROI"
"generative AI {INDUSTRY} adoption enterprise"
"{INDUSTRY} AI disruption job displacement"
"{INDUSTRY} machine learning deployment"
"{INDUSTRY} AI人工智能应用 渗透率 落地案例"
```

---

### T06：技术采用曲线定位

```
"{INDUSTRY} technology adoption rate penetration"
"{INDUSTRY} early adopter mainstream laggard"
"crossing the chasm {INDUSTRY} technology"
"{INDUSTRY} digital transformation maturity curve"
```

---

### T07：开源与学术信号

```
"{INDUSTRY} research paper arxiv academic breakthrough"
"{INDUSTRY} open source project GitHub activity"
"{INDUSTRY} university research commercialization"
"{INDUSTRY} emerging technology academic signal"
"site:arxiv.org {INDUSTRY} latest"
```

---

## F系列查询模板

### F01：商业模式分类

```
"{INDUSTRY} business models types revenue streams"
"{INDUSTRY} SaaS subscription transaction licensing model"
"{INDUSTRY} monetization strategy comparison"
"{INDUSTRY} business model innovation example"
"{INDUSTRY} 商业模式 盈利模式 收入来源"
```

---

### F02：单位经济学基准

```
"{INDUSTRY} unit economics LTV CAC payback period"
"{INDUSTRY} customer lifetime value calculation"
"{INDUSTRY} cost to acquire customer benchmark"
"{INDUSTRY} gross margin per unit product"
"{INDUSTRY} 单位经济 LTV CAC 投资回报"
```

---

### F03：资本密度分析

```
"{INDUSTRY} capital intensity asset turnover ROIC"
"{INDUSTRY} return on invested capital WACC spread"
"{INDUSTRY} capex intensity revenue ratio"
"{INDUSTRY} asset light heavy capital requirements"
"{INDUSTRY} 资本密度 ROIC 资产周转率 重资产"
```

---

### F04：利润结构解剖

```
"{INDUSTRY} gross margin EBITDA margin net margin benchmark"
"{INDUSTRY} operating leverage profit margin range"
"{INDUSTRY} profitability drivers margin expansion"
"{INDUSTRY} cost structure breakdown COGS SG&A"
"{INDUSTRY} 毛利率 净利率 利润结构 成本构成"
```

---

### F05：估值倍数图谱

```
"{INDUSTRY} EV/EBITDA multiple valuation range"
"{INDUSTRY} P/E P/S price to sales valuation"
"{INDUSTRY} public company comparable valuation"
"{INDUSTRY} premium discount valuation multiple"
"how to value {INDUSTRY} company DCF multiple"
"{INDUSTRY} 估值倍数 市销率 EV/EBITDA 合理区间"
```

---

### F06：投资流向分析

```
"{INDUSTRY} institutional investor holding inflow outflow"
"{INDUSTRY} ETF fund flow capital allocation"
"{INDUSTRY} sell side buy side sentiment rating"
"{INDUSTRY} short interest bearish bullish"
"{INDUSTRY} 机构持仓 资金流向 做多做空 市场情绪"
```

---

### F07：宏观敏感性映射

```
"{INDUSTRY} interest rate sensitivity impact"
"{INDUSTRY} GDP growth correlation recession proof"
"{INDUSTRY} inflation impact pricing power"
"{INDUSTRY} currency exchange rate exposure"
"{INDUSTRY} cyclical defensive characteristic"
"{INDUSTRY} 宏观敏感性 利率 通胀 GDP 周期性"
```

---

### F08：财务压力信号扫描

```
"{INDUSTRY} financial stress default risk"
"{INDUSTRY} leverage ratio debt covenant"
"{INDUSTRY} cash burn rate runway startup"
"{INDUSTRY} credit rating downgrade warning"
"{INDUSTRY} 财务风险 杠杆率 偿债压力 流动性"
```

---

## R系列查询模板

### R01：监管体系测绘

```
"{INDUSTRY} regulatory framework who regulates"
"{INDUSTRY} key regulations laws compliance"
"{INDUSTRY} regulatory body oversight agency"
"{INDUSTRY} licensing requirement barriers"
"{INDUSTRY} 监管框架 主管部门 核心法规 许可证"
"site:gov.cn {INDUSTRY} 监管 政策"
```

---

### R02：政策变化地平线扫描

```
"{INDUSTRY} regulatory change upcoming policy {YEAR}"
"{INDUSTRY} legislation pending bill congress"
"{INDUSTRY} policy signal government stance"
"{INDUSTRY} deregulation regulation tightening"
"{INDUSTRY} 政策变化 监管趋势 即将出台 草案"
```

---

### R03：合规成本基准

```
"{INDUSTRY} compliance cost revenue percentage"
"{INDUSTRY} regulatory burden cost estimate"
"{INDUSTRY} compliance spending benchmark"
```

---

### R04：反垄断监管

```
"{INDUSTRY} antitrust investigation competition probe"
"{INDUSTRY} merger blocked regulators competition"
"{INDUSTRY} monopoly market power abuse"
"{INDUSTRY} {COMPANY} antitrust fine penalty"
"{INDUSTRY} 反垄断 竞争执法 合并审查 罚款"
```

---

### R05：国际贸易与关税

```
"{INDUSTRY} tariff import export restriction"
"{INDUSTRY} trade war impact supply chain"
"{INDUSTRY} export control technology restriction"
"{INDUSTRY} geopolitical risk supply chain"
"{INDUSTRY} 关税 贸易壁垒 出口管制 地缘政治"
```

---

### R06：ESG与可持续监管

```
"{INDUSTRY} ESG regulation carbon emission requirement"
"{INDUSTRY} sustainability mandate net zero target"
"{INDUSTRY} scope 1 2 3 emission disclosure"
"{INDUSTRY} green taxonomy sustainable finance"
"{INDUSTRY} ESG评级 碳排放 可持续 绿色监管"
```

---

## D系列查询模板

### D01：消费者分层画像

```
"{INDUSTRY} customer segmentation demographics psychographics"
"{INDUSTRY} buyer persona target audience"
"{INDUSTRY} consumer survey research insight"
"{INDUSTRY} who buys why purchase decision"
"{INDUSTRY} 用户画像 消费者研究 购买决策"
```

---

### D02：行为变迁追踪

```
"{INDUSTRY} consumer behavior shift trend change"
"{INDUSTRY} changing customer preference"
"{INDUSTRY} post-pandemic behavior shift"
"{INDUSTRY} Gen Z millennial behavior impact"
"{INDUSTRY} 消费行为变化 趋势 代际差异"
```

---

### D03：支付意愿研究

```
"{INDUSTRY} willingness to pay premium survey"
"{INDUSTRY} price sensitivity consumer research"
"{INDUSTRY} conjoint analysis pricing research"
"{INDUSTRY} consumer value perception premium"
"{INDUSTRY} 支付意愿 溢价 价格敏感度"
```

---

### D04：渠道偏好映射

```
"{INDUSTRY} channel preference online offline"
"{INDUSTRY} where do customers buy purchase channel"
"{INDUSTRY} direct to consumer DTC trend"
"{INDUSTRY} omnichannel behavior"
```

---

### D05：需求弹性估算

```
"{INDUSTRY} price elasticity demand coefficient"
"{INDUSTRY} demand response price change"
"{INDUSTRY} elastic inelastic demand"
```

---

### D06：痛点与需求缺口

```
"{INDUSTRY} customer pain points unmet needs"
"{INDUSTRY} product gap white space opportunity"
"{INDUSTRY} dissatisfaction complaint review"
"{INDUSTRY} Jobs to be Done JTBD"
"{INDUSTRY} 用户痛点 需求缺口 白板机会"
```

---

## S系列查询模板

### S01：原材料测绘

```
"{INDUSTRY} raw material input commodity"
"{INDUSTRY} key material supply source concentration"
"{INDUSTRY} raw material price trend volatility"
"{INDUSTRY} critical material shortage risk"
"{INDUSTRY} 原材料 上游资源 大宗商品 价格走势"
```

---

### S02：供应商集中度

```
"{INDUSTRY} supplier concentration sole source risk"
"{INDUSTRY} supply chain vulnerability single point failure"
"{INDUSTRY} supplier diversification multi-sourcing"
"{INDUSTRY} key supplier dependency"
```

---

### S03：地理与物流格局

```
"{INDUSTRY} manufacturing geography production location"
"{INDUSTRY} nearshoring reshoring supply chain shift"
"{INDUSTRY} logistics cost freight last mile"
"{INDUSTRY} supply chain map visualization"
"{INDUSTRY} 产业转移 制造布局 物流成本"
```

---

### S04：营运资本基准

```
"{INDUSTRY} inventory turnover days DSO DPO"
"{INDUSTRY} working capital cycle cash conversion"
"{INDUSTRY} accounts receivable payable benchmark"
"{INDUSTRY} 库存周转 应收账款 营运资本效率"
```

---

## X系列查询模板

### X01：招聘信号情报

```
"site:linkedin.com {COMPANY} hiring {ROLE} {YEAR}"
"{COMPANY} job posting AI ML strategy signal"
"{COMPANY} headcount growth hiring freeze"
"{INDUSTRY} talent demand skills shortage"
```

---

### X02：电话会议与财报挖掘

```
"{COMPANY} earnings call transcript Q{Q} {YEAR}"
"{COMPANY} CEO comments outlook guidance {YEAR}"
"{COMPANY} investor day presentation {YEAR}"
"{INDUSTRY} earnings sentiment positive negative"
"site:seekingalpha.com {COMPANY} earnings call"
"{COMPANY} 业绩说明会 电话会 管理层表态"
```

---

### X03：另类数据信号

```
"{COMPANY} app download rank Sensor Tower AppFollow"
"{COMPANY} web traffic Similarweb trend"
"{INDUSTRY} satellite imagery foot traffic signal"
"{COMPANY} employee review Glassdoor trend"
"{COMPANY} social media sentiment trend"
```

---

## 通用下钻查询模式

当搜索结果不充分时，使用以下下钻策略：

```
# 策略1：时间下钻
→ 指定更精确年份/季度："Q3 2024" "first half 2024"

# 策略2：地理下钻
→ 从全球缩小到地区："Asia Pacific" "Greater China" "Europe"

# 策略3：细分下钻
→ 从行业缩小到子赛道：一级行业 → 二级子行业 → 细分品类

# 策略4：机构下钻
→ 直接点名权威来源：
  "McKinsey {INDUSTRY} 2024"
  "Goldman Sachs {INDUSTRY} research note"
  "Morgan Stanley {INDUSTRY} overweight"
  "site:mckinsey.com {INDUSTRY}"
  "site:hbr.org {INDUSTRY}"

# 策略5：原文下钻
→ 找到权威报告后，用 web_fetch 获取完整内容

# 策略6：中文下钻
→ 切换中文搜索获取国内视角：
  "{INDUSTRY} 行业研究报告 {YEAR}"
  "中信证券 {INDUSTRY} 研报"
  "国泰君安 {INDUSTRY} 深度报告"
```
