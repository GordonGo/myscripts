#!/usr/bin/python 
#coding:utf-8 

import json
import urllib2
from urllib2 import URLError
import sys
import argparse


class zabbix_api:
	def __init__(self):
		self.url = 'http://zabbix3.51xianqu.net/api_jsonrpc.php' #修改URL
		self.header = {"Content-Type":"application/json"}
		self.user = 'zabbix_admin' #修改用户名
		self.passwd = '18d389cc7bbc7f624de6647441783592' #修改密码


	def user_login(self):
		data = json.dumps({
		"jsonrpc": "2.0",
		"method": "user.login",
		"params": {
		"user": self.user,
		"password": self.passwd
		},
		"id": 0
		})

		request = urllib2.Request(self.url, data)
		for key in self.header:
			request.add_header(key, self.header[key])

		try:
			result = urllib2.urlopen(request)
		except URLError as e:
			print ("\033[041m 用户认证失败，请检查 !\033[0m", e.code)
		else:
			response = json.loads(result.read())
			result.close()
			#print response['result']
			self.authID = response['result']
			return self.authID

	def proxy_get(self,hostName=''):
		data=json.dumps({
		"jsonrpc": "2.0",
		"method": "proxy.get",
		"params": {
		"output": "extend",
		"selectInterface": "extend"
		},
		"auth": self.user_login(),
		"id": 1
		})
		request = urllib2.Request(self.url,data)
		for key in self.header:
			request.add_header(key, self.header[key])

		try:
			result = urllib2.urlopen(request)
		except URLError as e:
			if hasattr(e, 'reason'):
				print 'We failed to reach a server.'
				print 'Reason: ', e.reason
			elif hasattr(e, 'code'):
				print 'The server could not fulfill the request.'
				print 'Error code: ', e.code
		else:
			response = json.loads(result.read())
			print response
			result.close()
			print "主机数量: \033[31m%s\033[0m"%(len(response['result']))
		for host in response['result']:
			print "ProxyId : \033[31m%s\033[0m\t HostName : \033[31m%s\033[0m\t "%(host['proxyid'],host['host'])

	def host_get(self,hostName=''):
		data=json.dumps({
		"jsonrpc": "2.0",
		"method": "host.get",
		"params": {
		"output": "extend",
		"filter":{"host":hostName}
		},
		"auth": self.user_login(),
		"id": 1
		})
		request = urllib2.Request(self.url,data)
		for key in self.header:
			request.add_header(key, self.header[key])


		try:
			result = urllib2.urlopen(request)
		except URLError as e:
			if hasattr(e, 'reason'):
				print 'We failed to reach a server.'
				print 'Reason: ', e.reason
			elif hasattr(e, 'code'):
				print 'The server could not fulfill the request.'
				print 'Error code: ', e.code
		else:
			response = json.loads(result.read())
			#print response
			result.close()
			print "主机数量: \033[31m%s\033[0m"%(len(response['result']))
			for host in response['result']:
				status={"0":"OK","1":"Disabled"}
				available={"0":"Unknown","1":"available","2":"Unavailable"}
				#print host
				if len(hostName)==0:
					print "HostID : %s\t HostName : %s\t Status :\033[32m%s\033[0m \t Available :\033[31m%s\033[0m"%(host['hostid'],host['name'],status[host['status']],available[host['available']])
				else:
					print "HostID : %s\t HostName : %s\t Status :\033[32m%s\033[0m \t Available :\033[31m%s\033[0m"%(host['hostid'],host['name'],status[host['status']],available[host['available']])
					return host['hostid']

	def hostgroup_get(self, hostgroupName=''):
		data = json.dumps({
		"jsonrpc":"2.0",
		"method":"hostgroup.get",
		"params":{
		"output": "extend",
		"filter": {
		"name": hostgroupName
		}
		},
		"auth":self.user_login(),
		"id":1,
		})

		request = urllib2.Request(self.url,data)
		for key in self.header:
			request.add_header(key, self.header[key])

		try:
			result = urllib2.urlopen(request)
		except URLError as e:
			print "Error as ", e
		else:
			#print result.read()
			response = json.loads(result.read())
			result.close()
			#print response()
			for group in response['result']:
				if  len(hostgroupName)==0:
					print "hostgroup:  \033[31m%s\033[0m \tgroupid : %s" %(group['name'],group['groupid'])
				else:
					print "hostgroup:  \033[31m%s\033[0m\tgroupid : %s" %(group['name'],group['groupid'])
					self.hostgroupID = group['groupid']
					return group['groupid']

	def usergroup_get(self, usergroupName=''):
		data = json.dumps({
		"jsonrpc": "2.0",
		"method": "usergroup.get",
		"params": {
		"output": "extend",
		"status": 0
		},
		"auth": self.user_login(),
		"id": 1
		})
		request = urllib2.Request(self.url,data)
		for key in self.header:
			request.add_header(key, self.header[key])

		try:
			result = urllib2.urlopen(request)
		except URLError as e:
			print "Error as ", e
		else:
			#print result.read()
			response = json.loads(result.read())
			result.close()
			#print response
			for usergroup in response['result']:
				if  len(usergroupName)==0:
					print "usrgrpid: %s \tname: %s" %(usergroup['usrgrpid'],usergroup['name'])
				else:
					print "usergroup:  \033[31m%s\033[0m\tgroupid : %s" %(usergroup['name'],usergroup['groupid'])
					self.usergroupID = usergroup['usrgrpid']
					return usergroup['usrgrpid']

	def user_get(self, userName=''):
		data = json.dumps({
		"jsonrpc": "2.0",
		"method": "user.get",
		"params": {
		"output": "extend"
		},
		"auth": self.user_login(),
		"id": 1
		})

		request = urllib2.Request(self.url,data)
		for key in self.header:
			request.add_header(key, self.header[key])
		try:
			result = urllib2.urlopen(request)
		except URLError as e:
			print "Error as ", e
		else:
			#print result.read()
			response = json.loads(result.read())
			result.close()
			print response
			for user in response['result']:
				if  len(userName)==0:
					print "user: \033[042m %s \033[0m \t name: \033[042m %s \033[0m \t userid: \033[042m %s \033[0m" %(user['alias'],user['name'],user['userid'])
				else:
					self.userID = user['userid']
					return user['userid']

	def template_get(self,templateName=''):
		data = json.dumps({
		"jsonrpc":"2.0",
		"method": "template.get",
		"params": {
		"output": "extend",
		"filter": {
		"name":templateName
		}
		},
		"auth":self.user_login(),
		"id":1,
		})

		request = urllib2.Request(self.url, data)
		for key in self.header:
			request.add_header(key, self.header[key])

		try:
			result = urllib2.urlopen(request)
		except URLError as e:
			print "Error as ", e
		else:
			response = json.loads(result.read())
			result.close()
			#print response
			for template in response['result']:
				if len(templateName)==0:
					print "template : \033[31m%s\033[0m\t  id : %s" % (template['name'], template['templateid'])
				else:
					self.templateID = response['result'][0]['templateid']
					print "Template Name :  \033[31m%s\033[0m "%templateName
					return response['result'][0]['templateid']

	def hostgroup_create(self,hostgroupName):

		if self.hostgroup_get(hostgroupName):
			print "hostgroup  \033[42m%s\033[0m is exist !"%hostgroupName
			sys.exit(1)
		data = json.dumps({
		"jsonrpc": "2.0",
		"method": "hostgroup.create",
		"params": {
		"name": hostgroupName
		},
		"auth": self.user_login(),
		"id": 1
		})
		request=urllib2.Request(self.url,data)

		for key in self.header:
			request.add_header(key, self.header[key])

		try:
			result = urllib2.urlopen(request)
		except URLError as e:
			print "Error as ", e
		else:
			response = json.loads(result.read())
			result.close()
			print "\033[042m 添加主机组:%s\033[0m  hostgroupID : %s"%(hostgroupName,response['result']['groupids'])

	def usergroup_create(self,usergroupName):
		data = json.dumps({
		"jsonrpc": "2.0",
		"method": "usergroup.create",
		"params": {
		"name": usergroupName,
		"rights": {
		"permission": 1,
		"id": "2"
		},
		},
		"auth": self.user_login(),
		"id": 1
		})
		request=urllib2.Request(self.url,data)

		for key in self.header:
			request.add_header(key, self.header[key])

		try:
			result = urllib2.urlopen(request)
		except URLError as e:
			print "Error as ", e
		else:
			response = json.loads(result.read())
			result.close()
			#print response
			print "\033[042m 添加用户组:%s\033[0m \t 用户组ID : %s"%(usergroupName,response['result']['usrgrpids'])

	def host_create(self, hostip, hostname , hostgroupName, templateName , rmiPort , tomcatAppName ,tomcatHttpPort):
		if self.host_get(hostip):
			print "\033[041m该主机已经添加!\033[0m"
			sys.exit(1)

		group_list=[]
		template_list=[]
		macro_list=[]
		for i in hostgroupName.split(','):
			var = {}
			var['groupid'] = self.hostgroup_get(i)
			group_list.append(var)
		for i in templateName.split(','):
			var={}
			var['templateid']=self.template_get(i)
			template_list.append(var)

		data = json.dumps({
		"jsonrpc":"2.0",
		"method":"host.create",
		"params":{
		"host": hostname,
		"proxy_hostid": "10218",
		"interfaces": [
			{
			"type": 1,
			"main": 1,
			"useip": 1,
			"ip": hostip,
			"dns": "",
			"port": "10050"
			},
			{
			"type": 4,
			"main": 1,
			"useip": 1,
			"ip": hostip,
			"dns": "",
			"port": rmiPort
			}
		],
		"groups": group_list,
		"templates": template_list,
		"macros": [
			{
			"macro": "{$APP_NAME}",
			"value": tomcatAppName
			},
			{
			"macro": "{$HTTP_PORT}",
			"value": tomcatHttpPort
			}
		]
		},
		"auth": self.user_login(),
		"id":1
		})
		request = urllib2.Request(self.url, data)
		for key in self.header:
			request.add_header(key, self.header[key])

		try:
			result = urllib2.urlopen(request)
		except URLError as e:
			print "Error as ", e
		else:
			response = json.loads(result.read())
			result.close()
			print response
			print "添加主机 : \033[042m %s \033[0m \tid :%s" % (hostip, response['result']['hostids'])
			#print "添加主机 : \033[042m %s \033[0m \tid :%s" % (hostip, hostids)

	def mysql_host_create(self, hostip, hostname,hostgroupName,templateName ):
		if self.host_get(hostip):
			print "\033[041m该主机已经添加!\033[0m"
			sys.exit(1)
		group_list=[]
		template_list=[]
		macro_list=[]
		for i in hostgroupName.split(','):
			var = {}
			var['groupid'] = self.hostgroup_get(i)
			group_list.append(var)
		for i in templateName.split(','):
			var={}
			var['templateid']=self.template_get(i)
			template_list.append(var)
		data = json.dumps({
		"jsonrpc":"2.0",
		"method":"host.create",
		"params":{
		"host": hostname,
		"proxy_hostid": "10218",
		"interfaces": [
			{
			"type": 1,
			"main": 1,
			"useip": 1,
			"ip": hostip,
			"dns": "",
			"port": "10050"
			}
		],
		"groups": group_list,
		"templates": template_list,
		"macros": [
			{
			"macro": "{$PROCESS_NAME}",
			"value": "mysqld"
			},
			{
			"macro": "{$PROCESS_CMDLINE}",
			"value": "mysqld"
			}
		]
		},
		"auth": self.user_login(),
		"id":1
		})
		request = urllib2.Request(self.url, data)
		for key in self.header:
			request.add_header(key, self.header[key])

		try:
			result = urllib2.urlopen(request)
		except URLError as e:
			print "Error as ", e
		else:
			response = json.loads(result.read())
			result.close()
			print response
			print "添加主机 : \033[042m %s \033[0m \tid :%s" % (hostip, response['result']['hostids'])
			#print "添加主机 : \033[042m %s \033[0m \tid :%s" % (hostip, hostids)

	def redis_host_create(self, hostip, hostname,hostgroupName,templateName ):
		if self.host_get(hostip):
			print "\033[041m该主机已经添加!\033[0m"
			sys.exit(1)
		group_list=[]
		template_list=[]
		macro_list=[]
		for i in hostgroupName.split(','):
			var = {}
			var['groupid'] = self.hostgroup_get(i)
			group_list.append(var)
		for i in templateName.split(','):
			var={}
			var['templateid']=self.template_get(i)
			template_list.append(var)
		data = json.dumps({
		"jsonrpc":"2.0",
		"method":"host.create",
		"params":{
		"host": hostname,
		"proxy_hostid": "10218",
		"interfaces": [
			{
			"type": 1,
			"main": 1,
			"useip": 1,
			"ip": hostip,
			"dns": "",
			"port": "10050"
			}
		],
		"groups": group_list,
		"templates": template_list,
		"macros": [
			{
			"macro": "{$PROCESS_NAME}",
			"value": "redis-server"
			},
			{
			"macro": "{$PROCESS_CMDLINE}",
			"value": "redis-server"
			}
		]
		},
		"auth": self.user_login(),
		"id":1
		})
		request = urllib2.Request(self.url, data)
		for key in self.header:
			request.add_header(key, self.header[key])

		try:
			result = urllib2.urlopen(request)
		except URLError as e:
			print "Error as ", e
		else:
			response = json.loads(result.read())
			result.close()
			print response
			print "添加主机 : \033[042m %s \033[0m \tid :%s" % (hostip, response['result']['hostids'])
			#print "添加主机 : \033[042m %s \033[0m \tid :%s" % (hostip, hostids)


	def user_create(self, user, name,usrgrpid , sms):
		data = json.dumps({
		"jsonrpc": "2.0",
		"method": "user.create",
		"params": {
		"alias": user,
		"name": name ,
		"passwd": "",
		"usrgrps": [
			{
			"usrgrpid": usrgrpid
			}
		],
		"user_medias": [
			{
			"mediatypeid": "1",
			"sendto": user+"@51xianqu.net",
			"active": 0,
			"severity": 48,
			"period": "1-7,00:00-24:00"
			},
		    {
			"mediatypeid": "3",
			"sendto": sms,
			"active": 0,
			"severity": 48,
			"period": "1-7,00:00-24:00"
			}
		]
		},
		"auth": self.user_login(),
		"id": 1
		})
		request = urllib2.Request(self.url, data)
		for key in self.header:
			request.add_header(key, self.header[key])

		try:
			result = urllib2.urlopen(request)
		except URLError as e:
			print "Error as ", e
		else:
			response = json.loads(result.read())
			result.close()
			print response
			#print "添加主机 : \033[042m %s \033[0m \tid :%s" % (hostip, response['result']['hostids'])


	def host_disable(self,hostip):
		data=json.dumps({
		"jsonrpc": "2.0",
		"method": "host.update",
		"params": {
		"hostid": self.host_get(hostip),
		"status": 1
		},
		"auth": self.user_login(),
		"id": 1
		})
		request = urllib2.Request(self.url,data)
		for key in self.header:
			request.add_header(key, self.header[key])
		try:
			result = urllib2.urlopen(request)
		except URLError as e:
			print "Error as ", e
		else:
			response = json.loads(result.read())
			result.close()
			print '----主机现在状态------------'
			print self.host_get(hostip)

	def host_delete(self,hostid):
		hostid_list=[]
		#print type(hostid)
		for i in hostid.split(','):
			var = {}
			var['hostid'] = self.host_get(i)
			hostid_list.append(var)
		data=json.dumps({
		"jsonrpc": "2.0",
		"method": "host.delete",
		"params": hostid_list,
		"auth": self.user_login(),
		"id": 1
		})

		request = urllib2.Request(self.url,data)
		for key in self.header:
			request.add_header(key, self.header[key])

		try:
			result = urllib2.urlopen(request)
		except Exception,e:
			print  e
		else:

			result.close()
			print "主机 \033[041m %s\033[0m  已经删除 !"%hostid

# def user_create(self, user, usrgrpid , sms):
if __name__ == "__main__":
	zabbix=zabbix_api()
	parser=argparse.ArgumentParser(description='zabbix  api ',usage='%(prog)s [options]')
	parser.add_argument('-H','--host',nargs='?',dest='listhost',default='host',help='查询主机')
	parser.add_argument('-P','--proxy',nargs='?',dest='listproxy',default='proxy',help='查询代理')
	parser.add_argument('-G','--group',nargs='?',dest='listgroup',default='group',help='查询主机组')
	parser.add_argument('-U','--user',nargs='?',dest='listuser',default='user',help='查询用户')
	parser.add_argument('-g','--usergroup',nargs='?',dest='listusergroup',default='usergroup',help='查询用户组')
	parser.add_argument('-T','--template',nargs='?',dest='listtemp',default='template',help='查询模板信息')
	parser.add_argument('-A','--add-group',nargs=1,dest='addgroup',help='添加主机组')
	parser.add_argument('-C','--add-host',dest='addhost',nargs=7,metavar=('host_ip','host_name','group','template','rmi_port','tomcat_app_name','tomcat_http_port'),help='添加主机,多个主机组或模板使用分号')
	parser.add_argument('-M','--add-mysql-host',dest='addmysqlhost',nargs=4,metavar=('host_ip','host_name','group','template'),help='添加MYSQL主机,多个主机组或模板使用分号')
	parser.add_argument('-R','--add-redis-host',dest='addredishost',nargs=4,metavar=('host_ip','host_name','group','template'),help='添加REDIS主机,多个主机组或模板使用分号')
	parser.add_argument('-u','--add-user',dest='adduser',nargs=4,metavar=('user','name','usrgrpid','sms'),help='添加用户')
	parser.add_argument('-s','--add-usergroup',dest='addusergroup',nargs=1,metavar=('usergroupname'),help='添加用户组')
	parser.add_argument('-d','--disable',dest='disablehost',nargs=1,metavar=('192.168.2.1'),help='禁用主机')
	parser.add_argument('-D','--delete',dest='deletehost',nargs='+',metavar=('192.168.2.1'),help='删除主机,多个主机之间用分号')
	parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0')
	if len(sys.argv)==1:
		print parser.print_help()
	else:
		args=parser.parse_args()

		if args.listhost != 'host' :
			if args.listhost:
				zabbix.host_get(args.listhost)
			else:
				zabbix.host_get()
		if args.listproxy != 'proxy' :
			if args.listproxy:
				zabbix.proxy_get(args.listproxy)
			else:
				zabbix.proxy_get()
		if args.listgroup !='group':
			if args.listgroup:
				zabbix.hostgroup_get(args.listgroup)
			else:
				zabbix.hostgroup_get()
		if args.listuser !='user':
			if args.listuser:
				zabbix.user_get(args.listuser)
			else:
				zabbix.user_get()
		if args.listusergroup !='usergroup':
			if args.listusergroup:
				zabbix.usergroup_get(args.listusergroup)
			else:
				zabbix.usergroup_get()
		if args.listtemp != 'template':
			if args.listtemp:
				zabbix.template_get(args.listtemp)
			else:
				zabbix.template_get()
		if args.addgroup:
			zabbix.hostgroup_create(args.addgroup[0])
		if args.addusergroup:
			zabbix.usergroup_create(args.addusergroup[0])
		if args.adduser:
			zabbix.user_create(args.adduser[0], args.adduser[1], args.adduser[2],args.adduser[3])
		if args.disablehost:
			zabbix.host_disable(args.disablehost)
		if args.deletehost:
			zabbix.host_delete(args.deletehost[0])
		# 添加主机
		if args.addhost:
			zabbix.host_create(args.addhost[0], args.addhost[1], args.addhost[2],args.addhost[3],args.addhost[4],args.addhost[5],args.addhost[6])
		# 添加mysql主机
		if args.addmysqlhost:
			zabbix.mysql_host_create(args.addmysqlhost[0], args.addmysqlhost[1], args.addmysqlhost[2],args.addmysqlhost[3])
		# 添加redis主机
		if args.addredishost:
			zabbix.redis_host_create(args.addredishost[0], args.addredishost[1], args.addredishost[2],args.addredishost[3])

