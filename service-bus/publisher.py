import logging
import os
import asyncio
from azure.servicebus import ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient
from config import config
import json
import random
import time
import uuid

logger = logging.getLogger("azure.eventhub.publisher")
logging.basicConfig(level=logging.INFO)

async def send_batch_message(sender):
  batch_message = await sender.create_message_batch()
  for _ in range(10):
    random_number = random.random()
    data = { 'number': random_number }
    data_str = json.dumps(data)
    batch_message.add_message(ServiceBusMessage(data_str, session_id=config['SESSION_ID']))
  logger.info("sending message to service bus...")
  await sender.send_messages(batch_message)

async def run():
  servicebus_client = ServiceBusClient.from_connection_string(conn_str=config['SERVICE_BUS_CONNECTION_STRING_PUBLISHER'])
  async with servicebus_client:
    sender = servicebus_client.get_queue_sender(queue_name=config['SERVICE_BUS_QUEUE_NAME'])
    async with sender:
      while True:
        await send_batch_message(sender)
        time.sleep(30)

if __name__ == "__main__":
  asyncio.run(run())