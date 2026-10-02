import check50
import check50.c
import re

# a declaration statement of type unsigned int declaring variable, possibly
# among others, e.g. "unsigned variable;", "const unsigned int a, variable = 10;"
# but not "unsigned long variable;"
DECL_RE = (r"(?:^|[;{}])\s*(?:(?:const|static|volatile)\s+)*"
           r"unsigned(?:\s+int)?\s+(?!(?:char|short|int|long)\b)"
           r"[^;{}()]*\bvariable\b")

# a printf call with a format string followed by arguments mentioning variable
PRINTF_ARG_RE = r'\bprintf\s*\(\s*"(?:[^"\\]|\\.)*"\s*,[^;]*\bvariable\b'

@check50.check()
def exists():
    check50.exists("types.c")
    with open("types.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("types.c", cc="gcc")

@check50.check(exists)
def check_type(sources_buf):
    """variable is declared as unsigned int"""
    if not re.search(DECL_RE, sources_buf, re.MULTILINE):
        raise check50.Failure("Could not find a declaration with the correct "
                "type")

@check50.check(exists)
def keeps_printf(sources_buf):
    """printf still uses %u to print variable"""
    if "%u" not in sources_buf:
        raise check50.Failure("The format specifier %u should be kept, choose "
                "the type of variable to match it")
    if not re.search(PRINTF_ARG_RE, sources_buf):
        raise check50.Failure("Could not find a call to printf with variable "
                "as an argument")

@check50.check(compiles)
def output_correct():
    """output is exactly 'variable is 10'"""
    out = check50.run("./types").stdout()
    if out != "variable is 10\n":
        raise check50.Failure(f"Expected 'variable is 10\\n', got {out!r}")

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./types").exit(0)

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Wformat-signedness -Werror)"""
    check50.c.compile("types.c", exe_name="types_warn", cc="gcc",
                      Wall=True, Wextra=True, Wformat_signedness=True,
                      Werror=True)
