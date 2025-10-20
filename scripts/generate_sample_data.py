import csv
import random
import argparse
import os

def gen_nodes(nodes_file: str, num_nodes: int, types: list):
    with open(nodes_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'label', 'name'])
        for i in range(num_nodes):
            label = types[i % len(types)]
            name = f"name_{i}"
            writer.writerow([i, label, name])
            if i and i % 1_000_000 == 0:
                print(f"  → {i} nodes generated")

def gen_edges(edges_file: str, num_edges: int, num_nodes: int, edge_type: str = 'REL'):
    with open(edges_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['src', 'dst', 'type'])
        for j in range(num_edges):
            src = random.randrange(0, num_nodes)
            dst = random.randrange(0, num_nodes)
            if src == dst:
                dst = (dst + 1) % num_nodes
            writer.writerow([src, dst, edge_type])
            if j and j % 1_000_000 == 0:
                print(f"  → {j} edges generated")

def main():
    parser = argparse.ArgumentParser(description="Génère des fichiers sample nodes & edges pour KG import")
    parser.add_argument('--num_nodes', type=int, default=1_000_000,
                        help="Nombre de nœuds à générer (défaut 1 000 000)")
    parser.add_argument('--num_edges', type=int, default=5_000_000,
                        help="Nombre de relations à générer (défaut 5 000 000)")
    parser.add_argument('--out_dir', type=str, default='data/raw',
                        help="Répertoire de sortie pour nodes.csv et edges.csv")
    args = parser.parse_args()

    types = ['Person', 'Org', 'Paper']

    os.makedirs(args.out_dir, exist_ok=True)
    nodes_file = os.path.join(args.out_dir, 'nodes.csv')
    edges_file = os.path.join(args.out_dir, 'edges.csv')

    print(f"Generating {args.num_nodes} nodes into {nodes_file} …")
    gen_nodes(nodes_file, args.num_nodes, types)
    print("Nodes generation completed.")

    print(f"Generating {args.num_edges} edges into {edges_file} …")
    gen_edges(edges_file, args.num_edges, args.num_nodes)
    print("Edges generation completed.")

if __name__ == '__main__':
    main()
