import requests
import json
try:
    f = open('conf','r')
except IOError:
    print "File 'conf' not found"
    exit()
lin = f.readlines()
f.close()
st = lin[0].split("=")[1]
login = st[0:len(st)-1]
st = lin[1].split("=")[1]
passw = st[0:len(st)-1]
st = lin[2].split("=")[1]
org_name = st[0:len(st)-1]
host = 'https://api.github.com/'


#create team
def create_team(team_name,permission,repo_name):
	reqq = 'orgs/%s/teams' % org_name
	url = host + reqq
	r = requests.post(url,auth = (login,passw),data = '{"name":"%s", "repo_names":["%s/%s"], "permission":"%s"}' % (team_name,org_name,repo_name,permission))
	if r.status_code != 201:
		res = "Error "+ r.headers['status']
	else:
		res = "%s was created" % team_name
	return res

# create repo
def create_repo(repo_name,private,description):
    reqq='orgs/%s/repos' % (org_name)
    url = host + reqq
    r = requests.post(url, auth=(login,passw),data = '{"name":"%s","private":"%s","description":"%s"}' % (repo_name,private,description))
    if r.status_code == 201:
        res = "Done! Repo %s created" % repo_name
        # creating 3 teams
        create_team(repo_name,'pull',repo_name)
        create_team(repo_name+'-guests','push',repo_name)
        create_team(repo_name+'-owners','admin',repo_name)
    else:
        res = "Error "+ r.headers['status']
    return res

#search id_team by name
def search_id_team(team_name):
    reqq = 'orgs/%s/teams' % (org_name)
    url = host + reqq
    r = requests.get(url, auth = (login,passw))
    cont = json.loads(r.content)
    i = 0
    while 1:
        try:
            if cont[i]['name'] == team_name:
                break
            i += 1
        except:
            return "Team not found"
    return cont[i]['id']

#add user to team
def add_user_to_team(user,team_name):
	team_id = str(search_id_team(team_name))
	if team_id == "Team not found":
		return "Team not found"
	reqq = 'teams/%s/members/%s' % (team_id,user)
	url = host + reqq
	r = requests.put(url,auth = (login,passw),data = '{"login":"%s"}' % user)
	if r.status_code != 204:
		res = "Error "+ r.headers['status']
	else:
		res = "%s was added to team" % user
	return res

#delete from team
def del_user_from_team(user,team_name):
    if search_id_team(team_name) == "Team not found":
        return "Team not found"
    reqq = 'teams/%s/members/%s' % (str(search_id_team(team_name)),user)
    url = host + reqq
    r = requests.delete(url, auth = (login,passw))
    if r.status_code == 204:
        res = "User '" + user + "' was deleted from team " + team_name
    else:
        res = "Error "+ r.headers['status']
    return res

#delete user from org
def del_user_from_org(user):
	reqq = 'orgs/%s/members/%s' % (org_name,user)
	url = host + reqq
	r = requests.delete(url,auth = (login,passw))
	if r.status_code != 204:
		res = "Error "+ r.headers['status']
	else:
		res = user + " succesfully removed"
	return res
