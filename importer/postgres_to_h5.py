from sqlalchemy import create_engine, column, Integer, String
from sqlalchemy.orm import create_session

import pandas.io.sql as psql
import schema

import configparser
config = configparser.ConfigParser()
config.read('importer.ini')
username = config['Authentification']['username']
password = config['Authentification']['password']

engine = create_engine('postgresql://{}:{}@fr0235lin06.grabels-fr0235.slb.com:5432/benchmark'.format(username, password))
session = create_session(bind=engine)

q = session.query(schema.t_benchstep_result.c.benchstep_result_date,
                  schema.t_benchstep_result.c.value,
                  schema.Benchstep.benchstep_name,
                  schema.Benchmark,
                  schema.Version.version,
                  schema.Revision.revision
                  ).join(schema.Benchstep
                         ).join(schema.Benchmark
                                ).join(schema.t_bench_run
                                       ).join(schema.Revision
                                              ).join(schema.Version
                                                     )
print (q.count())

dataframe = psql.read_sql(q.statement, q.session.bind)
print(dataframe.info())

dataframe.to_hdf("performances.h5", "performances", mode="w")