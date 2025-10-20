# Smart Portfolio Agent - Agent Flow Implementation

## Overview
This document details the multi-agent workflow for the Smart Portfolio (CapitalCube) system, focusing on the **F1: Portfolio Allocation Generation** feature. The system uses LangGraph to orchestrate specialized agents that analyze financial data and generate risk-adjusted portfolio allocations.

---

## Feature F1: Portfolio Allocation Generation

### Input Parameters
- `ticker` (string, required): Target company ticker symbol (e.g., "AAPL")
- `investment_amount` (float, required): Total capital to allocate ($1,000 - $1,000,000)
- `risk_level` (enum, required): "low" | "medium" | "high"
- `include_etfs` (boolean, optional): Include sector ETFs in recommendations (default: false)
- `max_holdings` (integer, optional): 3-5 holdings (default: 5)

### Output Format
```json
{
  "request": {
    "ticker": "AAPL",
    "ticker_name": "Apple Inc.",
    "investment_amount": 10000,
    "risk_level": "medium",
    "analysis_date": "2025-10-20"
  },
  "allocation": [
    {
      "ticker": "AAPL",
      "company_name": "Apple Inc.",
      "allocation_percent": 35,
      "allocation_amount": 3500,
      "sector": "Technology",
      "earnings_quality_score": 4.2,
      "market_cap": "2.8T",
      "rationale": "Core holding - strong fundamentals, consistent earnings growth, market leader"
    },
    {
      "ticker": "MSFT",
      "company_name": "Microsoft Corporation",
      "allocation_percent": 30,
      "allocation_amount": 3000,
      "sector": "Technology",
      "earnings_quality_score": 4.5,
      "market_cap": "2.9T",
      "rationale": "Peer diversification - cloud leadership, recurring revenue model"
    }
  ],
  "summary": {
    "total_holdings": 5,
    "average_earnings_quality": 4.1,
    "risk_profile": "moderate",
    "expected_volatility": "medium",
    "sector_concentration": {
      "Technology": 85,
      "Semiconductors": 10,
      "ETF": 5
    },
    "key_insights": [
      "Portfolio maintains 65% exposure to original ticker and direct peers",
      "Average earnings quality score of 4.1/5 indicates strong fundamental health",
      "Moderate risk profile achieved through large-cap tech concentration"
    ]
  },
  "rationale": "This allocation prioritizes quality mega-cap technology companies with proven earnings power...",
  "risk_disclosure": "Past performance does not guarantee future results. All investments carry risk of loss.",
  "data_sources": [
    "CapitalCube Peer Group Analysis",
    "CapitalCube Earnings Quality Scores",
    "Real-time market data (Yahoo Finance)",
    "Sector classifications (GICS)"
  ]
}
```

---

## Agent Graph Architecture

### Agent Workflow
The system uses **4 specialized agents** working in a sequential-parallel pattern:

```
                    START
                      |
                      v
            ┌─────────────────┐
            │  Peer Research  │  Agent 1: Discover peer companies
            │     Agent       │           via CapitalCube
            └────────┬────────┘
                     │
                     v
            ┌─────────────────┐
            │     Scoring     │  Agent 2: Fetch/calculate earnings
            │     Agent       │           quality scores
            └────────┬────────┘
                     │
                     v
            ┌─────────────────┐
            │   Allocation    │  Agent 3: Apply risk-based allocation
            │     Agent       │           algorithms
            └────────┬────────┘
                     │
                     v
            ┌─────────────────┐
            │    Summary      │  Agent 4: Generate rationale & insights
            │     Agent       │           using LLM
            └────────┬────────┘
                     │
                     v
                    END
```

### Why Sequential?
Unlike the trip planner's parallel agents, the portfolio flow is **sequential** because each agent depends on the previous agent's output:
- **Scoring Agent** needs peer list from **Peer Research Agent**
- **Allocation Agent** needs scores from **Scoring Agent**
- **Summary Agent** needs final allocation from **Allocation Agent**

---

## State Management

### PortfolioState TypedDict
```python
from typing import TypedDict, Annotated, Optional, List, Dict, Any
from langgraph.graph import StateGraph, START, END
import operator

class PortfolioState(TypedDict):
    # Input from user
    ticker: str
    investment_amount: float
    risk_level: str  # "low" | "medium" | "high"
    include_etfs: bool
    max_holdings: int
    
    # Agent outputs (accumulated through workflow)
    peer_candidates: Annotated[List[str], operator.add]  # ["MSFT", "GOOGL", ...]
    peer_scores: Dict[str, float]  # {"AAPL": 4.2, "MSFT": 4.5, ...}
    market_data: Dict[str, Dict]  # Price, market cap for each ticker
    allocation: List[Dict[str, Any]]  # Final allocation list
    rationale: Optional[str]  # LLM-generated explanation
    summary: Optional[Dict]  # Summary statistics
    
    # Metadata
    errors: Annotated[List[str], operator.add]  # Track any errors
    tool_calls: Annotated[List[Dict[str, Any]], operator.add]  # For observability
```

---

## Agent Implementations

### Agent 1: Peer Research Agent

**Responsibility:** Discover peer companies using CapitalCube data

**Tools:**
- `parse_capitalcube_report(ticker)` - Extract peers from PDF
- `search_sector_peers(ticker)` - Fallback using sector lookup

**Implementation:**
```python
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

@tool
def parse_capitalcube_report(ticker: str) -> dict:
    """Parse CapitalCube PDF report to extract peer group."""
    pdf_path = f"data/capitalcube_cache/{ticker}_earnings_quality.pdf"
    
    if not os.path.exists(pdf_path):
        # Download report (implement based on CapitalCube access method)
        pdf_path = download_capitalcube_report(ticker)
    
    # Extract data using PDF parser (see PRD Section C)
    data = extract_capitalcube_data(pdf_path)
    
    return {
        "peers": data["peers"],  # ["COIN-US", "SCHW-US", ...]
        "net_margin_ttm": data["net_margin_ttm"],
        "accruals_ttm": data["accruals_ttm"],
        "accounting_quality": data["accounting_quality"],
        "total_issues": data["total_issues"]
    }

@tool
def search_sector_peers(ticker: str, limit: int = 10) -> List[str]:
    """Fallback: Find peers by sector using Yahoo Finance or similar."""
    import yfinance as yf
    
    stock = yf.Ticker(ticker)
    sector = stock.info.get("sector")
    industry = stock.info.get("industry")
    
    # Query similar companies by sector/industry
    # (Simplified - actual implementation would use screener API)
    peers = query_sector_companies(sector, industry, limit=limit)
    return peers

# Agent function
def peer_research_agent(state: PortfolioState) -> PortfolioState:
    """Agent 1: Discover peer companies."""
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [parse_capitalcube_report, search_sector_peers]
    llm_with_tools = llm.bind_tools(tools)
    
    prompt = f"""
    You are a financial research analyst. Your task is to identify peer companies 
    for {state["ticker"]} using CapitalCube's peer group analysis.
    
    Steps:
    1. Use parse_capitalcube_report to get CapitalCube's assigned peer group
    2. If that fails, use search_sector_peers as fallback
    3. Return 5-8 high-quality peer companies
    
    Target ticker: {state["ticker"]}
    Include ETFs: {state["include_etfs"]}
    """
    
    # Execute LLM with tools
    response = llm_with_tools.invoke(prompt)
    
    # Extract tool results
    if response.tool_calls:
        for tool_call in response.tool_calls:
            result = execute_tool(tool_call)
            state["peer_candidates"].extend(result.get("peers", []))
            state["tool_calls"].append({
                "agent": "peer_research",
                "tool": tool_call["name"],
                "result": result
            })
    
    # Add target ticker to candidates
    if state["ticker"] not in state["peer_candidates"]:
        state["peer_candidates"].insert(0, state["ticker"])
    
    return state
```

---

### Agent 2: Scoring Agent

**Responsibility:** Calculate earnings quality scores for all peer candidates

**Tools:**
- `calculate_quality_score(ticker)` - Derive 1-5 score from CapitalCube data
- `get_market_data(ticker)` - Fetch price, market cap from Yahoo Finance

**Implementation:**
```python
@tool
def calculate_quality_score(ticker: str) -> dict:
    """Calculate earnings quality score from CapitalCube analytics."""
    
    # Check cache first
    cached_score = get_cached_score(ticker)
    if cached_score:
        return cached_score
    
    # Parse CapitalCube report
    data = parse_capitalcube_report(ticker)
    
    # Apply scoring formula (PRD Section F3)
    base_score = 5.0 - (data["total_issues"] / 50) * 3.0
    
    # Adjustments
    if data["accounting_quality"] == "Conservative":
        base_score += 0.5
    elif data["accounting_quality"] == "Aggressive":
        base_score -= 0.5
    
    if data["net_margin_ttm"] > data.get("net_margin_peer_median", 0):
        base_score += 0.3
    
    final_score = max(1.0, min(5.0, base_score))
    
    result = {
        "ticker": ticker,
        "score": round(final_score, 1),
        "net_margin": data["net_margin_ttm"],
        "accounting_quality": data["accounting_quality"],
        "issues_count": data["total_issues"]
    }
    
    # Cache for 7 days
    cache_score(ticker, result, ttl=604800)
    
    return result

@tool
def get_market_data(ticker: str) -> dict:
    """Fetch current price and market cap from Yahoo Finance."""
    import yfinance as yf
    
    stock = yf.Ticker(ticker)
    info = stock.info
    
    return {
        "ticker": ticker,
        "price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "sector": info.get("sector"),
        "company_name": info.get("longName")
    }

def scoring_agent(state: PortfolioState) -> PortfolioState:
    """Agent 2: Calculate quality scores for all candidates."""
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [calculate_quality_score, get_market_data]
    llm_with_tools = llm.bind_tools(tools)
    
    peers_str = ", ".join(state["peer_candidates"][:10])
    
    prompt = f"""
    You are a financial analyst calculating earnings quality scores.
    
    For each ticker: {peers_str}
    
    1. Use calculate_quality_score to get CapitalCube-derived score (1-5 scale)
    2. Use get_market_data to fetch price and market cap
    3. Filter out any tickers with score < 2.5 (too risky)
    4. Return top {state["max_holdings"]} by score
    """
    
    response = llm_with_tools.invoke(prompt)
    
    # Process tool results
    for tool_call in response.tool_calls:
        result = execute_tool(tool_call)
        
        if tool_call["name"] == "calculate_quality_score":
            ticker = result["ticker"]
            state["peer_scores"][ticker] = result["score"]
        
        elif tool_call["name"] == "get_market_data":
            ticker = result["ticker"]
            state["market_data"][ticker] = result
        
        state["tool_calls"].append({
            "agent": "scoring",
            "tool": tool_call["name"],
            "result": result
        })
    
    return state
```

---

### Agent 3: Allocation Agent

**Responsibility:** Apply risk-based allocation algorithms

**Implementation:**
```python
def allocation_agent(state: PortfolioState) -> PortfolioState:
    """Agent 3: Calculate optimal allocation based on risk level."""
    
    risk_level = state["risk_level"]
    amount = state["investment_amount"]
    scores = state["peer_scores"]
    market_data = state["market_data"]
    
    # Sort candidates by score
    sorted_peers = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_peers = sorted_peers[:state["max_holdings"]]
    
    # Apply allocation algorithm based on risk level
    if risk_level == "low":
        allocations = allocate_low_risk(top_peers, amount, state["include_etfs"])
    elif risk_level == "medium":
        allocations = allocate_medium_risk(top_peers, amount, state["include_etfs"])
    else:  # high
        allocations = allocate_high_risk(top_peers, amount, state["ticker"], state["include_etfs"])
    
    # Build allocation objects
    allocation_list = []
    for ticker, percent in allocations:
        allocation_list.append({
            "ticker": ticker,
            "company_name": market_data[ticker]["company_name"],
            "allocation_percent": int(percent * 100),
            "allocation_amount": int(amount * percent),
            "sector": market_data[ticker]["sector"],
            "earnings_quality_score": scores.get(ticker),
            "market_cap": format_market_cap(market_data[ticker]["market_cap"]),
            "rationale": ""  # Filled by summary agent
        })
    
    state["allocation"] = allocation_list
    
    # Calculate summary statistics
    avg_score = sum(a["earnings_quality_score"] for a in allocation_list if a["earnings_quality_score"]) / len(allocation_list)
    
    state["summary"] = {
        "total_holdings": len(allocation_list),
        "average_earnings_quality": round(avg_score, 1),
        "risk_profile": risk_level,
        "expected_volatility": get_volatility_label(risk_level)
    }
    
    return state

# Allocation algorithms (PRD Section 11.1)
def allocate_medium_risk(peers_with_scores: List[tuple], amount: float, include_etfs: bool) -> List[tuple]:
    """Quality-weighted allocation for medium risk."""
    
    total_score = sum(score for ticker, score in peers_with_scores)
    
    allocations = []
    for ticker, score in peers_with_scores:
        raw_weight = score / total_score
        capped_weight = min(raw_weight, 0.35)  # Max 35% per holding
        allocations.append((ticker, capped_weight))
    
    # Normalize to 100%
    total_allocated = sum(weight for _, weight in allocations)
    allocations = [(ticker, weight / total_allocated) for ticker, weight in allocations]
    
    # Add ETF if requested (5% allocation from top holding)
    if include_etfs and len(allocations) > 0:
        sector = get_primary_sector(allocations)
        etf_ticker = get_sector_etf(sector)  # e.g., "XLK" for tech
        
        # Reduce top holding by 5%
        allocations[0] = (allocations[0][0], allocations[0][1] - 0.05)
        allocations.append((etf_ticker, 0.05))
    
    return allocations
```

---

### Agent 4: Summary Agent

**Responsibility:** Generate human-readable rationale using LLM

**Implementation:**
```python
def summary_agent(state: PortfolioState) -> PortfolioState:
    """Agent 4: Generate portfolio rationale and per-holding explanations."""
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    
    # Build context for LLM
    allocation_summary = "\n".join([
        f"- {a['ticker']} ({a['company_name']}): {a['allocation_percent']}%, Score: {a['earnings_quality_score']}"
        for a in state["allocation"]
    ])
    
    prompt = f"""
    Act as a financial analyst with expertise in portfolio construction and fundamental analysis.
    
    TASK: Generate a concise, data-driven allocation rationale.
    
    INPUTS:
    - Target Ticker: {state['ticker']}
    - Investment Amount: ${state['investment_amount']:,}
    - Risk Level: {state['risk_level']}
    - Allocation:
    {allocation_summary}
    
    REQUIREMENTS:
    1. Write a 3-5 sentence overall rationale explaining:
       - Why these specific companies were selected
       - How the allocation balances risk and return
       - Key fundamental strengths (reference quality scores)
    
    2. Generate 2-3 key insights about:
       - Sector concentration implications
       - Overall portfolio quality (avg score: {state['summary']['average_earnings_quality']})
       - Risk profile appropriateness
    
    3. Provide a 1-sentence rationale for EACH holding explaining its role
    
    IMPORTANT:
    - Earnings quality scores (1-5) reflect conservative accounting and cash-backed earnings
    - Higher scores = stronger fundamentals
    - Reference CapitalCube peer analysis
    
    OUTPUT FORMAT: JSON with fields:
    {{
      "overall_rationale": "...",
      "key_insights": ["insight1", "insight2"],
      "per_holding_rationale": {{"AAPL": "...", "MSFT": "..."}}
    }}
    """
    
    response = llm.invoke(prompt)
    rationale_data = parse_json_response(response.content)
    
    # Update state with rationale
    state["rationale"] = rationale_data["overall_rationale"]
    state["summary"]["key_insights"] = rationale_data["key_insights"]
    
    # Add per-holding rationale to allocation objects
    for allocation in state["allocation"]:
        ticker = allocation["ticker"]
        allocation["rationale"] = rationale_data["per_holding_rationale"].get(
            ticker, 
            "Diversification component"
        )
    
    # Add risk disclosure
    state["risk_disclosure"] = "Past performance does not guarantee future results. All investments carry risk of loss. This allocation is for informational purposes only and does not constitute financial advice."
    
    # Add data sources
    state["data_sources"] = [
        "CapitalCube Peer Group Analysis",
        "CapitalCube Earnings Quality Scores",
        "Real-time market data (Yahoo Finance)",
        "Sector classifications (GICS)"
    ]
    
    return state
```

---

## Graph Construction

```python
from langgraph.graph import StateGraph, START, END

def build_portfolio_graph():
    """Build the LangGraph workflow for portfolio generation."""
    
    graph = StateGraph(PortfolioState)
    
    # Add nodes
    graph.add_node("peer_research", peer_research_agent)
    graph.add_node("scoring", scoring_agent)
    graph.add_node("allocation", allocation_agent)
    graph.add_node("summary", summary_agent)
    
    # Add edges (sequential flow)
    graph.add_edge(START, "peer_research")
    graph.add_edge("peer_research", "scoring")
    graph.add_edge("scoring", "allocation")
    graph.add_edge("allocation", "summary")
    graph.add_edge("summary", END)
    
    return graph.compile()
```

---

## FastAPI Endpoint

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Smart Portfolio API")

class PortfolioRequest(BaseModel):
    ticker: str
    investment_amount: float
    risk_level: str
    include_etfs: bool = True
    max_holdings: int = 5

class PortfolioResponse(BaseModel):
    request: dict
    allocation: list
    summary: dict
    rationale: str
    risk_disclosure: str
    data_sources: list

@app.post("/api/v1/portfolio/generate", response_model=PortfolioResponse)
async def generate_portfolio(req: PortfolioRequest):
    """Generate optimized portfolio allocation."""
    
    # Validate inputs
    if req.investment_amount < 1000 or req.investment_amount > 1000000:
        raise HTTPException(status_code=400, detail="Investment amount must be between $1,000 and $1,000,000")
    
    if req.risk_level not in ["low", "medium", "high"]:
        raise HTTPException(status_code=400, detail="Risk level must be 'low', 'medium', or 'high'")
    
    # Build graph
    graph = build_portfolio_graph()
    
    # Initialize state
    initial_state = {
        "ticker": req.ticker.upper(),
        "investment_amount": req.investment_amount,
        "risk_level": req.risk_level,
        "include_etfs": req.include_etfs,
        "max_holdings": req.max_holdings,
        "peer_candidates": [],
        "peer_scores": {},
        "market_data": {},
        "allocation": [],
        "rationale": None,
        "summary": None,
        "errors": [],
        "tool_calls": []
    }
    
    # Execute graph
    try:
        final_state = graph.invoke(initial_state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Portfolio generation failed: {str(e)}")
    
    # Format response
    return PortfolioResponse(
        request={
            "ticker": final_state["ticker"],
            "investment_amount": final_state["investment_amount"],
            "risk_level": final_state["risk_level"],
            "analysis_date": datetime.now().strftime("%Y-%m-%d")
        },
        allocation=final_state["allocation"],
        summary=final_state["summary"],
        rationale=final_state["rationale"],
        risk_disclosure=final_state["risk_disclosure"],
        data_sources=final_state["data_sources"]
    )
```

---

## Performance Expectations

### Latency Breakdown
| Agent | Typical Duration | Operations |
|-------|------------------|------------|
| Peer Research | 2-3s | PDF parsing or API call |
| Scoring | 3-4s | 5-8 score calculations + market data |
| Allocation | <1s | Pure computation |
| Summary | 2-3s | LLM generation (GPT-4) |
| **Total** | **8-10s** | **Full workflow** |

### Optimization Strategies
1. **Caching**: Store CapitalCube scores for 7 days (reports update infrequently)
2. **Parallel Scoring**: Fetch scores for multiple tickers concurrently
3. **Async Tools**: Use `httpx.AsyncClient` for all API calls
4. **Faster LLM**: Use GPT-4o-mini for summary (2x faster, 50% cheaper)

---

## Error Handling

```python
def handle_agent_error(state: PortfolioState, error: Exception, agent_name: str) -> PortfolioState:
    """Gracefully handle agent failures with fallbacks."""
    
    state["errors"].append(f"{agent_name}: {str(error)}")
    
    if agent_name == "peer_research":
        # Fallback: Use sector-based peer discovery
        state["peer_candidates"] = search_sector_peers(state["ticker"], limit=8)
    
    elif agent_name == "scoring":
        # Fallback: Use default scores based on market cap
        for ticker in state["peer_candidates"]:
            state["peer_scores"][ticker] = 3.5  # Neutral score
    
    elif agent_name == "allocation":
        # Fallback: Equal-weight allocation
        equal_weight = 1.0 / state["max_holdings"]
        state["allocation"] = [
            {"ticker": t, "allocation_percent": int(equal_weight * 100)}
            for t in list(state["peer_scores"].keys())[:state["max_holdings"]]
        ]
    
    elif agent_name == "summary":
        # Fallback: Template-based rationale
        state["rationale"] = generate_template_rationale(state["allocation"])
    
    return state
```

---

## Testing

### Unit Test Example
```python
import pytest

def test_peer_research_agent():
    """Test peer discovery for AAPL."""
    state = {
        "ticker": "AAPL",
        "include_etfs": False,
        "peer_candidates": [],
        "tool_calls": []
    }
    
    result = peer_research_agent(state)
    
    assert "AAPL" in result["peer_candidates"]
    assert len(result["peer_candidates"]) >= 5
    assert any("MSFT" in peer or "GOOGL" in peer for peer in result["peer_candidates"])

def test_medium_risk_allocation():
    """Test medium risk allocation algorithm."""
    peers = [("AAPL", 4.2), ("MSFT", 4.5), ("GOOGL", 3.8)]
    amount = 10000
    
    allocations = allocate_medium_risk(peers, amount, include_etfs=False)
    
    # Check total allocation = 100%
    total = sum(weight for _, weight in allocations)
    assert abs(total - 1.0) < 0.01
    
    # Check max single holding <= 35%
    max_allocation = max(weight for _, weight in allocations)
    assert max_allocation <= 0.35
```

### Integration Test
```bash
curl -X POST http://localhost:8000/api/v1/portfolio/generate \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "HOOD",
    "investment_amount": 10000,
    "risk_level": "medium",
    "include_etfs": true,
    "max_holdings": 5
  }'
```

---

## Observability

### Arize Tracing
```python
from arize_otel import register_otel, Endpoints
from openinference.instrumentation.langchain import LangChainInstrumentor

# Initialize tracing
tracer_provider = register_otel(
    space_id=os.getenv("ARIZE_SPACE_ID"),
    api_key=os.getenv("ARIZE_API_KEY"),
    project_name="smart-portfolio",
    endpoints=Endpoints.ARIZE
)

LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

# Traces will show:
# - Each agent execution time
# - Tool calls (PDF parsing, API requests)
# - LLM token usage
# - End-to-end latency
```

---

## Next Steps

1. **Implement PDF Parser** (see PRD Section C for code)
2. **Set up CapitalCube data access** (API or web scraping)
3. **Build allocation algorithms** (PRD Section 11.1)
4. **Create LLM prompts** (PRD Section 9.1)
5. **Deploy with Render.com** (use existing render.yaml)
6. **Add caching layer** (Redis for scores and peer data)

---

**Status:** Ready for Implementation  
**Reference:** `SMART_PORTFOLIO_AGENT_PRD.md` (Section 5.1, Feature F1)  
**Sample Data:** `sample-data/Valisha---EarningsQuality-HOOD-US-10-18-2025.pdf`

