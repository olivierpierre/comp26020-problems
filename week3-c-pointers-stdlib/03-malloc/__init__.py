import check50
import check50.c
import os
import random
import re

# linked with the student's program (-Wl,--wrap=malloc) to record the number
# of calls to malloc and the total number of bytes requested
MALLOC_COUNT = r"""
#include <stdio.h>
#include <stddef.h>

void *__real_malloc(size_t size);
static size_t calls, bytes;

void *__wrap_malloc(size_t size) {
    calls++;
    bytes += size;
    return __real_malloc(size);
}

__attribute__((destructor)) static void malloc_count_report(void) {
    FILE *f = fopen("malloc_stats.txt", "w");
    if (f) {
        fprintf(f, "%zu %zu\n", calls, bytes);
        fclose(f);
    }
}
"""

def strip_comments(buf):
    """remove comments and string/char literals"""
    return re.sub(r"//[^\n]*|/\*.*?\*/|\"(?:\\.|[^\"\\\n])*\"|'(?:\\.|[^'\\\n])*'",
                  " ", buf, flags=re.DOTALL)

def check_sort(*args):
    exp = " ".join(str(v) for v in sorted(args))
    args_str = " ".join(str(v) for v in args)
    out = check50.run("./malloc " + args_str).stdout()
    # tolerate a trailing space and/or newline, as printed by a "%d " loop
    if not re.fullmatch(re.escape(exp) + r" ?\n?", out):
        raise check50.Failure(f"With arguments {args_str}: expected {exp!r}, "
                f"got {out!r}")

def check_valgrind(args):
    if os.path.exists("valgrind.log"):
        os.remove("valgrind.log")
    check50.run("valgrind -q --leak-check=full --show-leak-kinds=all "
                "--errors-for-leak-kinds=all --log-file=valgrind.log "
                "./malloc " + args).stdout(timeout=20)
    with open("valgrind.log") as f:
        log = f.read()
    # with -q the log only contains errors, the first line of each error is
    # the only one not indented
    errors = re.findall(r"^==\d+== (\S.*)$", log, re.MULTILINE)
    if errors:
        for line in log.splitlines():
            check50.log(line)
        where = re.search(r"\(malloc\.c:(\d+)\)", log)
        raise check50.Failure(f"With arguments {args}: valgrind reported: "
                f"{errors[0]}" + (f" (malloc.c line {where.group(1)})"
                if where else "") + f", run 'valgrind --leak-check=full "
                f"./malloc {args}' to see the full report")

@check50.check()
def exists():
    check50.exists("malloc.c")
    with open("malloc.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("malloc.c", cc="gcc")

@check50.check(exists)
def validate(sources_buf):
    """calls malloc and free"""
    buf = strip_comments(sources_buf)
    if not re.search(r"\bmalloc\s*\(", buf):
        raise check50.Failure("Cannot find call to malloc")
    if not re.search(r"\bfree\s*\(", buf):
        raise check50.Failure("Cannot find a call to free")

@check50.check(compiles)
def output_correct():
    """sorts the README examples and a 31 integers list"""
    check_sort(5, 4, 3, 2, 1)
    check_sort(546, 874, 18, 13, 87, 54, 4651, 54, 877, 8, 46351, 87, 654,
            657, 654)
    check_sort(546, 874, 18, 13, 87, 54, 4651, 54, 877, 8, 46351, 87, 654,
            657, 654, 546, 87, 45, 67, 6, 546, 85746, 984, 4, 5646, 68, 47,
            654, 654, 6, 87674)

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
def large_values():
    """handles values close to the limits of int"""
    check_sort(2000000000, -2000000000, 0)
    check_sort(2147483647, -2147483648, 1, -1)

@check50.check(compiles)
def random_inputs():
    """sorts random lists of 1 to 50 integers"""
    for _ in range(10):
        n = random.randint(1, 50)
        check_sort(*[random.randint(-100000, 100000) for _ in range(n)])

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./malloc 5 4 3 2 1").exit(0)

@check50.check(compiles)
def uses_malloc():
    """the integers are stored in memory allocated with malloc"""
    with open("malloc_count.c", "w") as f:
        f.write(MALLOC_COUNT)
    # the linker flag is passed along with the file names
    check50.c.compile("malloc.c", "malloc_count.c", "-Wl,--wrap=malloc",
                      exe_name="malloc_count", cc="gcc")
    args = [random.randint(-1000, 1000) for _ in range(20)]
    args_str = " ".join(str(v) for v in args)
    if os.path.exists("malloc_stats.txt"):
        os.remove("malloc_stats.txt")
    check50.run("./malloc_count " + args_str).stdout()
    try:
        with open("malloc_stats.txt") as f:
            calls, size = (int(v) for v in f.read().split())
    except (OSError, ValueError):
        raise check50.Failure(f"With arguments {args_str}: could not monitor "
                "the calls to malloc, did the program crash?")
    if calls == 0:
        raise check50.Failure(f"With arguments {args_str}: malloc was never "
                "called")
    if size < 20 * 4:
        raise check50.Failure(f"With arguments {args_str}: malloc was called "
                f"for a total of {size} bytes, but 20 integers need "
                f"{20 * 4} bytes (20 * sizeof(int))")

@check50.check(compiles)
def valgrind_memcheck():
    """no memory errors or leaks (valgrind)"""
    check_valgrind("5 4 3 2 1")
    check_valgrind("42")
    check_valgrind(" ".join(str(random.randint(-1000, 1000))
                            for _ in range(30)))

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    check50.c.compile("malloc.c", exe_name="malloc_warn", cc="gcc",
                      Wall=True, Wextra=True, Werror=True)
