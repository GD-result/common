import requests
import json

from conf import password
from conf import login
from conf import org_name
from conf import debug
from conf import type_pass
from conf import token

host = 'https://api.github.com/'

class auth:     
    """
    class auth
    Use this class to connect with URL different types of authorization
        and methods 
    Input:
    url - Required string
    data - Required string
    """ 
    global_url = ""
    global_auth = "";
    def type_p(self,url):
        if type_pass:
            self.global_url = url;
            self.global_auth = (login,password)
        else:
            self.global_url = url + "?access_token=" + token;
            self.global_auth = ""            
    def put(self,url,data):
        self.type_p(url);
        return requests.put(url = self.global_url, auth = self.global_auth, data = data);
    def post(self,url,data):
        self.type_p(url)
        return requests.post(url = self.global_url,auth = self.global_auth,data = data)
    def delete(self,url):
        self.type_p(url)
        return requests.delete(url = self.global_url, auth = self.global_auth)
    def get(self,url):
        self.type_p(url)
        return requests.get(url = self.global_url, auth = self.global_auth)
    
type_connect = auth();

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
    r = type_connect.post(url, data) 
    if (errors_requests(r))&(r.status_code == requests.codes.OK): 
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
    r = type_connect.post(url, data)
    if (errors_requests(r))&(r.status_code == requests.codes.CREATED):
        create_team(repo_name,'pull',repo_name)
        create_team(repo_name+'-guests','push',repo_name)
        create_team(repo_name+'-owners','admin',repo_name)
        return 0

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
    r = type_connect.get(url)
    if (errors_requests(r))&(r.status_code == requests.codes.OK):
        cont = json.loads(r.content)
        for i, item in enumerate(cont):
            if item['name'] == team_name:
                return item['id']
    else:
        if debug:
            print_debug(r)        
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
        if debug: 
            print requests.codes.NOT_FOUND
        return -1
    reqq = 'teams/%s/members/%s' % (team_id,user)
    url = host + reqq
    data = '{}'
    r = type_connect.put(url, data)
    if (errors_requests(r))&(r.status_code == requests.codes.NO_CONTENT):
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
            print requests.codes.NOT_FOUND
        return -1
    reqq = 'teams/%d/members/%s' % (team_id,user)
    url = host + reqq
    r = type_connect.delete(url)
    if (errors_requests(r))&(r.status_code == requests.codes.NO_CONTENT):
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
    r = type_connect.delete(url)
    if (errors_requests(r))&(r.status_code == requests.codes.NO_CONTENT):
        return 0
    else:
        if debug:
            print_debug(r)       
        return -1

def list_auth():
    """
    list_auth()
    Use this function to list your authorizations
    """
    url = host + 'authorizations'
    r = requests.get(url = url ,auth = (login,password))
    if (errors_requests(r))&(r.status_code == requests.codes.OK):
        js = json.loads(r.content)
        for i in range (len(js)):
            print "id: ", js[i]["id"]
            print "url: ", js[i]["url"]
            print "scopes: ", js[i]["scopes"]
            print "token: ", js[i]["token"]
            print "app: ", js[i]["app"]
            print "updated_at: ", js[i]["updated_at"], "\n"
        return 0
    else:
        if debug:
            print_debug(r)       
        return -1
