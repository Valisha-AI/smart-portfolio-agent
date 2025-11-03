"""
Arize Tracing Configuration for Smart Portfolio Agent
Implements OpenTelemetry instrumentation for LangGraph, LangChain, and OpenAI.
"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def init_arize_tracing() -> bool:
    """
    Initialize Arize tracing for the Smart Portfolio Agent.
    
    Returns:
        bool: True if tracing was successfully initialized, False otherwise.
    
    Environment Variables Required:
        - ARIZE_SPACE_ID: Your Arize space ID
        - ARIZE_API_KEY: Your Arize API key
        - ARIZE_PROJECT_NAME: Project name for tracing (default: smart-portfolio-agent)
    """
    
    # Check if Arize credentials are configured
    space_id = os.getenv("ARIZE_SPACE_ID")
    api_key = os.getenv("ARIZE_API_KEY")
    project_name = os.getenv("ARIZE_PROJECT_NAME", "smart-portfolio-agent")
    
    if not space_id or not api_key:
        logger.warning(
            "Arize tracing not configured. Set ARIZE_SPACE_ID and ARIZE_API_KEY "
            "environment variables to enable tracing."
        )
        return False
    
    try:
        # Import Arize tracing libraries
        from arize_otel import register
        from openinference.instrumentation.langchain import LangChainInstrumentor
        from openinference.instrumentation.openai import OpenAIInstrumentor
        
        # Register the Arize tracer provider
        tracer_provider = register(
            space_id=space_id,
            api_key=api_key,
            project_name=project_name
        )
        
        # Instrument LangChain (which includes LangGraph)
        LangChainInstrumentor().instrument(tracer_provider=tracer_provider)
        
        # Instrument OpenAI for deeper traces
        OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
        
        logger.info(
            f"✅ Arize tracing initialized successfully for project: {project_name}"
        )
        logger.info(
            "🔍 Traces will be available at: https://app.arize.com/organizations/YOUR_ORG/spaces/YOUR_SPACE"
        )
        return True
        
    except ImportError as e:
        logger.error(
            f"Failed to import Arize tracing libraries: {e}. "
            "Install with: pip install -r requirements.txt"
        )
        return False
    except Exception as e:
        logger.error(f"Failed to initialize Arize tracing: {e}")
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

