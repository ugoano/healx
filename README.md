# Ugo

## Set up

### Install dependencies 
(wanted to dockerize, but time)

```
python3 -m venv .healx_env
source .healx_env/bin/activate
pip install -r requirements.txt
```

### Start up Elasticsearch

```
docker-compose up -d
```

## Add downloaded metadata

```
python indexer.py metadata.csv
```

## Run server

Ensure you are in the virtual env

```
./start_server.sh
```

## Testing

This uses pytest, you can optionally add `--pdb` for debugging

This creates and destroys a `test-index` to ingest test data into.

```
pytest 
```
