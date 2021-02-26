import os
import guppy
import src.config as config
import json
import inspect

PROFILING_DIRECTORY = "memory_profiling"
PROFILING_OUTPUT_FILE = "raw_memory_usage.txt"
REPORT_OUTPUT_FILE = "memory_profile_report.txt"


def setup_memory_usage_file_if_enabled() -> None:
    if config.USE_MEMORY_PROFILING:
        print(f"Setting up memory profile output file: {PROFILING_OUTPUT_FILE}")
        # Clear the file so each run is unique.
        with open(os.path.join(PROFILING_DIRECTORY, PROFILING_OUTPUT_FILE), "w"):
            pass


def record_current_memory_usage_if_enabled() -> None:
    """
    Write the memory usage at the current context- file name and line number- (in bytes) to the output file.
    """
    if config.USE_MEMORY_PROFILING:
        calling_frame = inspect.stack()[1]
        with open(os.path.join(PROFILING_DIRECTORY, PROFILING_OUTPUT_FILE), "a") as f:
            hp = guppy.hpy()
            entry = {'file_name': calling_frame.filename, 'line_number': calling_frame.lineno,
                     'heap_size_bytes': hp.heap().size}
            f.write(json.dumps(entry) + "\n")


def generate_report_if_enabled() -> None:
    if config.USE_MEMORY_PROFILING:
        with open(os.path.join(PROFILING_DIRECTORY, PROFILING_OUTPUT_FILE), "r") as rf:
            # remove blank lines
            raw_lines = filter(lambda l: len(l) > 0, rf.readlines())
            with open(os.path.join(PROFILING_DIRECTORY, REPORT_OUTPUT_FILE), "w") as wf:
                print(f"Writing report to: {REPORT_OUTPUT_FILE}")
                for i, v in enumerate(raw_lines):
                    report_block = []
                    memory_dict = json.loads(v)
                    report_block.append(f"Memory checkpoint # {i + 1}")
                    report_block.append(f"\tFile Name: {memory_dict.get('file_name', 'MISSING_FILE_NAME')}")
                    report_block.append(f"\tLine Number: {memory_dict.get('line_number', 'MISSING_LINE_NUMBER')}")
                    heap_bytes = memory_dict.get('heap_size_bytes', 0)
                    heap_mb = int(heap_bytes/1048576 )
                    report_block.append(f"\tCurrent Memory Usage: {heap_mb} MB")
                    wf.writelines(map(lambda l: l + "\n", report_block))
