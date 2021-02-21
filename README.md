# Instructions

## MySQL

Install and setup MySQL.

## Python

### Setup

Create isolated environment

```bash
py -m venv env
```

Activate isolated environment

```bash
.\env\Scripts\activate
```

Install required packages

```bash
pip install --upgrade google-cloud-bigquery
pip install mysql-connector-python
```

For BigQuery API to work, you need an active project in Google Cloud Platform and an `Service Account Key` setup as environment variable. See [Documentation](https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries) for help.

#### Running

You need to update both `init.py` and `index.py` to contain correct connection config for MySQL:

`index.py`:

```python
connection = connect(
      host="localhost",
      user='root', # Your username
      password="123456", # Your password
      database="tripdb" # Your DB name
    )
```

If you haven't created a database inside MySQL yet, run (script will create a DB named tripdb):

```bash
python .\init.py
```

Running the actual script (1000 rows):

```bash
python .\index.py 1000
```

If it's not working correctly try running with "verbose"-mode on:

```bash
python .\index.py 1000 v
```
