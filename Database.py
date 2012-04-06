#!/usr/bin/env python

import sys
import os
import time
import sqlite3

if __name__ == "__main__":
	print("Nope")
	sys.exit(0)

class MemoServDatabase(object):
	def __init__(self):
		self.databaseConnection = sqlite3.connect("inbox.db", check_same_thread=False)
		self.database = self.databaseConnection.cursor()
		self.checkDatabase()
		
	def checkDatabase(self):
		try:
			self.database.execute("SELECT * FROM "+os.getlogin()+";")
		except sqlite3.OperationalError:
		# Table does not exist for this user, so create one.
			self.database.execute(
				"CREATE TABLE "+os.getlogin()+" (id INTEGER PRIMARY KEY, unread INTEGER, "\
				"sender TEXT, content TEXT, timestamp INTEGER);")
			self.databaseConnection.commit()

	def getNewMemos(self):
		self.database.execute("SELECT * FROM "+os.getlogin()+" WHERE unread=1;")
		return self.database
	def listMemos(self):
		self.database.execute("SELECT * FROM "+os.getlogin()+";")
		return self.database
	def getLastMemo(self):
		self.database.execute("SELECT MAX(id) FROM "+os.getlogin()+";")
		self.database.execute("SELECT * FROM "+os.getlogin()+" WHERE id=:id;", {
			"id":[i for i in self.database][0][0]})
		return self.database

	def readMemo(self, id):
		return self.database.execute("SELECT * FROM "+os.getlogin()+" WHERE id=:id;", {
			"id":id})
	def setRead(self, id):
		self.database.execute("UPDATE "+os.getlogin()+" SET unread=0 WHERE id=:id;", {
			"id":id})
		self.databaseConnection.commit()

	def sendMemo(self, recipient, content):
		self.database.execute(
			"INSERT INTO "+recipient+" VALUES (NULL, 1, :user, :content, :timestamp);", {
				"user":os.getlogin(),
				"content":content,
				"timestamp":str(time.time()).split(".")[0]})
		self.databaseConnection.commit()

	def delMemo(self, id):
		if id == "ALL":
			self.database.execute("DELETE FROM "+os.getlogin()+" WHERE id;")
		else:
			self.database.execute("DELETE FROM "+os.getlogin()+" WHERE id=:id;", {
					"id":id})
		self.databaseConnection.commit()
		