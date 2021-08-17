import time
import subprocess


class BaseStat:

    def __init__(self):
        self.failed_cases = 0
        self.all_cases = 0
        self.run_results = []

    def run_test(self):
        print(f"Running command: {self.start_command}")
        start_time = time.time()
        result = subprocess.Popen(self.start_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = result.communicate()
        output = out.decode(self.encoding)
        end_time = time.time()
        td = end_time - start_time
        self.run_results.append(td)
        self.extract_data_from_result(output)
        print(f"Time difference is: {td}")
        return td
