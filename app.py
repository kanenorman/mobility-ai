from typing import Dict

import psycopg2
from flask import Flask, render_template

from config import configs

app = Flask(__name__)


def _database_params() -> Dict:
    """
    Return Postgres Database parameters

    Returns
    -------
    Dict
       Database parameters
    """
    return {
        "dbname": configs.POSTGRES_DB,
        "user": configs.POSTGRES_USER,
        "password": configs.POSTGRES_PASSWORD,
        "host": configs.POSTGRES_HOST,
        "port": configs.POSTGRES_PORT,
    }


@app.route("/")
def index():
    conn = psycopg2.connect(**_database_params())
    cursor = conn.cursor()

    query = f"SELECT * FROM {configs.POSTGRES_TABLE}"
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
