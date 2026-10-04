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

def check_matrix(x, y):
    """./malloc2 x y prints x lines of y integers (as in the README examples)"""
    expected = [" ".join(str(i * y + j) for j in range(y)) for i in range(x)]
    out = check50.run(f"./malloc2 {x} {y}").stdout()
    # tolerate trailing spaces on each line and trailing blank lines
    actual = [l.rstrip(" ") for l in out.rstrip("\n").split("\n")]
    for i in range(max(len(expected), len(actual))):
        if i >= len(expected):
            raise check50.Failure(f"With arguments {x} {y}: expected {x} "
                    f"lines, unexpected extra output on line {i+1}: "
                    f"{actual[i]!r}")
        if i >= len(actual):
            raise check50.Failure(f"With arguments {x} {y}: expected {x} "
                    f"lines, got {len(actual)}, missing line {i+1}: "
                    f"{expected[i]!r}")
        if actual[i] != expected[i]:
            raise check50.Failure(f"With arguments {x} {y}: line {i+1}: "
                    f"expected {expected[i]!r}, got {actual[i]!r}")

def check_valgrind(args):
    if os.path.exists("valgrind.log"):
        os.remove("valgrind.log")
    check50.run("valgrind -q --leak-check=full --show-leak-kinds=all "
                "--errors-for-leak-kinds=all --log-file=valgrind.log "
                "./malloc2 " + args).stdout(timeout=20)
    with open("valgrind.log") as f:
        log = f.read()
    # with -q the log only contains errors, the first line of each error is
    # the only one not indented
    errors = re.findall(r"^==\d+== (\S.*)$", log, re.MULTILINE)
    if errors:
        for line in log.splitlines():
            check50.log(line)
        where = re.search(r"\(malloc2\.c:(\d+)\)", log)
        raise check50.Failure(f"With arguments {args}: valgrind reported: "
                f"{errors[0]}" + (f" (malloc2.c line {where.group(1)})"
                if where else "") + f", run 'valgrind --leak-check=full "
                f"./malloc2 {args}' to see the full report")

@check50.check()
def exists():
    check50.exists("malloc2.c")
    with open("malloc2.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("malloc2.c", cc="gcc")

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
    """prints the README examples and a few other sizes"""
    check_matrix(3, 4)
    check_matrix(2, 5)
    check_matrix(10, 11)
    check_matrix(3, 5)
    check_matrix(4, 4)
    check_matrix(5, 10)

@check50.check(compiles)
def edge_cases():
    """handles a single row and/or a single column"""
    check_matrix(1, 1)
    check_matrix(1, 7)
    check_matrix(7, 1)

@check50.check(compiles)
def random_inputs():
    """prints random sizes from 1x1 to 20x20"""
    for _ in range(10):
        check_matrix(random.randint(1, 20), random.randint(1, 20))

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./malloc2 3 4").exit(0)

@check50.check(compiles)
def uses_malloc():
    """the integers are stored in memory allocated with malloc"""
    with open("malloc_count.c", "w") as f:
        f.write(MALLOC_COUNT)
    # the linker flag is passed along with the file names
    check50.c.compile("malloc2.c", "malloc_count.c", "-Wl,--wrap=malloc",
                      exe_name="malloc2_count", cc="gcc")
    x, y = 7, 9
    if os.path.exists("malloc_stats.txt"):
        os.remove("malloc_stats.txt")
    check50.run(f"./malloc2_count {x} {y}").stdout()
    try:
        with open("malloc_stats.txt") as f:
            calls, size = (int(v) for v in f.read().split())
    except (OSError, ValueError):
        raise check50.Failure(f"With arguments {x} {y}: could not monitor "
                "the calls to malloc, did the program crash?")
    if calls == 0:
        raise check50.Failure(f"With arguments {x} {y}: malloc was never "
                "called")
    if size < x * y * 4:
        raise check50.Failure(f"With arguments {x} {y}: malloc was called "
                f"for a total of {size} bytes, but {x * y} integers need "
                f"{x * y * 4} bytes ({x * y} * sizeof(int))")

@check50.check(compiles)
def valgrind_memcheck():
    """no memory errors or leaks (valgrind)"""
    check_valgrind("3 4")
    check_valgrind("1 1")
    check_valgrind("6 9")

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    # argc may legitimately be unused, don't flag it
    check50.c.compile("malloc2.c", exe_name="malloc2_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
