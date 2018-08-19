"""
database_utils.py

Description:
    database tools and utilities
"""
# Python libraries
import os
import re
import collections
import traceback

# MySQL libraries
import mysql.connector as connector

# local libraries
import fitness


# ==============================================================================
# constants / globals
# ==============================================================================
TABLES_FILE = os.path.join(fitness.CONFIGS, "db_tables.sql")


# ==============================================================================
# schema
# ==============================================================================
def create_db(database, user, user_alias):
    """
    Creates the specified database at the specified location.

    :param database: full file path of the database
    :type database: string
    :param user: user name like: ${USER}@localhost
    :type user: string
    :param user_alias: user name alias
    :type user_alias: string
    :return: n/a
    :rtype: n/a
    """
    location, name = os.path.split(database)

    # change into db directory
    cwd = os.getcwd()
    os.chdir(location)

    # connect to server
    conn = connector.connect(user='root', password='r00t', host='localhost')
    cursor = conn.cursor()

    # create database
    cursor.execute("DROP DATABASE IF EXISTS {};".format(name))
    fitness.LOGGER.info("Creating database @: {}".format(database))
    cursor.execute("CREATE DATABASE {};".format(name))

    # grant access
    cmd = "grant all privileges on {}.* to {!r} identified by {!r};".format(
        name, user, user_alias
    )
    cursor.execute(cmd)

    # reset to previous working directory
    os.chdir(cwd)


# ==============================================================================
# tables
# ==============================================================================
def _table_commands(sourcefile):
    """
    Returns a mapping of table name, MySQL command pairs used to create database
    tables specified by the given table definitions file

    :param sourcefile: file containing MySQL table creation statements
    :type sourcefile: string
    :return: MySQL table creation commands like: {"table_name": "MySQL_command", ...}
    :rtype: instance of <class 'OrderedDict'>
    """
    table_cmds = collections.OrderedDict()
    key = None
    cmd = ""
    for line in open(sourcefile, 'r'):
        if line.startswith("#"):
            continue
        result = re.search("^CREATE TABLE IF NOT EXISTS +(\w+)", line)
        if result:
            key = result.groups()[0]
            cmd = line
        else:
            cmd += line
            if re.search("^\);", line):
                table_cmds[key] = cmd
    return table_cmds


def create_tables(sourcefile, database):
    """
    Creates the tables specified by the given table definitions file for the
    given database

    :param sourcefile: file containing MySQL table creation statements
    :type sourcefile: string
    :param database: disk location of the database you want to create tables for
    :type database: string
    :return: MySQL table creation commands like: {"table_name": "MySQL_command", ...}
    :rtype: instance of <class 'OrderedDict'>
    """
    # connect to db
    db_dir, db_name = os.path.split(database)
    pwd = os.getcwd()
    os.chdir(db_dir)
    conn = connector.connect(user='root',
                             password='r00t',
                             host='localhost',
                             database=db_name)
    cursor = conn.cursor()

    # create tables
    table_cmd_data = _table_command(sourcefile)
    for table, cmd in table_cmd_data.items():
        fitness.LOGGER.info("Creating table: {}".format(table))
        try:
            cursor.execute(cmd)
        except:
            traceback.print_exc()

    os.chdir(pwd)

    return table_cmd_data


# ==============================================================================
# main
# ==============================================================================
def main():
    """
    Builds a fitness database

    :return: dabase creation data like: {"database": db, "table_cmds": {}}
    :rtype: dictionary
    """
    database = os.path.join(os.getenv("HOME"), "fitness.db")
    create_db(database, "pkatzen@localhost", "pkatzen")
    table_data = create_tables(TABLES_FILE, database)
    return {"database": database, "table_data": table_data}
