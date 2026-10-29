"""A deployment must reject an artifact from a different build before starting Compose."""

import json
from types import SimpleNamespace

import pytest

from scripts import deploy_simulated


@pytest.mark.parametrize("wrong_identity", ["image_id", "revision"])
def test_wrong_build_is_rejected_before_creating_resources(monkeypatch, tmp_path, wrong_identity):
    commit = "a" * 40
    image_id = "sha256:" + "b" * 64
    output = tmp_path / "report.json"
    calls = []

    def inspect_image(command, **kwargs):
        calls.append(command)
        return SimpleNamespace(returncode=0, stdout=json.dumps([{
            "Id": "sha256:" + "c" * 64 if wrong_identity == "image_id" else image_id,
            "Config": {"Labels": {"org.opencontainers.image.revision":
                                   "d" * 40 if wrong_identity == "revision" else commit}},
        }]))

    monkeypatch.setattr(deploy_simulated.subprocess, "run", inspect_image)
    monkeypatch.delenv("GITHUB_RUN_ID", raising=False)
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    monkeypatch.setattr("sys.argv", [
        "deploy_simulated.py", "--image", "inventory-api:expected",
        "--expected-image-id", image_id, "--commit", commit,
        "--environment", "unit-test", "--output", str(output),
    ])

    assert deploy_simulated.main() == 1
    assert calls == [["docker", "image", "inspect", "inventory-api:expected"]]
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["status"] == "failure"
    assert report["failed_stage"] == "image_identity"
    assert report["cleanup"] == "not_needed"
    assert "project" not in report
