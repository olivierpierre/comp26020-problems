import check50
import check50.c
import re

EXPECTED = ("".join(f"before realloc, array[{i}] = {i * 10}\n" for i in range(5)) +
            "".join(f"after realloc, array[{i}] = {i * 10}\n" for i in range(10)))

# test program calling the student's my_realloc directly. malloc, calloc and
# free are wrapped to track the live heap buffers and their sizes, the
# student's main is renamed so that it does not clash with ours. Compiled with
# AddressSanitizer to catch out-of-bounds copies.
HARNESS = r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_BUFS 64
static void *bufs[MAX_BUFS];
static size_t sizes[MAX_BUFS];

static void track(void *p, size_t size) {
    for (int i = 0; i < MAX_BUFS; i++)
        if (!bufs[i]) { bufs[i] = p; sizes[i] = size; return; }
}

static long tracked_size(void *p) {
    for (int i = 0; i < MAX_BUFS; i++)
        if (p && bufs[i] == p) return (long)sizes[i];
    return -1;
}

static void *h_malloc(size_t size) {
    void *p = malloc(size);
    if (p) track(p, size);
    return p;
}

static void *h_calloc(size_t n, size_t size) {
    void *p = calloc(n, size);
    if (p) track(p, n * size);
    return p;
}

static void h_free(void *p) {
    for (int i = 0; i < MAX_BUFS; i++)
        if (p && bufs[i] == p) bufs[i] = NULL;
    free(p);
}

#define malloc(s) h_malloc(s)
#define calloc(n, s) h_calloc(n, s)
#define free(p) h_free(p)
#define main student_main
#include "malloc5.c"
#undef main
#undef malloc
#undef calloc
#undef free

int main(int argc, char **argv) {
    if (argc != 3) return 2;
    size_t old_size = atol(argv[1]), new_size = atol(argv[2]);
    size_t keep = old_size < new_size ? old_size : new_size;

    unsigned char *p = h_malloc(old_size);
    for (size_t i = 0; i < old_size; i++) p[i] = (unsigned char)(i * 7 + 3);

    unsigned char *q = my_realloc(p, old_size, new_size);
    if (!q) {
        printf("my_realloc returned NULL\n");
        return 1;
    }
    long size = tracked_size(q);
    if (size < 0) {
        printf("the returned pointer was not obtained from malloc\n");
        return 1;
    }
    if ((size_t)size < new_size) {
        printf("the returned buffer is only %ld bytes large\n", size);
        return 1;
    }
    for (size_t i = 0; i < keep; i++)
        if (q[i] != (unsigned char)(i * 7 + 3)) {
            printf("byte %zu of the buffer was not preserved\n", i);
            return 1;
        }
    if (q != p && tracked_size(p) >= 0) {
        printf("the old buffer was not freed\n");
        return 1;
    }
    memset(q, 0, new_size);
    h_free(q);
    printf("OK\n");
    return 0;
}
"""

def strip_comments(buf):
    return re.sub(r"//[^\n]*|/\*.*?\*/", " ", buf, flags=re.DOTALL)

def compile_harness():
    with open("harness.c", "w") as f:
        f.write(HARNESS)
    try:
        check50.c.compile("harness.c", cc="gcc", fsanitize="address")
    except check50.Failure:
        raise check50.Failure("Could not call my_realloc(void *ptr, size_t "
                "old_size, size_t new_size) and get a pointer back")

def check_realloc(old_size, new_size):
    # leaks are detected by the harness itself, with a clearer message
    run = check50.run(f"./harness {old_size} {new_size}",
                      env={"ASAN_OPTIONS": "detect_leaks=0"})
    out = run.stdout()  # waits for the program to exit and sets exitcode
    # the student's function may print things, only look at the last line
    if run.exitcode == 0 and out.rstrip("\n").endswith("OK"):
        return
    what = f"my_realloc(ptr, {old_size}, {new_size})"
    error = re.search(r"AddressSanitizer: [\w-]+", out)
    if error:
        raise check50.Failure(f"With {what}: memory error detected: "
                f"{error.group(0)}, compile with 'gcc -fsanitize=address "
                "malloc5.c -o malloc5' and run it to see the full report")
    raise check50.Failure(f"With {what} on a buffer allocated with malloc: "
            f"{out.strip() or 'the program crashed'}")

@check50.check()
def exists():
    check50.exists("malloc5.c")
    with open("malloc5.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("malloc5.c", cc="gcc")

@check50.check(exists)
def validate(sources_buf):
    """my_realloc is defined and the standard realloc is not used"""
    buf = strip_comments(sources_buf)
    if not re.search(r"\bmy_realloc\s*\([^;{]*\)\s*\{", buf):
        raise check50.Failure("Cannot find the definition of my_realloc")
    if not re.search(r"\bmalloc\s*\(", buf):
        raise check50.Failure("Cannot find call to malloc")
    if not re.search(r"\bfree\s*\(", buf):
        raise check50.Failure("Cannot find a call to free")
    if re.search(r"\brealloc\s*\(", buf):
        raise check50.Failure("my_realloc should be implemented manually, "
                "without calling the standard realloc function")

@check50.check(compiles)
def output_correct():
    """output is exactly the one given in the README"""
    out = check50.run("./malloc5").stdout()
    if out.rstrip("\n") + "\n" != EXPECTED:
        exp_lines, got_lines = EXPECTED.split("\n"), out.split("\n")
        for i, exp in enumerate(exp_lines[:-1]):
            got = got_lines[i] if i < len(got_lines) else None
            if got != exp:
                raise check50.Failure(f"Line {i + 1}: expected {exp!r}, got "
                        f"{got!r}" if got is not None else
                        f"Line {i + 1}: expected {exp!r}, got nothing")
        raise check50.Failure(f"Unexpected extra output after the last line: "
                f"{chr(10).join(got_lines[len(exp_lines) - 1:])!r}")

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    check50.run("./malloc5").exit(0)

@check50.check(compiles)
def my_realloc_grows():
    """my_realloc enlarges a buffer, keeps its content and frees the old one"""
    compile_harness()
    check_realloc(20, 40)
    check_realloc(8, 1000)
    check_realloc(7, 13)
    check_realloc(16, 16)

@check50.check(compiles)
def my_realloc_shrinks():
    """my_realloc shrinks a buffer, keeping only the content that fits"""
    compile_harness()
    check_realloc(40, 12)
    check_realloc(1000, 8)
    check_realloc(13, 7)

@check50.check(compiles)
def valgrind_memcheck():
    """no memory errors or leaks (valgrind)"""
    check50.c.valgrind("./malloc5").exit(0)

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    # argc and argv are unused in the provided code, don't flag them
    check50.c.compile("malloc5.c", exe_name="malloc5_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
