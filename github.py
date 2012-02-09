'''
Created on 06.02.2012

@author: ninja
'''

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
    """
    help()
    Use this function to print help 
    """  
    print "\n        Function: create_team(team_name,permission,repo_name)\n\
        Function: create_repo(repo_name,private,description)\n\
        Function: search_id_team(team_name)\n\
        Function: add_user_to_team(user,team_name)\n\
        Function: del_user_from_team(user,team_name)\n\
        Function: del_user_from_org(user)\n"    
    
def print_debug(r):
    """
    print_debug(r)
    Use this function to print headers and content of HTTP requests 
    r - Required Requests's type
    """  
    print r.headers, "\n\n", r.content

def errors_requests(value):
    """
    errors_requests(value)
    Use this function to check for errors associated with the ratelimit 
    value - Required Requests's type
    """
    if value.headers['x-ratelimit-remaining'] > 0:
        return True
    return False

def connect(url,method = "get",data = ""):
    """
    connect(url,method = "get",data = "")
    Use this function to connect with URL different types of authorization 
    Input:
    url - Required string
    method - Optional string (defaut method = 'get')
        'get'
        'post' 
        'put'
        'delete'
    data - Optional string (defaut method = 'get')
    """   
    global r
    if type_pass:
        #login pass
        if method == 'get':
            r = requests.get(url, auth = (login,password))
            return r
        if method == 'post':
            r = requests.post(url,auth = (login,password),data = data)
            return r
        if method == 'put':
            r = requests.put(url,auth = (login,password),data = data)
            return r
        if method == 'delete':
            r = requests.delete(url, auth = (login,password))
            return r
    else:
        #token
        if method == 'get':
            r = requests.get(url + "?access_token=%s") % token
            return r
        if method == 'post':
            r = requests.post(url + "?access_token=%s" % token, data = data)
            return r
        if method == 'put':
            r = requests.put(url + "?access_token=%s" % token, data = data)
            return r
        if method == 'delete':
            r = requests.delete(url + "?access_token=%s") % token
            return r

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
            print_debug(r)        
        return -1


def create_repo(repo_name, private = 'false', description = ''):
    """
    create_repo(repo_name,private,description)
    Use this function to create a repository and
        3 teams (*, *-guests, *-owners) in your organization
    Input:
	repo_name - Required string
	private - Optional string. true to create a private repository, 
        false to create a public one. Default is false.
	description - Optional string
    """
    reqq='orgs/%s/repos' % (org_name)
    url = host + reqq
    data = '{"name":"%s","private":"%s","description":"%s"}'\
    % (repo_name,private,description)
    r = connect(url,"post",data)
    if (errors_requests(r))&(r.status_code == httplib.CREATED):
        create_team(repo_name,'pull',repo_name)
        create_team(repo_name+'-guests','push',repo_name)
        create_team(repo_name+'-owners','admin',repo_name)
        return 0;

    else:
        if debug:
            print_debug(r)        
        return -1

def search_id_team(team_name):
    """
    search_id_team(team_name)
    Use this function to search team`s id by team`s name
    Input:
    team_name - Required string
    """
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
            print_debug(r)        
        return -1
    return -1

def add_user_to_team(user,team_name):   #don't works with token scopes repo.
    # Github's bug (204 status code and no user in team)
    """
    add_user_to_team(user,team_name)
    Use this function to add a user to a team
    Input:
    user - Required string. Username
    team_name - Required string
    """
    team_id = search_id_team(team_name)
    if team_id == -1:
        if debug: 
            print httplib.NOT_FOUND
        return -1
    reqq = 'teams/%d/members/%s' % (team_id,user)
    url = host + reqq
    data = '{"login":"%s"}' % user
    r = connect(url,"put",data)
    #print r.read();
    #r = requests.put(url,auth = (login,password),data = data)
    if (errors_requests(r))&(r.status_code == httplib.NO_CONTENT):
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
    team_id = search_id_team(team_name)
    if team_id == -1:
        if debug: 
            print httplib.NOT_FOUND
        return -1
    reqq = 'teams/%d/members/%s' % (team_id,user)
    url = host + reqq
    r = connect(url,"delete")
    if (errors_requests(r))&(r.status_code == httplib.NO_CONTENT):
        return 0
    else:
        if debug:
            print_debug(r)           
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
    if (errors_requests(r))&(r.status_code == httplib.NO_CONTENT):
        return 0
    else:
        if debug:
            print_debug(r)       
        return -1
