from stats.base_stat import BaseStat


class Espresso(BaseStat):

    def __init__(self):
        super().__init__()
        self.start_command = 'adb shell am instrument -w -m -e debug false si.uni_lj.fri.pbd.thesisapp.test/androidx.test.runner.AndroidJUnitRunner'
        self.encoding = 'Latin-1'

    def extract_data_from_result(self, result):
        last_line = [s for s in result.splitlines() if s][-1]
        split_line = last_line.split(" ")
        failed = split_line[0] == "Tests"
        if failed:
            all_tests = int(split_line[2][0])
            failed_tests = int(split_line[-1])
        else:
            all_tests = int(split_line[1][1])
            failed_tests = 0
        self.all_cases += all_tests
        self.failed_cases += failed_tests
