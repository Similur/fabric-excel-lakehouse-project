# Excel to Delta Lakehouse in Microsoft Fabric

I built this demo to work through a common reporting problem: recurring Excel files with overlapping records. It loads those files into a Microsoft Fabric Lakehouse, keeps the latest update for each record ID, and merges the results into a Delta table. Rerunning the pipeline leaves one row per ID in Silver.

This is an independent portfolio and testing project. The report data and business rules are fictional. The repository contains no employer-owned code, private datasets, API keys, or connections to company systems, and it requires no company credentials.

## What's included

- Two sample Excel reports, one month-to-date and one year-to-date, that share some record IDs.
- A Bronze notebook that loads the rows and records each source filename and ingestion time.
- A Silver notebook that checks required columns, converts data types, selects the latest update per record, and upserts it into Delta.
- A validation notebook that checks duplicate and blank IDs, invalid amounts, and record counts.
- Python unit tests for timestamp parsing and overlapping records.

Each notebook needs a Microsoft Fabric Lakehouse attached as its default lakehouse. Input files go under `/lakehouse/default/Files/...`; the notebooks write to managed Delta tables.

## Project layout

```text
notebooks/
  01_bronze_ingestion.ipynb
  02_silver_transform.ipynb
  03_validate.ipynb
sample_data/
  january_mtd.xlsx
  january_ytd.xlsx
src/fabric_excel_demo/
  transform.py
tests/
  test_transform.py
```

## Run it in Fabric

1. Create a Fabric workspace and a Lakehouse, then attach that Lakehouse to each notebook.
2. Upload both `.xlsx` files from `sample_data/` to the Lakehouse Files/sample_reports/ folder.
3. Import the notebooks into the workspace and run them in order: 01, 02, then 03.
4. Inspect the managed tables `demo_bronze_activity` and `demo_silver_activity` in the Lakehouse.
5. Run the notebooks again. The Silver table should still have one row per record ID.

Bronze is an append-only ingestion log. Every run of notebook 01 adds another copy of the source rows. Notebook 02 deduplicates the full Bronze history before merging into Silver. For production use, I'd track which files have already been ingested to avoid loading them again.

The notebooks read Excel files with `pandas.read_excel`. If `openpyxl` isn't available in your Fabric environment, attach an Environment that includes it. Running the notebooks locally would also require a Spark/Delta session and access to the Fabric Lakehouse paths.

## Run the unit tests locally

The transformation tests require Python 3.10 or newer:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

## Scope and limitations

The sample data is small, and each record has a last-updated timestamp to decide which version to keep. A production pipeline would need to account for late-arriving records, deletes, schema changes, and conflicting source updates. I'd also add ingestion audit tables, monitoring, and a way to rerun Bronze loads without appending duplicates.

The Silver `MERGE` updates matching rows and inserts new ones. It doesn't implement a full change-data-capture process. See [project notes](docs/PROJECT_NOTES.md) for possible next steps.
