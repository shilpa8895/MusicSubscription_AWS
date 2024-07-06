import boto3
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('subscribedMusicTable') 
    user_name = event.get('user_name')
    title = event.get('title')

    try:
        # Scan the table to find the item to delete
        response = table.scan(
            FilterExpression=Attr('user_name').eq(user_name) & Attr('title').eq(title)
        )
        print("Response :", response)
        items = response.get('Items')
        
        if not items:
            return {
                'statusCode': 404,
                'body': 'No Item Found.'
            }

        # Delete each item found in the scan result
        for item in items:
            print(item['id'])
            subscription_id = item['id']
            # Delete the item
            table.delete_item(
                Key={
                    'id': subscription_id
                }
            )

        return {
            'statusCode': 200,
            'body': 'Items removed successfully.'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
