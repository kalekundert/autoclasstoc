#!/usr/bin/env python3
"""sphinxclasstocr.utils Test Suite"""

import pytest

from sphinxclasstocr import utils
from sphinxclasstocr.errors import ConfigError
from sphinxclasstocr.sections import Section


class SphinxClassTocr1(Section):
    """First test class"""

    key = "dummy-section-1"
    title = "Dummy Section 1:"


class SphinxClassTocr2(Section):
    """Second test classs"""

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
    assert utils.pick_sections(given, exclude) == expected


@pytest.mark.parametrize(
    "given, exclude, err",
    [
        (["unknown-section"], [], "unknown-section"),
        (
            [3],
            ["unknown-section"],
            "Must be type(sphinxclasstocr.Section), type(<class 'int'>) was supplied",
        ),
        ([], ["unknown-section"], "unknown-section"),
    ],
)
def test_pick_sections_err(given, exclude, err):
    with pytest.raises(ConfigError) as err_msg:
        utils.pick_sections(given, exclude)
    assert err in str(err_msg.value)
