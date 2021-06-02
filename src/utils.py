from typing import List
import networkx as nx
import pandas as pd


def count_sentence_occurrence_in_graph(graph: nx.DiGraph, quoted_sentence: List[str], sentence_statics: pd.Series):
    nodes = graph.nodes
    quos_in_graphs = [quoted_sentence[i] for i in nodes]
    return sentence_statics[quos_in_graphs].values.sum()
