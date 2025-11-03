"""
Arize AX Tracing Configuration for Smart Portfolio Agent
Implements OpenTelemetry instrumentation for LangGraph, LangChain, and OpenAI.

This enables full observability of your portfolio generation agent in Arize AX:
- LangGraph workflow visualization
- Agent node execution traces
- Tool call monitoring
- OpenAI API call tracking (tokens, costs, latency)
- Error debugging and performance analysis
"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def init_arize_tracing() -> bool:
    """
    Initialize Arize AX tracing for the Smart Portfolio Agent.
    
    This will instrument:
    - LangChain/LangGraph: Agent workflows, tool calls, chains
    - OpenAI: LLM calls, token usage, costs, prompts/responses
    
    Returns:
        bool: True if tracing was successfully initialized, False otherwise.
    
    Environment Variables Required:
        - ARIZE_SPACE_ID: Your Arize space ID (from app.arize.com/settings)
        - ARIZE_API_KEY: Your Arize API key
        - ARIZE_PROJECT_NAME: Project name (default: smart-portfolio-agent)
    
    Usage:
        Set environment variables, then call this function on app startup.
        All subsequent LangGraph/OpenAI calls will be automatically traced.
    """
    
    # Check if Arize credentials are configured
    space_id = os.getenv("ARIZE_SPACE_ID")
    api_key = os.getenv("ARIZE_API_KEY")
    project_name = os.getenv("ARIZE_PROJECT_NAME", "smart-portfolio-agent")
    
    if not space_id or not api_key:
        logger.warning(
            "Arize AX tracing not configured. Set ARIZE_SPACE_ID and ARIZE_API_KEY "
            "environment variables to enable observability."
        )
        print("Arize tracing not configured. Set ARIZE_SPACE_ID and ARIZE_API_KEY environment variables to enable tracing.")
        return False
    
    try:
        # Import Arize AX tracing libraries
        from arize.otel import register
        from openinference.instrumentation.langchain import LangChainInstrumentor
        from openinference.instrumentation.openai import OpenAIInstrumentor
        
        # Register the Arize tracer provider
        # This sends traces to Arize AX at otlp.arize.com
        tracer_provider = register(
            space_id=space_id,
            api_key=api_key,
            project_name=project_name
        )
        
        # Instrument LangChain (which includes LangGraph)
        # This will automatically trace:
        # - Agent invocations
        # - Tool executions
        # - Chain operations
        # - State transitions
        LangChainInstrumentor().instrument(tracer_provider=tracer_provider)
        
        # Instrument OpenAI for deeper LLM traces
        # This captures:
        # - Model name (gpt-4o-mini, etc.)
        # - Prompts and responses
        # - Token usage (input/output)
        # - Costs per request
        # - Latency metrics
        OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
        
        logger.info(
            f"✅ Arize AX tracing initialized successfully for project: {project_name}"
        )
        logger.info(
            f"🔍 View traces at: https://app.arize.com"
        )
        print(f"✅ Arize AX tracing enabled: {project_name}")
        return True
        
    except ImportError as e:
        logger.error(
            f"Failed to import Arize tracing libraries: {e}. "
            "Install with: pip install arize-otel openinference-instrumentation-langchain openinference-instrumentation-openai"
        )
        print(f"⚠️  Arize tracing setup failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Failed to initialize Arize AX tracing: {e}")
        print(f"⚠️  Arize tracing initialization error: {e}")
        return False


def get_tracing_status() -> dict:
    """
    Get the current tracing configuration status.
    
    Returns:
        dict: Status information about tracing configuration.
    """
    space_id = os.getenv("ARIZE_SPACE_ID")
    api_key = os.getenv("ARIZE_API_KEY")
    project_name = os.getenv("ARIZE_PROJECT_NAME", "smart-portfolio-agent")
    
    return {
        "enabled": bool(space_id and api_key),
        "space_id_configured": bool(space_id),
        "api_key_configured": bool(api_key),
        "project_name": project_name
    }

