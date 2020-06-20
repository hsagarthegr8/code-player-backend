import time
import subprocess


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        return result, round(te-ts, 6)
    return timed


@timeit
def run_code(filepath, stdin):
    with open(stdin, 'r') as file:
        runner = subprocess.run(
            args=['python', filepath], capture_output=True, stdin=file)
    return runner
