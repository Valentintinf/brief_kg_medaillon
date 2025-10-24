#!/usr/bin/env python3
import os
import pandas as pd
import sys

def check_nodes(nodes_path: str) -> bool:
    print(f"Checking nodes file: {nodes_path}")
    df = pd.read_parquet(nodes_path)
    n = len(df)
    n_unique = df['id'].nunique(dropna=False)
    print(f" → Total rows: {n}, Unique id: {n_unique}")
    if n_unique != n:
        print("❌ ERROR: There are duplicate ids in nodes.")
        return False
    null_ids = df['id'].isnull().sum()
    print(f" → Null values in id: {null_ids}")
    if null_ids > 0:
        print("❌ ERROR: There are null ids in nodes.")
        return False
    print("✔ Nodes check passed.")
    return True

def check_edges(edges_path: str) -> bool:
    print(f"Checking edges file: {edges_path}")
    df = pd.read_parquet(edges_path)
    null_src = df['src'].isnull().sum()
    null_dst = df['dst'].isnull().sum()
    print(f" → Null values in src: {null_src}")
    print(f" → Null values in dst: {null_dst}")
    if null_src > 0 or null_dst > 0:
        print("❌ ERROR: There are nulls in src or dst in edges.")
        return False
    # Check type domain
    unique_types = df['type'].unique()
    print(f" → Unique types in edges: {unique_types}")
    invalid_type = df[~df['type'].isin(['REL'])]
    if len(invalid_type) > 0:
        print(f"❌ ERROR: Found {len(invalid_type)} edges with type not 'REL'.")
        return False
    print("✔ Edges check passed.")
    return True

def main():
    nodes_file = os.path.join('data', 'bronze', 'nodes.parquet')
    edges_file = os.path.join('data', 'bronze', 'edges.parquet')

    ok1 = check_nodes(nodes_file)
    ok2 = check_edges(edges_file)

    if ok1 and ok2:
        print("✅ All pandas quality checks passed.")
        sys.exit(0)
    else:
        print("❌ Some pandas quality checks failed.")
        sys.exit(1)

if __name__ == '__main__':
    main()
