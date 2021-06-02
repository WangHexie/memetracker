import os

with open("./data/quotes_2008-08.txt", "r", encoding="utf-8") as f:
    data = f.read()
    print(data[:1000])

    splits = data.split("\n\n")
    print(len(splits))
    print(splits[512])