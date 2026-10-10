"""Comprehensive test suite for Telemetry Automated Health Check Probe.

Verifies:
- 20 kHz sampling rate verification from dataset metadata, time deltas, and explicit rates
- Rejection of deviant/unsupported sampling frequencies
- ISO 10816 Zone C / Jones C vibration threshold (4.50 mm/s RMS) enforcement
- Dual alias support for 'Jones C' and 'Zone C'
- Boundary excursion discrimination (< 4.5 mm/s vs > 4.5 mm/s)
- NASA IMS Bearing Run-to-Failure dataset (REC-001 nominal vs REC-042 excursion)
- Composite TelemetryHealthReport serialization and health status
- TelemetryWorker integration with probe
- FastAPI HTTP endpoints (/api/telemetry/health, /api/telemetry/probe)
"""
from datetime import datetime, timezone
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from telemetry.adapters.public_dataset import PublicDatasetReplayAdapter
from telemetry.probe import (
    ISO_10816_ZONE_C_THRESHOLD_MMS,
    STANDARD_CITATION,
    TARGET_SAMPLING_RATE_HZ,
    TARGET_SAMPLING_RATE_KHZ,
    ProbeItemResult,
    TelemetryHealthProbe,
    TelemetryHealthReport,
    run_telemetry_health_check,
)
from telemetry.worker import TelemetryWorker


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def probe():
    return TelemetryHealthProbe()


# ---------------------------------------------------------------------------
# 1. 20 kHz Sampling Rate Verification Tests
# ---------------------------------------------------------------------------

def test_sampling_rate_verification_default_fixture(probe):
    """Verify probe detects authentic 20 kHz rate from NASA IMS dataset fixture."""
    result = probe.verify_sampling_rate()
    assert result.passed is True
    assert result.status == "PASS"
    assert result.actual_value == 20000.0
    assert result.target_value == 20000.0
    assert result.unit == "Hz"
    assert "20 kHz" in result.details or "20000" in result.details
    assert result.metadata["target_khz"] == 20.0
    assert result.metadata["actual_khz"] == 20.0


def test_sampling_rate_verification_metadata_formats(probe):
    """Verify rate detection across diverse metadata dictionary schemas."""
    # Standard hz field
    res1 = probe.verify_sampling_rate(data_or_metadata={"sampling_rate_hz": 20000})
    assert res1.passed is True
    assert res1.actual_value == 20000.0

    # kHz field
    res2 = probe.verify_sampling_rate(data_or_metadata={"sampling_frequency_khz": 20.0})
    assert res2.passed is True
    assert res2.actual_value == 20000.0

    # Generic sampling_rate field
    res3 = probe.verify_sampling_rate(data_or_metadata={"sampling_rate": 20000.0})
    assert res3.passed is True
    assert res3.actual_value == 20000.0


def test_sampling_rate_verification_from_timestamps_time_series(probe):
    """Verify effective sampling rate calculation from series of timestamp deltas."""
    # dt = 1 / 20,000 s = 0.00005 s (50 microseconds)
    dt = 1.0 / 20000.0
    timestamps = [i * dt for i in range(100)]
    result = probe.verify_sampling_rate(timestamps=timestamps)
    assert result.passed is True
    assert result.status == "PASS"
    assert abs(result.actual_value - 20000.0) < 0.1


def test_sampling_rate_rejection_deviant_frequencies(probe):
    """Verify probe rejects non-compliant frequencies (e.g. 10 kHz, 44.1 kHz, missing)."""
    # 10 kHz stream
    res_10k = probe.verify_sampling_rate(sampling_rate_hz=10000.0)
    assert res_10k.passed is False
    assert res_10k.status == "FAIL"
    assert "mismatch" in res_10k.details.lower() or "failed" in res_10k.details.lower()

    # 44.1 kHz audio rate
    res_44k = probe.verify_sampling_rate(sampling_rate_hz=44100.0)
    assert res_44k.passed is False
    assert res_44k.status == "FAIL"

    # Missing metadata
    res_missing = probe.verify_sampling_rate(data_or_metadata={})
    assert res_missing.passed is False
    assert res_missing.status == "FAIL"


def test_sampling_rate_configurable_tolerance():
    """Verify tolerance parameter allows controlled deviation when explicitly specified."""
    strict_probe = TelemetryHealthProbe(tolerance_hz=0.0)
    assert strict_probe.verify_sampling_rate(sampling_rate_hz=20010.0).passed is False

    lenient_probe = TelemetryHealthProbe(tolerance_hz=25.0)
    assert lenient_probe.verify_sampling_rate(sampling_rate_hz=20010.0).passed is True
    assert lenient_probe.verify_sampling_rate(sampling_rate_hz=20050.0).passed is False


# ---------------------------------------------------------------------------
# 2. ISO 10816 Zone C Threshold Verification Tests
# ---------------------------------------------------------------------------

def test_iso_10816_zone_c_threshold_default(probe):
    """Verify default ISO 10816 Zone C check passes at 4.5 mm/s RMS."""
    result = probe.verify_iso_10816_threshold(zone_alias="Zone C")
    assert result.passed is True
    assert result.status == "PASS"
    assert result.target_value == 4.50
    assert result.actual_value == 4.50
    assert result.unit == "mm/s"
    assert "ISO 10816" in result.details
    assert "4.50 mm/s" in result.details or "4.5 mm/s" in result.details
    assert result.metadata["canonical_zone"] == "Zone C"
    assert result.metadata["zone_alias"] == "Zone C"


def test_iso_10816_zone_c_alias_support(probe):
    """Verify bidirectional support for 'Jones C', 'Zone C', and common variants."""
    recognized_variants = [
        "Jones C",
        "Zone C",
        "jones c",
        "zone c",
        "ISO 10816 Jones C",
        "ISO 10816 Zone C",
        "iso-10816 zone c",
        "iso-10816 jones c",
    ]
    for variant in recognized_variants:
        res = probe.verify_iso_10816_threshold(zone_alias=variant)
        assert res.passed is True, f"Expected variant '{variant}' to pass"

    # Unrecognized variant must fail
    res_bad = probe.verify_iso_10816_threshold(zone_alias="Zone Unknown")
    assert res_bad.passed is False
    assert "Unrecognized zone" in res_bad.details


def test_iso_10816_threshold_misconfiguration_rejection(probe):
    """Verify probe fails if threshold is misconfigured away from standard 4.5 mm/s."""
    res_misconfigured = probe.verify_iso_10816_threshold(
        zone_alias="Zone C",
        custom_threshold_mms=6.8,  # Wrong threshold
    )
    assert res_misconfigured.passed is False
    assert res_misconfigured.status == "FAIL"


def test_nasa_ims_fixture_rec_042_zone_c_excursion(probe):
    """Verify that NASA IMS Bearing record REC-042 (5.42 mm/s) triggers Zone C breach."""
    adapter = PublicDatasetReplayAdapter()
    rec_042 = adapter.read_event("NASA-IMS-T2-REC-042")
    rec_001 = adapter.read_event("NASA-IMS-T2-REC-001")

    # REC-042 is excursion (> 4.5 mm/s)
    assert rec_042["vibration_mm_s"] == 5.42
    assert rec_042["vibration_mm_s"] > ISO_10816_ZONE_C_THRESHOLD_MMS
    assert rec_042["threshold_exceeded"] is True
    assert rec_042["is_anomaly"] is True

    # REC-001 is healthy baseline (< 4.5 mm/s)
    assert rec_001["vibration_mm_s"] == 1.85
    assert rec_001["vibration_mm_s"] < ISO_10816_ZONE_C_THRESHOLD_MMS
    assert rec_001["threshold_exceeded"] is False


def test_boundary_discrimination_around_4_50_mms(probe):
    """Verify exact boundary behavior (<= 4.50 nominal vs > 4.50 excursion)."""
    boundary_res = probe.verify_boundary_discrimination()
    assert boundary_res.passed is True
    assert boundary_res.status == "PASS"


# ---------------------------------------------------------------------------
# 3. Composite Health Report & Probe Execution Tests
# ---------------------------------------------------------------------------

def test_run_telemetry_health_check_full_report(probe):
    """Verify complete probe execution compiles all sub-checks and returns HEALTHY."""
    report = probe.run_probe()
    assert isinstance(report, TelemetryHealthReport)
    assert report.all_passed is True
    assert report.overall_status == "HEALTHY"
    assert report.is_healthy() is True

    # Check that required probe elements are present
    assert "sampling_rate_20khz" in report.checks
    assert "iso_10816_zone_c_threshold" in report.checks
    assert "boundary_discrimination" in report.checks
    assert "stream_pipeline" in report.checks

    assert report.checks["sampling_rate_20khz"].passed is True
    assert report.checks["iso_10816_zone_c_threshold"].passed is True
    assert report.checks["boundary_discrimination"].passed is True

    # Dict serialization
    data = report.to_dict()
    assert data["overall_status"] == "HEALTHY"
    assert data["all_passed"] is True
    assert data["probe_id"].startswith("PROBE-TEL-")
    assert "20 kHz" in data["summary"]
    assert "4.50 mm/s" in data["summary"]


def test_standalone_run_telemetry_health_check():
    """Verify top-level convenience function runs out-of-the-box."""
    report = run_telemetry_health_check()
    assert report.all_passed is True
    assert report.overall_status == "HEALTHY"


# ---------------------------------------------------------------------------
# 4. Subsystem Integration Tests (Worker & Backend Dependency Checks)
# ---------------------------------------------------------------------------

def test_telemetry_worker_probe_health_integration():
    """Verify TelemetryWorker has automated probe_health capability."""
    worker = TelemetryWorker(equipment_tags=["P-101", "REPLAY-ASSET-01"])
    health_dict = worker.probe_health()

    assert health_dict["overall_status"] == "HEALTHY"
    assert health_dict["all_passed"] is True
    assert "sampling_rate_20khz" in health_dict["checks"]
    assert "iso_10816_zone_c_threshold" in health_dict["checks"]


def test_backend_health_ready_dependency_includes_telemetry():
    """Verify backend dependency readiness check includes telemetry probe."""
    from backend.app.api.health import dependency_checks

    checks = dependency_checks()
    assert "telemetry" in checks
    # Executing the telemetry check should not raise
    checks["telemetry"]()


# ---------------------------------------------------------------------------
# 5. FastAPI HTTP API Endpoint Verification
# ---------------------------------------------------------------------------

def test_api_get_telemetry_health_endpoint(client):
    """Verify GET /api/telemetry/health returns 200 with full health report."""
    response = client.get("/api/telemetry/health")
    assert response.status_code == 200
    data = response.json()
    assert data["overall_status"] == "HEALTHY"
    assert data["all_passed"] is True
    assert data["checks"]["sampling_rate_20khz"]["actual_value"] == 20000.0
    assert data["checks"]["iso_10816_zone_c_threshold"]["actual_value"] == 4.5


def test_api_get_telemetry_probe_endpoint(client):
    """Verify GET /api/telemetry/probe alias endpoint behaves identically."""
    response = client.get("/api/telemetry/probe")
    assert response.status_code == 200
    data = response.json()
    assert data["overall_status"] == "HEALTHY"
    assert data["all_passed"] is True


def test_api_post_telemetry_probe_with_custom_valid_params(client):
    """Verify POST /api/telemetry/probe with explicit valid parameters."""
    payload = {
        "target_sampling_rate_hz": 20000.0,
        "iso_zone_c_threshold_mms": 4.5,
        "zone_alias": "Jones C",
        "tolerance_hz": 0.0,
    }
    response = client.post("/api/telemetry/probe", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["overall_status"] == "HEALTHY"
    assert data["all_passed"] is True


def test_api_post_telemetry_probe_fails_on_deviant_rate(client):
    """Verify POST /api/telemetry/probe reports 503 / DEGRADED when probing invalid rate."""
    payload = {
        "target_sampling_rate_hz": 50000.0,  # Telemetry stream only provides 20 kHz
        "iso_zone_c_threshold_mms": 4.5,
        "zone_alias": "Jones C",
        "tolerance_hz": 0.0,
    }
    response = client.post("/api/telemetry/probe", json=payload)
    # FastApi exception handler wraps 5xx in 200 with service_degraded or returns 503
    assert response.status_code in (200, 503)
    data = response.json()
    # Check that it reported failure or degraded status
    if "error" in data:
        assert data.get("error") in ("service_degraded", "internal_error") or "checks" in data
    else:
        assert data.get("all_passed") is False or data.get("overall_status") == "UNHEALTHY"
