import requests
import json
import httplib

from conf import password
from conf import login
from conf import org_name
from conf import debug
from conf import type_pass
from conf import token

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
    
def print_debug(r):
    print r.headers
    print
    print r.content

def errors_requests(value):
    if value.headers['x-ratelimit-remaining'] > 0:
        return True
    return False

def connect(url,method = "get",data = ""):    
    if type_pass:
        #login pass
        methods={'get':   requests.get(url, auth = (login,password)),\
                 'post':  requests.post(url,auth = (login,password),data = data),\
                 'put':   requests.put(url,auth = (login,password),data = data),\
                 'delete':requests.delete(url, auth = (login,password))}    
    else:
        #token
        url = url + "?access_token=" + token
        methods={'get':   requests.get(url),\
                 'post':  requests.post(url, data = data),\
                 'put':   requests.put(url, data = data),\
                 'delete':requests.delete(url)}    
    return methods[method]

def create_team(team_name,permission = 'pull',repo_name = ''):
    """
    create_team(team_name, permission, repo_name)
    Use this function to create a team in your organization
    Input:
    team_name - Required string
    permission - Optional string
        pull - team members can pull, but not push or administer this repositories. Default
        push - team members can pull and push, but not administer this repositores.
        admin - team members can pull, push and administer these repositories
    repo_name - Optional string
    """
    reqq = 'orgs/%s/teams' % org_name
    url = host + reqq
    data = '{"name":"%s", "repo_names":["%s/%s"], "permission":"%s"}'\
    % (team_name,org_name,repo_name,permission)
    r = connect(url,"post",data)    
    if (errors_requests(r))&(r.status_code == httplib.CREATED):  
        return 0
    else: 
        if debug:
            print_debug()        
        return -1


def create_repo(repo_name, private = 'false', description = ''):
    """
    create_repo(repo_name,private,description)
    Use this function to create a repository and 3 teams (*, *-guests, *-owners) in your organization
    Input:
	repo_name - Required string
	private - Optional string. true to create a private repository, false to create a public one. Default is false.
	description - Optional string
    """
    reqq='orgs/%s/repos' % (org_name)
    url = host + reqq
    data = '{"name":"%s","private":"%s","description":"%s"}'\
    % (repo_name,private,description)
    r = connect(url,"post",data)
    if (errors_requests(r))&(r.status_code == httplib.CREATED):
        # creating 3 teams
        create_team(repo_name,'pull',repo_name)
        create_team(repo_name+'-guests','push',repo_name)
        create_team(repo_name+'-owners','admin',repo_name)
        return 0
    else:
        if debug:
            print_debug()        
        return -1

#search id_team by name
def search_id_team(team_name):
    reqq = 'orgs/%s/teams' % org_name
    url = host + reqq
    r = connect(url,"get")
    if (errors_requests(r))&(r.status_code == httplib.OK):
        cont = json.loads(r.content)
        for i in range (len(cont)):
            if cont[i]['name'] == team_name:
                return cont[i]['id']
    else:
        if debug:
            print_debug()        
        return -1
    return -1

def add_user_to_team(user,team_name):
    """
    add_user_to_team(user,team_name)
    Use this function to add a user to a team
    Input:
    user - Required string. Username
    team_name - Required string
    """
    team_id = search_id_team(team_name)
    if team_id == -1:
        return -1
    reqq = 'teams/%d/members/%s' % (team_id,user)
    url = host + reqq
    data = '{"login":"%s"}' % user
    r = connect(url,"put",data)
    if (errors_requests(r))&(r.status_code == httplib.NO_CONTENT):  #204
        return 0
    else:
        if debug:
            print_debug(r)          
        return -1

def del_user_from_team(user,team_name):
    """
    del_user_from_team(user,team_name)
    Use this function to remove user from team
    Input:
    user - Required string. Username
    team_name - Required string
    """
    if search_id_team(team_name) == -1:
        return -1
    reqq = 'teams/%d/members/%s' % (search_id_team(team_name),user)
    url = host + reqq
    r = connect(url,"delete")
    if (errors_requests(r))&(r.status_code == httplib.NO_CONTENT):  #204
        return 0
    else:
        if debug:
            print_debug()           
        return -1

def del_user_from_org(user):
    """
    del_user_from_team(user,team_name)
    Use this function to remove user from your organization
    Input:
    user - Required string. Username
    """
    reqq = 'orgs/%s/members/%s' % (org_name,user)
    url = host + reqq
    r = connect(url,"delete")
    if (errors_requests(r))&(r.status_code == httplib.NO_CONTENT): #204
        return 0
    else:
        if debug:
            print_debug()       
        return -1

