import requests
import json
import httplib

try:
    f = open('conf.py','r')
except IOError:
    print "File 'conf' not found"
    exit()
from conf import password
from conf import login
from conf import org_name
host = 'https://api.github.com/'

#create team
def create_team(team_name,permission = 'pull',repo_name = ''):
	reqq = 'orgs/%s/teams' % org_name
	url = host + reqq
	r = requests.post(url,auth = (login,password),data = '{"name":"%s", "repo_names":["%s/%s"], "permission":"%s"}' % (team_name,org_name,repo_name,permission))
	if r.status_code == httplib.CREATED:
		res = "%s was created" % team_name
	else:
		res = r.status_code
	return res

# create repo
def create_repo(repo_name,private,description):
    reqq='orgs/%s/repos' % (org_name)
    url = host + reqq
    r = requests.post(url, auth=(login,password),data = '{"name":"%s","private":"%s","description":"%s"}' % (repo_name,private,description))
    if r.status_code == httplib.CREATED:
        res = "Repo %s created" % repo_name
        # creating 3 teams
        create_team(repo_name,'pull',repo_name)
        create_team(repo_name+'-guests','push',repo_name)
        create_team(repo_name+'-owners','admin',repo_name)
    else:
        res = r.status_code
    return res

#search id_team by name
def search_id_team(team_name):
	reqq = 'orgs/%s/teams' % org_name
	url = host + reqq
	r = requests.get(url, auth = (login,password))
	if r.status_code == httplib.OK:
		cont = json.loads(r.content)
		i = 0
		while 1:
			try:
				if cont[i]['name'] == team_name:
					break
				i += 1
			except:
				res = -1
			else:
				res = cont[i]['id']
	else:
		res = r.status_code
	return res

#add user to team
def add_user_to_team(user,team_name):
	team_id = search_id_team(team_name)
	if team_id == -1:
		return "Team not found"
	reqq = 'teams/%d/members/%s' % (team_id,user)
	url = host + reqq
	r = requests.put(url,auth = (login,password),data = '{"login":"%s"}' % user)
	if r.status_code == httplib.NO_CONTENT:
		res = "%s was added to team" % user
	else:
		res = r.status_code
	return res

#delete from team
def del_user_from_team(user,team_name):
    if search_id_team(team_name) == -1:
        return "Team not found"
    reqq = 'teams/%d/members/%s' % (search_id_team(team_name),user)
    url = host + reqq
    r = requests.delete(url, auth = (login,password))
    if r.status_code == httplib.NO_CONTENT:
        res = "User '" + user + "' was deleted from team " + team_name
    else:
        res = r.status_code
    return res

#delete user from org
def del_user_from_org(user):
	reqq = 'orgs/%s/members/%s' % (org_name,user)
	url = host + reqq
	r = requests.delete(url,auth = (login,password))
	if r.status_code == httplib.NO_CONTENT:
		res = user + " succesfully removed"
	else:
		res = r.status_code
	return res
