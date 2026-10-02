import check50
import check50.c
import re

@check50.check()
def exists():
    check50.exists("compilation-errors.c")
    with open("compilation-errors.c") as f:
        return f.read()

@check50.check(exists)
def compiles(sources_buf):
    check50.c.compile("compilation-errors.c", cc="gcc")

@check50.check(exists)
def includes_stdio(sources_buf):
    """source code includes stdio.h"""
    if not re.search(r"^\s*#\s*include\s*<stdio\.h>", sources_buf, re.MULTILINE):
        raise check50.Failure("Could not find #include <stdio.h>")

@check50.check(exists)
def main_returns_int(sources_buf):
    """main is declared as returning int"""
    if not re.search(r"\bint\s+main\s*\(", sources_buf):
        raise check50.Failure("main should be declared as returning int")

@check50.check(compiles)
def correct_output():
    """output is exactly 'This should work!'"""
    out = check50.run("./compilation-errors").stdout()
    if out != "This should work!\n":
        raise check50.Failure(f"Expected 'This should work!\\n', got {out!r}")

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./compilation-errors").exit(0)

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    check50.c.compile("compilation-errors.c", exe_name="compilation-errors_warn",
                      cc="gcc", Wall=True, Wextra=True, Werror=True)
