from typing import List
from tqdm import tqdm
from config import mode
import pandas as pd


class Dataset:
    def __init__(self, path, time_span="1h"):
        """
        self.data = List[dict("P", "T", "Q", "L")]
        :param path:
        :param max_unit:
        """
        self.path = path
        self.time_span = time_span
        self.data: List[dict] = []

    @staticmethod
    def _construct_data_dict(data: str):
        data_dict = dict([("P", None),
                          ("T", None),
                          ("Q", []),
                          ("L", [])])

        data_split = data.split("\n")
        for i in data_split:
            if i[0] in ["P", "T"]:
                # use [2:] to avoid \t
                data_dict[i[0]] = i[2:]
            else:
                data_dict[i[0]].append(i[2:])
        return data_dict

    def build_from_one_file(self, path):
        with open(path, "r", encoding="utf-8") as f:
            if mode == "test":
                data = f.read(1000000000)
            else:
                data = f.read()

            splits = data.split("\n\n")
            print("number of units:", len(splits))
            for i in tqdm(splits):
                try:
                    self.data.append(self._construct_data_dict(i))
                except IndexError:
                    print("error construct data:", i)
        return self

    def output_quoted_data(self):
        quoted_sentences = []
        for i in tqdm(range(len(self.data))):
            quoted_sentences += self.data[i]["Q"]
        return quoted_sentences

    def output_quoted_data_with_time(self):
        quoted_sentences = []
        time = []
        for i in tqdm(range(len(self.data))):
            quoted_sentences += self.data[i]["Q"]
            time += [self.data[i]["T"]] * len(self.data[i]["Q"])

        df = pd.DataFrame({"quoted": quoted_sentences, "time": time})
        df['time'] = pd.to_datetime(df['time'])

        return df

    def statics_of_quoted_data(self):
        df = self.output_quoted_data_with_time()
        result = df.groupby([pd.Grouper(key="time", freq=self.time_span), "quoted"]).size()
        return result


def delete_too_short_phrase(data: pd.DataFrame, min_length=4):
    string_length = data["str"].map(lambda x: len(x.split()))
    return data[string_length > min_length]


def delete_meaningless_gt(data: pd.DataFrame, str_to_exclude=" gt "):
    string_length = data["str"].map(lambda x: str_to_exclude not in x)
    return data[string_length.values]


def delete_uncommon_phrase(data: pd.DataFrame, min_occurrence=10):
    counts = data["str"].value_counts()
    # TODO: bug warning!!!!. return a series, not dataframe ,
    return counts[counts.values > min_occurrence]


def filter_data(data: List[str]):
    data_df = pd.DataFrame(data, columns=["str"])

    data_df = delete_too_short_phrase(data_df)
    data_df = delete_meaningless_gt(data_df)
    data_df = delete_uncommon_phrase(data_df)
    # counts = data_df["str"].value_counts()
    counts = data_df
    return counts.index.tolist()


if __name__ == '__main__':
    data = Dataset(None, None).build_from_one_file("./data/quotes_2008-08.txt").output_quoted_data_with_time()

    # data = filter_data(data)
    print(data["time"])
    result = data.groupby([pd.Grouper(key="time", freq="1min"), "quoted"]).size()
    print(result)
    print(result[0])
    print(result.index.levels[0])
    print(result.loc["2008-08-01 00:00:00", "4 minutes to live"])
    print(result.loc["2008-08-01 00:00:00", "4 minutes     to live"])
    print(result[result.loc["2008-08-01 00:00:00"][0]])

    # print(len(data.data))
    # for i in range(10):
    #     print(data.data[i])
