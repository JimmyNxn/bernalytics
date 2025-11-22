"""
Tests for JobCounts model.
"""

import pytest

from bernalytics.models import JobCounts


def test_create_job_counts():
    """Test creating a JobCounts instance."""
    counts = JobCounts(
        data_engineer=237,
        junior_data_engineer=10,
        senior_data_engineer=191
    )

    assert counts.data_engineer == 237
    assert counts.junior_data_engineer == 10
    assert counts.senior_data_engineer == 191


def test_job_counts_defaults():
    """Test JobCounts with default values."""
    counts = JobCounts()

    assert counts.data_engineer == 0
    assert counts.junior_data_engineer == 0
    assert counts.senior_data_engineer == 0


def test_job_counts_negative_values():
    """Test that negative values are rejected."""
    with pytest.raises(ValueError):
        JobCounts(
            data_engineer=-5,
            junior_data_engineer=10,
            senior_data_engineer=191
        )
