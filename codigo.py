import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from scipy.integrate import odeint

n = 20
prob_spread = 0.58 # prob 58%
initial_fire = [(n//2, n//2)]

G = nx.grid_2d_graph(n, n)
status = {node: "green" for node in G.nodes()}
for node in initial_fire:
    status[node] = "burning"

color_map = {
    "green": "#2ecc71",    
    "burning": "#e74c3c",  
    "burnt": "#2c3e50"     
}


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
    burnt_fraction = [] 
    for step in range(max_steps):
        num_burnt = sum(1 for s in status.values() if s == "burnt")
        burnt_fraction.append(num_burnt / len(G.nodes()))
        
        colors = [color_map[status[node]] for node in G.nodes()]
        plt.figure(figsize=(6, 6))
        nx.draw(G, pos={node: node for node in G.nodes()},
                node_color=colors, with_labels=False, node_size=30)
        plt.title(f"Etapa {step}")
        plt.axis('off')
        plt.show()

        if all(s != "burning" for s in status.values()):
            break
        status = update_fire(status, G, prob_spread)
    return burnt_fraction, status, step + 1

burnt_fraction_discrete, final_status, total_steps = simulate_fire(G, status, prob_spread)

def logistic_fire(B, t, r):
    return r * B * (1 - B)

r = 0.56 
B0 = 1 / (n * n)  
t = np.linspace(0, total_steps, total_steps * 10)  

B_t = odeint(logistic_fire, B0, t, args=(r,)).flatten()

plt.figure(figsize=(8, 5))
plt.plot(np.arange(len(burnt_fraction_discrete)), burnt_fraction_discrete, 'o-', label='Simulação em Rede')
plt.plot(t, B_t, '-', label='Modelo Diferencial (Logístico)')
plt.xlabel("Tempo (etapas)")
plt.ylabel("Proporção de área queimada")
plt.title("Comparação: Simulação vs. Modelo Diferencial")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

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