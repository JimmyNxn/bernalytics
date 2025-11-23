"""
SERP API client for fetching LinkedIn job counts via Google Search.
"""

import os
from typing import Optional

from loguru import logger
from serpapi import GoogleSearch

from bernalytics.models import JobCounts


class SerpClient:
    """Client for fetching job counts from LinkedIn via Google Search."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        """Initialize the SERP API client."""
        self.api_key = api_key or os.getenv("SERP_API_KEY")
        if not self.api_key:
            raise ValueError("SERP API key required. Set SERP_API_KEY environment variable.")

    def get_job_counts(
        self,
        job_title: str = "Data Engineer",
        location: str = "Berlin, Germany",
        time_period: str = "week",
    ) -> JobCounts:
        """
        Get job counts for three LinkedIn search terms.

        Args:
            job_title: Job title to search for
            location: Location to search in
            time_period: Time period (default: week)

        Returns:
            JobCounts with results for each search term

        Note:
            Searches for jobs posted in the past week on LinkedIn.
            Uses 'linkedin.com/jobs' in query instead of site: operator for better results.
        """
        logger.info(f"Fetching job counts for '{job_title}' in {location} (period: {time_period})")

        # Extract city name
        city = location.split(",")[0].strip()

        # Perform three searches (without time filter for accurate counts)
        data_engineer_count = self._search(job_title, city)
        junior_count = self._search(f"Junior {job_title}", city)
        senior_count = self._search(f"Senior {job_title}", city)

        counts = JobCounts(
            data_engineer=data_engineer_count,
            junior_data_engineer=junior_count,
            senior_data_engineer=senior_count,
        )

        logger.info(
            f'Results - "Data Engineer": {counts.data_engineer}, '
            f'"Junior Data Engineer": {counts.junior_data_engineer}, '
            f'"Senior Data Engineer": {counts.senior_data_engineer}'
        )

        return counts

    def _search(self, term: str, location: str) -> int:
        """
        Execute a single LinkedIn job search.

        Note: We include 'linkedin.com/jobs' in the query text (not using site: operator)
        because Google provides total_results for these queries with time filters.
        """
        query = f'"{term}" {location} site:linkedin.com/jobs'

        params = {
            "api_key": self.api_key,
            "engine": "google",
            "q": query,
            "num": 10,  # Using 10 instead of 100 - Google returns total_results with smaller num values
            "tbs": "qdr:w",  # Past week filter
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()

            count = 0

            # Try to get total_results from search_information
            if "search_information" in results:
                total_results = results["search_information"].get("total_results")
                if total_results:
                    count = int(str(total_results).replace(",", ""))

            # Fallback to organic_results count
            if count == 0 and "organic_results" in results:
                count = len(results["organic_results"])

            logger.info(f'Query "{term}": ~{count} results found')
            return count

        except Exception as e:
            logger.error(f'Error fetching count for "{term}": {e}')
            return 0
