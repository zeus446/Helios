import httpx
import os

JSEARCH_BASE_URL = "https://jsearch.p.rapidapi.com/search"

API_KEY = os.getenv("JSEARCH_API_KEY","")

async def search_jobs(query:str,location:str,remote_only:bool,employment_type:str):

    if location:
        full_query = f"{query} in {location}"

    else:
        full_query = query


    param = {
        "q":full_query,
        "page":"1",
        "num_pages":"1"
    }

    if remote_only:
        param["remote_jobs_only"] = "true"


    if employment_type:
        param["employments_types"] = employment_type.upper()


    header = {
        "x-rapidapi-key":API_KEY,
        "x-rapidapi-host":"jsearch.p.rapidapi.com"
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await  client.get(JSEARCH_BASE_URL,headers=header,params=param)

            if response.status_code ==200:
                return response.json().get("data", [])
            return[]

        except (httpx.HTTPError,Exception):
            return []


