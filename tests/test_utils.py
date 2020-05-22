#!/usr/bin/env python3

import pytest
import autoclasstoc

class DummySection1(autoclasstoc.Section):
    key = 'dummy-section-1'
    title = "Dummy Section 1:"

class DummySection2(autoclasstoc.Section):
    key = 'dummy-section-2'
    title = "Dummy Section 2:"

@pytest.mark.parametrize(
        'given, exclude, expected', [(
            [],
            [],
            [],
        ), (
            [DummySection1],
            [],
            [DummySection1],
        ), (
            ['dummy-section-1'],
            [],
            [DummySection1],
        ), (
            [DummySection1, DummySection2],
            [],
            [DummySection1, DummySection2],
        ), (
            [DummySection1, 'dummy-section-2'],
            [],
            [DummySection1, DummySection2],
        ), (
            ['dummy-section-1', DummySection2],
            [],
            [DummySection1, DummySection2],
        ), (
            ['dummy-section-1', 'dummy-section-2'],
            [],
            [DummySection1, DummySection2],
        ), (
            [DummySection1, DummySection2],
            [DummySection1],
            [DummySection2],
        ), (
            [DummySection1, DummySection2],
            ['dummy-section-1'],
            [DummySection2],
        ), (
            [DummySection1, DummySection2],
            [DummySection2],
            [DummySection1],
        ), (
            [DummySection1, DummySection2],
            ['dummy-section-2'],
            [DummySection1],
        ), (
            [DummySection1],
            [DummySection2],
            [DummySection1],
)])
def test_pick_sections(given, exclude, expected):
    assert autoclasstoc.utils.pick_sections(given, exclude) == expected

@pytest.mark.parametrize(
        'given, exclude, err', [
            (['unknown-section'], [], "unknown-section"),
            ([], ['unknown-section'], "unknown-section"),
        ]
)
def test_pick_sections_err(given, exclude, err):
    with pytest.raises(autoclasstoc.ConfigError, match=err):
        autoclasstoc.utils.pick_sections(given, exclude)
