import boto3

def lambda_handler(event, context):
    email = event.get('email')
    password = event.get('password')
    print("email and password",email, password)
    
    db_resource = boto3.resource('dynamodb')
    table = db_resource.Table("login")
    response = table.get_item(Key={'email': email})
    item = response.get('Item')
    print('item', item)
    print('respose', response)
    if email and password:

        if item:
                # Extract the user's password from the user_data
                user_password = item.get('password')
                user_name = item.get('user_name')
                
                if user_password == password:
                    # Valid credentials, redirect to main page
                    return {
                        'statusCode': 200,
                        'headers': {
                            'Access-Control-Allow-Headers': 'Content-Type',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': '*'
                        },
                        'body': {
                        'user_name': user_name
                        }
                    }
                else:
                    # Invalid password
                    return {
                        'statusCode': 401,
                        'body': 'Email or Password is invalid.'
                    }
        else:
                # User not found
            return {
                'statusCode': 401,
                'body': 'User not found'
            }
    else:
        # Missing email or password
        return {
            'statusCode': 400,
            'body': 'Email and password are required.'
        }
