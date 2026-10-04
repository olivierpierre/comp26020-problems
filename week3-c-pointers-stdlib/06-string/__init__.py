import check50
import check50.c
import random
import re
import string

# prompts may be followed by a space and/or a newline, the result line may be
# followed by trailing spaces and an extra empty line
OUTPUT_RE = (r"input string1: ?\n?input string2: ?\n?strings are {}[ \t]*"
             r"\n{{0,2}}")

def strip_comments(buf):
    return re.sub(r"//[^\n]*|/\*.*?\*/", " ", buf, flags=re.DOTALL)

def run_with(exe, s1, s2):
    """run exe, feeding it the two strings, return (run, full output)"""
    run = check50.run(exe)
    run.stdin(s1, prompt=False)
    run.stdin(s2, prompt=False)
    out = run.stdout()  # waits for the program to exit and sets exitcode
    return run, out

def check_compare(s1, s2):
    res = "similar" if s1 == s2 else "different"
    run, out = run_with("./string", s1, s2)
    if not re.fullmatch(OUTPUT_RE.format(res), out):
        exp = f"input string1:\ninput string2:\nstrings are {res}\n"
        raise check50.Failure(f"With input strings {s1!r} and {s2!r}: "
                f"expected {exp!r}, got {out!r}")

@check50.check()
def exists():
    check50.exists("string.c")
    with open("string.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("string.c", cc="gcc")

@check50.check(exists)
def uses_fgets(sources_buf):
    """the strings are read with fgets"""
    if not re.search(r"\bfgets\s*\(", strip_comments(sources_buf)):
        raise check50.Failure("Found no call to fgets in the source code")

@check50.check(compiles)
def output_correct():
    """compares the README examples and a few other strings"""
    check_compare("test", "test")
    check_compare("hello world!", "goodbye")
    check_compare("testtest", "test")
    check_compare("goodbye", "goodbye")

@check50.check(compiles)
def edge_cases():
    """handles prefixes, single character and empty strings"""
    check_compare("test", "testtest")
    check_compare("abcd", "abce")
    check_compare("xbcd", "abcd")
    check_compare("abc", "abc ")
    check_compare("hello world", "hello world")
    check_compare("hello world", "hello")
    check_compare("a", "a")
    check_compare("a", "b")
    check_compare("", "")
    check_compare("", "a")
    check_compare("a", "")

@check50.check(compiles)
def random_inputs():
    """compares random pairs of identical and different strings"""
    chars = string.ascii_letters + string.digits + " "
    for i in range(10):
        s1 = "".join(random.choice(chars)
                     for _ in range(random.randint(1, 12)))
        if i % 2 == 0:
            s2 = s1
        else:
            # change one character, or append/remove some
            s2 = list(s1)
            pos = random.randrange(len(s2))
            s2[pos] = random.choice(chars.replace(s2[pos], ""))
            s2 = random.choice(["".join(s2), s1 + "x", s1[:-1]])
        check_compare(s1.strip() or "x", s2.strip() or "y")

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    for s1, s2 in [("test", "test"), ("hello world!", "goodbye")]:
        run, out = run_with("./string", s1, s2)
        if run.exitcode != 0:
            raise check50.Failure(f"With input strings {s1!r} and {s2!r}: "
                    f"expected exit code 0, got {run.exitcode}")

@check50.check(compiles)
def valgrind_memcheck():
    """no uninitialised or invalid memory accesses (valgrind)"""
    for s1, s2 in [("abcd", "efgh"), ("test", "test"), ("", "hello world!")]:
        run = check50.run("valgrind -q --leak-check=no --error-exitcode=99 "
                          "./string")
        run.stdin(s1, prompt=False)
        run.stdin(s2, prompt=False)
        run.stdout()
        if run.exitcode == 99:
            raise check50.Failure(f"With input strings {s1!r} and {s2!r}: "
                    "valgrind detected memory errors, run 'valgrind ./string' "
                    "to see the full report")

@check50.check(exists)
def no_memory_errors(sources_buf):
    """no out-of-bounds memory accesses (AddressSanitizer)"""
    check50.c.compile("string.c", exe_name="string_asan", cc="gcc",
                      fsanitize="address")
    for s1, s2 in [("abcd", "efgh"), ("test", "test"), ("", "hello world!"),
                   ("hello world!", "hello world!")]:
        run = check50.run("./string_asan", env={"ASAN_OPTIONS":
                                                "detect_leaks=0"})
        run.stdin(s1, prompt=False)
        run.stdin(s2, prompt=False)
        out = run.stdout()  # waits for the program to exit and sets exitcode
        error = re.search(r"AddressSanitizer: [\w-]+", out)
        if error:
            raise check50.Failure(f"With input strings {s1!r} and {s2!r}: "
                    "memory error detected: " + error.group(0) +
                    ", compile with 'gcc -fsanitize=address string.c -o "
                    "string' and run ./string to see the full report")

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    # argc and argv are typically unused in this program, don't flag them
    check50.c.compile("string.c", exe_name="string_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
