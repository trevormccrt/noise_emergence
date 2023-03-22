import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

import general_network_visualization, analysis_util

connectivity = np.array([[1, 3],[2, 0],[3, 1],[0, 2]]).astype(np.uint8)
used_connectivity = np.ones_like(connectivity).astype(np.bool_)
functions = np.array([[0, 0, 0, 1], [0, 1, 1, 0], [1, 0, 0, 0], [0, 1, 1, 1]])

g = general_network_visualization.influence_graph_from_ragged_spec(functions, connectivity, used_connectivity)
pos = nx.spring_layout(g)
#fig, axs = plt.subplots()
#general_network_visualization.plot_network_directed(g, pos, axs, ["C0"] * 4, colorbar=True)

states, _ = analysis_util.run_dynamics_forward_save_state(np.array([1, 0, 0, 0], dtype=np.bool_), functions, connectivity, used_connectivity, 5, 0.0)
to_plot_states = states[:4]
fig, axs = plt.subplots(nrows=1, ncols=4)
for ax, state in zip(axs, states):
    node_colors = ["yellow" if x else "purple" for x in state ]
    general_network_visualization.plot_network_directed(g, pos, ax, node_colors, colorbar=False)
    fig.tight_layout()


used_connectivity_rag = np.array([[True, True], [False, True], [True, False], [True, True]])
g_rag = general_network_visualization.influence_graph_from_ragged_spec(functions, connectivity, used_connectivity_rag)
fig_rag, ax_rag = plt.subplots()
general_network_visualization.plot_network_directed(g_rag, pos, ax_rag, ["C0"] * 4, colorbar=False)
plt.show()
# \begin{tabular}{||c c || c ||}
#  \hline
#  $x_1[t]$ & $x_3[t]$ & $x_0[t+1]$ \\ [0.5ex]
#  \hline\hline
#  0 & 0 & 0 \\
#  \hline
#  1 & 0 & 0  \\
#  \hline
#  0 & 1 & 0\\
#  \hline
#  1 & 1 & 1 \\
#  \hline
# \end{tabular}
#
# \newline
#
#
# \begin{tabular}{||c c || c ||}
#  \hline
#  $x_2[t]$ & $x_0[t]$ & $x_1[t+1]$ \\ [0.5ex]
#  \hline\hline
#  0 & 0 & 0 \\
#  \hline
#  1 & 0 & 1  \\
#  \hline
#  0 & 1 & 1\\
#  \hline
#  1 & 1 & 0 \\
#  \hline
# \end{tabular}
#
# \newline
#
#
# \begin{tabular}{||c c || c ||}
#  \hline
#  $x_3[t]$ & $x_1[t]$ & $x_2[t+1]$ \\ [0.5ex]
#  \hline\hline
#  0 & 0 & 1 \\
#  \hline
#  1 & 0 & 0  \\
#  \hline
#  0 & 1 & 0\\
#  \hline
#  1 & 1 & 0 \\
#  \hline
# \end{tabular}
#
# \newline
#
#
# \begin{tabular}{||c c || c ||}
#  \hline
#  $x_0[t]$ & $x_2[t]$ & $x_3[t+1]$ \\ [0.5ex]
#  \hline\hline
#  0 & 0 & 0 \\
#  \hline
#  1 & 0 & 1 \\
#  \hline
#  0 & 1 & 1 \\
#  \hline
#  1 & 1 & 1 \\
#  \hline
# \end{tabular}
