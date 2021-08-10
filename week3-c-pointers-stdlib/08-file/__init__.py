import check50
import check50.c
import re

expected_file = " world\nthis is a test file containing the word  several " \
    "times\nsome lines do not contain that word\nwhile others do: \n"
expected_file2 = " world\nthis is a test file containing the word  several " \
    "times\nsome lines do not contain that word\nwhile others do: "

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
    check50.run("./file sample-file-1 hello")\
            .exit()
    with open("sample-file-1-processed") as f:
        buf = f.read()
        if not (buf == expected_file) and not (buf == expected_file2):
            print("------ got: --------")
            print(buf)
            print("---- expected: -----")
            print(expected_file2)
            raise check50.Failure("Bad output file")

