from dataclasses import dataclass, asdict
from json import load as load_json, dumps as dumps_json
from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv


load_dotenv()


USER_DATA_JSON_FILE_NAME = 'udata.json'

DB_NAME = getenv("DB_NAME")
DB_HOST = getenv("DB_HOST")
DB_PORT = int(getenv("DB_PORT"))
DB_COLLECTION = getenv("DB_COLLECTION")


def get_user_roles(user_data):
    role_mapping = {
        "is_user_admin": "admin",
        "is_user_manager": "manager",
        "is_user_tester": "tester",
    }

    roles = []

    for attribute, role in role_mapping.items():
        if user_data.get(attribute):
            roles.append(role)

    return roles

@dataclass
class UserPreferences:
	timezone: str

@dataclass
class User:
    username: str
    password: str
    roles: list
    preferences: UserPreferences
    created_at: str
    active: bool = True

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
            user_data_list = load_json(users)["users"]
        print("Loading user data JSON completed successfully \n")
    except FileNotFoundError as error:
        print(f'It was not possible to load {USER_DATA_JSON_FILE_NAME} because the following error: {error}')

        return
    
    print("The user data JSON, which was loaded, has started to be inserted into the user database...")
    for user in user_data_list:
        user_data_parser = User(
            username=user["user"],
            password=user["password"],
            roles=get_user_roles(user),
            preferences=UserPreferences(timezone=user["user_timezone"]),
            active=user["is_user_active"],
            created_at=user["created_at"]
        )

        try:
            Collection.insert_one(asdict(user_data_parser))
        except:
            print(f'It was not possible to add the user {user_data_parser.username} in the database!')

            return
    
    print("User data JSON insertion completed successfully")


if __name__ == "__main__":
    runImportScript()