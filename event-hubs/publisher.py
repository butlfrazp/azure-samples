import logging
import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
from config import config
import json
import random
import time

logger = logging.getLogger("azure.eventhub.publisher")
logging.basicConfig(level=logging.INFO)

async def send_message(producer):
  event_data_batch = await producer.create_batch(partition_id='0')
  for _ in range(10):
    random_number = random.random()
    data = { 'number': random_number }
    data_str = json.dumps(data)
    event_data_batch.add(EventData(data_str))
  await producer.send_batch(event_data_batch)
  logger.info("created and sent batch...")
  time.sleep(30)

async def run():
  producer = EventHubProducerClient.from_connection_string(
    config['EVENTHUB_CONNECTION_STRING_PUBLISHER'],
    eventhub_name=config['EVENTHUB_NAME']
  )
  async with producer:
    while True:
      await send_message(producer)

if __name__ == "__main__":
  asyncio.run(run())