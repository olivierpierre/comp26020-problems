import check50
import check50.c
import re

expected_file = " world\nthis is a test file containing the word  several " \
    "times\nsome lines do not contain that word\nwhile others do: \n"
expected_file2 = " world\nthis is a test file containing the word  several " \
    "times\nsome lines do not contain that word\nwhile others do: "

@check50.check()
def exists():
    check50.exists("stream.c")
    check50.exists("sample-file-1")
    with open("stream.c") as f:
        sources_buf = f.read()
    return sources_buf

@check50.check(exists)
def uses_stream_based_IO(sources_buf):
    if("fopen" not in sources_buf and "fread" not in sources_buf and
            "fwrite" not in sources_buf):
        raise check50.Failure("Cannot find calls to fopen/fread/fwrite")

@check50.check(exists)
def compiles():
    check50.c.compile("stream.c", cc="gcc")

@check50.check(compiles)
def output_correct():
    check50.run("./stream sample-file-1 hello")\
            .exit()
    with open("sample-file-1-processed") as f:
        buf = f.read()
        if not (buf == expected_file) and not (buf == expected_file2):
            print("------ got: --------")
            print(buf)
            print("---- expected: -----")
            print(expected_file2)
            raise check50.Failure("Bad output file")

