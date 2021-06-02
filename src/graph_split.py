import random
from typing import List

import networkx as nx
import numpy as np
from tqdm import tqdm


def remove_reversible_links(graph):
    set_list = [set(a) for a in graph.edges()]  # collect all edges, lose positional information
    remove_list = []  # initialise

    for i in range(len(set_list)):
        edge = set_list.pop(0)  # look at zeroth element in list:

        # if there is still an edge like the current one in the list,
        # add the current edge to the remove list:
        if set_list.count(edge) > 0:
            u, v = edge

            # add the reversed edge
            remove_list.append((v, u))

            # alternatively, add the original edge:
            # remove_list.append((u, v))

    graph.remove_edges_from(remove_list)  # remove all edges collected above
    return graph


class GraphComponent:
    def __init__(self, edges: List, nodes: List[int]):
        """

        :param edges: List[(int, int)]
        :param nodes:
        """
        self.edges = edges
        self.nodes = nodes

        self.DG: nx.DiGraph = None
        self._build_graph()

        self.disconnected_graph = []

        self.final_trees = []

    def _build_graph(self):
        self.DG = nx.DiGraph()
        self.DG.add_edges_from(self.edges)
        return self

    def output_result(self):
        return self.final_trees

    def split_disconnected_graphs(self):
        # components = [self.DG.subgraph(c).copy() for c in tqdm(nx.connected_components(self.DG.to_undirected()))]
        self.disconnected_graph = self._split_graphs(self.DG)
        self.disconnected_graph = [remove_reversible_links(i) for i in self.disconnected_graph]
        return self

    @staticmethod
    def _split_graphs(graphs: nx.DiGraph):
        components = [graphs.subgraph(c).copy() for c in nx.connected_components(graphs.to_undirected())]
        return components

    def delete_edges_and_split(self):
        for graph in tqdm(self.disconnected_graph):
            out_degrees = graph.out_degree(graph.nodes())
            out_degrees = list(map(lambda x: x[1], out_degrees))
            count = out_degrees.count(0)
            if count == 1:
                self.final_trees.append(graph)
                continue

            self.delete_edges(graph)
            self.final_trees += self._split_graphs(graph)
        return self

    @staticmethod
    def delete_edges(graph: nx.DiGraph):
        out_degrees = graph.out_degree(graph.nodes())

        colours = {}

        # find roots
        root = []
        for index, out_degrees in out_degrees:
            if out_degrees == 0:
                root.append(index)

        # give root initial colour
        colours = dict(zip(root, range(len(root))))
        number_of_colours = len(root)

        # init queue with the nodes connect to the root directly
        process_queue = []
        for i in root:
            assert len(list(graph.predecessors(i))) > 0
            process_queue += list(graph.predecessors(i))

        while len(process_queue) > 0:
            node = process_queue.pop(0)

            # count the colours of connected node
            upper_class_nodes = list(graph.neighbors(node))
            connected_colours = dict(zip(range(number_of_colours), [0]*number_of_colours))
            coloured_edges = dict(zip(range(number_of_colours+1), [None]*(number_of_colours+1)))
            for i in coloured_edges.keys():
                coloured_edges[i] = []
            for upper_class_node in upper_class_nodes:
                try:
                    colour_of_upper_class_node = colours[upper_class_node]
                    connected_colours[colour_of_upper_class_node] += 1

                    coloured_edges[colour_of_upper_class_node].append([node, upper_class_node])
                except KeyError:
                    coloured_edges[number_of_colours].append([node, upper_class_node])

            # choose the most coloured node
            max_connection = max(list(connected_colours.values()))
            max_colours = []
            for colour, connection in connected_colours.items():
                if connection == max_connection:
                    max_colours.append(colour)

            random.shuffle(max_colours)
            final_colour = max_colours[0]
            # inform the final colour of node
            colours[node] = final_colour

            # collect edges to delete
            edges_to_delete = []
            for colour, edges in coloured_edges.items():
                if colour != final_colour:
                    edges_to_delete += edges
                else:
                    edges.pop()
                    edges_to_delete += edges

            graph.remove_edges_from(edges_to_delete)

            # add nodes to  process queue
            process_queue += list(graph.predecessors(node))


def test():
    edges = np.random.randint(1, 1000, size=(100, 2)).tolist() + np.random.randint(1001, 2000, size=(1000, 2)).tolist()
    g = GraphComponent(edges, []).split_disconnected_graphs().delete_edges_and_split()

    print(len(g.final_trees), len(g.disconnected_graph))
    for i in g.final_trees:
        print(i.nodes())
        print(i.edges())

if __name__ == '__main__':
    g = GraphComponent(edges, []).split_disconnected_graphs().delete_edges_and_split()

    print(len(g.final_trees), len(g.disconnected_graph))
    for i in g.final_trees:
        print(i.nodes())
        print(i.edges())
