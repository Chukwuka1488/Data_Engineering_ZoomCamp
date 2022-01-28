#!/usr/bin/env python
# coding: utf-8
# import wget
import os
from time import time
from sqlalchemy import create_engine
import pandas as pd
import argparse


def main(params):
    username = params.username
    password = params.password
    host = params.host
    port = params.port
    db_name = params.db_name
    table_name = params.table_name
    url = params.url
    csv_name = "output.csv"

    # download the csv file
    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{db_name}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        t_start = time()

        df = next(df_iter)

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists='append')

        t_end = time()

        print("inserted another chunk of data..., took %.3f seconds" % (t_end - t_start))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest csv Data to postgresql.')

    # user, pass, host, port, db name, table name
    # url of the csv file

    parser.add_argument('--username', help='user name for the postgres')
    parser.add_argument('--password', help='password for the postgres')
    parser.add_argument('--host', help='host for the postgres')
    parser.add_argument('--port', help='port for the postgres')
    parser.add_argument('--db_name', help='database name for the postgres')
    parser.add_argument('--table_name', help='table name for the postgres')
    parser.add_argument('--url', help='url for the csv file')

    args = parser.parse_args()

    main(args)
