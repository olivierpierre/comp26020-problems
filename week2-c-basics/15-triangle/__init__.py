import check50
import check50.c
import random

def check_triangle(n):
    exp = ["*" * i for i in range(1, n + 1)]
    out = check50.run(f"./triangle {n}").stdout()
    # tolerate trailing spaces on each line
    actual = [l.rstrip(" ") for l in out.rstrip("\n").split("\n")] \
            if out.strip() else []
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
    check50.exists("triangle.c")
    with open("triangle.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("triangle.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    """prints the README examples"""
    for n in [2, 5, 15]:
        check_triangle(n)

@check50.check(compiles)
def small_sizes():
    """prints nothing for 0 and a single star for 1"""
    check_triangle(0)
    check_triangle(1)

@check50.check(compiles)
def other_sizes():
    """prints triangles of other sizes"""
    for n in [3, 4, 50] + [random.randint(6, 30) for _ in range(3)]:
        check_triangle(n)

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./triangle 5").exit(0)
    check50.run("./triangle 0").exit(0)

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    # argc may legitimately be unused, don't flag it
    check50.c.compile("triangle.c", exe_name="triangle_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
