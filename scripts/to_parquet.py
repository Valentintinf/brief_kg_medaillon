import os
import argparse
import pandas as pd

def convert_file(csv_path: str, parquet_path: str, compression: str = 'snappy'):
    print(f"Converting {csv_path} → {parquet_path} (compression={compression})")
    df = pd.read_csv(csv_path)
    df.to_parquet(parquet_path, compression=compression, index=False)
    print(f"Written {parquet_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert raw CSVs to Parquet (bronze layer)")
    parser.add_argument('--in_dir', type=str, default='data/raw', help="Directory for raw CSVs")
    parser.add_argument('--out_dir', type=str, default='data/bronze', help="Directory for Parquet output")
    parser.add_argument('--compression', type=str, default='snappy', help="Parquet compression codec")
    args = parser.parse_args()
    
    os.makedirs(args.out_dir, exist_ok=True)
    
    # define expected csv filenames
    nodes_csv = os.path.join(args.in_dir, 'nodes.csv')
    edges_csv = os.path.join(args.in_dir, 'edges.csv')
    
    nodes_parquet = os.path.join(args.out_dir, 'nodes.parquet')
    edges_parquet = os.path.join(args.out_dir, 'edges.parquet')
    
    convert_file(nodes_csv, nodes_parquet, args.compression)
    convert_file(edges_csv, edges_parquet, args.compression)
    
    print("Conversion to Parquet done.")

if __name__ == '__main__':
    main()
