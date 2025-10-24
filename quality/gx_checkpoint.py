#### !!! Not working !!! ####

# import os
# import pandas as pd
# import great_expectations as ge
# from great_expectations.core.expectation_suite import ExpectationSuite
# from great_expectations.core.batch import RuntimeBatchRequest

# def ensure_datasource_and_asset(context, datasource_name: str, asset_name: str, df: pd.DataFrame):
#     try:
#         datasource = context.data_sources.get(name=datasource_name)
#     except Exception:
#         datasource = context.data_sources.add_pandas(name=datasource_name)
#     try:
#         _ = datasource.get_asset(asset_name)
#     except Exception:
#         datasource.add_dataframe_asset(name=asset_name)

# def ensure_suite(context, suite_name: str):
#     try:
#         _ = context.suites.get(name=suite_name)
#     except Exception:
#         context.suites.add(ExpectationSuite(name=suite_name))

# def validate_nodes(nodes_path: str, context) -> bool:
#     print(f"Loading nodes from {nodes_path}")
#     df = pd.read_parquet(nodes_path)

#     datasource_name = "pandas_ds"
#     asset_name = "nodes_asset"
#     suite_name = "nodes_suite"

#     ensure_datasource_and_asset(context, datasource_name, asset_name, df)
#     ensure_suite(context, suite_name)

#     batch_request = RuntimeBatchRequest(
#         datasource_name=datasource_name,
#         data_connector_name="default_runtime_data_connector_name",
#         data_asset_name=asset_name,
#         runtime_parameters={"batch_data": df},
#         batch_identifiers={"default_identifier_name": "nodes_batch"},
#     )

#     validator = context.get_validator(
#         batch_request=batch_request,
#         expectation_suite_name=suite_name
#     )

#     validator.expect_column_values_to_be_unique(column="id")
#     validator.expect_column_values_to_not_be_null(column="name")

#     result = validator.validate()
#     print(f"Nodes validation success: {result.success}")
#     return result.success

# def validate_edges(edges_path: str, context) -> bool:
#     print(f"Loading edges from {edges_path}")
#     df = pd.read_parquet(edges_path)

#     datasource_name = "pandas_ds"
#     asset_name = "edges_asset"
#     suite_name = "edges_suite"

#     ensure_datasource_and_asset(context, datasource_name, asset_name, df)
#     ensure_suite(context, suite_name)

#     batch_request = RuntimeBatchRequest(
#         datasource_name=datasource_name,
#         data_connector_name="default_runtime_data_connector_name",
#         data_asset_name=asset_name,
#         runtime_parameters={"batch_data": df},
#         batch_identifiers={"default_identifier_name": "edges_batch"},
#     )

#     validator = context.get_validator(
#         batch_request=batch_request,
#         expectation_suite_name=suite_name
#     )

#     validator.expect_column_values_to_not_be_null(column="src")
#     validator.expect_column_values_to_not_be_null(column="dst")

#     result = validator.validate()
#     print(f"Edges validation success: {result.success}")
#     return result.success

# def main():
#     context = ge.get_context()
#     nodes_file = os.path.join("data", "bronze", "nodes.parquet")
#     edges_file = os.path.join("data", "bronze", "edges.parquet")

#     ok_nodes = validate_nodes(nodes_file, context)
#     ok_edges = validate_edges(edges_file, context)

#     if not (ok_nodes and ok_edges):
#         print("❗ Validation failed — exiting with error.")
#         exit(1)

#     print("✔ All validations passed — ready to proceed.")

# if __name__ == "__main__":
#     main()
