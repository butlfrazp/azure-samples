import os
from dotenv import load_dotenv

load_dotenv()

config = {
  'EVENTHUB_CONNECTION_STRING_PUBLISHER': os.environ.get('EVENTHUB_CONNECTION_STRING_PUBLISHER'),
  'EVENTHUB_CONNECTION_STRING_SUBSCRIBER': os.environ.get('EVENTHUB_CONNECTION_STRING_SUBSCRIBER'),
  'EVENTHUB_NAME': os.environ.get('EVENTHUB_NAME')
}
