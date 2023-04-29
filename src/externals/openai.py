import openai
import os
from django.conf import settings

openai.organization = "org-Mos6UT6EjhlhAQjS4A2Gev4j"

def get_openai_query(company_from_name, company_from_about, company_to_about):
    my_description = "I work in company named " + str(company_from_name) + "." + " We do the following " + str(company_from_about) + "."
    my_description += "I want to sell our products to the company" 
    my_description += ", that has following about description on their webpage info: " + str(company_to_about)
    my_description += ". Write me a letter to the CEO of the company that will convince him to buy my product. Format it properly."
    return my_description

def get_openai_response(company_from_name, company_from_about, company_to_about, temperature = 0):
    if not settings.DEBUG:
        print("RELEASE MODE")
        response = openai.Completion.create(
            engine="davinci",
            prompt=get_openai_query(company_from_name, company_from_about, company_to_about),
            temperature=temperature,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0)

        return response['choices'][0]['text']
    
    print("DEBUG MODE")
    return "Sales letter from " + company_from_name + "|With following about: " + company_from_about + "|To the company with following about: " + company_to_about +". T= " + str(temperature)