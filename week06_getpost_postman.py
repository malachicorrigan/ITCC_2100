#Author: Malachi Corrigan
#Date: 02/18/2023

#Scope:
#Define 3 functions

#Import requests module
import requests

#Define http get, return nothing
#Using JSONPlaceholder
def invoke_http_get(url:str) -> None:
    
    #create response which is get request of the url
    response = requests.get(url)
    
    #If http response is not 'ok' per code then raise ValueError that it has failed
    if not response.ok:
        #raise an exception with critical error warning
        raise ValueError('Critical Error: API Call Failure')
    
    #Takes object and returns JSON object of it
    obj = response.json()
    
    #Is obj a list? If so, do the following
    if isinstance(obj, list):
        #For each resource in the list of resources, do the following
        for res in obj:
            #For each, print value, can be found here https://jsonplaceholder.typicode.com/users/1/posts
            print(res['userId'])
            print(res['id'])
            print(res['title'])
            print(res['body'])
            print("############")
            
            
#Define http post, return nothing
#Using JSONPlaceholder
def invoke_http_post(url:str) -> None:

    #Declare data to post
    data = {'userId':586,'title':'Hello','body':'Hello World from MCC!'}
    
    #create response which is post request of the url using the data we declared to post
    response = requests.post(url, data)
    
    #If http response is not 'ok' per code then raise ValueError that it has failed
    if not response.ok:
        #raise an exception with critical error warning
        raise ValueError('Critical Error: API Call Failure')
    
    #Takes object and returns JSON object of it
    obj = response.json()
    
    #Print objects that we're posting
    print(obj['userId'])
    print(obj['id'])
    print(obj['title'])
    print(obj['body'])
    print("############")

#Main function
if __name__ == '__main__':
    
    #Print that we're using GET and to invoke http get on the url we specified
    print ("Now GETTING...")
    url = "https://jsonplaceholder.typicode.com/users/1/posts"
    invoke_http_get(url)
    
    #Print that we're using POST and to invoke http get on the url we specified
    print ("Now POSTING...")
    url = "https://jsonplaceholder.typicode.com/posts"
    invoke_http_post(url)
