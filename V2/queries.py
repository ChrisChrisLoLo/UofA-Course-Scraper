#!/usr/bin/env python3

"""
Christian Lo (clo1), Kelly Luc (kluc1), Tem Tamre (ttamre)

Contains the functions that clear and initialize the database to be used
"""

import sqlite3
import time

# Establish a connection to the database and return the connection and a cursor
def connect(path):
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return connection, cursor

# Drop all tables in the given database
def drop_tables(connection, cursor):
    drop_query= '''
	            drop table if exists sections;
                drop table if exists courses;
                drop table if exists subjects;
                drop table if exists faculties;
                '''
    cursor.executescript(drop_query)
    connection.commit()
    return


# Define and create tables in the given databse
def define_tables(connection, cursor):
    table_query = '''
        PRAGMA foreign_keys = ON;
        
        create table faculties (
        name    char(60),
        primary key (name)
        );

        create table subjects (
        name            char(120),
		code			char(6),
        faculty         char(60),
        primary key (code),
        foreign key (faculty) references faculties
		on delete cascade
        );

        create table courses (
		code            char(10),
		name            char(120),
        description     char(1600),
        subject         char(6),
        primary key (code),
        foreign key (subject) references subjects
		on delete cascade
        );
        
        create table sections (
        id              int,
        sectionType     char(3),
        sectionCode     char(4),
        daysOffered     char(7),
        roomLocation    char(15),
        instructorEmail char(254),
        termOffered     char(6),
        yearOffered     int,
        subject         char(6),
        course          char(120),
        primary key (id),
        foreign key (course) references courses
		on delete cascade
        );

        '''
    cursor.executescript(table_query)
    connection.commit()
    return

def insertFaculty(connection,cursor,facultyName):
	print(facultyName)
	print(type(facultyName))
	cursor.execute('''
					insert into faculties values
					(?);
					''',(facultyName,))
	connection.commit()

def insertSubject(connection,cursor,subjectName,subjectCode,faculty):
	cursor.execute('''
					insert into subjects values
					(?,?,?);
					''',(subjectName,subjectCode,faculty))
	connection.commit()

def insertCourse(connection,cursor,courseCode,courseTitle,courseSummary,subject):
	cursor.execute('''
					insert into courses values
					(?,?,?,?);
					''',(courseCode,courseTitle,courseSummary,subject))
	connection.commit()
