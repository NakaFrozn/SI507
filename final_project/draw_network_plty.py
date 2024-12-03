import plotly.graph_objects as go
import numpy as np
# Create a network graph with NetworkX
def draw_graph(G, pos):
    # use plotly to draw the graph
    node_x, node_y, node_size, node_text = [], [], [], []
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    for node in G.nodes(data=True):
        x, y = pos[node[0]]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node[0])
        player_value = node[1].get("player_value", 0)
        if player_value is None or np.isnan(player_value):
            player_value = 0
        node_size.append(player_value / 1000000)
    
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        marker=dict(
            size=node_size,
            color='blue',
            line=dict(color='black', width=2)
        )
    )

    fig = go.Figure(data =[edge_trace, node_trace])
    fig.update_layout(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    fig.write_html("./output/plotly_figure.html")
    fig.show()
