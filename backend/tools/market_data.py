"""
Market Data Tools - Yahoo Finance Integration
Free market data and peer discovery.
"""

import yfinance as yf
from typing import Dict, List, Optional
import pandas as pd

def get_stock_info(ticker: str) -> Dict:
    """Get comprehensive stock information from Yahoo Finance."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get market cap - try multiple fields
        market_cap = info.get("marketCap", 0)
        if market_cap == 0 or market_cap is None:
            market_cap = info.get("market_cap", 0)
        
        # Format it immediately
        market_cap_formatted = format_market_cap(market_cap) if market_cap else "N/A"
        
        return {
            "ticker": ticker,
            "company_name": info.get("longName", info.get("shortName", ticker)),
            "sector": info.get("sector", "Unknown"),
            "industry": info.get("industry", "Unknown"),
            "market_cap": market_cap,
            "market_cap_formatted": market_cap_formatted,
            "price": info.get("currentPrice", info.get("regularMarketPrice", 0)),
            "pe_ratio": info.get("trailingPE", 0),
            "profit_margin": info.get("profitMargins", 0),
            "debt_to_equity": info.get("debtToEquity", 0),
            "revenue_growth": info.get("revenueGrowth", 0),
            "earnings_growth": info.get("earningsGrowth", 0),
        }
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return {
            "ticker": ticker,
            "company_name": ticker,
            "sector": "Unknown",
            "market_cap": 0,
            "market_cap_formatted": "N/A",
            "price": 0
        }

def find_sector_peers(ticker: str, limit: int = 10) -> List[str]:
    """
    Find peer companies in the same sector/industry.
    Uses a curated list of major companies by sector.
    """
    try:
        stock = yf.Ticker(ticker)
        sector = stock.info.get("sector", "")
        industry = stock.info.get("industry", "")
        
        # Curated peer groups by sector
        sector_peers = {
            "Technology": ["AAPL", "MSFT", "GOOGL", "META", "NVDA", "AMD", "INTC", "AVGO", "ORCL", "CRM"],
            "Financial Services": ["JPM", "BAC", "WFC", "GS", "MS", "C", "SCHW", "BLK"],
            "Communication Services": ["GOOGL", "META", "DIS", "NFLX", "CMCSA", "T", "VZ"],
            "Consumer Cyclical": ["AMZN", "TSLA", "HD", "NKE", "MCD", "SBUX", "TGT"],
            "Healthcare": ["JNJ", "UNH", "PFE", "ABBV", "TMO", "MRK", "ABT", "DHR"],
            "Consumer Defensive": ["PG", "KO", "PEP", "WMT", "COST", "PM", "MO"],
            "Industrials": ["BA", "HON", "UPS", "CAT", "GE", "MMM", "LMT"],
            "Energy": ["XOM", "CVX", "COP", "SLB", "EOG", "MPC"],
            "Real Estate": ["AMT", "PLD", "CCI", "EQIX", "PSA", "SPG"],
            "Utilities": ["NEE", "DUK", "SO", "D", "AEP"],
            "Basic Materials": ["LIN", "APD", "ECL", "DD", "NEM"]
        }
        
        # Special case: Fintech companies
        fintech_tickers = ["HOOD", "COIN", "SOFI", "SQ", "PYPL", "AFRM"]
        if ticker in fintech_tickers:
            peers = [t for t in fintech_tickers if t != ticker]
            peers.extend(["SCHW", "MS", "GS"])  # Add traditional finance
            return peers[:limit]
        
        # Get peers from sector
        if sector in sector_peers:
            peers = [t for t in sector_peers[sector] if t != ticker]
            return peers[:limit]
        
        # Fallback: return some large-cap stocks
        return ["SPY", "QQQ", "AAPL", "MSFT", "GOOGL"][:limit]
        
    except Exception as e:
        print(f"Error finding peers for {ticker}: {e}")
        return ["SPY", "QQQ"]

def calculate_fundamental_score(stock_info: Dict) -> float:
    """
    Calculate a quality score (1-5) based on fundamentals.
    Similar to CapitalCube's approach but using available metrics.
    """
    score = 3.0  # Start at neutral
    
    # Profit margin (higher is better)
    profit_margin = stock_info.get("profit_margin", 0)
    if profit_margin > 0.20:
        score += 0.5
    elif profit_margin > 0.10:
        score += 0.3
    elif profit_margin < 0:
        score -= 0.5
    
    # P/E ratio (reasonable range is good)
    pe_ratio = stock_info.get("pe_ratio", 0)
    if 10 < pe_ratio < 25:
        score += 0.3
    elif pe_ratio > 50:
        score -= 0.3
    
    # Debt to equity (lower is better)
    debt_to_equity = stock_info.get("debt_to_equity", 0)
    if debt_to_equity < 50:
        score += 0.4
    elif debt_to_equity > 150:
        score -= 0.4
    
    # Revenue growth (positive is good)
    revenue_growth = stock_info.get("revenue_growth", 0)
    if revenue_growth > 0.15:
        score += 0.4
    elif revenue_growth < 0:
        score -= 0.3
    
    # Earnings growth
    earnings_growth = stock_info.get("earnings_growth", 0)
    if earnings_growth > 0.15:
        score += 0.3
    elif earnings_growth < 0:
        score -= 0.3
    
    # Cap between 1.0 and 5.0
    return max(1.0, min(5.0, round(score, 1)))

def get_sector_etf(sector: str) -> Optional[str]:
    """Get the appropriate sector ETF ticker."""
    sector_etfs = {
        "Technology": "XLK",
        "Financial Services": "XLF",
        "Healthcare": "XLV",
        "Energy": "XLE",
        "Consumer Cyclical": "XLY",
        "Consumer Defensive": "XLP",
        "Industrials": "XLI",
        "Real Estate": "XLRE",
        "Utilities": "XLU",
        "Basic Materials": "XLB",
        "Communication Services": "XLC"
    }
    return sector_etfs.get(sector, "SPY")  # Default to S&P 500

def format_market_cap(market_cap: int) -> str:
    """Format market cap in readable form."""
    if market_cap >= 1_000_000_000_000:
        return f"${market_cap / 1_000_000_000_000:.1f}T"
    elif market_cap >= 1_000_000_000:
        return f"${market_cap / 1_000_000_000:.1f}B"
    elif market_cap >= 1_000_000:
        return f"${market_cap / 1_000_000:.1f}M"
    else:
        return f"${market_cap:,.0f}"

