import boto3
import json

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('music')

    search_query = {
        'TableName': 'music',
        'ExpressionAttributeNames': {}, 
        'ExpressionAttributeValues': {}  
    }

    filter_expression = ""
    if event.get('artist'):
        search_query['ExpressionAttributeNames']['#artist'] = 'artist'
        filter_expression += '#artist = :artist'
        search_query['ExpressionAttributeValues'][':artist'] = event['artist']

    if event.get('title'):
        if filter_expression:
            filter_expression += " AND "
    
        search_query['ExpressionAttributeNames']['#title'] = 'title'
        filter_expression += '#title = :title'
        search_query['ExpressionAttributeValues'][':title'] = event['title']

    if event.get('year'):
        if filter_expression:
            filter_expression += " AND "
        search_query['ExpressionAttributeNames']['#yr'] = 'year'
        filter_expression += '#yr = :year'
        search_query['ExpressionAttributeValues'][':year'] = int(event['year'])

    try:
        if not any(event.get(param) for param in ['title', 'artist', 'year']):
            return {
                'statusCode': 404,
                'body': "No result is retrieved. Please query again"
            }

        search_query['FilterExpression'] = filter_expression

        response = table.scan(**search_query)
        items = response['Items']

        if not items:
            return {
                'statusCode': 404,
                'body': "No result is retrieved. Please query again"
            }

        return {
            'statusCode': 200,
            'body': items
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
