import check50
import check50.c
import random

def expected(n):
    if n % 2 == 0:
        n += 1
    return ["*" * min(i, n + 1 - i) for i in range(1, n + 1)]

def get_lines(arg):
    out = check50.run(f"./triangle2 {arg}").stdout()
    # tolerate trailing spaces on each line
    return [l.rstrip(" ") for l in out.rstrip("\n").split("\n")] \
            if out.strip() else []

def check_triangle(n):
    exp = expected(n)
    actual = get_lines(n)
    for i in range(max(len(exp), len(actual))):
        if i >= len(exp):
            raise check50.Failure(f"With argument {n}: unexpected extra "
                    f"output on line {i+1}: {actual[i]!r}")
        if i >= len(actual):
            raise check50.Failure(f"With argument {n}: missing line {i+1}: "
                    f"expected {exp[i]!r}")
        if actual[i] != exp[i]:
            raise check50.Failure(f"With argument {n}: line {i+1}: expected "
                    f"{exp[i]!r}, got {actual[i]!r}")

@check50.check()
def exists():
    check50.exists("triangle2.c")
    with open("triangle2.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("triangle2.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    """prints the README examples"""
    for n in [3, 5, 15]:
        check_triangle(n)

@check50.check(compiles)
def small_sizes():
    """prints a single star for 1, and nothing or a single star for 0"""
    check_triangle(1)
    # 0 is even so the README rule corrects it to 1, but printing nothing is
    # also accepted
    actual = get_lines(0)
    if actual not in [[], ["*"]]:
        raise check50.Failure(f"With argument 0: expected no output or '*', "
                f"got {actual!r}")

@check50.check(compiles)
def other_odd_sizes():
    """prints triangles of other odd sizes"""
    for n in [7, 9, 51] + [random.randrange(11, 41, 2) for _ in range(3)]:
        check_triangle(n)

@check50.check(compiles)
def even_sizes():
    """corrects even sizes to the next odd number"""
    for n in [2, 4, 14] + [random.randrange(16, 40, 2) for _ in range(3)]:
        check_triangle(n)

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./triangle2 5").exit(0)
    check50.run("./triangle2 4").exit(0)

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    # argc may legitimately be unused, don't flag it
    check50.c.compile("triangle2.c", exe_name="triangle2_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
