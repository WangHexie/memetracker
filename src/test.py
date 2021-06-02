from config import mode
from dataset import Dataset, filter_data
from graph_split import GraphComponent
from meme_trend import count_based_on_single_graph
from sentence_graph import SentenceGraph
from trend_visualization import draw_trend, draw_multiple_trend
import pandas as pd

from utils import count_sentence_occurrence_in_graph


def test_graph_split():
    data = Dataset(None, None).build_from_one_file("./data/quotes_2008-08.txt").output_quoted_data()
    data = filter_data(data)
    sg = SentenceGraph(data).create_graph()

    g = GraphComponent(sg.edges, []).split_disconnected_graphs().delete_edges_and_split()

    print(len(g.final_trees), len(g.disconnected_graph))
    for i in g.final_trees:
        print(i.nodes())
        print(i.edges())
        if 1.3 * len(i.nodes()) < len(i.edges()):
            k = i.nodes()

    for i in k:
        print(sg.quoted_sentences[i])


def test_trend_count():
    dataset = Dataset(None, None).build_from_one_file("./data/quotes_2008-08.txt")
    statics = dataset.statics_of_quoted_data()

    data = dataset.output_quoted_data()
    data = filter_data(data)
    sg = SentenceGraph(data).create_graph()

    g = GraphComponent(sg.edges, []).split_disconnected_graphs().delete_edges_and_split()
    trees = g.output_result()
    quoted_sentences = sg.quoted_sentences
    max_node = 0
    for i in trees:
        if len(i.nodes()) > max_node:
            max_node = len(i.nodes())

    tree = None
    for i in trees:
        if len(i.nodes()) == max_node:
            tree = i

    result = count_based_on_single_graph(statics, quoted_sentences, tree)
    print(result)
    return result


def test_draw():
    dataset = Dataset(None, None).build_from_one_file("./data/quotes_2008-08.txt")
    statics = dataset.statics_of_quoted_data()

    data = dataset.output_quoted_data()
    data = filter_data(data)
    sg = SentenceGraph(data).create_graph()

    g = GraphComponent(sg.edges, []).split_disconnected_graphs().delete_edges_and_split()
    trees = g.output_result()
    quoted_sentences = sg.quoted_sentences
    max_node = 0
    for i in trees:
        if len(i.nodes()) > max_node:
            max_node = len(i.nodes())

    tree = None
    for i in trees:
        if len(i.nodes()) == max_node:
            tree = i

    trees_and_nodes = [[i, len(i.nodes())] for i in trees]

    trees_and_nodes.sort(key=lambda x: x[1], reverse=True)

    num_of_trees_to_keep = 10

    trees_to_visualize = list(map(lambda x: x[0], trees_and_nodes[:num_of_trees_to_keep]))

    result, string = count_based_on_single_graph(statics, quoted_sentences, tree)
    print(result)

    draw_trend(result)
    return result


def test_draw_multiple_words():
    dataset = Dataset(None, time_span="3h").build_from_one_file("./data/quotes_2008-08.txt")
    statics = dataset.statics_of_quoted_data()

    quo_data = dataset.output_quoted_data()
    data = filter_data(quo_data)
    sg = SentenceGraph(data).create_graph()

    g = GraphComponent(sg.edges, []).split_disconnected_graphs().delete_edges_and_split()
    trees = g.output_result()
    quoted_sentences = sg.quoted_sentences

    trees_and_nodes = [[i, len(i.nodes())] for i in trees]
    trees_and_nodes.sort(key=lambda x: x[1], reverse=True)

    num_of_trees_to_keep = 10

    trees_to_visualize = list(map(lambda x: x[0], trees_and_nodes[:num_of_trees_to_keep]))

    results = []
    memes = []
    for tree in trees_to_visualize:
        result, string = count_based_on_single_graph(statics, quoted_sentences, tree)
        results.append(result)
        memes.append(string)
    print(memes)
    # shorten memes to avoid legend being too long.
    memes = [" ".join(i.split()[:20]) for i in memes]
    draw_multiple_trend(results, memes)
    return results


def test_draw_multiple_words_select_most_occurrence():
    dataset = Dataset(None, time_span="10m").build_from_one_file("./data/quotes_2008-08.txt")
    statics = dataset.statics_of_quoted_data()

    quo_data = dataset.output_quoted_data()

    # sentence count
    sentence_count = pd.DataFrame(quo_data, columns=["str"]).value_counts()

    data = filter_data(quo_data)
    sg = SentenceGraph(data).create_graph()

    g = GraphComponent(sg.edges, []).split_disconnected_graphs().delete_edges_and_split()
    trees = g.output_result()
    quoted_sentences = sg.quoted_sentences

    trees_and_nodes = [[i, count_sentence_occurrence_in_graph(i, quoted_sentences, sentence_count)] for i in trees]
    trees_and_nodes.sort(key=lambda x: x[1], reverse=True)

    num_of_trees_to_keep = 10

    trees_to_visualize = list(map(lambda x: x[0], trees_and_nodes[:num_of_trees_to_keep]))

    results = []
    memes = []
    for tree in trees_to_visualize:
        result, string = count_based_on_single_graph(statics, quoted_sentences, tree)
        results.append(result)
        memes.append(string)
    print(memes)
    memes = [" ".join(i.split()[:15]) for i in memes]
    draw_multiple_trend(results, memes)
    return results


if __name__ == '__main__':
    test_draw_multiple_words_select_most_occurrence()
