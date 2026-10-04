import check50
import check50.c
import re

EXPECTED = "third member value is: 3\n"

# a printf call with a format string and arguments (args in group 2), the
# arguments may span several lines
PRINTF_RE = r'\bprintf\s*\(\s*"((?:[^"\\]|\\.)*)"\s*,([^;]*)\)\s*;'

# leaks are not checked, ASan errors are reported with a distinctive exit code
ASAN_EXITCODE = 99
ASAN_OPTIONS = f"detect_leaks=0:exitcode={ASAN_EXITCODE}"

# code inserted before the printf: lm1 now leads to a different chain, the
# printed value must follow it
REDIRECT = ("{ static __typeof__(lm1) chk2, chk3; "
            "chk3.value = 42; chk3.next = 0; "
            "chk2.value = 41; chk2.next = &chk3; "
            "lm1.next = &chk2; } ")

def strip_comments(buf):
    return re.sub(r"//[^\n]*|/\*.*?\*/", " ", buf, flags=re.DOTALL)

def printf_calls(buf):
    """(match, arguments) of each printf call with arguments"""
    return [(m, m.group(2)) for m in re.finditer(PRINTF_RE, buf)]

def check_output(out, exp):
    if out != exp and out != exp.rstrip("\n"):
        raise check50.Failure(f"Expected {exp!r}, got {out!r}")

@check50.check()
def exists():
    check50.exists("pointer2.c")
    with open("pointer2.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("pointer2.c", cc="gcc")

@check50.check(exists)
def validate(sources_buf):
    """lm2 and lm3 are not used in the printf parameters"""
    calls = printf_calls(strip_comments(sources_buf))
    if not calls:
        raise check50.Failure("Could not find a call to printf with a "
                "parameter after the format string")
    for _, args in calls:
        for var in ["lm3", "lm2"]:
            if re.search(rf"\b{var}\b", args):
                raise check50.Failure(f"Do not use {var} in printf parameters")

@check50.check(exists)
def validate2(sources_buf):
    """the printf parameter walks the pointer chain from lm1"""
    for _, args in printf_calls(strip_comments(sources_buf)):
        if re.search(r"\blm1\b", args) and \
                len(re.findall(r"\bnext\b", args)) >= 2 and \
                re.search(r"\bvalue\b", args):
            return
    raise check50.Failure("Could not find the proper pointer chain walk: the "
            "printf parameter should start from lm1 and follow the next "
            "pointers twice to reach the value")

@check50.check(compiles)
def output_correct():
    """output is exactly 'third member value is: 3'"""
    check_output(check50.run("./pointer2").stdout(), EXPECTED)

@check50.check(validate2)
def follows_chain():
    """the printed value follows the chain starting at lm1"""
    with open("pointer2.c") as f:
        buf = strip_comments(f.read())
    m = [m for m, args in printf_calls(buf) if re.search(r"\blm1\b", args)][0]
    with open("pointer2_mut.c", "w") as f:
        f.write(buf[:m.start()] + REDIRECT + buf[m.start():])
    try:
        check50.c.compile("pointer2_mut.c", cc="gcc")
    except check50.Failure:
        raise check50.Failure("Could not compile the program after redirecting "
                "lm1.next to another list before the printf")
    out = check50.run("./pointer2_mut").stdout()
    if not re.search(r"value is: 42\b", out):
        raise check50.Failure("After changing lm1.next to point to a list "
                "whose third element has value 42, expected 'third member "
                f"value is: 42\\n', got {out!r}: the value should be obtained "
                "by following the pointers from lm1")

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./pointer2").exit(0)

@check50.check(exists)
def no_memory_errors(sources_buf):
    """no invalid memory accesses (AddressSanitizer)"""
    check50.c.compile("pointer2.c", exe_name="pointer2_asan", cc="gcc",
                      fsanitize="address")
    run = check50.run("./pointer2_asan", env={"ASAN_OPTIONS": ASAN_OPTIONS})
    out = run.stdout()  # waits for the program to exit and sets exitcode
    if run.exitcode == ASAN_EXITCODE or "AddressSanitizer" in out:
        error = re.search(r"AddressSanitizer: [\w-]+", out)
        raise check50.Failure("Memory error detected: " +
                (error.group(0) if error else "unknown error") +
                ", compile with 'gcc -fsanitize=address pointer2.c -o "
                "pointer2' and run ./pointer2 to see the full report")

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    # argc and argv are unused in the provided code, don't flag them
    check50.c.compile("pointer2.c", exe_name="pointer2_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
