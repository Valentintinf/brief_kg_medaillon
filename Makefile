seed:
	python3 scripts/generate_sample_data.py --out data/raw --nodes 1000000 --edges 5000000
bronze:
	python3 scripts/to_parquet.py --in data/raw --out data/bronze
silver:
	python3 scripts/partition_edges.py --in data/bronze --out data/silver --partitions 8
import:
	bash scripts/neo4j_bulk_import.sh
up:
	docker compose up -d
down:
	docker compose down -v
e2e: 
	seed bronze silver import