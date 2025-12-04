# Create template for fastapi with crud endpoints
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional 
import boto3
import json

queue_name = ""
aws_account_id = ""
role_name = ""

# Assume the role to access SQS in another account
sts_client = boto3.client("sts")
assumed_role = sts_client.assume_role(
    RoleArn=f"arn:aws:iam::{aws_account_id}:role/{role_name}",
    RoleSessionName="session_name"
)
credentials = assumed_role['Credentials']

sqs_resource = boto3.resource(
    'sqs',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken'],
)

def send_message_to_queue(queue_name: str, message_body: dict):
    queue = sqs_resource.get_queue_by_name(QueueName=queue_name)
    response = queue.send_message(MessageBody=json.dumps(message_body))
    return response

app = FastAPI() 

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

items = []
@app.post("/items/")
def create_item(item: Item):
    resp = send_message_to_queue(queue_name, item.model_dump())
    if resp.get('MessageId') is None:
        raise HTTPException(status_code=500, detail="Failed to send message to SQS")
    return {"detail": "Item created", "message_id": resp['MessageId']}

@app.get("/items/", response_model=List[Item])
def read_items():
    return items

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items):
        if item.id == item_id:
            items[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for index, item in enumerate(items):
        if item.id == item_id:
            del items[index]
            return {"detail": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)