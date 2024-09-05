import azure.functions as func
import logging
import os
from azure.storage.queue import QueueClient

app = func.FunctionApp()

@app.cosmos_db_trigger(arg_name="azcosmosdb", container_name="Items",
                        database_name="ToDoList", connection="cdb_hh_demo_connection",
                        create_lease_container_if_not_exists=True, lease_container_name="leases")  
def cosmosdb_trigger(azcosmosdb: func.DocumentList):
    logging.info('Python CosmosDB triggered.')
    queue_connection_string = os.environ.get("QUEUE_CONNECTION_STRING")
    queue_name = os.environ.get("QUEUE_NAME")

    queue_client = QueueClient.from_connection_string(queue_connection_string, queue_name)

    for item in azcosmosdb:
        json_data = item.to_json()
        queue_client.send_message(json_data)
