import boto3
import json
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('subscribedMusicTable')  

def lambda_handler(event, context):
    # Extract information from the event
    user_name = event.get('user_name')
    title = event.get('title')
    artist = event.get('artist')
    year = event.get('year')

    # Generate a unique ID for the subscription
    subscription_id = str(uuid.uuid4())

    # Check if all required information is present
    if not user_name or not title or not artist or not year:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing required parameters.')
        }

    try:
        # Check if the item already exists
        response = table.scan(
            FilterExpression='user_name = :user_name and title = :title',
            ExpressionAttributeValues={':user_name': user_name, ':title': title}
        )
        items = response['Items']
        if items:
            return {
                'statusCode': 409,  # Conflict status code
                'body': 'User has already subscribed to the same title.'
            }
            
        # Put the subscription information into the DynamoDB table
        table.put_item(
            Item={
                'id': subscription_id,
                'user_name': user_name,
                'title': title,
                'artist': artist,
                'year': year
            }
        )

        return {
            'statusCode': 200,
            'body': "Subscription successful."
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body':str(e)
        }
