import requests
import json
import httplib
f = open('conf.py','r')
from conf import password
from conf import login
from conf import org_name
host = 'https://api.github.com/'

def help():
    print
    print "        Function: create_team(team_name,permission,repo_name)"
    print "        Function: create_repo(repo_name,private,description)"
    print "        Function: search_id_team(team_name)"
    print "        Function: add_user_to_team(user,team_name)"
    print "        Function: del_user_from_team(user,team_name)"
    print "        Function: del_user_from_org(user)"
    print    
    
debug = 0;
    
def debug_mode(value):
    
    print "Debug mode is " + value;
    
    if string.upper(value) == "ON":
        debug = 1;
    
    if  string.upper(value) == "OFF":
        debug = 0;
    else:
        debug = -1; 

    


#create team
def create_team(team_name,permission="pull",repo_name=""):
    reqq = 'orgs/%s/teams' % org_name
    url = host + reqq
    r = requests.post(url,auth = (login,password),data = '{"name":"%s", "repo_names":["%s/%s"], "permission":"%s"}' % (team_name,org_name,repo_name,permission))
	if errors_requests(r)==-1:
		return -1
    if r.status_code == httplib.CREATED:  
        return 0
    else: 
        if debug == 1:
            print r.headers           
        
        return -1


# create repo
def create_repo(repo_name,private,description):
    reqq='orgs/%s/repos' % (org_name)
    url = host + reqq
    r = requests.post(url, auth=(login,password),data = '{"name":"%s","private":"%s","description":"%s"}' % (repo_name,private,description))
    if r.status_code == httplib.CREATED:    # ERROR 201
        create_team(repo_name,'pull',repo_name)
        create_team(repo_name+'-guests','push',repo_name)
        create_team(repo_name+'-owners','admin',repo_name)
        print "Done! Repo %s created" % repo_name
        return 0;
    else:
        if debug == 1:
            print r.headers      
        
        return -1

#search id_team by name
def search_id_team(team_name):
    reqq = 'orgs/%s/teams' % org_name;
    url = host + reqq;
    r = requests.get(url, auth = (login,password))
    if r.status_code == httplib.OK:
        cont = json.loads(r.content);
        i = 0;
        result = 0;
        for i in cont.count-1:
            if cont[i]['name'] == team_name:
                result = cont[i]['id']
                break;
            
    else:
        if debug == 1:
            print r.headers;           
        
        return -1;
        
    if  result != 0:
        return result;
    else:    
        return -1;

#add user to team
def add_user_to_team(user,team_name):
    team_id = search_id_team(team_name)
    if team_id == -1:
        return -1;
    reqq = 'teams/%d/members/%s' % (team_id,user)
    url = host + reqq
    r = requests.put(url,auth = (login,password),data = '{"login":"%s"}' % user)
    if r.status_code == httplib.NO_CONTENT:  #204
        print "%s was added to team" % user;
        return 0;
    else:
        if debug == 1:
            print r.headers;                      
        return -1

#delete from team
def del_user_from_team(user,team_name):
    if search_id_team(team_name) == -1:
        return -1;
    reqq = 'teams/%d/members/%s' % (search_id_team(team_name),user)
    url = host + reqq
    r = requests.delete(url, auth = (login,password))
    if r.status_code == httplib.NO_CONTENT:  #ERROR 204
        result = "User '" + user + "' was deleted from team " + team_name
        print result;
        return 0;
    else:
        if debug == 1:
            print r.headers;          
            
        return -1

#delete user from org
def del_user_from_org(user):
    reqq = 'orgs/%s/members/%s' % (org_name,user)
    url = host + reqq
    r = requests.delete(url,auth = (login,password))
    if r.status_code == httplib.NO_CONTENT: #ERROR 204
        result = "Error "+ r.headers['status']
        print result;
        return 0
    else:
        if debug == 1:
            print r.headers;     
            
        return -1
print create_team("fakeuser")
