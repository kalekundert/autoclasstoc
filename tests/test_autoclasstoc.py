# Integration tests, where the inputs are RST files and the outputs are HTML 
# files.

import pytest, parametrize_from_file as pff, re_assert
import lxml.html
import sys, io

from pathlib import Path
from contextlib import contextmanager, redirect_stderr

@pff.parametrize(
        schema=pff.defaults(expected={}, forbidden={}, stderr=[]),
        indirect=['tmp_files'],
)
def test_autoclasstoc(tmp_files, expected, forbidden, stderr, monkeypatch):
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

    io_out = io.StringIO()
    io_err = io.StringIO()

    with cleanup_imports(), tee() as captured:
        from sphinx.cmd.build import build_main
        build_main([
                '-b', 'html',
                str(tmp_files),
                str(tmp_files / 'build'),
        ])

    # Check the error messages:

    (tmp_files / 'build' / 'stdout').write_text(captured.stdout)
    (tmp_files / 'build' / 'stderr').write_text(captured.stderr)

    for pattern in stderr:
        re_assert.Matches(pattern).assert_matches(captured.stderr)

    if not stderr:
        expected_warnings = [
                # This happens because the `autoclasstoc` directive puts a 
                # horizontal line after itself to separate the TOC from the 
                # full method descriptions.  It would be easy to avoid this 
                # warning by putting some arbitrary text after every 
                # `autoclasstoc` directive, but I felt this would be too much 
                # of a distraction from the tests themselves.
                'Document may not end with a transition.',
        ]
        unexpected_warnings = [
            line for line in captured.stderr.splitlines()
            if not any(warning in line for warning in expected_warnings)
        ]
        assert not unexpected_warnings

    # Check the HTML results:

    html_paths = [*expected.keys(), *forbidden.keys()]

    for html_path in html_paths:
        html_str = (tmp_files / 'build' / html_path).read_text()
        html = lxml.html.fromstring(html_str)

        for xpath, pattern in expected.get(html_path, {}).items():
            hits = html.xpath(xpath)

            if not hits:
                raise AssertionError(f"xpath query didn't match any elements in {html_path!r}: {xpath}")

            for hit in hits:
                if isinstance(hit, lxml.html.HtmlElement):
                    hit = hit.text_content()
                re_assert.Matches(pattern).assert_matches(hit)

        for xpath in forbidden.get(html_path, []):
            if html.xpath(xpath):
                raise AssertionError(f"forbidden xpath query matched {html_path!r}: {xpath}")

@contextmanager
def cleanup_imports():
    """
    Unimport any modules/packages that were imported within the `with` block.

    The reason for doing this is to keep the test cases independent from each 
    other.  Python caches imported modules/packages by default, so without 
    this, imports made by one test case would persist into the next.

    There are really two specific modules/packages that cause problems:

        `mock_project`:
            Most of the test cases include a module with this name that defines 
            the python objects to document in that test.  It's easy to see how 
            caching this module between test cases could lead to problems.  
            This could be avoided by using a different module name for each 
            test case, but that's too much of a burden on the test author.

        `sphinx`:
            I don't exactly understand how, but there is some amount of global 
            state that is stored somewhere in the this package.  I think it has 
            something to do with the way attribute docstrings are parsed, 
            because (i) the tests that involve attributes fail when sphinx 
            isn't un-imported between test cases and (ii) attributes don't 
            really have docstrings, so sphinx has to do some magic to make it 
            seem like they do.  In any case, un-importing this module solves 
            the problem.
    """
    try:
        whitelist = set(sys.modules.keys())
        yield
    finally:
        for key in list(sys.modules):
            if key not in whitelist:
                del sys.modules[key]

class tee:

    class IO:

        def __init__(self, *files):
            self.files = files

        def write(self, str):
            for file in self.files:
                file.write(str)

        def flush(self):
            for file in self.files:
                file.flush()

    def __enter__(self):
        self.stdout_original = sys.stdout
        self.stdout_captured = io.StringIO()

        sys.stdout = self.IO(
            self.stdout_original,
            self.stdout_captured,
        )

        self.stderr_original = sys.stderr
        self.stderr_captured = io.StringIO()

        sys.stderr = self.IO(
            self.stderr_original,
            self.stderr_captured,
        )

        return self

    def __exit__(self, *args):
        sys.stdout = self.stdout_original
        sys.stderr = self.stderr_original

    @property
    def stdout(self):
        return self.stdout_captured.getvalue()

    @property
    def stderr(self):
        return self.stderr_captured.getvalue()

