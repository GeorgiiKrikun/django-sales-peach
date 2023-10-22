# import openai
import httpx, requests
import core.settings as settings
# openai.organization = "org-Mos6UT6EjhlhAQjS4A2Gev4j"

TIMEOUT=20

async def get_suggestion_from_api_async(company_from_name, company_from_about, service, company_to_about, temperature = 0):
    request = {
        "company_from_name": company_from_name,
        "company_from_about": company_from_about,
        "service": service,
        "company_to_about": company_to_about,
        "temperature": temperature,
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(settings.OPEN_API_SERVICE+"suggestions/get", json=request, timeout=TIMEOUT) 
    return r.content.decode("utf-8")

def get_suggestion_from_api(company_from_name, company_from_about, service, company_to_about, temperature = 0):
    request = {
        "company_from_name": company_from_name,
        "company_from_about": company_from_about,
        "service": service,
        "company_to_about": company_to_about,
        "temperature": temperature,
    }
    r = requests.post(settings.OPEN_API_SERVICE+"suggestions/get", json=request, timeout=TIMEOUT) 
    # print(settings.OPEN_API_SERVICE)
    return r.content.decode("utf-8")