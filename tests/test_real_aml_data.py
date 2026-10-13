"""Test suite for source-verified AML metadata and Elliptic dataset integration."""

import random
import pytest

from src.data_processing.real_aml_data import (
    VERIFIED_BANKS,
    VERIFIED_MERCHANTS,
    VERIFIED_TYPOLOGIES,
    generate_luhn_imei,
    generate_verified_device_profile,
    generate_verified_merchant_profile,
    generate_verified_user_profile,
    get_verified_ring_typology,
)
from src.data_processing.elliptic_dataset import EllipticDataLoader, EllipticConfig


def test_luhn_imei_checksum_validity():
    rng = random.Random(42)
    # Test multiple generations
    for _ in range(20):
        imei = generate_luhn_imei("35689110", rng)
        assert len(imei) == 15
        assert imei.isdigit()
        
        # Verify Luhn formula
        digits = [int(c) for c in imei]
        total = 0
        for i, d in enumerate(reversed(digits)):
            if i % 2 == 1:
                doubled = d * 2
                total += doubled if doubled < 10 else (doubled - 9)
            else:
                total += d
        assert total % 10 == 0


def test_verified_user_profile_structure():
    rng = random.Random(123)
    profile = generate_verified_user_profile(user_id=42, rng=rng)
    assert profile["user_id"] == 42
    assert "name" in profile
    assert profile["bank_name"] in [b["bank_name"] for b in VERIFIED_BANKS]
    assert "****" in profile["account_masked"]
    assert len(profile["swift_bic"]) == 8
    assert "Tier-" in profile["kyc_tier"]


def test_verified_merchant_profile_mcc():
    rng = random.Random(999)
    profile = generate_verified_merchant_profile(merchant_id=0, rng=rng)
    assert profile["merchant_id"] == 0
    assert profile["mcc"] in ["6051", "7995", "5094", "5732", "6012", "5999"]
    assert profile["risk_tier"] in ["Critical", "High", "Elevated", "Medium"]


def test_ring_typology_deterministic_assignment():
    t0 = get_verified_ring_typology(0)
    t1 = get_verified_ring_typology(1)
    assert t0["typology_code"] != t1["typology_code"]
    assert t0["authority"] in [t["authority"] for t in VERIFIED_TYPOLOGIES]


def test_elliptic_mock_loader_schema():
    loader = EllipticDataLoader(EllipticConfig())
    hetero = loader.generate_mock_elliptic_graph(num_nodes=50)
    assert "user" in hetero.node_types
    assert "merchant" in hetero.node_types
    assert ("user", "transacts", "merchant") in hetero.edge_types
    assert hetero["user"].x.shape[0] == 50
    assert hetero["user"].x.shape[1] == 166

