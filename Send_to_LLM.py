import boto3
import json
import re

def call_bedrock_api(prompt):
    # Keep existing bedrock call implementation
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
        # Parse input with proper JSON handling
        body_data = json.loads(event["body"]) if isinstance(event.get("body"), str) else event.get("body", {})
        
        responses = []
        
        # Regex pattern to identify complete schema/rule pairs with XML tags
        xml_pattern = re.compile(
            r"(<SCHEMA>.*?</SCHEMA>\s*<RULE>.*?</RULE>)", 
            re.DOTALL
        )

        if isinstance(body_data, dict):
            for category in ['abonnement', 'conso', 'facture']:
                items = body_data.get(category, [])
                for item in items:
                    # Decode Unicode escapes first
                    decoded_item = bytes(item, "utf-8").decode("unicode_escape")
                    
                    # Find all complete XML-tagged pairs
                    matches = xml_pattern.findall(decoded_item)
                    
                    for match in matches:
                        # Preserve XML tags in the prompt
                        prompt = match.strip()
                        print("Processing XML prompt:", prompt)
                        
                        # Call Bedrock and store response
                        bedrock_response = call_bedrock_api(prompt)
                        responses.append(bedrock_response)

        return {
            'statusCode': 200,
            'body': json.dumps({'bedrock_responses': responses}, ensure_ascii=False)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }