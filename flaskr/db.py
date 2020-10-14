import sqlite3
import mysql.connector
from mysql.connector import errorcode

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            user='pi', 
            password='raspberry',
            host='127.0.0.1',
            database='flaskr'
        )

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        
def init_db():
    db = get_db()
    cursor = db.cursor()
    
    from flaskr import schema
    
    init = True;
    
    # Create Database
    try:
        cursor.execute("DROP DATABASE IF EXISTS {}".format(schema.DB_NAME))
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(schema.DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        return False;
    else:
        print("Database {}: OK.".format(schema.DB_NAME))
        
        
    # Create Tables
    for table_name in schema.TABLES:
        table_description = schema.TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            init = False
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
    
    return init
    

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    if(init_db()):
        click.echo('Initialized the database.')
    else:
        click.echo('Failed to initialize the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
