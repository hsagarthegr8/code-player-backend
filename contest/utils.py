import time
import subprocess
import os


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


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
