from typing import List

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def draw_trend(count_result: dict):
    sns.set_theme(style="whitegrid")

    # Load the diamonds dataset
    diamonds = pd.DataFrame(list(zip(list(count_result.keys()), list(count_result.values()))), columns=["x", "y"])

    # print(diamonds["x"])
    diamonds.set_index(["x"], inplace=True)

    # sns.lineplot(data=diamonds, palette="tab10", linewidth=2.5)

    sns.displot(data=diamonds, palette="tab10", kind="kde")
    plt.show()

    # Plot the distribution of clarity ratings, conditional on carat
    # sns.displot(
    #     data=diamonds,
    #     x="x",
    #     kind="kde", height=6,
    #     multiple="fill", clip=(0, None),
    #     palette="ch:rot=-.25,hue=1,light=.75",
    # )


def draw_multiple_trend(count_result: List[dict], memes: List[str]):
    sns.set_theme(style="whitegrid")

    data_dict = {"time":[], "meme":[], "count":[]}
    for count, meme in zip(count_result, memes):
        data_dict["time"] += list(count.keys())
        data_dict["meme"] += [meme] * len(list(count.keys()))
        data_dict["count"] += list(count.values())

    diamonds = pd.DataFrame(data_dict)

    # # diamonds.set_index(["x"], inplace=True)
    # data_wide = diamonds.pivot(index="time", columns="meme", values="count")
    # # sns.displot(data=flights_wide, palette="tab10", kind="kde")
    # sns.displot(data=diamonds,x="time", y="count",hue="meme", palette="tab10", kind="kde")
    # plt.show()

    a4_dims = (15.7, 8.27)
    from matplotlib import pyplot

    fig, ax = pyplot.subplots(figsize=a4_dims)

    sns.lineplot(ax=ax, data=diamonds,x="time", y="count",hue="meme", sizes=(40,10))
    plt.show()
