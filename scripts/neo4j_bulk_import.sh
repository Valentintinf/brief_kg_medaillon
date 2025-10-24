#!/usr/bin/env bash
set -euo pipefail

SILVER_DIR="./data/silver"
GOLD_DIR="./data/gold"
NODES_PARQUET="${SILVER_DIR}/nodes.parquet"
EDGES_GLOB="${SILVER_DIR}/shard=*/edges.parquet"
CSV_NODES="${GOLD_DIR}/nodes.csv"
CSV_EDGES="${GOLD_DIR}/edges.csv"
DB_NAME="neo4j"
IMPORT_DIR="${GOLD_DIR}/import"

mkdir -p "${IMPORT_DIR}"

echo "=== Converting Parquet to CSV for Neo4j bulk import ==="

# Export variables pour Python
export NODES_PARQUET
export CSV_NODES
export EDGES_GLOB
export CSV_EDGES

python3 - << 'PYCODE'
import os
import pandas as pd
import glob

# Nodes
parquet_path = os.environ["NODES_PARQUET"]
csv_path     = os.environ["CSV_NODES"]
df_nodes = pd.read_parquet(parquet_path)
df_nodes = df_nodes.rename(columns={"id": "id:ID", "name": "name", "label": "label"})
df_nodes.to_csv(csv_path, index=False)
print(f"Wrote {len(df_nodes)} nodes to {csv_path}")

# Edges
pattern     = os.environ["EDGES_GLOB"]
csv_path_e  = os.environ["CSV_EDGES"]
files       = glob.glob(pattern, recursive=True)
df_list     = []
for f in files:
    df_list.append(pd.read_parquet(f))
df_edges = pd.concat(df_list, ignore_index=True)
df_edges = df_edges.rename(columns={"src": ":START_ID", "dst": ":END_ID", "type": "type"})
df_edges.to_csv(csv_path_e, index=False)
print(f"Wrote {len(df_edges)} edges from {len(files)} shards to {csv_path_e}")
PYCODE

echo "=== Running Neo4j bulk import ==="
neo4j-admin database import full \
  --nodes="${CSV_NODES}" \
  --relationships="${CSV_EDGES}" \
  --database="${DB_NAME}"

echo "=== Import finished. Verify database ==="
