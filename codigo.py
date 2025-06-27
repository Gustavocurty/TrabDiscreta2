import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

n = 20  
prob_spread = 0.4
initial_fire = [(n//2, n//2)] 

G = nx.grid_2d_graph(n, n)
status = {node: "green" for node in G.nodes()}
for node in initial_fire:
    status[node] = "burning"

color_map = {"green": "green", "burning": "red", "burnt": "black"}

def update_fire(status, G, prob_spread):
    new_status = status.copy()
    for node in G.nodes():
        if status[node] == "burning":
            new_status[node] = "burnt"
            for neighbor in G.neighbors(node):
                if status[neighbor] == "green" and random.random() < prob_spread:
                    new_status[neighbor] = "burning"
    return new_status

def simulate_fire(G, status, prob_spread, max_steps=100):
    results = []
    for step in range(max_steps):
        colors = [color_map[status[node]] for node in G.nodes()]
        results.append((step, dict(status)))
        
        plt.figure(figsize=(6, 6))
        nx.draw(G, pos={node: node for node in G.nodes()}, 
                node_color=colors, with_labels=False, node_size=30)
        plt.title(f"Etapa {step}")
        plt.axis('off')
        plt.show()

        if all(s != "burning" for s in status.values()):
            break
        status = update_fire(status, G, prob_spread)
    return results, status, step + 1  

fire_history, final_status, total_steps = simulate_fire(G, status, prob_spread)

total_burnt = sum(1 for s in final_status.values() if s == "burnt")

final_colors = [color_map[final_status[node]] for node in G.nodes()]
plt.figure(figsize=(8, 8))
nx.draw(G, pos={node: node for node in G.nodes()},
        node_color=final_colors, with_labels=False, node_size=30)

info_text = (f"Prob. de propagação: {prob_spread}\n"
             f"Total de nós queimados: {total_burnt}\n"
             f"Etapas até extinção: {total_steps}")

plt.title("Estado Final do Incêndio", fontsize=14)
plt.annotate(info_text, xy=(0.02, 0.95), xycoords='axes fraction',
             fontsize=10, ha='left', va='top',
             bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

plt.axis('off')
plt.tight_layout()
plt.savefig("estado_final_incendio.png", dpi=300)
plt.show()

