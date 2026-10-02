import check50
import check50.c
import random
import re

def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def check_year(year):
    exp = f"{year} is {'a' if is_leap(year) else 'not a'} leap year"
    out = check50.run(f"./leap {year}").stdout()
    if not re.fullmatch(re.escape(exp) + r"\n?", out):
        raise check50.Failure(f"With argument {year}: expected {exp!r}, got "
                f"{out!r}")

@check50.check()
def exists():
    check50.exists("leap.c")
    with open("leap.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("leap.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    """correct output for the README examples and a few other years"""
    for year in [1994, 0, 2000, 2100, 2300, 1715, 1716]:
        check_year(year)

@check50.check(compiles)
def not_divisible_by_4():
    """years not divisible by 4 are common years"""
    for year in [1, 2023, 2025, 1999]:
        check_year(year)

@check50.check(compiles)
def divisible_by_4_not_100():
    """years divisible by 4 but not by 100 are leap years"""
    for year in [4, 1996, 2024, 2104]:
        check_year(year)

@check50.check(compiles)
def divisible_by_100_not_400():
    """years divisible by 100 but not by 400 are common years"""
    for year in [100, 1800, 1900, 2200]:
        check_year(year)

@check50.check(compiles)
def divisible_by_400():
    """years divisible by 400 are leap years"""
    for year in [400, 1600, 2400, 10000]:
        check_year(year)

@check50.check(compiles)
def random_years():
    """correct output for random years"""
    for _ in range(10):
        check_year(random.randint(1, 9999))

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./leap 2000").exit(0)
    check50.run("./leap 2100").exit(0)

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    # argc may legitimately be unused, don't flag it
    check50.c.compile("leap.c", exe_name="leap_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
