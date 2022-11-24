# Integration tests, where the inputs are RST files and the outputs are HTML 
# files.

import pytest, parametrize_from_file as pff, re_assert
import lxml.html
import sys

from sphinx.cmd.build import build_main
from pathlib import Path

@pff.parametrize(
        schema=pff.defaults(expected={}, forbidden={}, stderr=[]),
        indirect=['tmp_files'],
)
def test_autoclasstoc(tmp_files, expected, forbidden, stderr, monkeypatch, capsys):

    # Fill in missing files:

    conf_py = tmp_files / 'conf.py'
    if not conf_py.exists():
        conf_py.write_text("""\
extensions = [
        'autoclasstoc',
        'sphinx.ext.autosummary',
]
""")

    # Run sphinx:

    monkeypatch.syspath_prepend(tmp_files)

    build_main([
            '-b', 'html',
            str(tmp_files),
            str(tmp_files / 'build'),
    ])

    # Un-import any test files imported in the process of running sphinx.  
    # Without this step, these imports would be cached, and could be wrongly 
    # used in future test cases.

    for name, mod in list(sys.modules.items()):
        try:
            mod_path = mod.__file__
        except AttributeError:
            continue

        if not mod_path:
            continue

        try:
            Path(mod_path).relative_to(tmp_files)
        except ValueError:
            continue

        del sys.modules[name]

    # Check the error messages:
    
    cap = capsys.readouterr()

    for pattern in stderr:
        re_assert.Matches(pattern).assert_matches(cap.err)

    # Check the HTML results:

    html_paths = [*expected.keys(), *forbidden.keys()]

    for html_path in html_paths:
        html_str = (tmp_files / 'build' / html_path).read_text()
        html = lxml.html.fromstring(html_str)

        for xpath, pattern in expected.get(html_path, {}).items():
            hits = html.xpath(xpath)

            if not hits:
                raise AssertionError(f"xpath query didn't match any elements: {xpath}")

            for hit in hits:
                if isinstance(hit, lxml.html.HtmlElement):
                    hit = hit.text_content()
                re_assert.Matches(pattern).assert_matches(hit)

        for xpath in forbidden.get(html_path, []):
            if html.xpath(xpath):
                raise AssertionError(f"forbidden xpath query matched document: {xpath}")



