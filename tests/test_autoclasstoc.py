"""\
Integration tests, where the inputs are RST files and the outputs are HTML 
files.

The basic process carried out by each of these tests is to (i) fill in a 
temporary directory with all the files needed by sphinx to build a project, 
(ii) invoke sphinx on those files, and (iii) check that the resulting HTML 
contains any expected elements.  This script implements all the logic that is 
shared that is shared between every test case.  The parameters that vary 
between each test (namely the specific files to populate the temporary 
directory and the expected HTML elements to check for) are specified in 
`test_autoclasstoc.nt`.

As mentioned above, each test project is built in its own temporary directory.  
The path to this directory is listed in the pytest output, and its contents are 
very useful for debugging.  Specifically, this directory contains:

- All the input files, so you can re-run sphinx for individual test cases.  
  Doing this in a way that exactly reproduces the test environment requires 
  some care.  Specifically, you need to (i) specify `$PYTHONPATH` to mimic 
  the way the way that `sys.path` is set in the test, (ii) use the tox 
  virtual environment that has the right dependencies installed, and (iii) 
  provide the right source/build directory arguments.  Here is the exact 
  command to use, assuming that the current working directory is the 
  temporary test directory and `$TOC` is the path to the autoclasstoc 
  repository:

  $ rm -rf build
  $ PYTHONPATH=. $TOC/.tox/py*-sphinx*/bin/sphinx-build -b html . build

  Rather than deleting the existing build directory, you may prefer to have 
  sphinx build into a new directory, so you can compare results.

  Note that changes to the source will not automatically be visible to the 
  tox virtual environments.  One way to get around this is to manually 
  install autoclasstoc in "editable" mode in the tox virtual environment:

  $ $TOC/.tox/py*-sphinx*/bin/pip install -e $TOC

- All the output HTML files, so you can look at them in a web browser and see 
  what's exactly wrong, e.g. is an element totally missing, is it just in the 
  wrong place, etc.

- Files called `stdout` and `stderr`, which contain any output that was 
  captured when sphinx was running.  This information is also included in the 
  pytest output, but it can be useful to review later.
"""

import parametrize_from_file as pff
import re_assert
import lxml.html
import subprocess
import sys

from pathlib import Path

ROOT = Path(__file__).parents[1]

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
]
""")

    # Run sphinx:

    sphinx_cmd = [
            sys.executable,
            '-m', 'sphinx.cmd.build',
            '-b', 'html',
            str(tmp_files),
            str(tmp_files / 'build'),
    ]
    p = subprocess.run(
            sphinx_cmd,
            cwd=tmp_files,
            env={
                'PYTHONPATH': str(tmp_files),
                'COVERAGE_PROCESS_START': str(ROOT / 'pyproject.toml'),
                'COVERAGE_OUTPUT_DIR': str(ROOT),
            },
            capture_output=True,
            text=True,
    )

    # Check the error messages:

    print(p.stdout, file=sys.stdout)
    print(p.stderr, file=sys.stderr)

    (tmp_files / 'build' / 'stdout').write_text(p.stdout)
    (tmp_files / 'build' / 'stderr').write_text(p.stderr)

    for pattern in stderr:
        re_assert.Matches(pattern).assert_matches(p.stderr)

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
            line for line in p.stderr.splitlines()
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

