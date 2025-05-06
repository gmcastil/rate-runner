import pytest
from unittest.mock import Mock, patch

from rate_runner.runner import HeavyIonRunner

def test_build_payload_minimal():

    session = Mock()
    runner = HeavyIonRunner(session=session)

    assert isinstance(runner, HeavyIonRunner)

    runner.add_part({
        "label": "testing",
        "rppz": 1,
        "bitsPerDevice": 1,
        "xsInputMethod": "Weibull",
        "onset": "1",
        "width": "10",
        "exponent": "1",
        "limitingXS": "1e-5"
        })

    payload = runner._build_payload(runner._parts)

    assert isinstance(payload, list)
    assert all(isinstance(p, tuple) and len(p) == 2 for p in payload)

    payload_keys = [key for key, value in payload]

    hup_keys = ["label:list",
                "comment1:list",
                "comment2:list",
                "rppx:list",
                "rppy:list",
                "rppz:list",
                "funnel:list",
                "bitsPerDevice:list",
                "onset:list",
                "width:list",
                "exponent:list",
                "limitingXS:list",
                "qcrit:list",
                "xsPerBit:list"
                ]

    for key in hup_keys:
        assert key in payload_keys

