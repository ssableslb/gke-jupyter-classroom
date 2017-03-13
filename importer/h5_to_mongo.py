"""This script import performance results from the legacy postgresql database to a mongodb instance"""

import pymongo
import pandas as pd

df = pd.read_hdf("performances.h5", "performances")

# cleanup data
# TODO: Check those components can be removed
for component in ["Variability", "Checkout", "ChangesetComplete", "Benchmark1Tests",
                  "", "PopulateMediumRepository", "misc", "PopulateRepository", "ComponentTest"]:

    df = df[df['component'] != component]

df.loc[df['component'] == "Ocean.OceanTest", 'component'] = "Ocean"
df.loc[df['component'] == "Ocean.Core", 'component'] = "Ocean"

df.loc[df['component'] == "Studio daily perf", 'component'] = "Studio"
df.loc[df['component'] == "STUDIO", 'component'] = "Studio"

df.loc[df['component'] == "Studio daily perf", 'component'] = "Studio"

df.loc[df['component'] == "WE.OceanTest", 'component'] = "Workflow Engine"

# Get most recent result for each component
print(df.ix[df.groupby('component').benchstep_result_date.idxmax(),["component", "benchstep_result_date", "version"]])

# Save to mongodb
client = pymongo.MongoClient()
db = client.performance_dashboard
coll = db.benchmark_results

# Warning: this will remove everything in the collection
db.benchmark_results.drop()

db.benchmark_results.create_index([("component", pymongo.ASCENDING)])

db.benchmark_results.create_index([("component", pymongo.ASCENDING),
                                   ("version", pymongo.ASCENDING)])

db.benchmark_results.create_index([("component", pymongo.ASCENDING),
                                   ("version", pymongo.ASCENDING),
                                   ("benchmark_name", pymongo.ASCENDING)
                                   ])

for row in df.to_dict('records'): # df[-100000:]
    row = {k: v for k, v in row.items() if v != "None" and k != "id" and v != ''}
    # print(row)
    result = db.benchmark_results.insert_one(row)

cursor = db.benchmark_results.find()
print(cursor.count())

cursor = db.benchmark_results.find({"component": "Ocean"})
print(cursor.count())
