import boto3
import os
import requests
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError
import json

def create_bucket(bucket_name):
    try:
        s3_client = boto3.client('s3')
        s3_client.create_bucket(Bucket=bucket_name)
        print("Bucket created successfully.")
    except ClientError as e:
        print("Unable to create bucket:", e)


def upload_data_to_s3(bucket_name, file_path):
    try:
        # Initialize S3 client
        s3 = boto3.client('s3')

        # Read data from the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Check if the bucket already exists
        existing_buckets = [bucket['Name'] for bucket in s3.list_buckets()['Buckets']]
        if bucket_name not in existing_buckets:
            # Create the bucket if it doesn't exist
            s3.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' created successfully.")

        # Extract unique artist names from the JSON data
        unique_artists = set(song['artist'] for song in data['songs'])

        # Upload images for each unique artist
        for artist_name in unique_artists:
            # Filter songs by the current artist
            songs_by_artist = [song for song in data['songs'] if song['artist'] == artist_name]
            if not songs_by_artist:
                continue

            # Get the first song image URL
            img_url = songs_by_artist[0]['img_url']

            # Download the image
            response = requests.get(img_url)
            if response.status_code == 200:
                image_data = response.content

                # Construct the object key
                object_key = f'song_images/{artist_name}.jpg'

                
                s3.put_object(Body=image_data, Bucket=bucket_name, Key=object_key)
                print(f"Uploaded '{artist_name}.jpg' to '{bucket_name}/{object_key}'")
            else:
                print(f"Failed to download image for artist '{artist_name}'.")

        return True

    except NoCredentialsError:
        print("Credentials not available. Please provide valid AWS credentials.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


bucket_name = 's3858297-mybucket'
file_path = 'a1.json'

create_bucket(bucket_name)
upload_data_to_s3(bucket_name, file_path)
