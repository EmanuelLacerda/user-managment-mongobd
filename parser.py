from json import load as load_json
from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv


load_dotenv()


USER_DATA_JSON_FILE_NAME = 'udata.json'

DB_NAME = getenv("DB_NAME")
DB_HOST = getenv("DB_HOST")
DB_PORT = int(getenv("DB_PORT"))
DB_COLLECTION = getenv("DB_COLLECTION")

def runImportScript():
    try:
        client = MongoClient(DB_HOST, DB_PORT)
        print("Client connected successfully \n")
    except:
        print("Could not connect to Client")

        return

    database = client[DB_NAME]
    print("User database created or accessed successfully \n")

    Collection = database[DB_COLLECTION]
    print("User collection created or accessed successfully \n")

    print("The user data JSON has started loading...")
    try:
        with open(USER_DATA_JSON_FILE_NAME, 'r') as users:
            user_data = load_json(users)
        print("Loading user data JSON completed successfully \n")
    except FileNotFoundError as error:
        print(f'It was not possible to load {USER_DATA_JSON_FILE_NAME} because the following error: {error}')

        return
    
    print("The user data JSON, which was loaded, has started to be inserted into the user database...")
    if isinstance(user_data, list):
        Collection.insert_many(user_data) 
    else:
        Collection.insert_one(user_data)
    print("User data JSON insertion completed successfully")


if __name__ == "__main__":
    runImportScript()