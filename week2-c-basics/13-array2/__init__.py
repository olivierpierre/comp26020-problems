import check50
import check50.c
import random
import re

def check_parity(*args):
    exp = [f"{v} is {'even' if v % 2 == 0 else 'odd'}" for v in args]
    args_str = " ".join(str(v) for v in args)
    out = check50.run(f"./array2 {args_str}").stdout()
    # tolerate trailing spaces on each line, as in the README examples
    actual = [l.rstrip(" ") for l in out.rstrip("\n").split("\n")] \
            if out.strip() else []
    for i in range(max(len(exp), len(actual))):
        if i >= len(exp):
            raise check50.Failure(f"With arguments {args_str}: unexpected "
                    f"extra output on line {i+1}: {actual[i]!r}")
        if i >= len(actual):
            raise check50.Failure(f"With arguments {args_str}: missing line "
                    f"{i+1}: expected {exp[i]!r}")
        if actual[i] != exp[i]:
            raise check50.Failure(f"With arguments {args_str}: line {i+1}: "
                    f"expected {exp[i]!r}, got {actual[i]!r}")

@check50.check()
def exists():
    check50.exists("array2.c")
    with open("array2.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("array2.c", cc="gcc")

@check50.check(exists)
def has_atoi(sources_buf):
    """converts the parameters with atoi, strtol or sscanf"""
    if not re.search(r"\b(atoi|atol|strtol|sscanf)\s*\(", sources_buf):
        raise check50.Failure("Found no call to the string to int conversion "
                "function")

@check50.check(exists)
def has_array(sources_buf):
    """declares an array of int named array"""
    if not re.search(r"\bint\s+array\s*\[", sources_buf):
        raise check50.Failure("Could not find the declaration of an array of "
                "int named array")

@check50.check(exists)
def has_for_loop(sources_buf):
    for_re = r"for\s*\(.*;.*;.*\)"
    while_re = r"while\s*\(.*\)"
    if not re.search(for_re, sources_buf) and not re.search(while_re, sources_buf):
        raise check50.Failure("Did not found a for loop in sources")

@check50.check(compiles)
def output_correct():
    """correct output for the README examples and a 10 integers list"""
    check_parity(1, 2, 3, 4, 5, 6)
    check_parity(5, 5, 120)
    check_parity(11654, 16544, 78789, 516, 7879, 4658, 546, 54687, 787, 88)

@check50.check(compiles)
def no_arguments():
    """prints nothing without arguments"""
    out = check50.run("./array2").stdout()
    if out.strip():
        raise check50.Failure(f"Expected no output, got {out!r}")

@check50.check(compiles)
def negative_numbers():
    """handles negative numbers and zero"""
    check_parity(0)
    check_parity(-3, -2, -1, 0, 1)
    check_parity(-77, -1000)

@check50.check(compiles)
def random_inputs():
    """correct output for random lists of 1 to 10 integers"""
    for _ in range(10):
        n = random.randint(1, 10)
        check_parity(*[random.randint(-1000, 1000) for _ in range(n)])

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./array2 1 2 3").exit(0)
    check50.run("./array2").exit(0)

@check50.check(exists)
def no_memory_errors(sources_buf):
    """no out-of-bounds memory accesses (AddressSanitizer)"""
    check50.c.compile("array2.c", exe_name="array2_asan", cc="gcc",
                      fsanitize="address")
    for args in ["10 9 8 7 6 5 4 3 2 1", "1", ""]:
        run = check50.run(("./array2_asan " + args).strip())
        out = run.stdout()  # waits for the program to exit and sets exitcode
        if run.exitcode != 0:
            error = re.search(r"AddressSanitizer: [\w-]+", out)
            raise check50.Failure(f"With arguments '{args}': memory error "
                    "detected: " +
                    (error.group(0) if error else "unknown error") +
                    ", compile with 'gcc -fsanitize=address array2.c -o array2'"
                    " and run it to see the full report")

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    check50.c.compile("array2.c", exe_name="array2_warn", cc="gcc",
                      Wall=True, Wextra=True, Werror=True)
