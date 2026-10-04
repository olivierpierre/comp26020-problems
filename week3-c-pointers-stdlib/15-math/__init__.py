import check50
import check50.c
import math
import random
import re

PROMPT1 = "Input a number:"
PROMPT2 = "Input 0 for ceil, 1 for floor"

def strip_comments_and_strings(buf):
    return re.sub(r"//[^\n]*|/\*.*?\*/|\"(?:\\.|[^\"\\\n])*\"", " ", buf,
            flags=re.DOTALL)

def expected(number, choice):
    v = float(number)
    return "%f" % (math.ceil(v) if choice == 0 else math.floor(v))

def check_math(number, choice):
    """run the program interactively: each input is sent only once the
    corresponding prompt has been displayed, then the result must be the only
    thing displayed after the second prompt"""
    op = "ceil" if choice == 0 else "floor"
    exp = expected(number, choice)
    run = check50.run("./math")
    for prompt, value in [(PROMPT1, number), (PROMPT2, str(choice))]:
        try:
            run.stdout(re.escape(prompt), str_output=prompt)
        except check50.Failure:
            raise check50.Failure(f"With input {number} and {choice} ({op}): "
                    f"expected the prompt {prompt!r} to be displayed before "
                    f"the input {value!r} is entered, it was not")
        run.stdin(value, prompt=False)
    out = run.stdout()  # everything displayed after the second prompt
    if not re.fullmatch(r"\s*" + re.escape(exp) + r"\s*", out):
        raise check50.Failure(f"With input {number} and {choice} ({op}): "
                f"expected {exp!r} after the second prompt, got {out!r}")

@check50.check()
def exists():
    check50.exists("math.c")
    with open("math.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("math.c", cc="gcc")

@check50.check(exists)
def uses_scanf(sources_buf):
    """reads the number with scanf"""
    if not re.search(r"\bscanf\s*\(", strip_comments_and_strings(sources_buf)):
        raise check50.Failure("Could not find a call to scanf")

@check50.check(exists)
def uses_ceil_floor(sources_buf):
    """uses the ceil and floor functions from math.h"""
    buf = strip_comments_and_strings(sources_buf)
    for f in ["ceil", "floor"]:
        if not re.search(r"\b" + f + r"[fl]?\s*\(", buf):
            raise check50.Failure(f"Could not find a call to {f}")

@check50.check(compiles)
def output_correct():
    """prompts for the inputs and displays the result for the README examples"""
    check_math("12.4", 0)
    check_math("45.87", 1)
    check_math("442.8", 1)

@check50.check(compiles)
def both_operations():
    """ceils and floors the same numbers"""
    for number in ["12.4", "45.87", "0.5", "99.99"]:
        check_math(number, 0)
        check_math(number, 1)

@check50.check(compiles)
def integers():
    """leaves numbers without a fractional part unchanged"""
    for number in ["7", "7.0", "0", "-3"]:
        check_math(number, 0)
        check_math(number, 1)

@check50.check(compiles)
def negative_numbers():
    """handles negative numbers"""
    check_math("-2.5", 0)
    check_math("-2.5", 1)
    check_math("-123.01", 0)
    check_math("-123.01", 1)

@check50.check(compiles)
def large_numbers():
    """handles numbers too large for an int"""
    check_math("3000000000.5", 0)
    check_math("-3000000000.5", 1)
    check_math("1e15", 1)

@check50.check(compiles)
def random_inputs():
    """ceils and floors random numbers"""
    tested = 0
    while tested < 6:
        number = "%.3f" % random.uniform(-10000, 10000)
        # ceil of a number in ]-1, 0[ is -0.0, displayed "-0.000000" by C and
        # "0.000000" by Python: avoid that range
        if -1 < float(number) < 0:
            continue
        check_math(number, tested % 2)
        tested += 1

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./math").stdin("12.4").stdin("0").exit(0)

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    check50.c.compile("math.c", exe_name="math_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
