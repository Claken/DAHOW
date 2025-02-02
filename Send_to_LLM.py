import boto3
import json

def call_bedrock_api(prompt):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2048,
            "temperature": 0.7,
            "top_p": 0.999,
            "top_k": 250,
            "stop_sequences": [],
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        })
    )
    return json.loads(response["body"].read().decode("utf-8"))

def lambda_handler(event, context):
    print("Event received:", event)
    try:
        # Parse the event body
        if "body" in event and isinstance(event["body"], str):
            body_data = json.loads(event["body"])
        elif isinstance(event["body"], (dict, list)):
            body_data = event["body"]
        else:
            return {
                'statusCode': 400,
                'body': 'Invalid event format. Expected a JSON object or string inside "body".'
            }
        
        # Ensure we always work with a list.
        if not isinstance(body_data, list):
            body_data = [body_data]
        
        responses = []
        # Loop over each top-level element
        for element in body_data:
            print("Processing element:", element)
            prompt = (
                "You are an expert SQL Query builder: Create an SQL Query with the following:\n" +
                str(element)
            )
            print("Constructed prompt:", prompt)
            bedrock_response = call_bedrock_api(prompt)
            responses.append(bedrock_response)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'bedrock_responses': responses})
        }

    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': 'Invalid JSON format in the event.'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"An unexpected error occurred: {str(e)}"
        }
