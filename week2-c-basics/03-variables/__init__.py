import check50
import check50.c
import re

# a declaration statement of type <type> declaring <var>, possibly among others,
# e.g. "int int_var;", "const int a = 1, int_var = 2;" but not "long int int_var;"
DECL_RE = (r"(?:^|[;{{}}])\s*(?:(?:const|static|volatile)\s+)*{}\s+"
           r"[^;{{}}()]*\b{}\b")

# a printf call with a format string followed by arguments mentioning <var>
PRINTF_ARG_RE = r'\bprintf\s*\(\s*"(?:[^"\\]|\\.)*"\s*,[^;]*\b{}\b'

@check50.check()
def exists():
    check50.exists("variables.c")
    with open("variables.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("variables.c", cc="gcc")

@check50.check(exists)
def has_variables(sources_buf):
    """int_var is declared as int and double_var as double"""
    if not re.search(DECL_RE.format("int", "int_var"), sources_buf,
            re.MULTILINE):
        raise check50.Failure("Could not find a declaration of int_var with "
                "type int")
    if not re.search(DECL_RE.format("double", "double_var"), sources_buf,
            re.MULTILINE):
        raise check50.Failure("Could not find a declaration of double_var "
                "with type double")

@check50.check(exists)
def has_format_specifier(sources_buf):
    buf = sources_buf
    if "%d" not in buf and "%i" not in buf:
        raise check50.Failure("Could not find an integer format specifier "
                "(%d or %i)")
    if "%f" not in buf and "%F" not in buf and "%lf" not in buf:
        raise check50.Failure("Could not find a floating point format "
                "specifier (%f, %F, %lf)")

@check50.check(exists)
def prints_variables(sources_buf):
    """the variables themselves are passed to printf"""
    for var in ["int_var", "double_var"]:
        if not re.search(PRINTF_ARG_RE.format(var), sources_buf):
            raise check50.Failure(f"Could not find a call to printf with "
                    f"{var} as an argument")

@check50.check(compiles)
def output_correct():
    """output has the expected format"""
    out = check50.run("./variables").stdout()
    if not re.fullmatch(r"int_var: -?[0-9]+\ndouble_var: -?[0-9]+\.[0-9]+\n",
            out):
        raise check50.Failure("Expected output of the form 'int_var: 42\\n"
                f"double_var: 24.000000\\n', got {out!r}")

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./variables").exit(0)

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    check50.c.compile("variables.c", exe_name="variables_warn", cc="gcc",
                      Wall=True, Wextra=True, Werror=True)
