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
import fitness.resources as resources


# ==============================================================================
# constants / globals
# ==============================================================================
TABLES_FILE = os.path.join(resources.ROOT, "configs", "db_tables.sql")
USER_DATA = {"pkatzen@localhost": "pkatzen"}


# ==============================================================================
# schema
# ==============================================================================
def createDb(database=resources.DATABASE):
    """
    Creates the specified database. Will overwrite it if it exists

    :param database: disk location of the database you want to create
    :type database: string
    :return: path to the new database
    :rtype: string
    """
    db_dir, db_name = os.path.split(database)
    # change into db directory
    pwd = os.getcwd()
    os.chdir(db_dir)

    # connect to server
    conn = connector.connect(user='root', password='r00t', host='localhost')
    cursor = conn.cursor()

    # create database - overwrite if nexessary
    cursor.execute("DROP DATABASE IF EXISTS {0};".format(db_name))
    _LOGGER.info("Creating database: {0}".format(database))
    cursor.execute("CREATE DATABASE {0};".format(db_name))

    # grant access
    for host, alias in USER_DATA.items():
        cmd = "grant all privileges on {0}.* ".format(db_name)
        cmd += "to \'{0}\' ".format(host)
        cmd += "identified by \'{0}\';".format(alias)
        cursor.execute(cmd)

    # reset to previous working durectory
    os.chdir(pwd)

    return database


# ==============================================================================
# tables
# ==============================================================================
def getCreateTableCmds(tables_path=TABLES_FILE):
    """
    Returns a mapping of table name, MySQL command pairs used to create database
    tables specified by the given table definitions file

    :param tables_path: file containing MySQL table creation statements
    :type tables_path: string
    :return: MySQL table creation commands
    :rtype: instance of <class 'OrderedDict'>
            {"table_name": "MySQL_command", ...}
    """
    table_cmds = collections.OrderedDict()
    key = None
    cmd = ""
    for line in open(tables_path, 'r'):
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


def createTables(tables_path=TABLES_FILE, database=resources.DATABASE):
    """
    Creates the tables specified by the given table definitions file for the
    given database

    :param tables_path: file containing MySQL table creation statements
    :type tables_path: string
    :param database: disk location of the database you want to create tables for
    :type database: string
    :return: MySQL table creation commands
    :rtype: instance of <class 'OrderedDict'>
            {"table_name": "MySQL_command", ...}
    """
    # get table creation commands
    table_cmd_data = getCreateTableCmds(tables_path)

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
    for name, cmd in table_cmd_data.items():
        _LOGGER.info("Creating table: {0}".format(name))
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
    Builds the fitness database

    :return: dabase creation data
    :rtype: dictionary
            {"database": db,
             "table_cmds": {"table_name": "MySQL_command", ...}}
    """
    db = createDb(resources.DATABASE)
    table_data = createTables(TABLES_FILE, resources.DATABASE)
    return {"database": db, "table_cmds": table_data}


# ==============================================================================
# Interactive session
# ==============================================================================
if __name__ == '__main__':
    main()
 
