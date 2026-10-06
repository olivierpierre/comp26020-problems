This is a dummy exercise asking you to create an empty C program.
To succeed in this exercise, simply write the following program:

```c
int main() {
    return 0;
}
```

To check the correctness of your program, use a [suitable development environment](https://github.com/olivierpierre/comp26020-devcontainer/blob/master/README.md) with [check50 installed](exercise-set-1.html#installing-check50) and write your solution in a file named **`sample-exercise.c`**.
In a terminal, with that file in the local directory, check with this command:

```shell
check50 -l --ansi-log olivierpierre/comp26020-problems/main/week1-intro/01-sample-exercise
```

If you are on a very recent (as of 2026) Ubuntu/Fedora distribution you may see the following error:

```console
:| exists
    check50 ran into an error while running checks!
    TypeError: unsupported operand type(s) for /: 'NoneType' and 'str'
      File "/home/pierre/.local/lib/python3.14/site-packages/check50/runner.py", line 138, in wrapper
    internal.run_dir = run_root_dir / check.__name__
                       ~~~~~~~~~~~~~^~~~~~~~~~~~~~~~
```

This is a know `check50` bug, if you encouter it, patch it by running the following command:

```console
$ sed -i 's/if multiprocessing.get_start_method() != "spawn":/if multiprocessing.get_start_method() == "fork":/' ~/.local/lib/python3.14/site-packages/check50/runner.py
```

You may need to replace the last argument with proper the path to `runner.py` indicated by the error, and possibly to prefix that command with `sudo` if `check50` is installed system-wide.

**Submission:** once your work is ready please submit it [here](https://comp26020.uom.pierreolivier.eu/).