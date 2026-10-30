"""Reject misleading capacity comparisons and successful HTTP responses with wrong data."""

from copy import deepcopy

import pytest

from scripts.capacity_workload import CASE, CASE_DIGEST, PROFILES, summarize, validate_response
from scripts.compare_capacity import ORDER, compare
from scripts.measure_resources import SERVICES, declared_limits


@pytest.fixture
def comparison_reports():
    reports = []
    for profile in ORDER:
        resources = {}
        for service in SERVICES:
            declared = declared_limits(PROFILES[profile] if service == "api" else
                                       {"cpus": 1, "mem_limit": "768m"})
            resources[service] = {"declared": declared,
                                 "actual": {**declared, "oom_killed": False, "restart_count": 0}}
        reports.append({"status": "success", "cleanup": "success", "resource_mode": "bounded",
            "capacity_profile": profile, "commit": "a" * 40, "image_id": "sha256:" + "b" * 64,
            "expected_image_id": "sha256:" + "b" * 64,
            "checks": dict.fromkeys(("build_identity", "container_identity", "migrations", "healthy",
                "openapi", "signup", "login", "database_read_write", "resource_limits", "capacity_workload"), True),
            "capacity_workload": {"case": deepcopy(CASE), "case_sha256": CASE_DIGEST,
                "requests": CASE["requests"], "successful": CASE["requests"], "errors": 0,
                "requests_per_second": 100 if profile == "standard" else 80, "p95_latency_ms": 50},
            "effective_limits": resources,
            "resource_measurements": {"sampling_errors": [],
                "services": {service: {"sample_count": 1} for service in SERVICES}}})
    return reports


@pytest.mark.parametrize("invalid", ["image", "workload", "errors", "quota", "cleanup", "missing_run"])
def test_noncomparable_or_failed_capacity_runs_are_rejected(comparison_reports, invalid):
    report = comparison_reports[1]
    if invalid == "image":
        report["image_id"] = "sha256:" + "c" * 64
    elif invalid == "workload":
        report["capacity_workload"]["case"]["concurrency"] += 1
    elif invalid == "errors":
        report["capacity_workload"]["errors"] = 1
    elif invalid == "quota":
        report["effective_limits"]["api"]["actual"]["nano_cpus"] = 0
    elif invalid == "cleanup":
        report["cleanup"] = "failure"
    else:
        comparison_reports.pop()
    with pytest.raises(ValueError):
        compare(comparison_reports)


def test_a_slower_expanded_profile_is_reported_without_inventing_an_improvement(comparison_reports):
    result = compare(comparison_reports)
    assert result["observed_throughput_ratio_expanded_over_standard"] == 0.8
    assert result["profiles"]["expanded"]["successful_requests"] == CASE["requests"] * 2


@pytest.mark.parametrize("rows", [[], [{"id": 999, "activo": True, "stock_minimo": 5}],
                                  [{"id": 1, "activo": True, "stock_minimo": 0}]])
def test_http_200_with_wrong_inventory_is_rejected(rows):
    with pytest.raises(ValueError):
        validate_response("/productos/", rows, {1})


def test_error_counts_and_nearest_rank_p95_include_all_attempts():
    result = summarize(list(range(1, 101)), {"TimeoutError": 2}, 10)
    assert result["successful"] == 98 and result["errors"] == 2
    assert result["p95_latency_ms"] == 95 and result["requests_per_second"] == 10
