"""
Smart Portfolio Agent - FastAPI Application
Main entry point for the portfolio allocation API.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Smart Portfolio API",
    description="AI-powered portfolio allocation using CapitalCube analytics",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Request/Response Models
# ============================================

class PortfolioRequest(BaseModel):
    ticker: str = Field(..., description="Target company ticker symbol (e.g., 'AAPL')")
    investment_amount: float = Field(..., ge=1000, le=1000000, description="Investment amount ($1K-$1M)")
    risk_level: str = Field(..., pattern="^(low|medium|high)$", description="Risk tolerance level")
    include_etfs: bool = Field(default=True, description="Include sector ETFs")
    max_holdings: int = Field(default=5, ge=3, le=5, description="Maximum number of holdings")

class AllocationItem(BaseModel):
    ticker: str
    company_name: str
    allocation_percent: int
    allocation_amount: int
    sector: str
    earnings_quality_score: Optional[float]
    market_cap: str
    rationale: str

class PortfolioSummary(BaseModel):
    total_holdings: int
    average_earnings_quality: float
    risk_profile: str
    expected_volatility: str
    sector_concentration: Dict[str, int]
    key_insights: List[str]

class PortfolioResponse(BaseModel):
    request: Dict[str, Any]
    allocation: List[AllocationItem]
    summary: PortfolioSummary
    rationale: str
    risk_disclosure: str
    data_sources: List[str]

# ============================================
# API Endpoints
# ============================================

@app.get("/")
async def root():
    """Serve the web UI."""
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "portfolio.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    else:
        return {
            "service": "Smart Portfolio API",
            "status": "healthy",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "web_ui": "Open /ui for the web interface"
        }

@app.get("/ui")
async def web_ui():
    """Serve the web UI."""
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "portfolio.html")
    return FileResponse(frontend_path)

@app.get("/api")
async def api_info():
    """API information endpoint."""
    return {
        "service": "Smart Portfolio API",
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check."""
    try:
        from config.tracing import get_tracing_status
        tracing_status = get_tracing_status()
    except:
        tracing_status = {"enabled": False}
    
    return {
        "status": "healthy",
        "checks": {
            "api": "ok",
            "llm": "ok" if os.getenv("OPENAI_API_KEY") else "missing_key",
            "cache": "ok" if os.getenv("REDIS_URL") else "not_configured",
            "tracing": "ok" if tracing_status.get("enabled") else "not_configured"
        },
        "tracing": tracing_status
    }

@app.post("/api/v1/portfolio/generate", response_model=PortfolioResponse)
async def generate_portfolio(req: PortfolioRequest):
    """
    Generate optimized portfolio allocation.
    
    This endpoint uses real market data and allocation algorithms:
    1. Peer Research - Yahoo Finance sector analysis
    2. Quality Scoring - Fundamental-based scores
    3. Allocation - Risk-based distribution algorithms
    4. Rationale - GPT-4 generated explanations
    """
    
    # Validate inputs
    if req.investment_amount < 1000 or req.investment_amount > 1000000:
        raise HTTPException(
            status_code=400,
            detail="Investment amount must be between $1,000 and $1,000,000"
        )
    
    if req.risk_level not in ["low", "medium", "high"]:
        raise HTTPException(
            status_code=400,
            detail="Risk level must be 'low', 'medium', or 'high'"
        )
    
    # Import the working agent
    try:
        from agents.portfolio_agent import generate_portfolio_allocation
        
        # Generate portfolio
        result = generate_portfolio_allocation(
            ticker=req.ticker.upper(),
            investment_amount=req.investment_amount,
            risk_level=req.risk_level,
            include_etfs=req.include_etfs,
            max_holdings=req.max_holdings
        )
        
        # Convert to response model
        return PortfolioResponse(**result)
        
    except Exception as e:
        print(f"Error generating portfolio: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Portfolio generation failed: {str(e)}"
        )

@app.get("/api/v1/scores/{ticker}")
async def get_ticker_score(ticker: str):
    """
    Get earnings quality score for a specific ticker.
    """
    # TODO: Implement score lookup
    raise HTTPException(
        status_code=501,
        detail="Score lookup not yet implemented"
    )

@app.get("/api/v1/portfolio/compare")
async def compare_risk_levels(
    ticker: str,
    amount: float,
    levels: str = "low,medium,high"
):
    """
    Compare portfolio allocations across multiple risk levels.
    """
    # TODO: Implement comparison logic
    raise HTTPException(
        status_code=501,
        detail="Comparison endpoint not yet implemented"
    )

# ============================================
# Startup/Shutdown Events
# ============================================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    print("🚀 Smart Portfolio API starting up...")
    print(f"📊 Version: 1.0.0")
    print(f"🔑 OpenAI API Key: {'✅ Configured' if os.getenv('OPENAI_API_KEY') else '❌ Missing'}")
    print(f"📈 CapitalCube: {'✅ Configured' if os.getenv('CAPITALCUBE_API_KEY') else '⚠️  Not configured'}")
    print(f"💾 Redis: {'✅ Configured' if os.getenv('REDIS_URL') else '⚠️  Not configured'}")
    
    # Initialize Arize tracing
    try:
        from config.tracing import init_arize_tracing, get_tracing_status
        tracing_enabled = init_arize_tracing()
        status = get_tracing_status()
        if tracing_enabled:
            print(f"🔍 Arize Tracing: ✅ Enabled (Project: {status['project_name']})")
        else:
            print("🔍 Arize Tracing: ⚠️  Not configured (set ARIZE_SPACE_ID and ARIZE_API_KEY)")
    except Exception as e:
        print(f"🔍 Arize Tracing: ⚠️  Initialization failed: {e}")
    
    print("Ready to accept requests!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    print("👋 Smart Portfolio API shutting down...")

# ============================================
# Run Server
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

