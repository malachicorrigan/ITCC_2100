#Author: Malachi Corrigan
#Date: 02/18/2023

#import requests module
import requests

#Define http get, return nothing
def invoke_my_function(url:str) -> bool:
    
    #create response which is get request of the url
    response = requests.get(url)
    
    #If http response is not 'ok' per code then return FALSE
    if not response.ok:
        #return bool false
        return False
    
    #Takes object and returns JSON object of it
    obj = response.json()
    
    #Prints object
    print (obj)
    
    #Returns True since not response.ok has evaluated this is good and 200 code
    return True

#Main function
if __name__ == '__main__':
    
    #Print that we're using GET and to invoke http get on the url we specified
    print ("Now GETTING...")
    #url is API invoke url with lamba function
    url = "https://9ux1nblb07.execute-api.us-east-1.amazonaws.com/my-function"
    #If returned bool is true, print status true
    if (invoke_my_function(url)):
        print ("Status: True")
    #If returned bool is false, print status false
    else:
        print ("Status: False")