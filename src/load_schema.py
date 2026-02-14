import os
import json
from sqlalchemy import create_engine, inspect
from geoalchemy2 import Geometry

def load_schema(db_name):
    schema_path = os.path.join(os.getenv("DATA_PATH"), f"{db_name}_schema.json")
    if os.path.exists(schema_path):
        print(f"{schema_path} already exists.")
        print("Loading schema from existing file.")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        return schema
    else:
        print(f"{schema_path} does not exist.")
        print("Loading schema from database.")
        db_url = os.getenv("DB_URL").replace("...", db_name)
        print(f"Connecting to database at {db_url}.")
        engine = create_engine(db_url)
        inspector = inspect(engine)

        schema = {}
        for table_name in inspector.get_table_names():
            columns = inspector.get_columns(table_name)
            schema[table_name] = {col['name']: str(col['type']) for col in columns}

        print("schema loaded from database.")
        print(f"Saving schema to {schema_path}.")

        with open(schema_path, "w", encoding="utf-8") as f:
            json.dump(schema, f, indent=4)
            print("Schema saved.")
        
        return schema
        
if __name__ == "__main__":
    import dotenv; dotenv.load_dotenv()
    load_schema("parks")