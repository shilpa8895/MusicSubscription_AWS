import boto3

def lambda_handler(event, context):
    # Get user details from the event
    user_name = event.get('user_name')
    email = event.get('email')
    password = event.get('password')

    # Check if email already exists in login DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('login')

    response = table.get_item(Key={'email': email})

    if 'Item' in response:
        # Email already exists, return error message
        return {
            'statusCode': 400,
            'body': 'The email already exists.'
        }
    else:
        # Email doesn't exist, store user details in the login DynamoDB table
        table.put_item(Item={'user_name': user_name, 'email': email, 'password': password})
        return {
            'statusCode': 200,
            'body': 'User registered successfully.'
        }
