import celluloid
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


import analysis_util


def graph_from_spec(connections):
    edges = []
    for node in range(np.shape(connections)[0]):
        for connection in connections[node, :]:
            edges.append((node, connection))
    graph = nx.Graph()
    graph.add_edges_from(edges)
    return graph


def graph_from_ragged_spec(connections, used_connections, node_labels=None):
    if node_labels is None:
        node_labels = np.arange(start=0, stop=np.shape(connections)[0], step=1)
    g = nx.DiGraph()
    g.add_nodes_from(node_labels)
    for i, (c, u) in enumerate(zip(connections, used_connections)):
        this_cons = np.squeeze(c[np.argwhere(u == 1)], -1)
        g.add_edges_from([(node_labels[x], node_labels[i]) for x in this_cons])
    return g


def influence_graph_from_ragged_spec(functions, connections, used_connections, node_labels=None):
    if node_labels is None:
        node_labels = np.arange(start=0, stop=np.shape(connections)[0], step=1)
    inf = analysis_util.compute_influence(functions)
    g = nx.DiGraph()
    g.add_nodes_from(node_labels)
    for i, (c, u, infs) in enumerate(zip(connections, used_connections, inf)):
        this_cons = np.squeeze(c[np.argwhere(u == 1)], -1)
        this_infs = np.squeeze(infs[np.argwhere(u == 1)], -1)
        edges = []
        for x, w in zip(this_cons, this_infs):
            if w>0:
                edges.append((node_labels[x], node_labels[i], w))

        g.add_weighted_edges_from(edges)
    return g


def prune_non_participating(g, skip_nodes):
    while True:
        all_edges = [e for e in g.edges]
        to_remove = []
        for node in g.nodes:
            active = False
            for edge in all_edges:
                if node == edge[0] and not node == edge[1]:
                    active = True
            if not active and not node in skip_nodes:
                to_remove.append(node)
        g.remove_nodes_from(to_remove)
        if not to_remove:
            break


def plot_network_directed(graph, pos, ax, node_colors, colorbar=False):
    labels = {}
    edges, weights = zip(*nx.get_edge_attributes(graph, 'weight').items())
    for node in graph.nodes():
        labels[node]=node
    nx.draw_networkx_nodes(graph, pos=pos, ax=ax, node_color=node_colors)
    g = nx.draw_networkx_edges(graph, pos=pos, arrowstyle="->", ax=ax, arrows=True, edge_color=weights, edge_cmap=plt.cm.Greys, edge_vmin=0, edge_vmax=1)

    nx.draw_networkx_labels(graph, pos, labels, ax=ax)
    if colorbar:
        sm = plt.cm.ScalarMappable(cmap=plt.cm.Greys, norm=plt.Normalize(vmin=0, vmax=1))
        sm._A = []
        plt.colorbar(sm)


def plot_graph_with_state(g, layout, state, ax, colors, **kwargs):
    color_list = [colors[0] if x else colors[1] for x in state]
    nx.draw(g, ax=ax, pos=layout, node_color=color_list, **kwargs)


def graph_animation(g, layout, trajectory, fig, ax, **kwargs):
    camera = celluloid.Camera(fig)
    for state in trajectory:
        plot_graph_with_state(g, layout, state, ax, **kwargs)
        camera.snap()
    animation = camera.animate()
    return animation
