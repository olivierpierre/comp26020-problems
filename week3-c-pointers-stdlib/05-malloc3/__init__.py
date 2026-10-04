import check50
import check50.c
import os
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

# the initialisation loop body of the provided code: a[i] = i*2;
INIT_RE = (r"\b\w+\s*\[\s*(\w+)\s*\]\s*=\s*"
           r"(?:\(?\s*\1\s*\)?\s*\*\s*2|2\s*\*\s*\(?\s*\1\s*\)?)\s*;")

def strip_comments(buf):
    """blank out comments and string/char literals, keeping offsets intact"""
    return re.sub(r"//[^\n]*|/\*.*?\*/|\"(?:\\.|[^\"\\\n])*\"|'(?:\\.|[^'\\\n])*'",
                  lambda m: re.sub(r"[^\n]", " ", m.group(0)), buf,
                  flags=re.DOTALL)

def check_output(exe, factor=2, context=""):
    exp = " ".join(str(i * factor) for i in range(10))
    out = check50.run("./" + exe).stdout()
    # tolerate a missing trailing space (the provided code prints one)
    if not re.fullmatch(re.escape(exp) + r" ?\n", out):
        raise check50.Failure(f"{context}Expected {exp + ' '!r} followed by a "
                f"newline, got {out!r}")

@check50.check()
def exists():
    check50.exists("malloc3.c")
    with open("malloc3.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("malloc3.c", cc="gcc")

@check50.check(exists)
def validate(sources_buf):
    """the array is still allocated with malloc and is freed"""
    buf = strip_comments(sources_buf)
    if not re.search(r"\bmalloc\s*\(", buf):
        raise check50.Failure("Cannot find call to malloc, the array should "
                "still be allocated with malloc")
    if not re.search(r"\bfree\s*\(", buf):
        raise check50.Failure("Cannot find a call to free")

@check50.check(compiles)
def output_correct():
    """output is exactly '0 2 4 6 8 10 12 14 16 18'"""
    check_output("malloc3")

@check50.check(exists)
def output_computed(sources_buf):
    """the printed values are the ones computed in the array"""
    m = re.search(INIT_RE, strip_comments(sources_buf))
    if not m:
        raise check50.Failure("Cannot find the initialisation of the array "
                "(a[i] = i*2;), only the memory leak should be fixed")
    # same program, with the array initialised with i*3 instead of i*2
    lhs = sources_buf[m.start():m.end()].split("=")[0]
    with open("malloc3_x3.c", "w") as f:
        f.write(sources_buf[:m.start()] + f"{lhs}= ({m.group(1)}) * 3;" +
                sources_buf[m.end():])
    check50.c.compile("malloc3_x3.c", cc="gcc")
    check_output("malloc3_x3", 3, "With the array initialised with i*3 "
            "instead of i*2: ")

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./malloc3").exit(0)

@check50.check(compiles)
def uses_malloc():
    """the array is still allocated with malloc"""
    with open("malloc_count.c", "w") as f:
        f.write(MALLOC_COUNT)
    # the linker flag is passed along with the file names
    check50.c.compile("malloc3.c", "malloc_count.c", "-Wl,--wrap=malloc",
                      exe_name="malloc3_count", cc="gcc")
    if os.path.exists("malloc_stats.txt"):
        os.remove("malloc_stats.txt")
    check50.run("./malloc3_count").stdout()
    try:
        with open("malloc_stats.txt") as f:
            calls, size = (int(v) for v in f.read().split())
    except (OSError, ValueError):
        raise check50.Failure("Could not monitor the calls to malloc, did "
                "the program crash?")
    if calls == 0:
        raise check50.Failure("malloc was never called")
    if size < 10 * 4:
        raise check50.Failure(f"malloc was called for a total of {size} "
                "bytes, but the array of 10 integers needs 40 bytes "
                "(10 * sizeof(int))")

@check50.check(compiles)
def valgrind_memcheck():
    """no memory errors or leaks (valgrind)"""
    if os.path.exists("valgrind.log"):
        os.remove("valgrind.log")
    check50.run("valgrind -q --leak-check=full --show-leak-kinds=all "
                "--errors-for-leak-kinds=all --log-file=valgrind.log "
                "./malloc3").stdout(timeout=20)
    with open("valgrind.log") as f:
        log = f.read()
    # with -q the log only contains errors, the first line of each error is
    # the only one not indented
    errors = re.findall(r"^==\d+== (\S.*)$", log, re.MULTILINE)
    if errors:
        for line in log.splitlines():
            check50.log(line)
        where = re.search(r"\(malloc3\.c:(\d+)\)", log)
        raise check50.Failure("valgrind reported: " + errors[0] +
                (f" (malloc3.c line {where.group(1)})" if where else "") +
                ", run 'valgrind --leak-check=full ./malloc3' to see the full "
                "report")

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    # argc and argv are unused in the provided code, don't flag them
    check50.c.compile("malloc3.c", exe_name="malloc3_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
