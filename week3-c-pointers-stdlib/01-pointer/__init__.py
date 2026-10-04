import check50
import check50.c
import random
import re

# one "int *" parameter, possibly const-qualified and/or unnamed
PARAM_RE = (r"\s*(?:const\s+)?int\s*(?:\bconst\b\s*)?\*\s*"
            r"(?:\b(?:const|restrict)\b\s*)?(?:[A-Za-z_]\w*)?\s*")
# definition (or prototype) of add with two int pointer parameters
ADD_DEF_RE = r"\badd\s*\(" + PARAM_RE + "," + PARAM_RE + r"\)"
# definition of add, up to and including the opening brace of its body
ADD_BODY_RE = r"\bint\s+add\s*\([^()]*\)\s*\{"

SENTINEL = 123456789

# leaks are not checked, ASan errors are reported with a distinctive exit code
ASAN_EXITCODE = 99
ASAN_OPTIONS = f"detect_leaks=0:exitcode={ASAN_EXITCODE}"

# test program calling the student's add function directly with two int
# pointers, the student's main is renamed so that it does not clash with ours
HARNESS = r"""
#include <stdio.h>
#include <stdlib.h>
#pragma GCC diagnostic error "-Wint-conversion"
#pragma GCC diagnostic error "-Wincompatible-pointer-types"
#define main student_main
#include "pointer.c"
#undef main

int main(int argc, char **argv) {
    int a, b, r;
    if (argc != 3)
        return 1;
    a = atoi(argv[1]);
    b = atoi(argv[2]);
    r = add(&a, &b);
    printf("%d\n", r);
    return 0;
}
"""

def strip_comments(buf):
    return re.sub(r"//[^\n]*|/\*.*?\*/", " ", buf, flags=re.DOTALL)

def check_add(exe, a, b, exp=None):
    """run ./exe a b and check the output is 'a + b = <exp>'"""
    if exp is None:
        exp = a + b
    if exe == "harness":
        exp_line = f"{exp}"
    else:
        exp_line = f"{a} + {b} = {exp}"
    out = check50.run(f"./{exe} {a} {b}").stdout()
    if not re.fullmatch(re.escape(exp_line) + r"\n?", out):
        raise check50.Failure(f"With arguments {a} {b}: expected "
                f"{exp_line!r}, got {out!r}")

@check50.check()
def exists():
    check50.exists("pointer.c")
    with open("pointer.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("pointer.c", cc="gcc")

@check50.check(exists)
def function_call(sources_buf):
    """add is defined with two int pointer parameters"""
    if not re.search(ADD_DEF_RE, strip_comments(sources_buf)):
        raise check50.Failure("The add function does not seem to be defined "
                "with two int pointer parameters")

@check50.check(compiles)
def output_correct():
    """outputs the sum for the README examples and other values"""
    check_add("pointer", 10, 20)
    check_add("pointer", 154, -12)
    check_add("pointer", 114324, 412443)
    check_add("pointer", -46546, 6544)

@check50.check(compiles)
def negative_and_zero():
    """handles zero and negative numbers"""
    check_add("pointer", 0, 0)
    check_add("pointer", -5, -7)
    check_add("pointer", 0, -42)
    check_add("pointer", 25, -25)

@check50.check(compiles)
def random_inputs():
    """outputs the sum for random inputs"""
    for _ in range(5):
        check_add("pointer", random.randint(-1000000, 1000000),
                random.randint(-1000000, 1000000))

@check50.check(function_call)
def add_takes_pointers():
    """add(int *, int *) can be called with two int pointers and returns the sum"""
    with open("harness.c", "w") as f:
        f.write(HARNESS)
    try:
        check50.c.compile("harness.c", cc="gcc")
    except check50.Failure:
        raise check50.Failure("Could not call add with two int pointer "
                "parameters (add(&a, &b)) and get an int back")
    check_add("harness", 10, 20)
    check_add("harness", 154, -12)
    check_add("harness", -46546, 6544)

@check50.check(compiles)
def main_calls_add():
    """main prints the value returned by add"""
    with open("pointer.c") as f:
        buf = strip_comments(f.read())
    if not re.search(ADD_BODY_RE, buf):
        raise check50.Failure("Could not find the definition of the add "
                "function returning an int")
    # make add return a sentinel value: main's output must change accordingly
    with open("pointer_mut.c", "w") as f:
        f.write(re.sub(ADD_BODY_RE, lambda m: m.group(0) +
                f" return {SENTINEL};", buf, count=1))
    try:
        check50.c.compile("pointer_mut.c", cc="gcc")
    except check50.Failure:
        raise check50.Failure("Could not compile the program after making add "
                f"return {SENTINEL}")
    out = check50.run("./pointer_mut 10 20").stdout()
    if not re.search(rf"=\s*{SENTINEL}\b", out):
        raise check50.Failure(f"With add modified to always return {SENTINEL}"
                f", expected '10 + 20 = {SENTINEL}', got {out!r}: main should "
                "print the result of calling add")

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./pointer 10 20").exit(0)

@check50.check(exists)
def no_memory_errors(sources_buf):
    """no invalid memory accesses (AddressSanitizer)"""
    check50.c.compile("pointer.c", exe_name="pointer_asan", cc="gcc",
                      fsanitize="address")
    for args in ["10 20", "154 -12", "0 0"]:
        run = check50.run("./pointer_asan " + args,
                          env={"ASAN_OPTIONS": ASAN_OPTIONS})
        out = run.stdout()  # waits for the program to exit and sets exitcode
        if run.exitcode == ASAN_EXITCODE or "AddressSanitizer" in out:
            error = re.search(r"AddressSanitizer: [\w-]+", out)
            raise check50.Failure(f"With arguments {args}: memory error "
                    "detected: " +
                    (error.group(0) if error else "unknown error") +
                    ", compile with 'gcc -fsanitize=address pointer.c -o "
                    "pointer' and run it to see the full report")

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    check50.c.compile("pointer.c", exe_name="pointer_warn", cc="gcc",
                      Wall=True, Wextra=True, Werror=True)
