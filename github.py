import requests
import json
import httplib
import string

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
    
debug = 1
    
def debug_mode(value):
    
    print "Debug mode is " + value
    
    if string.upper(value) == "ON":
        debug = 1
    if  string.upper(value) == "OFF":
        debug = 0

def errors_requests(value):
    if value.headers['x-ratelimit-remaining'] > 0:
        return 0
    return -1        

def create_team(team_name,permission = 'pull',repo_name = ''):
    """
    create_team(team_name, permission, repo_name)
    Use this function to create team in your organization
    team_name - Required string
    permission - Optional string
        pull - team members can pull, but not push or administer this repositories. Default
        push - team members can pull and push, but not administer this repositores.
        admin - team members can pull, push and administer these repositories
    repo_name - Optional string
    """
    reqq = 'orgs/%s/teams' % org_name
    url = host + reqq
    r = requests.post(url,auth = (login,password),\
data = '{"name":"%s", "repo_names":["%s/%s"], "permission":"%s"}' \
% (team_name,org_name,repo_name,permission))
    if (errors_requests(r)==0)&(r.status_code == httplib.CREATED):  
        return 0
    else: 
        if debug == 1:
            print r.headers         
        
        return -1

def create_repo(repo_name,private = 'false',description = ''):
    """
    create_repo(repo_name,private,description)
    Use this function to create repository and 3 teams (*, *-guests, *-owners) in your organization
	repo_name - Required string
	private - Optional string. true to create a private repository, false to create a public one. Default is false.
	description - Optional string
    """
    reqq='orgs/%s/repos' % (org_name)
    url = host + reqq
    r = requests.post(url, auth=(login,password),\
    data = '{"name":"%s","private":"%s","description":"%s"}' \
    % (repo_name,private,description))
    if (errors_requests(r)==0)&(r.status_code == httplib.CREATED):
        # creating 3 teams
        create_team(repo_name,'pull',repo_name)
        create_team(repo_name+'-guests','push',repo_name)
        create_team(repo_name+'-owners','admin',repo_name)
        return 0
    else:
        if debug == 1:
            print r.headers      
        
        return -1

#search id_team by name
def search_id_team(team_name):
    reqq = 'orgs/%s/teams' % org_name
    url = host + reqq
    r = requests.get(url, auth = (login,password))
    if (errors_requests(r)==0)&(r.status_code == httplib.OK):
        cont = json.loads(r.content)
        i = 0
        result = 0
        for i in range (len(cont) - 1):
            if cont[i]['name'] == team_name:
                result = cont[i]['id']
                break            
    else:
        print debug
        if debug == 1:
            print r.headers         
        
        return -1
        
    if  result != 0:
        return result
    else:    
        return -1

#add user to team
def add_user_to_team(user,team_name):
    team_id = search_id_team(team_name)
    if team_id == -1:
        return -1
    reqq = 'teams/%d/members/%s' % (team_id,user)
    url = host + reqq
    r = requests.put(url,auth = (login,password),data = '{"login":"%s"}' % user)
    if (errors_requests(r)==0)&(r.status_code == httplib.NO_CONTENT):  #204
        return 0
    else:
        if debug == 1:
            print r.headers          
 
        return -1

#delete from team
def del_user_from_team(user,team_name):
    if search_id_team(team_name) == -1:
        return -1
    reqq = 'teams/%d/members/%s' % (search_id_team(team_name),user)
    url = host + reqq
    r = requests.delete(url, auth = (login,password))
    if (errors_requests(r)==0)&(r.status_code == httplib.NO_CONTENT):  #204
        return 0
    else:
        if debug == 1:
            print r.headers           
            
        return -1

#delete user from org
def del_user_from_org(user):
    reqq = 'orgs/%s/members/%s' % (org_name,user)
    url = host + reqq
    r = requests.delete(url,auth = (login,password))
    if (errors_requests(r)==0)&(r.status_code == httplib.NO_CONTENT): #204
        return 0
    else:
        if debug == 1:
            print r.headers       
            
        return -1
