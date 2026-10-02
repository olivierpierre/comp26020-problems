import check50
import check50.c
import re

EXPECTED = [
    "   ######",
    " ##      ##",
    "#",
    "#",
    "#",
    "#",
    "#",
    " ##      ##",
    "   ######",
]

@check50.check()
def exists():
    check50.exists("printf.c")
    with open("printf.c") as f:
        return f.read()

@check50.check(exists)
def compiles(sources_buf):
    check50.c.compile("printf.c", cc="gcc")

@check50.check(compiles)
def large_c_printed():
    """output is exactly the expected 'C' shape"""
    out = check50.run("./printf").stdout()
    # tolerate trailing spaces on each line and trailing blank lines only
    actual = [l.rstrip(" ") for l in out.rstrip("\n").split("\n")]
    for i in range(max(len(EXPECTED), len(actual))):
        if i >= len(EXPECTED):
            raise check50.Failure(f"Unexpected extra output on line {i+1}: {actual[i]!r}")
        if i >= len(actual):
            raise check50.Failure(f"Missing line {i+1}: expected {EXPECTED[i]!r}")
        if actual[i] != EXPECTED[i]:
            raise check50.Failure(f"Line {i+1}: expected {EXPECTED[i]!r}, got {actual[i]!r}")

@check50.check(compiles)
def ends_with_newline():
    """output ends with a newline"""
    out = check50.run("./printf").stdout()
    if not out.endswith("\n"):
        raise check50.Failure("The last line of output should end with \\n")

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./printf").exit(0)

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    check50.c.compile("printf.c", exe_name="printf_warn", cc="gcc",
                      Wall=True, Wextra=True, Werror=True)
