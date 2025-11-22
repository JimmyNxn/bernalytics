"""
API module for interacting with external services.

This module contains clients for various APIs used in the pipeline,
primarily the SERP API for job search data.
"""

from bernalytics.api.serp_client import SerpClient

__all__ = ["SerpClient"]
