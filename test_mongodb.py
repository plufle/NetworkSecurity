from dotenv import load_dotenv
from pymongo import MongoClient
import os 

load_dotenv()
MONGODB_URL = os.getenv("MONGO_DB_URL")
# Create a new client and connect to the server
client = MongoClient(MONGODB_URL)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e) 