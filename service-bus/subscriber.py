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

logger = logging.getLogger("azure.eventhub.subscriber")
logging.basicConfig(level=logging.INFO)

async def run():
  servicebus_client = ServiceBusClient.from_connection_string(conn_str=config['SERVICE_BUS_CONNECTION_STRING_SUBSCRIBER'])
  async with servicebus_client:
    reciever = servicebus_client.get_queue_receiver(queue_name=config['SERVICE_BUS_QUEUE_NAME'], session_id=config['SESSION_ID'])
    async with reciever:
      session = reciever.session
      await session.set_state("START")
      print("Session state:", await session.get_state())
      received_msgs = await reciever.receive_messages(max_message_count=10, max_wait_time=5)
      for msg in received_msgs:
          print(str(msg))
          await reciever.complete_message(msg)
          await session.renew_lock()
      await session.set_state("END")
      print("Session state:", await session.get_state())

if __name__ == "__main__":
  asyncio.run(run())