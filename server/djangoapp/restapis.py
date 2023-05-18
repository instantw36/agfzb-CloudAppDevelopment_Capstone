import requests
import json
# import related models here
from .models import CarDealer, DealerReview, CarMake, CarModel
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions
import time


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    api_key = kwargs.get("api_key",None)
    print("||||||", kwargs,api_key)
    print("==== GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
# def post_request(url, payload, **kwargs):
#     print(kwargs)
#     print("POST to {} ".format(url))
#     print(payload)
#     response = requests.post(url, params=kwargs, json=payload)
#     status_code = response.status_code
#     print("With status {} ".format(status_code))
#     json_data = json.loads(response.text)
#     return json_data

#     print(kwargs)
#     print("GET from {} ".format(url))
#     api_key = kwargs.get("apikey")
#     try:
#         # Call get method of requests library with URL and parameters
#         if api_key:
#             # Basic authentication GET
#             params = dict()
#             params["text"] = kwargs["text"]
#             params["version"] = kwargs["version"]
#             params["features"] = kwargs["features"]
#             params["return_analyzed_text"] = kwargs["return_analyzed_text"]
#             response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                                 auth=HTTPBasicAuth('apikey', api_key))
#         else:
#             # no authentication GET
#             response = requests.get(url, headers={'Content-Type': 'application/json'},
#                                     params=kwargs)
#     except:
#         # If any error occurs
#         print("Network exception occurred")

#     status_code = response.status_code
#     print("With status {} ".format(status_code))
#     json_data = json.loads(response.text)
#     return json_data
def post_request(url, payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(payload)
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    state = kwargs.get("state")
    if state:
        json_result = get_request(url, state=state)
    else:
        json_result = get_request(url)

    # print('json_result from line 31', json_result)    

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result#["body"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # print(dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                                    address=dealer_doc["address"], 
                                    city=dealer_doc["city"],
                                    id=dealer_doc["id"], 
                                   lat=dealer_doc["lat"], 
                                   long=dealer_doc["long"], 
                                   full_name=dealer_doc["full_name"],
                                   short_name=dealer_doc["short_name"], 
                                   st=dealer_doc["st"], 
                                   zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
    if json_result:
        # reviews = json_result["body"]["data"]["docs"]
        reviews = json_result["data"]["docs"]
        for review in reviews:
            review = reviews[0]
            review_obj = DealerReview(
                                    dealership = review["dealership"],
                                    name = review["name"],
                                    purchase = review["purchase"],
                                    review = review["review"])

            if "id" in review:
                review_obj.id = review["id"]
            if "purchase_date" in review:
                review_obj.purchase_date = review["purchase_date"]
            if "car_make" in review:
                review_obj.car_make = review["car_make"]
            if "car_model" in review:
                review_obj.car_model = review["car_model"]
            if "car_year" in review:
                review_obj.car_year = review["car_year"]
            
            sentiment = analyze_review_sentiments(review_obj.review)
            print(sentiment)
            review_obj.sentiment = sentiment
            # review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    
    return results
    

def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)
    print('json_result from line 54',json_result)

    if json_result:
        dealers = json_result[0]
        # print("line 70 restapis",json_result)
        dealer_doc = dealers
        print("0th address element line 73",dealers["address"])
        dealer_obj = CarDealer(address=dealers["address"], city=dealers["city"],
                                id=dealers["id"], lat=dealers["lat"], 
                                long=dealers["long"],
                                full_name=dealers["full_name"],
                                short_name=dealers["short_name"],
                                st=dealers["st"], zip=dealers["zip"],
                                )
    return dealer_obj    
 

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/6da4cad0-e5b5-4436-b58a-22048efd30ee" 
    api_key = "F53zu46jgarUWCq9W048aeTWAO3UjtFYpdGsf-kx-TpD"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(
                text=dealerreview+"hello hello hello",
                features=Features(sentiment=SentimentOptions(
                    targets=[dealerreview+"hello hello hello"]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    
    
    return(label)    


