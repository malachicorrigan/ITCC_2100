from datetime import datetime
import logging
import boto3
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ENDPOINT = "arn:aws:dynamodb:us-east-1:970162354642:table/timesheet"
TABLE_NAME = "timesheet"

###############################################################################
# Put a DynamoDb Item.
###############################################################################
def time_punch(pk, sk, login):

    time_stamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    try:
        db_client = boto3.client("dynamodb")
        db_client.put_item(
            Item={
                "pk": {
                    "S": pk,
                },
                "sk": {
                    "S": sk,
                },
                #If false then they're punchingo ut
                "punch_in": {
                    "BOOL": login,
                },
                "timestamp": {
                    "S": time_stamp,
                },
            },
            ReturnConsumedCapacity="TOTAL",
            TableName=TABLE_NAME,
        )
        return True
    except Exception as e:
        logging.error(e)
        return False


###############################################################################
# Entrance to the lambda function.
###############################################################################
def lambda_handler(event, context):

    logger.info(event)
    logger.info(context)

    pk = "mc4455"
    sk = "MalachiCorrigan"
    if time_punch(pk, sk, True):
        return {"statusCode": 200, "body": "Successfully punched in!"}

    return {"statusCode": 400, "body": "Error punching in, contact your administrator!"}


#### For debugging only
if __name__ == "__main__":
    lambda_handler(None, None)
