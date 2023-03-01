#Author: Malachi Corrigan
#Class: ITCC_2100

import boto3
import os
import time
import logging
from botocore.exceptions import ClientError

#Define Endpoint
ENDPOINT = 'http://localhost:8000'


############################################################################################################
# An exampe object
# {
#     #Primary Key = Player ID
#     "pk": "78458952",
    
#     #Secondary Key = UserName
#     "sk": "John Doe Himself",
    
#     #Gold = Gold is the currency that is used in the shop
#     "gold": "8500",
    
#     #Clan = Clan that the user is apart of
#     "clan": "MCC Warriors",

#     #Membership = If they're paying for a premium membership
#     "membership": "True"
# }
############################################################################################################

#Creates Table
def createTable(table_name):
    try:
        db_client = boto3.client('dynamodb', endpoint_url=ENDPOINT)
        db_client.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName':  'playerid',
                    'AttributeType':  'N',
                },
                {
                    'AttributeName':  'username',
                    'AttributeType':  'S',
                }
                
                # {
                #     'AttributeName':  'gold',
                #     'AttributeType':  'N',
                # },
                # {
                #     'AttributeName':  'clan',
                #     'AttributeType':  'S',
                # },
                # {
                #     'AttributeName':  'membership',
                #     'AttributeType':  'S',
                # }
            ],
            KeySchema=[
                {
                    'AttributeName':  'playerid',
                    'KeyType':  'HASH',
                },
                {
                    'AttributeName':  'username',
                    'KeyType':  'RANGE',
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 2,
                'WriteCapacityUnits': 2,
            },
            GlobalSecondaryIndexes=[
            {
                    'IndexName': "GSI_SWAP",
                    'KeySchema': [
                        {
                        'AttributeName':  'username',
                        'KeyType':  'HASH',
                        },
                        {
                            'AttributeName':  'playerid',
                            'KeyType':  'RANGE',
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL',
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 2,
                        'WriteCapacityUnits': 2
                    }
                },
            ],
            TableName=table_name,
        )
        return True
                
    except ClientError as e:
        logging.error(e)
        return False

#Gets table's status    
def describeTable(table_name):
    
    try:
        db_client = boto3.client('dynamodb', endpoint_url=ENDPOINT)
        response = db_client.describe_table(TableName=table_name)
        return response['Table']['TableStatus']
    
    except ClientError as e:
        logging.error(e)
        return None

#Adds the 2 sets of 3 items
def putItem(table_name,pk,sk,gold,clan,membership):
    
    try:
        db_client = boto3.client('dynamodb', endpoint_url=ENDPOINT)
        db_client.put_item(
            Item={
                'playerid': {
                    'N': str(pk),
                },
                'username': {
                    'S': sk,
                },
                'gold': {
                    'N': str(gold), #Passed as string per Video time stampt 14:45
                },
                'clan': {
                    'S': clan,
                },
                'membership': {
                    'S': membership,
                },
            },
            ReturnConsumedCapacity='TOTAL', #Shows capacity
            TableName=table_name
        )
        return True
    
    except Exception as e:
        logging.error(e)
        return False
    
#Gets an item from a table
def getItem(table_name,pk,sk):
    
    try:
        db_client = boto3.client('dynamodb', endpoint_url=ENDPOINT)
        response = db_client.get_item(
            Key={
                'playerid': {
                    'N': pk,
                },
                'username': {
                    'S': sk,
                },
            },
            TableName=table_name
        )
        return response["Item"]
    
    except ClientError as e:
        logging.error(e)
        return None
    
#Deletes an item from a table
def deleteItem(table_name,pk,sk):
    
    try:
        db_client = boto3.client('dynamodb', endpoint_url=ENDPOINT)
        response = db_client.delete_item(
            Key={
                'playerid': {
                    'N': str(pk),
                },
                'username': {
                    'S': sk,
                },
            },
            TableName=table_name
        )
    
    except ClientError as e:
        logging.error(e)
        return None
    
#Deletes a table
def deleteTable(table_name):
    
    try:
        db_client = boto3.client('dynamodb', endpoint_url=ENDPOINT)
        db_client.delete_table(TableName=table_name)
        return True
    
    except ClientError as e:
        logging.error(e)
        return False


#Queries a table
def queryTable(table_name):
    
    try:
        db_client = boto3.client('dynamodb', endpoint_url=ENDPOINT)
        response = db_client.query(
            ExpressionAttributeValues={
                ':v1': {
                    'N': "445566",
                },
                ':v2': {
                    'S': "MCC_Malachi",
                },
            },
            KeyConditionalExpression='playerid = :v1 AND username = :v2',
            TableName = table_name,
        )
        return response["Items"]
    
    except Exception as e:
        logging.error(e)
        return None
    
    
#Main with menu
def main():
    menu=True
    #Print menu
    while menu:
        print ("""
        1. Create a Table & Add Items
        2. Get Item from Table using Key
        3. Delete an Item from Table using Key
        4. Delete a Table using Table name
        5. Query Table for items within a range
        6. Exit
        """)
        
        menu=input("Select the menu option you'd like to perform: ")
        
        #If Create a Table & Add Items is Selected
        if menu=="1":
            
            #Input for Table Name
            table_name = input("Enter Table Name: ")
            createTable(table_name)
            
            #wait for table to be created using describeTable function
            while True:
                results = describeTable(table_name)
                if results == 'ACTIVE':
                    break
                time.sleep(10)
            
            #Put 3 items that represent your item in your individual project per requirement (Same Primary, Different secondary hash key)
            putItem(table_name,147822,"Malachi Corrigan",8500,"MCC Warriors","True")
            putItem(table_name,147822,"The One And Only",8500,"MCC Warriors","True")
            putItem(table_name,147822,"MR Corrigan",8500,"MCC Warriors","True")
            print("Adding 3 Items Same Primary, Different secondary hash key")
            
            #Put 3 more items that represent your item in your individual project per requirement (Different Primary, Same secondary hash key)
            putItem(table_name,112233,"MCC_Malachi",8500,"MCC Warriors","True")
            putItem(table_name,445566,"MCC_Malachi",8500,"MCC Warriors","True")
            putItem(table_name,778899,"MCC_Malachi",8500,"MCC Warriors","True")
            print("Adding 3 Items Different Primary, Same secondary hash key")
            
        #If Get Item from Table using Key is Selected
        elif menu=="2":
            table_name = input ("Enter Table Name: ")
            pk = input ("Enter Primary Key: ")
            sk= input ("Enter Secondary Key: ")
            item = getItem(table_name,pk,sk)
            print('ITEM: ', item)
            
        #If Delete an Item from Table using Key Selected
        elif menu=="3":
            table_name = input ("Enter Table Name: ")
            pk = input ("Enter Primary Key: ")
            sk= input ("Enter Secondary Key: ")
            item = getItem(table_name,pk,sk)
            print('DELETING: ', item)
            deleteItem(table_name,pk,sk)
            
        #If Delete a Table using Table name is Selected
        elif menu=="4":
            table_name = input ("Enter Table Name: ")
            print("Deleting Table: ", table_name)
            deleteTable(table_name)
            
        #If Query Table for items within a range is Selected

        elif menu=="5":
            table_name = input ("Enter Table Name: ")
            query = queryTable(table_name)
            print("QUERY: ", query)
            
        #If Exit is Selected
        elif menu=="6":
            exit()
            
        #Anything else for invalid input
        else:
            os.system('cls')
            print("Not a valid choice, please try again.")

#Runs main
main()