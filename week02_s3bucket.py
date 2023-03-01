"""
Author: Malachi Corrigan
Date: 01/20/2023

Create a bucket (prompt for the name) - 5pts
List all buckets - 5pts
Upload a file - 5pts
List all files in a particular bucket - 5pts
Delete a file - 5pts
Delete a bucket - 5pts
Bonus 5pts: List the contents of the file that is in a bucket (not on your local hard drive)
"""

#Creds are taken from the path below
#C:\Users\Malachi\.aws\credentials

#Import Boto3 & UUID
import boto3

#Instantiate S3
s3client = boto3.client('s3')

#Prompt for bucket name
desiredBucketName = input("Enter Globally Unique Desired Bucket Name: ")

#Create the bucket with prompted name in US-EAST-2 which is Ohio with the help of LocationConstraint
print("Creating A Bucket With The Name: " + desiredBucketName)
s3client.create_bucket(Bucket=desiredBucketName,CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})

#List all buckets
print ("List of Buckets: ")
bucketList = s3client.list_buckets()
for bucket in bucketList['Buckets']:
    print ("Bucket: " + bucket['Name'])

#Upload a file
uploadObject = input("Enter Full Path of Object to Upload: ")
#Splits by literal backslash and then takes last index that is trailing and puts it into the variable which is the filename we're wanting
uploadObjectName = uploadObject.rsplit('\\', 1)[-1]
s3client.upload_file(uploadObject, desiredBucketName, uploadObjectName)
print ("File: " + str(uploadObjectName) + " uploaded!")

#List all files in a particular buccket
bucketFiles = s3client.list_objects_v2(Bucket=desiredBucketName,)
for file in bucketFiles['Contents']:
    print ("File: " + file['Key'])

#Create a secondary test bucket for Delete File & Delete Bucket Sections
secondaryBucket = desiredBucketName + "-secondary"
print ("Creating Bucket: " + str(secondaryBucket))
s3client.create_bucket(Bucket=secondaryBucket,CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
print ("Created Bucket: " + str(secondaryBucket))

#Create a file using PUT to delete
testFile = 'testfile.txt'
s3client.put_object(Bucket=secondaryBucket, Key=testFile, Body=b'I love being deleted!')
print ("Uploaded: " + testFile)

#Delete a file
input("Press Enter to Continue To Delete File Section...")
s3client.delete_object(Bucket=secondaryBucket,Key=testFile)
print ("File Deleted: " + testFile)

#setup S3 Service Resource 
s3resource = boto3.resource('s3')
secondaryBucket_Resource = s3resource.Bucket(secondaryBucket)

#Delete a bucket
#First delete all files, since like the GUI you cannot delete until it is emptied
#Selects Secondary Bucket Resource then selects all objects then deletes them all
secondaryBucket_Resource.objects.all().delete()

#Finally delete the bucket once empty
secondaryBucket_Resource.delete()
print ("Bucket Deleted: " + str(secondaryBucket))

#List the contents of the file that is in a bucket (Not local)
#Create object which defines bucket and key
readObject = s3resource.Object(desiredBucketName,uploadObjectName)
#Read the body of the object key and decode to UTF-8 so it legible
readObjectContent = readObject.get()['Body'].read().decode('utf-8')
#Print contents to screen
print (readObjectContent)
