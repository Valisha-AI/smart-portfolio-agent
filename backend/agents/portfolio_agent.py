"""
Portfolio Agent - Working Implementation
Uses Yahoo Finance for market data and real allocation algorithms.
"""

from typing import TypedDict, Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import os
import sys

# Add tools to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tools.market_data import (
    get_stock_info,
    find_sector_peers,
    calculate_fundamental_score,
    get_sector_etf,
    format_market_cap
)
from tools.allocation_algorithms import (
    allocate_low_risk,
    allocate_medium_risk,
    allocate_high_risk,
    format_allocation
)

class PortfolioState(TypedDict):
    """State for portfolio generation."""
    ticker: str
    investment_amount: float
    risk_level: str
    include_etfs: bool
    max_holdings: int
    
    # Agent outputs
    target_info: Dict
    peer_candidates: List[str]
    peer_data: Dict[str, Dict]
    allocation: List[Dict]
    rationale: str
    summary: Dict
    errors: List[str]

def generate_portfolio_allocation(
    ticker: str,
    investment_amount: float,
    risk_level: str,
    include_etfs: bool = True,
    max_holdings: int = 5
) -> Dict[str, Any]:
    """
    Main entry point for portfolio generation.
    Simplified single-function implementation for speed.
    """
    
    print(f"🔍 Generating portfolio for {ticker}...")
    
    # Step 1: Get target company info
    print(f"📊 Fetching data for {ticker}...")
    target_info = get_stock_info(ticker)
    target_score = calculate_fundamental_score(target_info)
    target_info["score"] = target_score
    
    # Step 2: Find peer companies
    print(f"🔎 Finding peer companies in {target_info['sector']}...")
    peer_tickers = find_sector_peers(ticker, limit=8)
    
    # Step 3: Get data and scores for all candidates
    print(f"💯 Calculating quality scores...")
    # Make sure target info has formatted market cap
    if "market_cap_formatted" not in target_info:
        target_info["market_cap_formatted"] = format_market_cap(target_info.get("market_cap", 0))
    
    peer_data = {ticker: target_info}
    scored_peers = [(ticker, target_score)]
    
    for peer_ticker in peer_tickers:
        if peer_ticker != ticker:
            peer_info = get_stock_info(peer_ticker)
            peer_score = calculate_fundamental_score(peer_info)
            peer_info["score"] = peer_score
            # Market cap should already be formatted in get_stock_info, but double-check
            if "market_cap_formatted" not in peer_info:
                peer_info["market_cap_formatted"] = format_market_cap(peer_info.get("market_cap", 0))
            peer_data[peer_ticker] = peer_info
            scored_peers.append((peer_ticker, peer_score))
    
    # Sort by score (highest first)
    scored_peers.sort(key=lambda x: x[1], reverse=True)
    
    # Step 4: Apply allocation algorithm
    print(f"💰 Applying {risk_level} risk allocation...")
    etf_ticker = get_sector_etf(target_info["sector"]) if include_etfs else None
    
    if risk_level == "low":
        allocations = allocate_low_risk(scored_peers, include_etfs, etf_ticker)
    elif risk_level == "medium":
        allocations = allocate_medium_risk(scored_peers, include_etfs, etf_ticker)
    else:  # high
        allocations = allocate_high_risk(scored_peers, ticker, include_etfs, etf_ticker)
    
    # Add ETF data if included
    if include_etfs and etf_ticker:
        etf_info = get_stock_info(etf_ticker)
        etf_info["score"] = None  # ETFs don't have quality scores
        etf_info["market_cap_formatted"] = "ETF"
        peer_data[etf_ticker] = etf_info
    
    # Format allocation
    formatted_allocation = format_allocation(allocations, investment_amount, peer_data)
    
    # Step 5: Generate rationale with LLM
    print(f"🤖 Generating portfolio rationale...")
    try:
        rationale, per_holding_rationale = generate_rationale_llm(
            ticker,
            target_info,
            formatted_allocation,
            risk_level
        )
        
        # Add per-holding rationale
        for item in formatted_allocation:
            item["rationale"] = per_holding_rationale.get(item["ticker"], "Diversification component")
    
    except Exception as e:
        print(f"⚠️  LLM generation failed: {e}")
        rationale = generate_template_rationale(ticker, formatted_allocation, risk_level)
        for item in formatted_allocation:
            item["rationale"] = f"{item['company_name']} - {item['sector']} exposure"
    
    # Step 6: Calculate summary
    avg_score = sum(
        item["earnings_quality_score"] 
        for item in formatted_allocation 
        if item["earnings_quality_score"] is not None
    ) / max(1, sum(1 for item in formatted_allocation if item["earnings_quality_score"] is not None))
    
    sector_concentration = {}
    for item in formatted_allocation:
        sector = item["sector"]
        percent = item["allocation_percent"]
        sector_concentration[sector] = sector_concentration.get(sector, 0) + percent
    
    summary = {
        "total_holdings": len(formatted_allocation),
        "average_earnings_quality": round(avg_score, 1),
        "risk_profile": risk_level,
        "expected_volatility": get_volatility_label(risk_level),
        "sector_concentration": sector_concentration,
        "key_insights": generate_insights(formatted_allocation, avg_score, risk_level)
    }
    
    print(f"✅ Portfolio generated successfully!")
    
    return {
        "request": {
            "ticker": ticker,
            "ticker_name": target_info["company_name"],
            "investment_amount": investment_amount,
            "risk_level": risk_level,
            "analysis_date": "2025-10-19"
        },
        "allocation": formatted_allocation,
        "summary": summary,
        "rationale": rationale,
        "risk_disclosure": "Past performance does not guarantee future results. All investments carry risk of loss. This allocation is for informational purposes only and does not constitute financial advice.",
        "data_sources": [
            "Yahoo Finance (market data)",
            "Fundamental analysis (quality scores)",
            "OpenAI GPT-4 (rationale generation)"
        ]
    }

def generate_rationale_llm(
    ticker: str,
    target_info: Dict,
    allocation: List[Dict],
    risk_level: str
) -> tuple:
    """Generate portfolio rationale using GPT-4."""
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    allocation_summary = "\n".join([
        f"- {item['ticker']} ({item['company_name']}): {item['allocation_percent']}%, "
        f"Sector: {item['sector']}, Quality Score: {item['earnings_quality_score']}"
        for item in allocation
    ])
    
    prompt = f"""You are a financial analyst explaining a portfolio allocation.

TARGET: {ticker} ({target_info['company_name']})
AMOUNT: ${investment_amount:,}
RISK LEVEL: {risk_level}

ALLOCATION:
{allocation_summary}

Write a 3-4 sentence rationale explaining:
1. Why these specific companies were selected
2. How this allocation balances risk and return for a {risk_level} risk investor
3. Key strengths of the portfolio (reference quality scores)

Then provide a 1-sentence rationale for EACH holding explaining its specific role.

Format as JSON:
{{
  "overall": "...",
  "holdings": {{
    "TICKER1": "...",
    "TICKER2": "..."
  }}
}}
"""
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    # Parse JSON response
    import json
    try:
        parsed = json.loads(response.content)
        return parsed["overall"], parsed["holdings"]
    except:
        # Fallback if JSON parsing fails
        return response.content, {}

def generate_template_rationale(ticker: str, allocation: List[Dict], risk_level: str) -> str:
    """Generate a template-based rationale as fallback."""
    avg_score = sum(item["earnings_quality_score"] or 0 for item in allocation) / len(allocation)
    
    risk_desc = {
        "low": "conservative, ETF-heavy",
        "medium": "balanced quality-weighted",
        "high": "concentrated high-conviction"
    }
    
    return f"""This {risk_desc[risk_level]} portfolio is centered on {ticker} with diversification across 
{len(allocation)} holdings. The average quality score of {avg_score:.1f}/5.0 indicates {
'strong' if avg_score > 3.5 else 'moderate'} fundamental health across the portfolio. 
The allocation strategy prioritizes {risk_level} risk tolerance while maintaining exposure to 
the target sector and related industries."""

def generate_insights(allocation: List[Dict], avg_score: float, risk_level: str) -> List[str]:
    """Generate key insights about the portfolio."""
    insights = []
    
    # Quality insight
    if avg_score >= 4.0:
        insights.append(f"Strong average quality score of {avg_score:.1f}/5 suggests robust fundamentals")
    elif avg_score >= 3.0:
        insights.append(f"Moderate quality score of {avg_score:.1f}/5 indicates balanced risk-return profile")
    else:
        insights.append(f"Below-average quality score of {avg_score:.1f}/5 suggests higher risk exposure")
    
    # Diversification insight
    holdings_count = len(allocation)
    if holdings_count >= 5:
        insights.append(f"Well-diversified across {holdings_count} holdings reduces single-stock risk")
    else:
        insights.append(f"Concentrated {holdings_count}-holding portfolio emphasizes conviction over diversification")
    
    # Top holding insight
    top_holding = max(allocation, key=lambda x: x["allocation_percent"])
    if top_holding["allocation_percent"] > 35:
        insights.append(f"Largest position {top_holding['ticker']} at {top_holding['allocation_percent']}% indicates high conviction")
    
    return insights

def get_volatility_label(risk_level: str) -> str:
    """Get volatility label for risk level."""
    return {
        "low": "Low (10-15% annual)",
        "medium": "Medium (15-25% annual)",
        "high": "High (25%+ annual)"
    }.get(risk_level, "Medium")
