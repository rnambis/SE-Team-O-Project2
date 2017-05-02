import sqlite3
import matplotlib.pyplot as plt

def percent_issues_user(conn,name):
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
	#print issues
	sizes = issues
	colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
	plt.pie(sizes, labels=users, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
	plt.axis('equal')
	plt.savefig(name+'_issues_per_user')
	plt.show()

def comments_per_user(conn, name):
	cur = conn.cursor()
	cur.execute('select distinct(user) from comment')
	items = cur.fetchall()
	users = [item.encode('utf-8') for i in items for item in i]
	cur.execute('select distinct(issueID) from comment')
	issues_total = cur.fetchall()
	issues_total = [i for issue in issues_total for i in issue]
	width = 0.35
	cur.execute("select count(*), issueID from comment where user ='%s' group by issueID" %(users[0]))	
	items = cur.fetchall()
	y = []
	issues = {}
	for i in items:
		issues[i[1]] = i[0]

	for item in issues_total:
		if item in issues:
			y.append(issues[item])
		else:
			y.append(0)
	#print items
	color = ['blue','green','red','yellow','orange']
	k = 0
	j = -0.2
	fig = plt.figure()
	ax = plt.subplot(111)						
	for user in users:
		#print issues_total	
		cur.execute("select count(*), issueID from comment where user ='%s' group by issueID" %(user))	
		items = cur.fetchall()
		y = []
		issues = {}
		for i in items:
			issues[i[1]] = i[0]

		for item in issues_total:
			if item in issues:
				y.append(issues[item])
			else:
				y.append(0)
		#print issues_total
		#print "hello"
		temp = [float(x)+j for x in issues_total]		
		ax.bar(temp, y, width = 0.2, color = color[k], align = 'center', label = str(user))
		j+=0.2
		#plt.plot(issues_total, y, color = color[k])
		k+=1
	ax.set_ylabel('No of comments')
	ax.set_xlabel('Issue IDs')
	ax.set_title('No of comments per issue per user')
	ax.legend(loc='upper left')
	plt.show()
	
def main():
	group1 = sqlite3.connect('group1.db')
	#percent_issues_user(group1, 'group1')
	
	group2 = sqlite3.connect('group2.db')
	#percent_issues_user(group2,'group2')

	group3 = sqlite3.connect('group3.db')
	#percent_issues_user(group3,'group3')
	comments_per_user(group3,'group3')
if __name__ == "__main__":
	main()
