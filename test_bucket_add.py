import boto3
import json

def lambda_handler(event, context):
    # Initialiser le client Lambda
    lambda_client = boto3.client('lambda')
    
    # Données à transmettre à la deuxième Lambda
    payload = {
        "message": "Données de test_bucket_add transmises à send_rule_to_mistral",
        "event": event  # Inclure l'événement reçu par test_bucket_add
    }
    
    try:
        # Appeler la deuxième Lambda en mode asynchrone
        response = lambda_client.invoke(
            FunctionName='send_rule_to_mistral',  # Nom de la fonction cible
            InvocationType='Event',  # Invocation asynchrone
            Payload=json.dumps(payload)  # Charger le payload
        )
        
        # Log du statut de l'invocation
        print("Invocation asynchrone effectuée pour send_rule_to_mistral. Réponse brute :", response)
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Appel de send_rule_to_mistral lancé avec succès en mode asynchrone",
                "invocation_status": response['StatusCode']  # Statut de l'invocation
            })
        }
    
    except Exception as e:
        print("Erreur lors de l'invocation de send_rule_to_mistral :", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

#import json

#def lambda_handler(event, context):
    # Imprimez l'événement dans CloudWatch Logs
   # print("Nouvel objet détecté dans S3 :")
  #  print(json.dumps(event, indent=4))
  #  return {
   #     "statusCode": 200,
  #      "body": json.dumps("Événement traité avec succès !")
  #  }
