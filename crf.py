import os
import re

class Result:

    def __init__(self, list):
        self.index = list[0]
        self.time = list[1]
        self.scramble = list[2]
        self.penalty = list[3]

    def get_time_including_penalty(self):

        if self.penalty == "none":
            return self.time

        if self.penalty == "DNF":
            return -2

        return self.time + int(self.penalty) * 1000


    def to_string(self):
        res = ""

        res += f"{self.index}. "

        if self.penalty.isdigit():
            res += f"{self.time}" + (int(int(self.penalty) / 2) * "+") + " "
        elif self.penalty == "DNF":
            res += f"DNF({self.time}) "
        else:
            res += f"{self.time} "

        res += self.scramble

        return res

    def add_penalty(self, penalty):

        if penalty == "none":
            self.penalty = "none"

        if penalty == "2":
            if self.penalty == "DNF":
                return

            if self.penalty == "none":
                self.penalty = "2"
                return

            self.penalty = str(int(self.penalty) + 2)
        if penalty == "DNF":
            self.penalty = "DNF"

class CrfHandler:

    def __init__(self):
        self.working_file = "test.crf"


    def check_file(self):
        if self.working_file not in os.listdir("."):
            with open(self.working_file, "x") as f:
                f.close()
                return

    def get_all(self):

        res = []

        with open(self.working_file, "r") as f:

            content = f.readlines()

            for i in range(len(content)):
                res.append(Result(self.parse(content[i])))

        return res


    def write(self, result: Result):
        with open(self.working_file, "a") as f:
            f.write(result.to_string() + "\n")
            f.close()

    def update_line(self, result: Result):
        with open(self.working_file, "r+") as f:
            lines = f.readlines()

            if 1 <= result.index <= len(lines):
                lines[result.index - 1] = result.to_string() + "\n"

            f.seek(0)
            f.truncate()
            f.writelines(lines)
            f.close()

    def get_index(self):
        with open(self.working_file, "r") as f:
            try:
                last = f.readlines()[-1]
            except:
                return 1
            return int(self.parse(last)[0]) + 1

    def parse(self, line):

        splitted = line.split(" ", 2)

        index = int(splitted[0].replace(".", ""))
        time = splitted[1]
        scramble = splitted[2].replace("\n", "")
        penalty = "none"

        if time.count("+") > 0:
            penalty = str(time.count("+") * 2)

        if time.startswith("DNF(") and time.endswith(")"):
            penalty = "DNF"

        time = int(re.sub(r"[DNF()+]", "", time))

        return [index, time, scramble, penalty]