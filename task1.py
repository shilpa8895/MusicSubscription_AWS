import boto3
import json

# 1.1 Create a “login” table in DynamoDB containing 10 entities with the following attributes and values.
# NOTE: This task is done via console

# 1.2 Write a program to automatically create a table titled “music” in DynamoDB with the following Attributes: 
# title, artist, year, web_url, image_url.
def create_music_table():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table_name = 'music'

    try:
        # Check if the table already exists
        existing_tables = dynamodb.tables.all()
        table_exists = any(table.name == table_name for table in existing_tables)

        # If the table doesn't exist, create it
        if not table_exists:
            print("Creating table; please wait...")
            table = dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {
                        'AttributeName': 'title',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'title',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
            # Wait for the table to become active
            table.wait_until_exists()
            print("Table created successfully.")
        else:
            print("Table already exists.")

    except Exception as e:
        print("Unable to create table:")
        print(e)

# Calling  function to create the table
create_music_table()



# 1.3 Write a program to automatically load the data from a1.json to your music table.
def load_data(table_name, json_file):
    
    dynamodb = boto3.resource('dynamodb',region_name='us-east-1')

    # Load JSON data from file
    with open(json_file) as f:
        data = json.load(f)

    table = dynamodb.Table(table_name)

    # Load each item from JSON into the table
    with table.batch_writer() as batch:
        for song in data['songs']:
            item = {
                'title': song['title'],
                'artist': song['artist'],
                'year': song['year'],
                'web_url': song['web_url'],
                'img_url': song['img_url']
            }
            batch.put_item(Item=item)

# Calling function
load_data('music', 'a1.json')
