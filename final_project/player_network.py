import networkx as nx
import gc
import math
from pyecharts import options as opts
from pyecharts.charts import Graph

# Define a new function to build up the network for a single player without using my previous code
# The size of nodes depends on the market value of the player
# The weight of the edges depends on the market value of the other player
def find_neighbors(G, player1, player2, limit = -1):
    """
    Build up the path for the two players, with a limit of the number of connecting nodes.
    If the connecting nodes are more than the limit, return the nodes of top highest market value.
    If there is no path between the two players, return the original graph.

    Parameters
    ----------
    G : nx.Graph
        The original graph
    player1 : str
        The name of the first player
    player2 : str
        The name of the second player
    limit : int
        The limit of the number of connecting nodes
    """
    if nx.has_path(G, player1, player2):
        connected_nodes = nx.node_connected_component(G, player1)
        if player2 in connected_nodes:
            subG = G.subgraph(connected_nodes).copy()
            neighbors1 = set(G.neighbors(player1))
            neighbors2 = set(G.neighbors(player2))
            overlapping = neighbors1.intersection(neighbors2)
            if limit > 0 and len(overlapping) > limit:
                sorted_neighbors = sorted(
                    overlapping,
                    key=lambda x: G.nodes[x].get("player_value", 0),
                    reverse=True,
                )
                overlapping = set(sorted_neighbors[:limit])
            subnodes = {player1, player2} | overlapping
            subG = G.subgraph(subnodes).copy()
            return subG, overlapping
    return G, set()

def build_network(player, df_players_relationship, relation="all", limit=-1):
    """
    Build up the network for the player(s) with the specified relation.
    If there is only one player, return the network for the player.
    If there is two players, return the connecting network for the two players.

    Parameters
    ----------
    player : str or list
        The name of the player(s)
    df_players_relationship : pd.DataFrame
        The dataframe of the player relationships
    relation : str
        The relation between the players (all, Same Country, Club Teammate). Default is "all".
    limit : int
        The limit of the number of connecting nodes. Default is no limit (-1)
    
    Returns
    -------
    G : nx.Graph
        The network of the player(s)
    """
    if type(player) == str:
        player = [player]
    # Filter the dataframe for the player
    df_player = df_players_relationship[
        (df_players_relationship["player1_name"].isin(player))
        | (df_players_relationship["player2_name"].isin(player))
    ]
    if relation != "all":
        df_player = df_player[df_player["relation"] == relation]

    G = nx.Graph()

    if len(player)==2:
        player1, player2 = player
        full_graph = nx.Graph()
        for player1_name, player2_name, rel, player1_val, player2_val in zip(
            df_player["player1_name"],
            df_player["player2_name"],
            df_player["relation"],
            df_player["player1_value"],
            df_player["player2_value"],
        ):
            full_graph.add_node(player1_name, player_value=player1_val)
            full_graph.add_node(player2_name, player_value=player2_val)
            full_graph.add_edge(player1_name, player2_name, relation=rel)

        subG, overlapping = find_neighbors(full_graph, player1, player2, limit)
        G.add_nodes_from(subG.nodes(data=True))
        G.add_edges_from(subG.edges(data=True))

        # Add or update attributes for overlapping nodes
        for node in G.nodes:
            G.nodes[node]["player_value"] = subG.nodes[node].get("player_value", 0)
            G.nodes[node]["overlap"] = node in overlapping
    else:
        # Build the graph for a single player
        for player1_name, player2_name, rel, player1_val, player2_val in zip(
            df_player["player1_name"],
            df_player["player2_name"],
            df_player["relation"],
            df_player["player1_value"],
            df_player["player2_value"],
        ):
            G.add_node(player1_name, player_value=player1_val)
            G.add_node(player2_name, player_value=player2_val)
            G.add_edge(player1_name, player2_name, relation=rel, weight=player2_val)

    return G

def illustrate_graph(G, players, title="Player Network"):
    """
    Visualize a NetworkX graph using Pyecharts with selected players on opposite sides.

    Parameters:
    - G (nx.Graph): The NetworkX graph to visualize.
    - selected_players (list): List of two players to position on opposite sides.
    - title (str): Title of the graph visualization.

    Returns:
    - Generates an interactive HTML file to visualize the graph.
    """

    player1, player2 = players

    # Extract nodes and edges
    nodes = []
    edges = []

    edge_color_map = {"Club Teammate": "green", "Same Country": "blue"}
    legend_entries = [{"name": "Club Teammate", "color": "green"}, {"name": "Same Country", "color": "blue"}]

    for u, v, data in G.edges(data=True):
        edge_entry = {
            'source': u,
            'target': v,
            'value': data.get('weight', 1),
            'tooltip': data.get('relation'),
            'lineStyle': {'color': edge_color_map[data.get('relation')]}
        }
        edges.append(edge_entry)
    
    # Manually position the selected players
    manual_positions = {
        player1: {"x": -300, "y": 0},  # Far-left
        player2: {"x": 300, "y": 0},   # Far-right
    }

    middle_nodes = [node for node in G.nodes if node not in players]

    # Spread connecting nodes across a grid in the middle
    # Circular layout for middle nodes
    middle_nodes = [node for node in G.nodes if node not in players]
    radius = 100  # Radius of the circle
    angle_step = 2 * math.pi / len(middle_nodes) if middle_nodes else 0

    for i, node in enumerate(middle_nodes):
        angle = i * angle_step
        x_pos = radius * math.cos(angle)  # Compute x using cosine
        # prevent the x_pos from being 0
        y_pos = radius * math.sin(angle)  # Compute y using sine
        if abs(y_pos) < 10:
            y_pos += 10 if y_pos>=0 else -10
        manual_positions[node] = {"x": x_pos, "y": y_pos}

    max_value = max((data.get("player_value", 0) for _, data in G.nodes(data=True)), default=1)
    min_value = min((data.get("player_value", 0) for _, data in G.nodes(data=True)), default=0)

    for node, data in G.nodes(data=True):
        # Determine node size
        raw_value = data.get("player_value", 0)
        scaled_size = (
            10 + (40 * (raw_value - min_value) / (max_value - min_value)) if max_value > min_value else 20
        )

        # Assign manual position
        pos = manual_positions.get(node, {"x": 0, "y": 0})  # Default position at center if not specified
        color = "red" if data.get("overlap") else "blue"  # Overlapping nodes are red
        node_entry = {
            "name": node,
            "value": raw_value,
            "symbolSize": scaled_size,
            "itemStyle": {"color": color},
            "x": pos["x"],  # Manually assign x position
            "y": pos["y"],  # Manually assign y position
        }
        nodes.append(node_entry)

     # Add dummy nodes for the legend
    legend_nodes = [
        {"name": entry["name"], "symbolSize": 20, "itemStyle": {"color": entry["color"]}, "x": 0, "y": 200 + i * 50}
        for i, entry in enumerate(legend_entries)
    ]

    # Add edges for the legend (dummy edges for display)
    legend_edges = [
        {"source": entry["name"], "target": entry["name"], "lineStyle": {"color": entry["color"]}}
        for entry in legend_entries
    ]

    # Combine legend and graph nodes/edges
    nodes += legend_nodes
    edges += legend_edges
    # Create the graph visualization
    graph = (
        Graph()
        .add(
            series_name="",
            nodes=nodes,
            links=edges,
            layout="none",  # Use manual layout
            label_opts=opts.LabelOpts(is_show=True, position="right"),  # Show labels
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            tooltip_opts=opts.TooltipOpts(formatter="{b}: €{c}"),
        )
    )

    # Render the graph to an HTML file
    output_file = "player_network.html"
    graph.render(output_file)
    print(f"Graph visualization saved to {output_file}")

def graph_player(player, relation="all", limit = -1):
    """
    Visualize the network of the players with the specified relation.

    Parameters
    ----------
    player : str or list
        The name of the player(s)
    relation : str
        The relation between the players (all, Same Country, Club Teammate). Default is "all".
    limit : int
        The limit of the number of connecting nodes. Default is no limit (-1)
    
    Returns
    -------
    None
    """
    G = build_network(player, relation, limit)
    illustrate_graph(G, player)
    gc.collect()