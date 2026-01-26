#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click


def download_file(url: str, filename: str):
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Downloaded {filename}")


def ingest_dataframe(df: pd.DataFrame, engine, table_name: str, chunk_size: int):
    df.head(0).to_sql(
        name=table_name,
        con=engine,
        if_exists="replace"
    )
    print(f"{table_name} schema created")

    for start in tqdm(range(0, len(df), chunk_size)):
        end = start + chunk_size
        chunk = df.iloc[start:end]
        chunk.to_sql(
            name=table_name,
            con=engine,
            if_exists="append"
        )
        print("Inserted chunk:", len(chunk))


@click.command()
@click.option('--pg-user', default='postgres', help='Postgres username')
@click.option('--pg-pass', default='postgres', help='Postgres password')
@click.option('--pg-host', default='localhost', help='Postgres host')
@click.option('--pg-port', default='5433', help='Postgres port')
@click.option('--pg-db', default='ny_taxi', help='Postgres database name')
@click.option('--green-parquet', default='green_tripdata_2025-11.parquet', help='Green taxi parquet filename')
@click.option('--zones-csv', default='taxi_zone_lookup.csv', help='Zones CSV filename')
@click.option('--chunk-green', default=10000, help='Chunk size for green taxi')
@click.option('--chunk-zones', default=5000, help='Chunk size for zones')
def main(pg_user, pg_pass, pg_host, pg_port, pg_db,
         green_parquet, zones_csv, chunk_green, chunk_zones):

    # Download files
    download_file(
        "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet",
        green_parquet
    )

    download_file(
        "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv",
        zones_csv
    )

    # Read data
    green_df = pd.read_parquet(green_parquet, engine="pyarrow")
    zones_df = pd.read_csv(zones_csv)

    # Create engine
    engine = create_engine(
        f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
    )

    # Ingest green taxi
    ingest_dataframe(green_df, engine, "green_taxi_data", chunk_green)

    # Ingest zones
    ingest_dataframe(zones_df, engine, "taxi_zone_lookup", chunk_zones)


if __name__ == "__main__":
    main()
