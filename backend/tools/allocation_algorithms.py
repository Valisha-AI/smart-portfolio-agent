"""
Allocation Algorithms - Risk-based portfolio distribution
Implements low, medium, and high risk strategies.
"""

from typing import List, Tuple, Dict

def allocate_low_risk(
    peers_with_scores: List[Tuple[str, float]],
    include_etf: bool = True,
    etf_ticker: str = "SPY"
) -> List[Tuple[str, float]]:
    """
    Low Risk Strategy: Conservative with ETF buffer
    - 40% in sector ETF
    - 60% split equally among top 4 peers
    - Max 20% per stock
    """
    allocations = []
    
    if include_etf:
        allocations.append((etf_ticker, 0.40))
        remaining = 0.60
        peer_count = min(4, len(peers_with_scores))
    else:
        remaining = 1.0
        peer_count = min(5, len(peers_with_scores))
    
    if peer_count > 0:
        per_peer = remaining / peer_count
        for ticker, score in peers_with_scores[:peer_count]:
            allocations.append((ticker, per_peer))
    
    return allocations

def allocate_medium_risk(
    peers_with_scores: List[Tuple[str, float]],
    include_etf: bool = True,
    etf_ticker: str = "SPY"
) -> List[Tuple[str, float]]:
    """
    Medium Risk Strategy: Quality-weighted allocation
    - Weight by quality score
    - Max 35% per holding
    - Optional 5% ETF for diversification
    """
    # Calculate total score
    total_score = sum(score for _, score in peers_with_scores)
    
    if total_score == 0:
        # Fallback to equal weight
        return allocate_low_risk(peers_with_scores, include_etf, etf_ticker)
    
    allocations = []
    
    # Calculate raw weights based on scores
    for ticker, score in peers_with_scores[:5]:
        raw_weight = score / total_score
        capped_weight = min(raw_weight, 0.35)  # Max 35% per holding
        allocations.append((ticker, capped_weight))
    
    # Normalize to sum to 1.0 (or 0.95 if including ETF)
    total_allocated = sum(weight for _, weight in allocations)
    
    if include_etf and total_allocated > 0.05:
        # Reserve 5% for ETF
        allocations = [(ticker, weight * 0.95 / total_allocated) for ticker, weight in allocations]
        allocations.append((etf_ticker, 0.05))
    else:
        # Normalize to 100%
        allocations = [(ticker, weight / total_allocated) for ticker, weight in allocations]
    
    return allocations

def allocate_high_risk(
    peers_with_scores: List[Tuple[str, float]],
    target_ticker: str,
    include_etf: bool = False,
    etf_ticker: str = "SPY"
) -> List[Tuple[str, float]]:
    """
    High Risk Strategy: Concentrated conviction
    - Target ticker: 40%
    - Top peer: 30%
    - Second peer: 20%
    - Third peer: 10%
    - Optional: Small ETF position
    """
    allocations = []
    
    # Ensure target ticker is first
    target_included = False
    sorted_peers = []
    
    for ticker, score in peers_with_scores:
        if ticker == target_ticker:
            target_included = True
        else:
            sorted_peers.append((ticker, score))
    
    if target_included or len(peers_with_scores) > 0:
        # Add target with 40%
        if target_ticker in [t for t, _ in peers_with_scores]:
            allocations.append((target_ticker, 0.40))
        else:
            # If target not in peers, use first peer as main holding
            allocations.append((peers_with_scores[0][0], 0.40))
            sorted_peers = peers_with_scores[1:]
        
        # Add remaining peers
        if len(sorted_peers) >= 1:
            allocations.append((sorted_peers[0][0], 0.30))
        if len(sorted_peers) >= 2:
            allocations.append((sorted_peers[1][0], 0.20))
        if len(sorted_peers) >= 3:
            if include_etf:
                allocations.append((sorted_peers[2][0], 0.07))
                allocations.append((etf_ticker, 0.03))
            else:
                allocations.append((sorted_peers[2][0], 0.10))
    
    return allocations

def format_allocation(
    allocations: List[Tuple[str, float]],
    amount: float,
    peer_data: Dict[str, Dict]
) -> List[Dict]:
    """
    Format allocation into detailed response structure.
    """
    formatted = []
    
    for ticker, percent in allocations:
        data = peer_data.get(ticker, {})
        
        formatted.append({
            "ticker": ticker,
            "company_name": data.get("company_name", ticker),
            "allocation_percent": int(percent * 100),
            "allocation_amount": int(amount * percent),
            "sector": data.get("sector", "Unknown"),
            "earnings_quality_score": data.get("score"),
            "market_cap": data.get("market_cap_formatted", "N/A"),
            "rationale": ""  # Will be filled by LLM
        })
    
    return formatted

