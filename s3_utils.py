import io
import boto3
import pandas as pd
import os


#from s3_credentials import S3_CREDS

s3 = boto3.client(
    "s3",
    aws_access_key_id= os.environ[ 'AWS_ACCESS_KEY_ID' ], #S3_CREDS["accessKeyId"],
    aws_secret_access_key=os.environ[ 'AWS_SECRET_ACCESS_KEY' ], #S3_CREDS["secretAccessKey"],
    region_name=os.environ['region_name'],
)


def read_csv_on_s3_into_dataframe(
        s3_bucket_name,
        filename,
):

    response = s3.get_object(
        Bucket=s3_bucket_name,
        Key=filename,
    )

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        print(f"Successful S3 get_object response. Status - {status}")

        df = pd.read_csv(response.get("Body"))

        return df

    else:
        print(f"Unsuccessful S3 get_object response. Status - {status}")


def write_dataframe_to_csv_in_s3(
        df,
        s3_bucket_name,
        filename,
):
    """
    Writes pandas dataframe to CSV file in s3

    Args:
        df ():
        s3_bucket_name ():
        filename ():

    Returns:

    """
    with io.StringIO() as csv_buffer:
        df.to_csv(csv_buffer, index=False)

        response = s3.put_object(
            Bucket=s3_bucket_name,
            Key=filename,
            Body=csv_buffer.getvalue()
        )

        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            print(f"Successful S3 put_object response. Status - {status}")
        else:
            print(f"Unsuccessful S3 put_object response. Status - {status}")
