from io import BytesIO 
import requests 
import zipfile 

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


