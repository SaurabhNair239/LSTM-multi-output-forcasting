import os

# get emails and password from environment variables
aws_access_key_id = os.environ.get("aws_access_key_id_val")
aws_secret_access_key = os.environ.get("aws_secret_access_key_val")


print("aws_access_key_id: ",aws_access_key_id)
print("aws_secret_access_key_val: ",aws_secret_access_key)
