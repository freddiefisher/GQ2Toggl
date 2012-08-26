import requests, sys
from getpass import getpass


# Resolve simplejson discrepancy
try: import simplejson
except ImportError: import json as simplejson

from urllib import urlencode



###############################################################

''' address of Toggl API
'''
API_PREFIX = "https://www.toggl.com/api/v6/"


########################

'''
load email from CMD args
else prompt user
'''
try :                EMAIL = sys.argv[1]
    
except IndexError :  EMAIL = raw_input( 'Your Toggl Email: ')

########################

''' always prompt for password
'''
PASSWORD = getpass( "Your Toggl Password: ")

AUTH     = ( EMAIL, PASSWORD )

print ''



###############################################################

def api(key, params=None):
    '''
    Return the API url call. 
    Potential keys:
        me
        time_entries
        workspaces
        clients
        projects
        tasks
        tags
        users

    For more info, see https://www.toggl.com/public/api

    params is a dictionary of key value pairs
    '''

    if params:
        apiCall =  API_PREFIX + key + ".json?" + urlencode(params)
    else:
        apiCall =  API_PREFIX + key + ".json"
    return apiCall



###############################################################

def session(headers=None):
    '''
    Session wrapper for convenience
    '''
    if headers:
        return requests.session(auth=AUTH, headers=headers)
    else:
        return requests.session(auth=AUTH)



###############################################################

def get_data(key):
    '''
    Get data from API. See list of keys in the api function in
    this document.
    
    '''
    with session() as r:
        response = r.get(api(key))

        content = response.content
        if response.ok:
            json = simplejson.loads(content)["data"]

            # Reverse the list to get correct chronological order. Also,
            # remove duplicates. But make sure this is actually a list!
            if type(json) is list:
                json.reverse()
            return json
        else:
            exit("Please verify your login credentials...")



###############################################################

def send_data(key, params=None, data=None):
    '''
    Use the api to send data.

    params: A dictionary that will be urlencoded

    Returns a dictionary.
    '''
    headers = {"Content-Type": "application/json"}

    # JSON Encode the data dict
    data=simplejson.dumps(data)
    with session(headers=headers) as r:
        response = r.post(api(key), data=data)

        content = response.content
        if response.ok:
            json = simplejson.loads(content)
            return json["data"]
        else:
            print response
            print response.content
            exit("Please verify your login credentials...")



###############################################################



def get_data_where(api, dataPair):
    
    '''
    load all data from API
    '''
    data = get_data(api)
    
    '''
    return filtered
    '''
    return filter_data( data, dataPair )
    


##############################################

def filter_data( data, dataPair ):
    
    '''
    Output the dicionary of a specific datakey (such as 'name') with a
    value (such as 'My Weekend Project' for a given apikey 
    (such as 'projects')
    
    
    e.g. 
    
    get_data_where( "projects", {  "client_project_name": 'name_of_project'  }  )
    
    '''
    
    ############################################
    
    ''' We'll append to this list and return it
    '''
    returnList = []

    ''' Change data type so we can iterate
    '''
    dataPair = dataPair.items()[0]

    
    ###############################
    
    '''
    Data is an array of dicts. See if we find our datakey. If so,
    return it. If not, return false.
    '''
    
    for x in data:
        if dataPair in x.items():
            returnList.append(x)
    
    
    ##################
    
    return returnList

    


