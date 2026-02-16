from __future__ import annotations

PHASES = [
    {
        "key": "company_intro",
        "title": "公司介绍",
        "instruction": (
            "围绕主营业务、最新年度营收规模与结构、毛利与毛利结构、费用与费用结构、"
            "净利润与净利率做结构化分析。给出关键数据，并标注数据口径与潜在不确定性。"
        ),
    },
    {
        "key": "industry",
        "title": "行业情况",
        "instruction": (
            "分析全球与中国市场的销量/销售额、竞争格局、主要玩家份额，指出当前体量最大和"
            "增速最快的细分赛道，给出3-5年趋势判断。"
        ),
    },
    {
        "key": "company_specific",
        "title": "公司具体情况",
        "instruction": (
            "评估核心管理层履历、资本配置能力、战略眼光、执行力与组织效率。"
            "区分事实、推断、风险。"
        ),
    },
    {
        "key": "investment_strategy",
        "title": "投资策略",
        "instruction": (
            "给出估值框架（如DCF/PE/PB/EV-EBITDA等适用者），形成买入/持有/卖出建议，"
            "给出价格区间、仓位建议、止盈止损、关键跟踪指标。"
        ),
    },
]


def system_prompt() -> str:
    return (
        "你是顶级价值投资研究员，风格结合巴菲特、芒格、段永平：\n"
        "1) 先事实后结论；2) 强调能力圈与安全边际；3) 明确假设与反例；"
        "4) 避免空话，优先可验证数据。"
    )
