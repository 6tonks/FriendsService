
import os
from database_services.Neo4JDataResource import Neo4JDataResource

def get_db_info():
    """
    :return: A dictionary with connect info for DB
    """
    db_type = os.environ.get("DBTYPE", None)
    db_host = os.environ.get("DBHOST", None)
    db_port = os.environ.get("DBPORT", None)
    db_user = os.environ.get("DBUSER", None)
    db_password = os.environ.get("DBPASSWORD", None)

    if db_host is not None:
        db_info = {
            "type": db_type,
            "host": db_host,
            "user": db_user,
            "password": db_password,
            "port": db_port,
        }
    else:
        db_info = {
            "type": "neo4j",
            "host": "localhost",
            "user": "dbuser",
            "password": "dbuserdbuser",
            "port": 7687,
        }

    return db_info

def get_db_resource():
    db_info = get_db_info()

    if db_info['type'] == 'neo4j':
        db_resource = Neo4JDataResource(
            auth=(db_info['user'], db_info['password']),
            host=db_info['host'],
            port=db_info['port'],
            secure=False,
        )
    elif db_info['type'] == 'neptune':
        # db_resource = NeptuneDataResource(
        #     auth=(db_info['user'], db_info['password']),
        #     host=db_info['host'],
        #     port=db_info['port'],
        #     secure=False,
        # )
        pass

    return db_resource