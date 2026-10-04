import check50
import check50.c
import os
import random
import re

# content of the sample-file-1 provided with the exercise, rewritten by the
# checks so that a locally modified copy does not change the results
SAMPLE = ("hello world\n"
          "this is a test file containing the word hello several times\n"
          "some lines do not contain that word\n"
          "while others do: hello\n")

# the word to delete always appears separated from the rest of the text by
# spaces/newlines, and is never part of another word, so that deleting
# substrings and deleting whole words give the same result
VOCAB = ["apple", "banana", "cherry", "grape", "lemon", "mango", "orange",
         "peach", "plum", "kiwi", "melon", "papaya", "fig", "lime", "date"]

def big_text(word, n_lines, seed):
    """many short lines with lots of occurrences of word"""
    rng = random.Random(seed)
    others = [w for w in VOCAB if word not in w and w not in word]
    lines = []
    for _ in range(n_lines):
        n = rng.randint(0, 12)
        lines.append(" ".join(rng.choice(others + [word, word])
                              for _ in range(n)))
    return "\n".join(lines) + "\n"

def show(s):
    return repr(s) if len(s) <= 300 else f"{len(s)} characters"

def first_difference(expected, got):
    exp_lines = expected.split("\n")
    got_lines = got.split("\n")
    for i, exp_line in enumerate(exp_lines):
        got_line = got_lines[i] if i < len(got_lines) else "<end of file>"
        if exp_line != got_line:
            return (f"line {i + 1}: expected {exp_line!r}, got {got_line!r}")
    return f"line {len(exp_lines) + 1}: unexpected extra content"

def check_processed(fname, content, word, prog="./file", old_output=None):
    """run prog on a file named fname containing content, check the result"""
    with open(fname, "w") as f:
        f.write(content)
    out_name = fname + "-processed"
    if old_output is None:
        if os.path.exists(out_name):
            os.remove(out_name)
    else:
        with open(out_name, "w") as f:
            f.write(old_output)

    code = check50.run(f"{prog} {fname} {word}").exit(timeout=10)

    desc = f"With file {fname} containing {show(content)} and word {word!r}"
    if not os.path.exists(out_name):
        status = "crashed" if code is None else f"exited with status {code}"
        raise check50.Failure(f"{desc}: the file {out_name} was not created "
                f"(the program {status})")
    with open(out_name, "rb") as f:
        got = f.read().decode("utf-8", errors="replace")

    expected = content.replace(word, "")
    # tolerate a missing newline at the very end of the file
    if got != expected and not (expected.endswith("\n") and
                                got == expected[:-1]):
        if len(expected) <= 300 and len(got) <= 300:
            raise check50.Failure(f"{desc}: expected {out_name} to contain "
                    f"{expected!r}, got {got!r}")
        raise check50.Failure(f"{desc}: wrong content in {out_name}, " +
                first_difference(expected, got))

    with open(fname) as f:
        if f.read() != content:
            raise check50.Failure(f"{desc}: the input file {fname} was "
                    "modified")

@check50.check()
def exists():
    check50.exists("file.c")
    check50.exists("sample-file-1")
    with open("file.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def compiles():
    check50.c.compile("file.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    """creates sample-file-1-processed as in the README example"""
    check_processed("sample-file-1", SAMPLE, "hello")

@check50.check(compiles)
def other_file_and_word():
    """works with other file names and words"""
    check_processed("input.txt",
            "the cat sat on the mat\nthe end\n", "the")
    check_processed("notes",
            "abc abc\nabc\n\nxyz abc xyz abc abc\n  abc  \nlast abc",
            "abc")
    check_processed("data.txt",
            "one two three\nfour five\n", "two")

@check50.check(compiles)
def edge_cases():
    """handles an absent word, an empty file, lines with only the word"""
    check_processed("absent.txt",
            "nothing to remove here\nreally nothing\n", "hello")
    check_processed("empty.txt", "", "hello")
    check_processed("only.txt", "hello\n", "hello")
    check_processed("lines.txt", "hello hello hello\nhello\n", "hello")

@check50.check(compiles)
def random_inputs():
    """handles random files and words"""
    for _ in range(5):
        word = random.choice(VOCAB)
        fname = "random-" + str(random.randint(0, 99999)) + ".txt"
        content = big_text(word, random.randint(1, 15), random.random())
        check_processed(fname, content, word)

@check50.check(compiles)
def large_file():
    """handles a file larger than typical buffer sizes (100 KB)"""
    for word in ["melon", "fig"]:
        content = big_text(word, 2000, word)
        check_processed("large.txt", content, word)

@check50.check(compiles)
def overwrites_output():
    """replaces the content of an already existing output file"""
    check_processed("sample-file-1", SAMPLE, "hello",
            old_output="old content that should be replaced\n" * 5)

@check50.check(compiles)
def exit_code():
    """program exits with status 0"""
    with open("sample-file-1", "w") as f:
        f.write(SAMPLE)
    check50.run("./file sample-file-1 hello").exit(0)

@check50.check(exists)
def no_memory_errors(sources_buf):
    """no out-of-bounds memory accesses (AddressSanitizer)"""
    check50.c.compile("file.c", exe_name="file_asan", cc="gcc",
                      fsanitize="address")
    tests = [("sample-file-1", SAMPLE, "hello"),
             ("empty.txt", "", "hello"),
             ("large.txt", big_text("plum", 2000, "asan"), "plum")]
    for fname, content, word in tests:
        with open(fname, "w") as f:
            f.write(content)
        run = check50.run(f"./file_asan {fname} {word}",
                          env={"ASAN_OPTIONS": "detect_leaks=0"})
        out = run.stdout(timeout=20)  # waits for the program to exit
        # the exit status is tested by exit_code, only look for ASan reports
        error = re.search(r"AddressSanitizer: [\w-]+", out)
        if error:
            raise check50.Failure(f"With arguments {fname} {word}: memory "
                    "error detected: " + error.group(0) +
                    ", compile with 'gcc -fsanitize=address file.c -o file' "
                    "and run it to see the full report")

@check50.check(exists)
def no_warnings(sources_buf):
    """compiles without warnings (-Wall -Wextra -Werror)"""
    # argc is often left unused in this exercise, don't flag it
    check50.c.compile("file.c", exe_name="file_warn", cc="gcc",
                      Wall=True, Wextra=True, Wno_unused_parameter=True,
                      Werror=True)
