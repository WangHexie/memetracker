from typing import List

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def draw_trend(count_result:dict):
    sns.set_theme(style="whitegrid")

    # Load the diamonds dataset
    diamonds = pd.DataFrame(list(zip(list(count_result.keys()), list(count_result.values()))), columns=["x", "y"])

    # print(diamonds["x"])
    diamonds.set_index(["x"], inplace=True)


    # sns.lineplot(data=diamonds, palette="tab10", linewidth=2.5)

    sns.displot(data=diamonds, palette="tab10",  kind="kde")
    plt.show()

    # Plot the distribution of clarity ratings, conditional on carat
    # sns.displot(
    #     data=diamonds,
    #     x="x",
    #     kind="kde", height=6,
    #     multiple="fill", clip=(0, None),
    #     palette="ch:rot=-.25,hue=1,light=.75",
    # )


def draw_multiple_trend(count_result:List[dict], memes:List[str]):
    sns.set_theme(style="whitegrid")

    time = list(count_result[0].keys())

    

    diamonds = pd.DataFrame(list(zip(list(count_result.keys()), list(count_result.values()))), columns=["x", "y"])

    diamonds.set_index(["x"], inplace=True)

    sns.displot(data=diamonds, palette="tab10",  kind="kde")
    plt.show()