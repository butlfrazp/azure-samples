import logging
import asyncio
from azure.eventhub.aio import EventHubConsumerClient
from config import config
import json

logger = logging.getLogger("azure.eventhub.subscriber")
logging.basicConfig(level=logging.INFO)

async def on_event(partition_context, event):
  message = event.body_as_json(encoding='UTF-8')
  logger.info("Received the event: \"{}\" from the partition with ID: \"{}\"".format(message['number'], partition_context.partition_id))

async def run():
  consumer = EventHubConsumerClient.from_connection_string(
    config['EVENTHUB_CONNECTION_STRING_SUBSCRIBER'],
    "$Default",
    eventhub_name=config['EVENTHUB_NAME']
  )
  async with consumer:
    await consumer.receive(
        on_event=on_event,
        starting_position="-1",
    )

if __name__ == "__main__":
  asyncio.run(run())