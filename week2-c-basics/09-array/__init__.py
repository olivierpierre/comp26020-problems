import check50
import check50.c
import random
import re

def check_sort(*args):
    exp = " ".join(str(v) for v in sorted(args))
    cmd = " ".join(["./array"] + [str(v) for v in args])
    out = check50.run(cmd).stdout()
    # tolerate a trailing space and/or newline, as printed by a "%d " loop
    if not re.fullmatch(re.escape(exp) + r" ?\n?", out):
        raise check50.Failure(f"With arguments {' '.join(str(v) for v in args)}"
                f": expected {exp!r}, got {out!r}")

@check50.check()
def exists():
    check50.exists("array.c")
    with open("array.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("array.c", cc="gcc")

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
        raise check50.Failure("Did not found a for/while loop in sources")

@check50.check(compiles)
def output_correct():
    """sorts the README examples and a 10 integers list"""
    check_sort(6, 5, 4, 3, 2, 1)
    check_sort(5, 5, 120)
    check_sort(4654, 87987, 16515, 4987, 465416, 4984, 4654, 498498, 16516,
            897484)

@check50.check(compiles)
def edge_cases():
    """handles a single integer, sorted input and identical values"""
    check_sort(42)
    check_sort(1, 2)
    check_sort(2, 1)
    check_sort(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    check_sort(7, 7, 7, 7)

@check50.check(compiles)
def negative_numbers():
    """handles negative numbers and zero"""
    check_sort(3, -1, 0, -20, 15)
    check_sort(-5, -10, -1)

@check50.check(compiles)
def random_inputs():
    """sorts random lists of 1 to 10 integers"""
    for _ in range(10):
        n = random.randint(1, 10)
        check_sort(*[random.randint(-1000, 1000) for _ in range(n)])

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./array 5 4 6 2 1 3").exit(0)

@check50.check(exists)
def no_memory_errors(sources_buf):
    """no out-of-bounds memory accesses (AddressSanitizer)"""
    check50.c.compile("array.c", exe_name="array_asan", cc="gcc",
                      fsanitize="address")
    for args in ["10 9 8 7 6 5 4 3 2 1", "1", "3 1 2"]:
        run = check50.run("./array_asan " + args)
        out = run.stdout()  # waits for the program to exit and sets exitcode
        if run.exitcode != 0:
            error = re.search(r"AddressSanitizer: [\w-]+", out)
            raise check50.Failure(f"With arguments {args}: memory error "
                    "detected: " +
                    (error.group(0) if error else "unknown error") +
                    ", compile with 'gcc -fsanitize=address array.c -o array' "
                    "and run it to see the full report")

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    check50.c.compile("array.c", exe_name="array_warn", cc="gcc",
                      Wall=True, Wextra=True, Werror=True)
