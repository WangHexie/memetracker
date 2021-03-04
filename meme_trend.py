from typing import List

import pandas as pd
import networkx as nx


def count_based_on_single_graph(sentence_count: pd.DataFrame, quoted_sentences: List[str], graph: nx.DiGraph):
    times = sentence_count.index.levels[0].tolist()

    out_degrees = graph.out_degree(graph.nodes())

    root = None
    for index, out_degrees in out_degrees:
        if out_degrees == 0:
            root = index
            break

    root_sentence = quoted_sentences[root]

    all_sentences_in_the_graph = [quoted_sentences[i] for i in graph.nodes()]

    count_sum_by_time = dict(zip(times, [0] * len(times)))
    for time in times:
        for sentence in all_sentences_in_the_graph:
            try:
                count = sentence_count.loc[time, sentence]
            except KeyError:
                count = 0
            count_sum_by_time[time] += count

    return count_sum_by_time, root_sentence


if __name__ == '__main__':
    pass
