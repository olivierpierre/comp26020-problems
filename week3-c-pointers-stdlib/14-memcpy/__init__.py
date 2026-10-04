import check50
import check50.c
import random
import re

# runs the student's program with memcpy wrapped to count the calls and the
# number of bytes copied, reported on the last output line at exit. After the
# copy, 1000 is added to each int of the source array so that we can tell
# which array is printed on the array2 line.
HARNESS = r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int memcpy_calls;
static size_t memcpy_bytes;

static void *h_memcpy(void *dst, const void *src, size_t n) {
    memcpy_calls++;
    memcpy_bytes += n;
    memcpy(dst, src, n);
    if (n % sizeof(int) == 0)
        for (size_t i = 0; i < n / sizeof(int); i++)
            ((int *)src)[i] += 1000;
    return dst;
}

static void report(void) {
    printf("\nMEMCPY %d %zu\n", memcpy_calls, memcpy_bytes);
}

#define memcpy(d, s, n) h_memcpy(d, s, n)
#define main student_main
#include "memcpy.c"
#undef main
#undef memcpy

int main(int argc, char **argv) {
    atexit(report);
    return student_main(argc, argv);
}
"""

def strip_comments(buf):
    return re.sub(r"//[^\n]*|/\*.*?\*/", " ", buf, flags=re.DOTALL)

def shorten(s, length=100):
    return s if len(s) <= length else s[:length] + "..."

def parse_lines(n, out):
    """checks the output format for size n, returns the two lists of values"""
    lines = out.rstrip("\n").split("\n")
    values = []
    for i, name in enumerate(["array1", "array2"]):
        line = lines[i] if i < len(lines) else ""
        m = re.fullmatch(name + r":((?:\s+-?[0-9]+)*)\s*", line)
        if not m:
            raise check50.Failure(f"With n = {n}: expected line {i + 1} to "
                    f"be '{name}:' followed by {n} integers separated by "
                    f"spaces, got {shorten(line)!r}")
        values.append([int(v) for v in m.group(1).split()])
        if len(values[i]) != n:
            raise check50.Failure(f"With n = {n}: expected {n} integers "
                    f"after '{name}:', got {len(values[i])}")
    if len(lines) > 2:
        raise check50.Failure(f"With n = {n}: unexpected extra output "
                f"after the two arrays: {shorten(chr(10).join(lines[2:]))!r}")
    return values

def parse_arrays(n, out):
    """checks the output for size n, returns the values of array1"""
    values = parse_lines(n, out)
    bad = [v for v in values[0] if v < 0 or v > 100]
    if bad:
        raise check50.Failure(f"With n = {n}: array1 contains {bad[0]}, "
                "values should be between 0 and 100")
    if values[0] != values[1]:
        raise check50.Failure(f"With n = {n}: array2 is not identical to "
                f"array1: {values[0][:20]} vs {values[1][:20]}")
    return values[0]

def check_memcpy(n, exe="memcpy"):
    out = check50.run(f"./{exe} {n}").stdout()
    return parse_arrays(n, out)

@check50.check()
def exists():
    check50.exists("memcpy.c")
    with open("memcpy.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("memcpy.c", cc="gcc")

@check50.check(exists)
def validate(sources_buf):
    """memcpy, malloc and rand are used"""
    buf = strip_comments(sources_buf)
    if not re.search(r"\bmemcpy\s*\(", buf):
        raise check50.Failure("Cannot find call to memcpy in the code")
    if not re.search(r"\b(malloc|calloc)\s*\(", buf):
        raise check50.Failure("Cannot find call to malloc: the arrays should "
                "be allocated dynamically")
    if not re.search(r"\b(rand|random|rand_r)\s*\(", buf):
        raise check50.Failure("Cannot find call to rand to generate the "
                "random integers")

@check50.check(compiles)
def output_correct():
    """prints two identical arrays of n integers for the README examples"""
    for n in [10, 15, 20]:
        check_memcpy(n)

@check50.check(compiles)
def edge_cases():
    """works with arrays of 1 and 2 elements and with a large array"""
    for n in [1, 2]:
        check_memcpy(n)
    values = check_memcpy(1000)
    if len(set(values)) < 20:
        raise check50.Failure(f"With n = 1000: only {len(set(values))} "
                "different values in the array, it should be filled with "
                "random integers between 0 and 100")
    if values == sorted(values) or values == sorted(values, reverse=True):
        raise check50.Failure("With n = 1000: the values are sorted, the "
                "array should be filled with random integers")

@check50.check(compiles)
def random_sizes():
    """works with random array sizes"""
    for _ in range(5):
        check_memcpy(random.randint(3, 300))

def compile_harness():
    with open("harness.c", "w") as f:
        f.write(HARNESS)
    try:
        check50.c.compile("harness.c", cc="gcc")
    except check50.Failure:
        raise check50.Failure("Could not compile the program with memcpy "
                "replaced by a wrapper counting the calls")

def run_harness(n):
    """returns the output of the student's program, number of memcpy calls
    and number of bytes copied"""
    out = check50.run(f"./harness {n}").stdout()
    m = re.search(r"\nMEMCPY ([0-9]+) ([0-9]+)\n?$", out)
    if not m:
        raise check50.Failure(f"With n = {n}: the program did not terminate "
                "normally")
    return out[:m.start()] + "\n", int(m.group(1)), int(m.group(2))

@check50.check(compiles)
def single_memcpy():
    """the array is copied with a single call to memcpy"""
    compile_harness()
    for n in [10, 50]:
        _, calls, size = run_harness(n)
        if calls != 1:
            raise check50.Failure(f"With n = {n}: memcpy was called {calls} "
                    "times, the array should be copied with a single call")
        if size < n * 4:
            raise check50.Failure(f"With n = {n}: memcpy copied {size} bytes, "
                    f"the array of {n} int is {n * 4} bytes large")

@check50.check(output_correct)
def prints_copy():
    """array2 is printed from the copy made by memcpy"""
    compile_harness()
    n = 10
    values = parse_lines(n, run_harness(n)[0])
    if any(v >= 1000 for v in values[1]):
        raise check50.Failure("The values printed on the array2 line are "
                "read from the first array (the checker modified the first "
                "array after the memcpy call): array2 should be printed from "
                "the second array")

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./memcpy 10").exit(0)

@check50.check(exists)
def no_memory_errors(sources_buf):
    """no out-of-bounds memory accesses (AddressSanitizer)"""
    check50.c.compile("memcpy.c", exe_name="memcpy_asan", cc="gcc",
                      fsanitize="address")
    for n in [1, 10, 100]:
        # leaks are checked by valgrind_memcheck
        run = check50.run(f"./memcpy_asan {n}",
                          env={"ASAN_OPTIONS": "detect_leaks=0"})
        out = run.stdout()  # waits for the program to exit and sets exitcode
        if run.exitcode != 0:
            error = re.search(r"AddressSanitizer: [\w-]+", out)
            raise check50.Failure(f"With n = {n}: memory error detected: " +
                    (error.group(0) if error else "unknown error") +
                    ", compile with 'gcc -fsanitize=address memcpy.c -o "
                    "memcpy' and run it to see the full report")

@check50.check(compiles)
def valgrind_memcheck():
    """no memory errors or leaks (valgrind)"""
    run = check50.c.valgrind("./memcpy 20")
    parse_arrays(20, run.stdout())
    if run.exitcode != 0:
        raise check50.Failure(f"Expected exit code 0, got {run.exitcode}")

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    # argc may legitimately be unused, don't flag it
    check50.c.compile("memcpy.c", exe_name="memcpy_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
