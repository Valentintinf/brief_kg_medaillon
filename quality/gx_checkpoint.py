#!/usr/bin/env python3
from lib2to3.fixes.fix_input import context
import os
import pandas as pd
import great_expectations as gx
from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.exceptions import DataContextError

def validate_with_manual_suite(df: pd.DataFrame, checks: list, suite_name: str, context) -> bool:
    # 1. Créer explicitement la suite
    try:
        suite = ExpectationSuite(name=suite_name)
        context.suites.add(expectation_suite=suite)
        print(f"✔ Created ExpectationSuite '{suite_name}'")
    except Exception as e:
        print(f"⚠️ Warning creating suite '{suite_name}': {e}")

    # 2. Construire un batch request
    batch_request = RuntimeBatchRequest(
        datasource_name="runtime_datasource",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name=suite_name + "_asset",
        runtime_parameters={"batch_data": df},
        batch_identifiers={"run_id": suite_name}
    )

    # 3. Obtenir un validator pour cette suite
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=suite_name,
        create_expectation_suite=False
    )

    # 4. Appliquer les vérifications
    for check in checks:
        col = check["column"]
        if check.get("not_null", False):
            validator.expect_column_values_to_not_be_null(column=col)
        if check.get("unique", False):
            validator.expect_column_values_to_be_unique(column=col)
        if "value_set" in check:
            validator.expect_column_values_to_be_in_set(column=col, value_set=check["value_set"])

    # 5. Valider
    result = validator.validate(run_name="run_"+suite_name)
    print(f"✔ Suite '{suite_name}' validation result: {result['success']}")
    return result["success"]

def main():
    context = gx.get_context()
    nodes_file = os.path.join('data', 'bronze', 'nodes.parquet')
    edges_file = os.path.join('data', 'bronze', 'edges.parquet')

    df_nodes = pd.read_parquet(nodes_file)
    df_edges = pd.read_parquet(edges_file)

    nodes_checks = [
        {"column": "id", "unique": True, "not_null": True}
    ]
    edges_checks = [
        {"column": "src", "not_null": True},
        {"column": "dst", "not_null": True},
        {"column": "type", "not_null": True, "value_set": ["REL"]}
    ]

    ok_nodes = validate_with_manual_suite(df_nodes, nodes_checks, "nodes_suite", context)
    ok_edges = validate_with_manual_suite(df_edges, edges_checks, "edges_suite", context)

    if ok_nodes and ok_edges:
        print("✅ All checks passed with manual suite.")
        exit(0)
    else:
        print("❌ Some checks failed with manual suite.")
        exit(1)

if __name__ == "__main__":
    main()
