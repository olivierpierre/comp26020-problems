import check50
import check50.c
import itertools
import random
import re

def expected(args):
    """the product of args formatted like printf's %f, or None if the result
    depends on the order of the multiplications"""
    results = {"%f" % (float(a) * float(b) * float(c))
               for a, b, c in itertools.permutations(args)}
    return results.pop() if len(results) == 1 else None

def check_product(*args):
    exp = expected(args)
    out = check50.run("./cmdline " + " ".join(args)).stdout()
    if not re.fullmatch(re.escape(exp) + r"\n?", out):
        raise check50.Failure(f"With arguments {' '.join(args)}: expected "
                f"{exp!r}, got {out!r}")

@check50.check()
def exists():
    check50.exists("cmdline.c")
    with open("cmdline.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("cmdline.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    """outputs the product for the README examples"""
    check_product("1.0", "2.0", "3.0")
    check_product("1.45", "2.78", "3.25")
    check_product("15.5", "56.89", "32.225")
    check_product("5.45", "6.9", "325.225")

@check50.check(compiles)
def negative_and_zero():
    """handles negative numbers and zero"""
    check_product("-1.5", "2.0", "3.0")
    check_product("-1.5", "-2.0", "-3.25")
    check_product("0.0", "123.456", "-7.5")

@check50.check(compiles)
def other_notations():
    """handles numbers without a decimal point or in scientific notation"""
    check_product("2", "3", "4")
    check_product("1e3", "2.5", "4E-2")

@check50.check(compiles)
def random_inputs():
    """outputs the product for random inputs"""
    tested = 0
    while tested < 5:
        args = ["%.3f" % random.uniform(-1000, 1000) for _ in range(3)]
        if expected(args) is None:
            continue
        check_product(*args)
        tested += 1

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./cmdline 1.0 2.0 3.0").exit(0)

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    # argc may legitimately be unused, don't flag it
    check50.c.compile("cmdline.c", exe_name="cmdline_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
