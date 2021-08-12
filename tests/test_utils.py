#!/usr/bin/env python3

import pytest

import sphinxclasstocr


class SphinxClassTocr1(sphinxclasstocr.Section):
    key = "dummy-section-1"
    title = "Dummy Section 1:"


class SphinxClassTocr2(sphinxclasstocr.Section):
    key = "dummy-section-2"
    title = "Dummy Section 2:"


@pytest.mark.parametrize(
    "given, exclude, expected",
    [
        (
            [],
            [],
            [],
        ),
        (
            [SphinxClassTocr1],
            [],
            [SphinxClassTocr1],
        ),
        (
            ["dummy-section-1"],
            [],
            [SphinxClassTocr1],
        ),
        (
            [SphinxClassTocr1, SphinxClassTocr2],
            [],
            [SphinxClassTocr1, SphinxClassTocr2],
        ),
        (
            [SphinxClassTocr1, "dummy-section-2"],
            [],
            [SphinxClassTocr1, SphinxClassTocr2],
        ),
        (
            ["dummy-section-1", SphinxClassTocr2],
            [],
            [SphinxClassTocr1, SphinxClassTocr2],
        ),
        (
            ["dummy-section-1", "dummy-section-2"],
            [],
            [SphinxClassTocr1, SphinxClassTocr2],
        ),
        (
            [SphinxClassTocr1, SphinxClassTocr2],
            [SphinxClassTocr1],
            [SphinxClassTocr2],
        ),
        (
            [SphinxClassTocr1, SphinxClassTocr2],
            ["dummy-section-1"],
            [SphinxClassTocr2],
        ),
        (
            [SphinxClassTocr1, SphinxClassTocr2],
            [SphinxClassTocr2],
            [SphinxClassTocr1],
        ),
        (
            [SphinxClassTocr1, SphinxClassTocr2],
            ["dummy-section-2"],
            [SphinxClassTocr1],
        ),
        (
            [SphinxClassTocr1],
            [SphinxClassTocr2],
            [SphinxClassTocr1],
        ),
    ],
)
def test_pick_sections(given, exclude, expected):
    assert sphinxclasstocr.utils.pick_sections(given, exclude) == expected


@pytest.mark.parametrize(
    "given, exclude, err",
    [
        (["unknown-section"], [], "unknown-section"),
        ([], ["unknown-section"], "unknown-section"),
    ],
)
def test_pick_sections_err(given, exclude, err):
    with pytest.raises(sphinxclasstocr.ConfigError, match=err):
        sphinxclasstocr.utils.pick_sections(given, exclude)
