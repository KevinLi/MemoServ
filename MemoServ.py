#!/usr/bin/env python

import os
import sys
import time

import Database

# Todo: reset id numbers when memos are deleted

if __name__ == "__main__":
	if "inbox.db" not in os.listdir("."):
		with open("inbox.db", "w") as x: pass
	db = Database.MemoServDatabase()
	
	if len(sys.argv) > 1:
		if sys.argv[1] == "read":
			if len(sys.argv) == 3:
				if sys.argv[2] == "new":
					unreadMemos = db.getNewMemos()
					for memo in unreadMemos:
						print("Memo {0} from {1} ({2})".format(memo[0], memo[2], time.ctime(int(memo[4]))))
						print(memo[3])
						db.setRead(memo[0])
				elif sys.argv[2] == "last":
					lastMemo = db.getLastMemo()
					for memo in lastMemo:
						print("Memo {0} from {1} ({2})".format(memo[0], memo[2], time.ctime(int(memo[4]))))
						print(memo[3])
						db.setRead(memo[0])
				else:
					try:
						toRead = [int(i) for i in sys.argv[2].split(",")]
						for x in xrange(len(toRead)):
							memo = db.readMemo(toRead[x])
							for item in memo:
								print("Memo {0} from {1} ({2}).".format(item[0], item[2], time.ctime(int(item[4]))))
								print(item[3])
							db.setRead(item[0])
					except ValueError:
						print("Syntax: READ {list | LAST | NEW}")
			else:
				print("Syntax: READ {list | LAST | NEW}")
		elif sys.argv[1] == "send":
			if len(sys.argv) <= 2:
				print("Syntax: SEND username memo-text")
			else:
				db.sendMemo(sys.argv[2], " ".join(sys.argv[3:]))
		elif sys.argv[1] == "del":
			print(sys.argv)
			if len(sys.argv) == 3:
				try:
					db.delMemo(int(sys.argv[2]))
				except ValueError: # Not an integer
					if type(sys.argv[2]) == list:
						for i in sys.argv[2]:
							db.delMemo(i)
					elif sys.argv[2] == "all":
						db.delMemo("ALL")
			else:
				print("Syntax: DEL {num | list | ALL}")
		elif sys.argv[1] == "list":
			if len(sys.argv) == 3:
				if sys.argv[2] == "new":
					unread = db.getNewMemos()
					for item in unread:
						print("* {0:2} {1:10} {2}".format(item[0], item[2], time.ctime(int(item[4]))))
				else:
					print("Syntax: LIST [list | NEW]")
			elif len(sys.argv) > 3:
				print("Syntax: LIST [list | NEW]")
			else:
				memos = db.listMemos()
				for item in memos:
					print("{0} {1:2} {2:10} {3}".format("*" if int(item[1])==1 else " ", item[0], item[2], time.ctime(int(item[4]))))
	else:
		print(
			"MemoServ is a utility allowing users to send short messages to one another.\n\n"\
			"SEND    Send a memo to a nick or channel"\
			"LIST    Lists memos\n"\
			"READ    Read a memo or memos\n"\
			"DEL     Delete a memo or memos\n")
		sys.exit()