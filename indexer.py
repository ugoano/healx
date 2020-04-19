import csv
import re
import argparse

from elasticsearch_dsl.exceptions import ValidationException

from models import Paper


def ingest_csv(csv_file_name, index_name):
    with open(csv_file_name, "r") as csv_file:
        reader = csv.reader(csv_file)
        headers = next(reader)
        # Normalize header titles to become valid attribute names
        headers = [(re.sub(r'\W+', '', h.strip().replace(' ', '_'))).lower() for h in headers]
        for row in reader:
            paper = Paper(meta={'id': row[0], 'index': index_name})
            for ind, header in enumerate(headers):
                setattr(paper, header, row[ind])
            try:
                paper.save(refresh=True)
                paper._index.refresh()
            except ValidationException as e:
                # There are a few blank publish_time values. Didn't find time to make optional
                print(f"Unable to save record with id {row[0]}")
                print(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pass the csv file to upload")
    parser.add_argument(dest="file_name")
    args = parser.parse_args()
    ingest_csv(args.file_name, "paper-index")
