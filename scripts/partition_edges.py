#!/usr/bin/env python3
import os
import pandas as pd

def partition_edges(edges_path: str, output_dir: str, num_shards: int = 8) -> None:
    print(f"Loading edges from {edges_path}")
    df = pd.read_csv(edges_path)
    # Assurez-vous que les colonnes s’appellent bien ‘src’, ‘dst’, ‘type’
    # Ajout d’une colonne shard via modulo
    df['shard'] = df['src'].astype(int) % num_shards

    for shard_id in range(num_shards):
        shard_dir = os.path.join(output_dir, f"shard={shard_id}")
        os.makedirs(shard_dir, exist_ok=True)
        shard_df = df[df['shard'] == shard_id].copy()
        # on peut supprimer la colonne shard si on veut
        shard_df = shard_df.drop(columns=['shard'])
        out_path = os.path.join(shard_dir, "edges.parquet")
        print(f"Writing shard {shard_id} with {len(shard_df)} records to {out_path}")
        shard_df.to_parquet(out_path, index=False)

def copy_nodes(nodes_src: str, nodes_dst: str) -> None:
    print(f"Copying nodes file from {nodes_src} to {nodes_dst}")
    os.makedirs(os.path.dirname(nodes_dst), exist_ok=True)
    # utilisation de pandas pour la copie
    df = pd.read_parquet(nodes_src)
    df.to_parquet(nodes_dst, index=False)

def main():
    raw_edges = os.path.join("data", "raw", "edges.csv")
    raw_nodes = os.path.join("data", "raw", "nodes.csv")
    bronze_nodes = os.path.join("data", "bronze", "nodes.parquet")
    silver_dir = os.path.join("data", "silver")

    # Partition edges
    partition_edges(raw_edges, silver_dir, num_shards=8)

    # Copy nodes (vous pouvez préférer depuis bronze plutôt que raw)
    copy_nodes(bronze_nodes, os.path.join(silver_dir, "nodes.parquet"))

if __name__ == "__main__":
    main()
