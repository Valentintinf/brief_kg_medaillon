from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 0,
}

with DAG(
    dag_id='ingest_kg',
    default_args=default_args,
    start_date=datetime(2025,10,24),
    schedule_interval=None,  # ou '@daily' selon besoin
    catchup=False,
) as dag:

    seed = BashOperator(
        task_id='seed',
        bash_command=(
            'python3 scripts/generate_sample_data.py '
            '--out data/raw --nodes 1000000 --edges 5000000'
        )
    )

    bronze = BashOperator(
        task_id='bronze',
        bash_command=(
            'python3 scripts/to_parquet.py '
            '--in data/raw --out data/bronze'
        )
    )

    checkpoint = BashOperator(
        task_id='checkpoint',
        bash_command=(
            'python3 scripts/pandas_checkpoint.py '
            '--input data/bronze/edges.parquet'
        )
    )

    silver = BashOperator(
        task_id='silver',
        bash_command=(
            'python3 scripts/partition_edges.py '
            '--in data/bronze --out data/silver --partitions 8'
        )
    )

    gold = BashOperator(
        task_id='gold',
        bash_command=(
            'bash scripts/neo4j_bulk_import.sh'
        )
    )

    seed >> bronze >> checkpoint >> silver >> gold
