from io import BytesIO 
import pandas as pd 
import requests 
import sqlite3
import zipfile 


pd.set_option("display.max_columns", None)
# Don't truncate text inside individual cell values
pd.set_option("display.max_colwidth", None)
# Prevents wide tables from wrapping onto a new line below
pd.set_option("display.width", None)

# Download GTFS data 
def download_gtfs(operator='nmbssncb'): 
    url = f"https://api-management-opendata-production.azure-api.net/api/gtfs/feed/{operator}/static/"

    headers = {
        "bmc-partner-key": "65c9bb975a44491989b15034635f8d76",
        # Tells the server not to give stale cached data
        "Cache-Control": "no-cache",
    }
    response = requests.get(url, headers=headers) 

    if response.status_code == 200: 
        return zipfile.ZipFile(BytesIO(response.content)) 
    else: 
        raise Exception(f"Failed to download: {response.status_code}") 
    
# Extract and read stops 
gtfs_zip = download_gtfs()
for document in gtfs_zip.namelist():
    doc_df = pd.read_csv(gtfs_zip.open(document))
    print("_" * 50)
    print(document, ":\n")
    print(doc_df.info(), "\n")
    print(doc_df.head(), "\n")
