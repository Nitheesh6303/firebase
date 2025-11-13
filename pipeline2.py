import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import firestore

db = firestore.Client()

class ReadCities(beam.DoFn):
    def setup(self):
        # This runs once per worker — safe place to make the client
        self.db = firestore.Client()
    def process(self,element):
        docs=self.db.collection("cities").stream()
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            yield data
def is_usa_city(city):
    if city.get("country") == "USA":
        print("✅ USA city:", city["name"])
        return True
    return False
            

options = PipelineOptions(
    project="thinkschool-6303",
    region="us-central1",
    temp_location="gs://your-temp-bucket/temp",
    runner="DirectRunner"  # or "DataflowRunner"
)

with beam.Pipeline(options=options) as P:
    (
        P
        |"start" >> beam.Create([None])
        |"Read Firestore" >> beam.ParDo(ReadCities())
        | "Filter USA" >> beam.Filter(is_usa_city)
    )