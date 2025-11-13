import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import firestore

# 1️⃣ Read all students and print names

class ReadStudents(beam.DoFn):
    def setup(self):
        self.db=firestore.Client()
    """def process(self,element):
        docs=self.db.collection("students").stream()
        for doc in docs:
            data=doc.to_dict()
            data["id"]=doc.id
            yield data"""
    '''def process(self,element):
        docs=self.db.collection("books").stream()
        for doc in docs:
            data=doc.to_dict()
            data["id"]=doc.id
            yield data'''
    def process(self,element):
        docs=self.db.collection("cities").stream()
        for doc in docs:
            data=doc.to_dict()
            data["id"]=doc.id
            yield data
 #2️⃣ Filter only students who have scored above 90

def is_above_90(student):
    if student.get("grade")>90:
        print(student["name"])

#3️⃣ Filter books published after 2020

def filter_books(book):
    if book.get("published_year")>2000:
        print(book["title"])

options=PipelineOptions(
    project="thinkschool-6303",
    runner="DirectRunner"
)

with beam.Pipeline(options=options) as P:
    (
        P
        |"start" >> beam.Create([None])
        |"read the docs">>beam.ParDo(ReadStudents())
        #|"Printing the file">>beam.Map(lambda s: print(s["name"]))
        #| "printing the names">>beam.Filter(is_above_90)
        #|"printing the books">> beam.Filter(filter_books)
        |"printing the cities">>beam.Filter(lambda c: c.get("country")=="USA") 
        |"Printing">>beam.Map(lambda c: print(c["name"]))
    )
    


