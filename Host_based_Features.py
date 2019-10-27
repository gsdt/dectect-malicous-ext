import whois
from datetime import datetime
import time
import requests
def AgeDomain(domain):# year
    try:
    	age= whois.query(domain)
	#print age	
    except:
	return 0
    try:
    	creation_date = age.creation_date
    	expiration_date = age.expiration_date
    except:
	return 0
    ageofdomain = 0
    if expiration_date:
 	ageofdomain = abs((expiration_date - creation_date).days)
    return 1 if ageofdomain/30 > 0 else 0

def rank(host):
        xmlpath='http://data.alexa.com/data?cli=10&dat=snbamz&url='+host
	rank_country=-1
	rank_host=-1
        #print xmlpath
        try:
	    r=requests.get(xmlpath)
	    #print r.content
	    rlist=r.content.split('>')
	    for i in rlist:
		if 'REACH' in i and 'RANK=' in i:
		    if int(i.split("\"")[-2])>0:
			rank_host=1
            	if 'COUNTRY' in i and 'RANK=' in i:
		    if int(i.split("\"")[-2])>0:
			rank_country=1
            return [rank_host,rank_country]

        except Exception as e:
            return [-1,-1]

#print AgeDomain('www.facebook.com')
