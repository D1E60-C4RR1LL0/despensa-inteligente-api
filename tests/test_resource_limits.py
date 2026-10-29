"""The deployment must reject missing limits, ignored limits and unstable containers."""

import pytest

from scripts.measure_resources import declared_limits, memory_bytes, verify_limits
from scripts import deploy_simulated


@pytest.mark.parametrize("raw,expected", [("128MiB", 134217728), ("1.5GiB", 1610612736),
                                         ("256m", 268435456), ("0B", 0)])
def test_docker_memory_units_are_preserved(raw, expected):
    assert memory_bytes(raw) == expected


def test_normalized_compose_limits_match_engine_units():
    assert declared_limits({"cpus": "0.50", "mem_limit": 268435456}) == {
        "nano_cpus": 500000000, "memory_bytes": 268435456,
    }


@pytest.mark.parametrize("configuration", [{}, {"cpus": "0.50", "mem_limit": 0}])
def test_missing_declared_limits_are_rejected_before_startup(configuration):
    with pytest.raises(ValueError):
        declared_limits(configuration)


def test_explicit_local_baseline_allows_unlimited_resources():
    assert declared_limits({}, require_limits=False) == {"nano_cpus": 0, "memory_bytes": 0}


def test_ci_cannot_use_the_unlimited_baseline(monkeypatch, tmp_path):
    output = tmp_path / "report.json"
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.delenv("GITHUB_RUN_ID", raising=False)
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    monkeypatch.setattr("sys.argv", [
        "deploy_simulated.py", "--image", "inventory-api:unit",
        "--expected-image-id", "sha256:" + "a" * 64, "--commit", "b" * 40,
        "--environment", "unit", "--output", str(output), "--baseline-resources",
    ])
    monkeypatch.setattr(deploy_simulated.subprocess, "run",
                        lambda *args, **kwargs: pytest.fail("La base sin limites no debe ejecutar Docker en CI"))
    assert deploy_simulated.main() == 1


@pytest.mark.parametrize("invalid", ["missing", "ignored", "oom", "restart"])
def test_deployment_rejects_invalid_or_unstable_resource_configuration(invalid):
    expected = {"nano_cpus": 500000000, "memory_bytes": 268435456}
    actual = {**expected, "oom_killed": False, "restart_count": 0}
    if invalid == "missing":
        expected["memory_bytes"] = actual["memory_bytes"] = 0
    elif invalid == "ignored":
        actual["nano_cpus"] = 0
    elif invalid == "oom":
        actual["oom_killed"] = True
    else:
        actual["restart_count"] = 1
    with pytest.raises(ValueError):
        verify_limits(expected, actual)


def test_deployment_accepts_matching_limits_without_oom_or_restarts():
    expected = {"nano_cpus": 500000000, "memory_bytes": 268435456}
    verify_limits(expected, {**expected, "oom_killed": False, "restart_count": 0})
