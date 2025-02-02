import boto3
import json

# Initialize the Glue client
glue_client = boto3.client('glue')
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    # Initialize a dictionary to store table names and their associated columns
    table_columns_info = {}
    
    try:
        # Step 1: Get a list of all databases in the Glue Catalog
        databases_response = glue_client.get_databases()

        # Loop over each database
        for database in databases_response['DatabaseList']:
            database_name = database['Name']

            # Step 2: Get a list of tables for each database
            tables_response = glue_client.get_tables(DatabaseName=database_name)

            # Loop over each table in the database
            for table in tables_response['TableList']:
                table_name = table['Name']

                # Step 3: Get metadata for each table
                table_metadata = glue_client.get_table(DatabaseName=database_name, Name=table_name)

                # Extract only column names (ignore types)
                columns = [col['Name'] for col in table_metadata['Table']['StorageDescriptor']['Columns']]

                # Store columns in the dictionary, with table name as the key
                table_columns_info[table_name] = columns

        # Pretty-print the dictionary (columns grouped by table)
        clean_output = json.dumps(table_columns_info, indent=2)

        # Step 4: Invoke the long-running task asynchronously
        lambda_client.invoke(
            FunctionName='arn:aws:lambda:us-west-2:135808932865:function:Prompt_Builder',
            InvocationType='Event',
            Payload=json.dumps(clean_output)  # Pass the same event for the next function execution
        )

        # Return the clean, structured output as a JSON string
        return {
            'statusCode': 200,
            'body': clean_output  # Return the column names grouped by table
        }
    
    except Exception as e:
        # If an error occurs, return the error message
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
