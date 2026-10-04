import check50
import check50.c
import random
import re

# the prompt may be followed by a space and/or a newline, the result may be
# followed by trailing spaces and an extra empty line
PROMPT_RE = r"input a string: ?\n?"
END_RE = r"[ \t]*\n{0,2}"

WORDS = ["the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog", "a",
         "i", "precious", "master", "shadows", "night", "wind", "will", "x",
         "zebra", "yellow", "one's", "it", "go"]

def capitalise(s):
    """expected result: first letter of each space-separated word upper case"""
    return "".join(c.upper() if (i == 0 or s[i - 1] == " ") else c
                   for i, c in enumerate(s))

def run_with(exe, s):
    """run exe, feeding it the string, return (run, full output)"""
    run = check50.run(exe)
    run.stdin(s, prompt=False)
    out = run.stdout()  # waits for the program to exit and sets exitcode
    return run, out

def check_capitalise(s):
    exp = capitalise(s)
    run, out = run_with("./string2", s)
    if not re.fullmatch(PROMPT_RE + re.escape(exp) + END_RE, out):
        raise check50.Failure(f"With input string {s!r}: expected "
                f"{'input a string:' + chr(10) + exp + chr(10)!r}, "
                f"got {out!r}")

@check50.check()
def exists():
    check50.exists("string2.c")
    with open("string2.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("string2.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    """capitalises the README examples and another sentence"""
    check_capitalise("we swears, to serve the master of the precious")
    check_capitalise("and following our will and wind we may just go where "
                     "no one's been")
    check_capitalise("It feels like chasing shadows in the night")

@check50.check(compiles)
def edge_cases():
    """handles single words, one-letter words and capitalised words"""
    check_capitalise("hello")
    check_capitalise("x")
    check_capitalise("a b c d")
    check_capitalise("Hello World")
    check_capitalise("ALREADY UPPER CASE")
    check_capitalise("hello, world!")

@check50.check(compiles)
def other_characters_unchanged():
    """leaves the other characters and the spacing unchanged"""
    check_capitalise("mcDonald sells iPhones")
    check_capitalise("route 66 is 3966 km long")
    check_capitalise("hello   world")
    check_capitalise("  leading spaces")

@check50.check(compiles)
def random_inputs():
    """capitalises random sentences"""
    for _ in range(10):
        n = random.randint(1, 8)
        check_capitalise(" ".join(random.choice(WORDS) for _ in range(n)))

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    s = "we swears, to serve the master of the precious"
    run, out = run_with("./string2", s)
    if run.exitcode != 0:
        raise check50.Failure(f"With input string {s!r}: expected exit code "
                f"0, got {run.exitcode}")

INPUTS = ["we swears, to serve the master of the precious", "x", "a b",
          "hello   world"]

@check50.check(compiles)
def valgrind_memcheck():
    """no uninitialised or invalid memory accesses (valgrind)"""
    for s in INPUTS:
        run = check50.run("valgrind -q --leak-check=no --error-exitcode=99 "
                          "./string2")
        run.stdin(s, prompt=False)
        run.stdout()
        if run.exitcode == 99:
            raise check50.Failure(f"With input string {s!r}: valgrind "
                    "detected memory errors, run 'valgrind ./string2' to see "
                    "the full report")

@check50.check(exists)
def no_memory_errors(sources_buf):
    """no out-of-bounds memory accesses (AddressSanitizer)"""
    check50.c.compile("string2.c", exe_name="string2_asan", cc="gcc",
                      fsanitize="address")
    for s in INPUTS:
        run = check50.run("./string2_asan", env={"ASAN_OPTIONS":
                                                 "detect_leaks=0"})
        run.stdin(s, prompt=False)
        out = run.stdout()  # waits for the program to exit and sets exitcode
        error = re.search(r"AddressSanitizer: [\w-]+", out)
        if error:
            raise check50.Failure(f"With input string {s!r}: memory error "
                    "detected: " + error.group(0) + ", compile with 'gcc "
                    "-fsanitize=address string2.c -o string2' and run "
                    "./string2 to see the full report")

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    # argc and argv are typically unused in this program, don't flag them
    check50.c.compile("string2.c", exe_name="string2_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
