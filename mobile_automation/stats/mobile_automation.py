import re
from stats.base_stat import BaseStat


class MobileAutomation(BaseStat):

    def __init__(self, android=True):
        super().__init__()
        self.base_path = "../mobile_automation"
        self.platform = "android" if android else "ios"
        self.start_command = f'pytest --config="andrija-{self.platform}" --app="thesis_app" {self.base_path}/tests/thesis_app/'
        self.encoding = 'utf-8'

    def extract_data_from_result(self, result):
        result = result.split("\n")[0]
        result = re.sub(r"\s\s+", " ", result)
        result = result.split(" ")[0]
        for res in result:
            if res == "F":
                self.failed_cases += 1
            self.all_cases += 1
