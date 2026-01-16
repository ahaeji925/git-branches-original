"""
Tests for gender pay gap analysis
"""
import pytest

from pay_gap import get_top_pay_disparities


def test_top_pay_disparities_1():
    result = get_top_pay_disparities(1)
    assert len(result) == 1
    assert result[0][0] == "Tajikistan"
    # use pytest.approx for comparing two floats safely accounting for
    # precision errors
    assert result[0][1] == pytest.approx(60.5782229)


def test_top_pay_disparities_top10():
    result = get_top_pay_disparities(10)
    assert len(result) == 10
    assert result[0][0] == "Tajikistan"
    assert result[1][0] == "Azerbaijan"
    assert result[2][0] == "Cameroon"
    assert result[3][0] == "Sudan"
    assert result[4][0] == "Mali"
    assert result[5][0] == "Switzerland"
    assert result[6][0] == "Germany"
    assert result[7][0] == "Pakistan"
    assert result[8][0] == "Georgia"
    assert result[9][0] == "Republic of Korea"
