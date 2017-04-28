import sqlite3
import matplotlib.pyplot as plt

def percent_issues_user(conn):
	cur = conn.cursor()
	# Getting the usser list
	cur.execute('select distinct(user) from event')
	items = cur.fetchall()
	users = [item.encode('utf-8') for i in items for item in i]
	issues = []
	for user in users:
		cur.execute("select count(issueID) from event where user = '%s'" %(user))
		res = cur.fetchone()
		issues.append(res[0])
	total = sum(issues)
	issues = [float(issue)/float(total) * 100 for issue in issues]
	print issues
	sizes = issues
	colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
	plt.pie(sizes, labels=users, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
	plt.axis('equal')
	plt.show()
def main():
	group1 = sqlite3.connect('group1.db')
	percent_issues_user(group1)


if __name__ == "__main__":
	main()
