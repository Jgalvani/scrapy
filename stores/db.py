import dotenv
import MySQLdb
import MySQLdb.cursors
import os

from scrapy.exceptions import CloseSpider

dotenv.load_dotenv()


def get_db():
    if "CONNECTION" not in os.environ:
        raise CloseSpider('The variable "CONNECTION" is not set in your environment')

    connection_string = os.environ["CONNECTION"]
    connection = urlparse(connection_string)
    database = connection.path.replace("/", "")

    db = MySQLdb.connect(
        charset="utf8",
        host=connection.hostname,
        database=database,
        user=connection.username,
        password=connection.password,
        autocommit="True",
        port=connection.port,
        cursorclass=MySQLdb.cursors.DictCursor,
    )

    return db


def insert_rows(rows):
    db = get_db()
    cursor = db.cursor()

    # Query definition
    print('Updating table "stores"...')
    table1_query = """
        INSERT INTO stores
            (store, name, address, zipcode, city, date)
        VALUES
            (%s, %s, %s, %s, %s, %s)

        ON DUPLICATE KEY UPDATE
            store       = store,
            name        = name,
            address     = addrees,
            zipcode     = zipcode,
            city        = city,
            date        = date
    """

    # Query execution
    cursor.execute_many(table1_query, rows)
    print('Results inserted!')

    cursor.close()
    db.close()
