import boto3

def lambda_handler(event, context):
    # Retrieve the username from the event
    username = event.get('user_name')
    # print("Username:", username)
    
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('subscribedMusicTable')
    
    try:
        # Scan the DynamoDB table to retrieve all items
        response = table.scan()
        
        # Extract the subscribed music items from the response
        subscribed_music = response.get('Items', [])
        print("subscribed_music",subscribed_music)
        
        # Filter the subscribed music items for the given username
        subscribed_music_for_user = [item for item in subscribed_music if item.get('user_name') == username]
        
        # Check if there are subscribed items for the given username
        if not subscribed_music_for_user:
            return {
                'statusCode': 200,
                'body': 'No subscribed items to display'
            }
        
        # Extract only the required information (title, artist, and year) from the subscribed music items
        music_info = [{'title': item['title'], 'artist': item['artist'], 'year': item['year']} for item in subscribed_music_for_user]
        
        # Return the subscribed music information
        return {
            'statusCode': 200,
            'body': music_info
        }
    
    except Exception as e:
        # Return an error message if an exception occurs
        return {
            'statusCode': 500,
            'body': str(e)
        }
