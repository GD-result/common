import xmlrpclib
import libvirt
SPACE='ITST'
TOP_PAGE='Proba'
WIKI_USER='smustafin'
WIKI_PASS='12as34df'
p = "h1." + "TEST" + "\n"
p = p + "||id||date||title||author||samary||\n"
# cycle
vm={
		"id":"000003",
		"date":"01120112",
		"title":"12312",
		"author":"qweqw",
		"samary":"sdfsdf"
	} 
p=p+"|["+vm["id"]  + "|" + vm["date"]+"|"+vm["title"]+"|"+vm["author"]+"|"+vm["samary"]+"|\n"
p=p+"|["+"))"+ "|" +"33"+ "|" + "134"+ "|" + "sdfjh"+ "|"+ "wert"+ "|"
print p
#conn = libvirt.openReadOnly('qemu:///system')
host = "smustafin"
print host

server = xmlrpclib.ServerProxy('https://wiki.griddynamics.net/rpc/xmlrpc');
token = server.confluence1.login(WIKI_USER, WIKI_PASS);
print token
try:
	page = server.confluence1.getPage(token, SPACE, host);
except:
	#parent = server.confluence1.getPage(token, SPACE, TOP_PAGE);
	page={
		'parentId': "71501338",
		'space': SPACE,
		'title': host,
		'content': p
		 }
	server.confluence1.storePage(token, page);
else:
	page['content'] = p;
	server.confluence1.updatePage(token, page,{'versionComment':'','minorEdit':1});
