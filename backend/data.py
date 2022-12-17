"""
Current table schema needs

user TABLE:
columns
id             => int: primary key
user           => text: username
creation_date  => text: date of account creation


todo_list TABLE:
columns
id             => int: primary key
user_id        => int: foriegn key references id from user table
todo_number    => int: item number of TODO item
todo_note      => text: the details of the TODO event
todo_staus     => text: status of the event (TODO, In Progress, complete)
todo_duedate   => text: duedate of TODO item
date_added     => text: date the TODO was added
date_modified  => text: last modification to TODO
date_completed => text: date to appear when completed.
 
"""

import sqlite3
from sqlite3 import Error
import os
from datetime import datetime

class Database:
    def __init__(self) -> None:
        self.cwd = os.getcwd()
        self.database_file = f'{self.cwd}/data/database.db'

        # statements to create tables
        self.user_table = """CREATE TABLE IF NOT EXISTS users (
                                id integer PRIMARY KEY,
                                name text NOT NULL UNIQUE,
                                create_date text
                             );"""
        self.todo_table = """CREATE TABLE IF NOT EXISTS todolist (
                                id integer PRIMARY KEY,
                                user_id integer NOT NULL,
                                todo_number integer,
                                todo_note text NOT NULL,
                                todo_status text NOT NULL,
                                todo_duedate text NOT NULL,
                                date_added text NOT NULL,
                                date_modified text,
                                date_completed text,
                                FOREIGN KEY (user_id) REFERENCES users (id)
                             );"""

        self.tables = [self.user_table, self.todo_table]

    def create_connection(self, db_file):
        """
        Create databases and a connection to the database.
        Return a connection to the database.
        :param db_file: the desired disk location of the database.
        :return: conn: the connection to the database referenced by future calls.
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        return conn

    def create_table(self, conn, table):
        """
        Create a table in the connected database.
        :param conn: This is connection to the database created in create_connection()
        :param table: This is the command to create the table.
        """
        try:
            c = conn.cursor()
            c.execute(table)
        except Error as e:
            print(e)

    def user_exists(self, conn, user):
        """
        Checks to see if a user exists.
        :param conn: This is connection to the database created in create_connection()
        :param user: This is the user name of a user that we are checking for.
        :return: This will return None unless a user is found then it will return the username.
        """
        try:
            cur = conn.cursor()
            cur.execute("SELECT name from users WHERE name=?", (user,))
            rows = cur.fetchall()
            if len(rows) == 0:
                return None
            else:
                return rows[0][0]
        except Error as e:
            print(e)
            return None

    def user_id(self, conn, user):
        """
        Finds the user_id (integer) of a user based upon their username.
        :param conn: This is connection to the database created in create_connection()
        :param user: This is the username of the user we need the ID for.
        :return: integer value of the user id.
        """
        try:
            cur = conn.cursor()
            cur.execute("SELECT * from users WHERE name=?", (user,))
            rows = cur.fetchall()
            return rows[0][0]
        except Error as e:
            print(e)
            return None

    def get_notes(self, conn, user):
        """
        Queries the DB and returns the TODO entries of a user.
        :param conn: This is connection to the database created in create_connection()
        :param user: This is the username.
        :return: TODO items of the user.
        """
        sql = """SELECT
                    id,
                    user_id,
                    todo_note,
                    todo_status,
                    todo_duedate,
                    date_added,
                    date_modified,
                    date_completed
                 FROM 
                    todolist
                 WHERE
                    user_id=?
              """
        try:
            cur = conn.cursor()
            user_id = self.user_id(conn, user)
            cur.execute(sql, (user_id,))
            rows = cur.fetchall()
            return rows
        except Error as e:
            print(e)
            return None

    def get_notes_by_status(self, conn, user, status):
        """
        gets a list of notes of a set user at a set status.
        :param conn: This is connection to the database created in create_connection()
        :param user: This is the username of a user. 
        :param status: This is the status we want to query for. 
        :returns: list of notes with a status. 
        """
        cur = conn.cursor()
        user_id = self.user_id(conn, user)
        # TODO: refine the * query to be exactly what I want. 
        old_sql = "SELECT * from todolist WHERE user_id=? AND todo_status=?"
        sql = """ SELECT 
                     id,
                     user_id,
                     todo_note,
                     todo_status,
                     todo_duedate,
                     date_added,
                     date_modified,
                     date_completed
                  FROM
                     todolist
                  WHERE
                     userid=?
                  AND
                     todostatus=?
              """
        try:
            cur.execute(sql, (user_id, status,))
            rows = cur.fetchall()
            return rows
        except Error as e:
            print(e)
            return None

    def add_user(self, conn, user, time):
        """
        This adds a user to the user table. 
        :param conn: This is connection to the database created in create_connection()
        :param user: This is the username for the user. 
        :param time: This is the time of creation for the account. 
        """
        sql = """INSERT INTO users(name, create_date)
                 VALUES(?,?)"""
        try:
            values = (user, time)
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()
            return cur.lastrowid
        except Error as e:
            print(e)
            return None

    def add_note(self, conn, user, note, time, duedate):
        """
        Adds a TODO note to the todolist table
        :param conn: This is connection to the database created in create_connection()
        :param user: This is the username. Used to find the user_id of the user for the note.
        :param note: This is the note the user is making.
        :param time: This is the datetime to track when it was created. 
        """
        sql = """INSERT INTO 
                    todolist(
                        user_id, 
                        todo_note, 
                        todo_status, 
                        todo_duedate, 
                        date_added, 
                        date_modified)
                 VALUES(?,?,?,?,?,?)"""
        user_id = self.user_id(conn, user)
        values = (user_id, note, "New", duedate, time, time)
        try:
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()
            return cur.lastrowid
        except Error as e:
            print(e)
            return None

    def update_status(self, conn, user, note_id, status):
        """
        Updates the status and date modified of an item. 
        :param conn: This is connection to the database created in create_connection()
        :param user: This is the username. Used to find the user_id of the user for the note.
        :param note_id: This is the note id fo the todolist table in sqlite.
        :param status: this is the new status we want the ticket to be. 
        """
        time = datetime.now()
        sql_check_status = '''SELECT
                                  todo_status
                              FROM
                                  todolist
                              WHERE
                                  id=?
                              AND
                                  user_id=?
                           '''
        sql_update = '''UPDATE
                            todolist
                        SET
                            todo_status=?,
                            date_modified=?
                        WHERE
                            id=?
                        AND
                            user_id=?
                     '''
        current_status = ""
        cur = conn.cursor()
        try:
            user_id = self.user_id(conn, user)
            cur.execute(sql_check_status, (note_id, user_id,))
            current_status = cur.fetchall()
            current_status = current_status
        except Error as e:
            print(e)
            return None

        if status != current_status:
            print(f"modifying old status {current_status} to {status}")
            values = (status, time, note_id, user_id)
            try:
                cur.execute(sql_update, values)
                conn.commit()
            except Error as e:
                print(e)
                return None
            try:
                cur.execute(sql_check_status, (note_id, user_id,))
                current_status = cur.fetchall()
                return current_status
            except Error as e:
                print(e)
                return None
        else:
            print("not Modifying")
            return f"current status: {current_status} is same as new status {status}."
        