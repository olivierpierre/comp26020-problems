import check50
import check50.c
import math
import re

def check_factorial(n):
    exp = f"{n}! = {math.factorial(n)}"
    out = check50.run(f"./factorial {n}").stdout()
    if not re.fullmatch(re.escape(exp) + r"\n?", out):
        raise check50.Failure(f"With argument {n}: expected {exp!r}, got "
                f"{out!r}")

@check50.check()
def exists():
    check50.exists("factorial.c")
    with open("factorial.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("factorial.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    """correct output for 0 to 10"""
    for n in range(11):
        check_factorial(n)

@check50.check(compiles)
def large_values():
    """correct output for 11 to 20 (13! and above exceed 32 bits)"""
    for n in range(11, 21):
        check_factorial(n)

@check50.check(exists)
def not_hardcoded(sources_buf):
    """factorials are computed, not hardcoded"""
    for n in range(7, 21):
        if re.search(rf"(?<!\d){math.factorial(n)}(?!\d)", sources_buf):
            raise check50.Failure(f"Found the hardcoded value of {n}! in the "
                    "source, it should be computed")

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./factorial 10").exit(0)

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    # argc may legitimately be unused, don't flag it
    check50.c.compile("factorial.c", exe_name="factorial_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
