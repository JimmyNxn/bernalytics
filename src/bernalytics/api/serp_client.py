"""
SERP API client for fetching job count data from LinkedIn via Google Search.

This module provides a client for using SERP API's Google Search engine
to count LinkedIn job postings by searching with site:linkedin.com/jobs filter.
This approach works better than Google Jobs API for certain locations.
"""

import os
from typing import Optional

from loguru import logger
from serpapi import GoogleSearch

from bernalytics.models import JobCounts


class SerpClient:
    """Client for fetching job counts from LinkedIn via Google Search."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Initialize the SERP API client.

        Args:
            api_key: SERP API key. If not provided, will look for SERP_API_KEY
                    environment variable.

        Raises:
            ValueError: If no API key is provided or found in environment.
        """
        self.api_key = api_key or os.getenv("SERP_API_KEY")
        if not self.api_key:
            raise ValueError(
                "SERP API key is required. Provide it as an argument or set "
                "SERP_API_KEY environment variable."
            )
        logger.info("SERP API client initialized")

    def get_job_counts(
        self,
        job_title: str = "Data Engineer",
        location: str = "Berlin, Germany",
        time_period: str = "week",
    ) -> JobCounts:
        """
        Get job counts for junior, mid, and senior level positions from LinkedIn.

        Uses Google Search with site:linkedin.com/jobs filter to count job postings.

        Args:
            job_title: Base job title to search for (default: "Data Engineer")
            location: Location to search in (default: "Berlin, Germany")
            time_period: Time period for job postings. Options: "day", "week",
                        "month", "year", "all" (default: "week")

        Returns:
            JobCounts object with counts for each experience level
        """
        logger.info(f"Fetching job counts for '{job_title}' in {location} (period: {time_period})")

        # Map time period to Google Search time range parameter
        time_range_mapping = {
            "day": "d",  # Past 24 hours
            "week": "w",  # Past week
            "month": "m",  # Past month
            "year": "y",  # Past year
            "all": None,  # All time
        }
        time_range = time_range_mapping.get(time_period.lower(), "w")

        # Extract city name from location (e.g., "Berlin, Germany" -> "Berlin")
        city = location.split(",")[0].strip()

        # Get counts for each search term
        # 1. "Data Engineer" (total)
        # 2. "Junior Data Engineer"
        # 3. "Senior Data Engineer"
        # Then calculate Mid = Total - Junior - Senior
        
        total_count = self._get_linkedin_count(
            job_title=job_title,
            level="Total",
            location=city,
            time_range=time_range,
        )

        junior_count = self._get_linkedin_count(
            job_title=job_title,
            level="Junior",
            location=city,
            time_range=time_range,
        )

        senior_count = self._get_linkedin_count(
            job_title=job_title,
            level="Senior",
            location=city,
            time_range=time_range,
        )

        counts = JobCounts(
            data_engineer=total_count,
            junior_data_engineer=junior_count,
            senior_data_engineer=senior_count,
        )

        logger.info(
            f'Search results - "Data Engineer": {counts.data_engineer}, '
            f'"Junior Data Engineer": {counts.junior_data_engineer}, '
            f'"Senior Data Engineer": {counts.senior_data_engineer}'
        )

        return counts

    def _get_linkedin_count(
        self,
        job_title: str,
        level: str,
        location: str,
        time_range: Optional[str],
    ) -> int:
        """
        Get the count of LinkedIn jobs for a specific search query.

        Args:
            job_title: Base job title (e.g., "Data Engineer")
            level: Experience level (e.g., "Junior", "Mid", "Senior")
            location: City name (e.g., "Berlin")
            time_range: Time range filter (d/w/m/y or None)

        Returns:
            Number of job postings found
        """
        # Build search query with LinkedIn site filter
        # Use quoted phrases for precise matching of job titles
        if level == "Total":
            # Search for just "Data Engineer" to get total count
            query = f'"{job_title}" {location} site:linkedin.com/jobs'
        else:
            # Use exact phrase matching for Junior and Senior
            query = f'"{level} {job_title}" {location} site:linkedin.com/jobs'
            query = f'"{level} {job_title}" {location} site:linkedin.com/jobs'

        # Build search parameters
        params = {
            "api_key": self.api_key,
            "engine": "google",
            "q": query,
            "num": 100,  # Request max results per page
        }

        # Add time range filter if specified
        if time_range:
            params["tbs"] = f"qdr:{time_range}"

        try:
            search = GoogleSearch(params)
            results = search.get_dict()

            # Debug: Log the response structure
            logger.debug(f"API response keys: {list(results.keys())}")

            # Get the count from results
            count = 0

            # First, try to get total_results from search_information
            if "search_information" in results:
                search_info = results["search_information"]

                if "total_results" in search_info:
                    total_results = search_info["total_results"]
                    try:
                        # Convert string like "1,234" or 1234 to integer
                        if isinstance(total_results, str):
                            count = int(total_results.replace(",", ""))
                        else:
                            count = int(total_results)
                        logger.debug(f"Found {count} results from search_information.total_results")
                    except (ValueError, TypeError) as e:
                        logger.warning(f"Failed to parse total_results '{total_results}': {e}")

            # For site: searches, Google often doesn't provide total_results
            # Use organic_results as an approximate count
            if count == 0 and "organic_results" in results:
                organic_count = len(results["organic_results"])
                if organic_count > 0:
                    # We got results but no total_results field
                    # This is typical for site: searches
                    # Use the organic results count as our estimate
                    count = organic_count
                    logger.debug(
                        f"Using organic_results count: {count} (site: search, no total_results)"
                    )
                else:
                    logger.debug(f"No organic_results found")

            if count == 0:
                logger.warning(f"Query '{query}': No results found")
            else:
                logger.info(f"Query '{query}': ~{count} results found")

            return count

        except Exception as e:
            logger.error(f"Error fetching job count for query '{query}': {e}")
            logger.debug(f"Full error details: {str(e)}", exc_info=True)
            return 0
