import check50
import check50.c
import random
import re

# the prompt may be followed by a newline, the message may be followed by
# trailing spaces and an extra empty line
PROMPT = "please enter an integer number (base 10): "
PROMPT_RE = re.escape(PROMPT.strip()) + r" ?\n?"
END_RE = r"[ \t]*\n{0,2}"

INVALID = "invalid string"
RANGE = "under/overflow"

# test program calling the student's convert_and_print function directly, the
# student's main is renamed so that it does not clash with ours
HARNESS = r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define main student_main
#include "strtol.c"
#undef main

int main(int argc, char **argv) {
    char buf[128];
    if (argc != 2)
        return 1;
    strncpy(buf, argv[1], 127);
    buf[127] = '\0';
    convert_and_print(buf);
    return 0;
}
"""

def strip_comments(buf):
    return re.sub(r"//[^\n]*|/\*.*?\*/", " ", buf, flags=re.DOTALL)

def run_with(exe, s):
    """run exe, feeding it the string, return (run, full output)"""
    run = check50.run(exe)
    run.stdin(s, prompt=False)
    out = run.stdout()  # waits for the program to exit and sets exitcode
    return run, out

def check_input(s, msg):
    """msg: expected message, an int means 'you have entered: <int>'"""
    if isinstance(msg, int):
        msg = f"you have entered: {msg}"
    run, out = run_with("./strtol", s)
    if not re.fullmatch(PROMPT_RE + re.escape(msg) + END_RE, out):
        raise check50.Failure(f"With input {s!r}: expected "
                f"{PROMPT + msg + chr(10)!r}, got {out!r}")

def check_function(s, msg):
    if isinstance(msg, int):
        msg = f"you have entered: {msg}"
    out = check50.run(f"./harness '{s}'").stdout()
    if not re.fullmatch(re.escape(msg) + END_RE, out):
        raise check50.Failure(f"convert_and_print(\"{s}\") should print "
                f"{msg + chr(10)!r}, got {out!r}")

@check50.check()
def exists():
    check50.exists("strtol.c")
    with open("strtol.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("strtol.c", cc="gcc")

@check50.check(exists)
def uses_strtol(sources_buf):
    """the conversion is done with strtol rather than atoi"""
    code = strip_comments(sources_buf)
    if not re.search(r"\bstrtol\s*\(", code):
        raise check50.Failure("Found no call to strtol in the source code")
    if re.search(r"\batoi\s*\(", code):
        raise check50.Failure("atoi is still called in the source code")

@check50.check(compiles)
def output_correct_standard_integer():
    """converts positive integers and zero"""
    check_input("42", 42)
    check_input("1234", 1234)
    check_input("7", 7)
    check_input("0", 0)

@check50.check(compiles)
def output_correct_negative_integer():
    """converts negative integers"""
    check_input("-42", -42)
    check_input("-1", -1)
    check_input("-98765", -98765)

@check50.check(compiles)
def output_correct_int_limits():
    """converts the smallest and largest values of an int"""
    check_input("2147483647", 2147483647)
    check_input("-2147483648", -2147483648)

@check50.check(compiles)
def output_correct_letters():
    """reports strings with no number as invalid"""
    for s in ["bar", "foo", "hello world", "x42", "-"]:
        check_input(s, INVALID)

@check50.check(compiles)
def output_correct_overflow():
    """reports overflows"""
    check_input("100000000000000000000", RANGE)
    check_input("99999999999999999999999999", RANGE)

@check50.check(compiles)
def output_correct_underflow():
    """reports underflows"""
    check_input("-100000000000000000000", RANGE)
    check_input("-99999999999999999999999999", RANGE)

@check50.check(compiles)
def random_inputs():
    """converts random integers"""
    for _ in range(10):
        n = random.randint(-2**31, 2**31 - 1)
        check_input(str(n), n)

@check50.check(compiles)
def convert_and_print_correct():
    """convert_and_print(buf) converts the string and prints the result"""
    with open("harness.c", "w") as f:
        f.write(HARNESS)
    try:
        check50.c.compile("harness.c", cc="gcc")
    except check50.Failure:
        raise check50.Failure("Could not call convert_and_print with a "
                "char * parameter")
    check_function("1234", 1234)
    check_function("-42", -42)
    check_function("foo", INVALID)
    check_function("100000000000000000000", RANGE)
    check_function("-100000000000000000000", RANGE)

@check50.check(compiles)
def exit_code():
    """program exits with status 0 when a valid integer is entered"""
    for s in ["1234", "-42"]:
        run, out = run_with("./strtol", s)
        if run.exitcode != 0:
            raise check50.Failure(f"With input {s!r}: expected exit code 0, "
                    f"got {run.exitcode}")

@check50.check(exists)
def no_memory_errors(sources_buf):
    """no out-of-bounds memory accesses (AddressSanitizer)"""
    check50.c.compile("strtol.c", exe_name="strtol_asan", cc="gcc",
                      fsanitize="address")
    for s in ["1234", "foo", "100000000000000000000", "-42", ""]:
        run = check50.run("./strtol_asan", env={"ASAN_OPTIONS":
                                                "detect_leaks=0"})
        run.stdin(s, prompt=False)
        out = run.stdout()  # waits for the program to exit and sets exitcode
        error = re.search(r"AddressSanitizer: [\w-]+", out)
        if error:
            raise check50.Failure(f"With input {s!r}: memory error detected: "
                    + error.group(0) + ", compile with 'gcc "
                    "-fsanitize=address strtol.c -o strtol' and run ./strtol "
                    "to see the full report")

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    # don't flag the warnings coming from the provided get_string/main code:
    # unused size/argc/argv, strlen used without including string.h, and
    # int/size_t comparison
    check50.c.compile("strtol.c", exe_name="strtol_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Wno_implicit_function_declaration=True,
                      Wno_builtin_declaration_mismatch=True,
                      Wno_sign_compare=True, Werror=True)
