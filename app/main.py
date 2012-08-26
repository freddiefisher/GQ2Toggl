'''
regular imports
'''
from cmd import select_from_menu


#####################

'''
imports that also print to cmd
and require user interaction

(i.e. their order is non trivial)

'''
print ''
print '***********************************************************'
print '***********************************************************'
print ''
print '*****  WELCOME TO THE GQUEUES -> TOGGL TASK EXPORTER  *****'
print ''

''' 
includes choosing which directory
to look for files in
'''

from gqueues_csv import projects_from_csv

print ''

'''
includes login to Toggle API
'''

import toggl_API





#######################################################################

'''
 _____         _        
|_   _|_ _ ___| | _____ 
  | |/ _` / __| |/ / __|
  | | (_| \__ \   <\__ \
  |_|\__,_|___/_|\_\___/
                        
response element: 

{
    "name": "Task",
    "workspace": {
        "name": "john.doe@gmail.com's workspace",
        "id": 31366
    },
    "id": 7140,
    "project": {
        "name": "Important project",
        "id": 279882
    },
    "user": {
        "fullname": "Jane Doe",
        "id": 104711
    },
    "estimated_workhours": 1,
    "estimated_seconds": 3600,
    "is_active": true
}


'''
tasks = toggl_API.get_data('tasks')




#######################################################################

'''

 ____            _           _       
|  _ \ _ __ ___ (_) ___  ___| |_ ___ 
| |_) | '__/ _ \| |/ _ \/ __| __/ __|
|  __/| | | (_) | |  __/ (__| |_\__ \
|_|   |_|  \___// |\___|\___|\__|___/
              |__/                   


Projects is a list of dictionaries that 
look like this...

[ { 
       
    'name': 'shelve', 
    'id'  : 1465381, 
    
    'is_active'   : True, 
    'updated_at'  : '2012-03-01T18:48:44+00:00', 
    'fixed_fee'   : 0.0, 
    'billable'    : True,     
    'is_private'  : True, 
    'hourly_rate' : 0.0,
    'is_fixed_fee': False, 
    
    'estimated_workhours' : None, 
    'client_project_name' : 'shelve', 
    
    'automatically_calculate_estimated_workhours': False,
    
        
    'workspace':   { 'name' : 'Unio', 
                     'id'   : 218104   }
    
    
    }, ...  ]



We load all projects at the start
and then filter by workspace, and name,
later


'''
projects = toggl_API.get_data('projects')






#######################################################################

'''
__        __         _                                  
\ \      / /__  _ __| | _____ _ __   __ _  ___ ___  ___ 
 \ \ /\ / / _ \| '__| |/ / __| '_ \ / _` |/ __/ _ \/ __|
  \ V  V / (_) | |  |   <\__ \ |_) | (_| | (_|  __/\__ \
   \_/\_/ \___/|_|  |_|\_\___/ .__/ \__,_|\___\___||___/
                             |_|                        



toggl_API.get_data('workspaces')
returns something like this: 


[

{ 'updated_at': '2012-03-21T14:08:18+00:00', 'profile_name': 'Pro',  
  'current_user_is_admin': True,             'name': 'Unio',                 'id': 218104  }, 
  
{ 'updated_at': '2012-02-29T15:59:16+00:00', 'profile_name': 'Free', 
  'current_user_is_admin': True,             'name': 'Business Development', 'id': 218112  }
  
]


'''
workspaces = toggl_API.get_data('workspaces')



####################################################

'''
we parse the response into a simple dictionary like: 


{ 'Business Development' : 218112, 
  'Unio'                 : 218104  }

'''
ws_ids = dict( [  ( ws['name'], ws['id'] )

                   for ws in workspaces  ] ) 

'''
and for convenience in menus, a list
of the workspace names
'''
ws_names = [  ws['name']  for ws in workspaces  ]




#######################################################################

'''

 ___                            _   
|_ _|_ __ ___  _ __   ___  _ __| |_ 
 | || '_ ` _ \| '_ \ / _ \| '__| __|
 | || | | | | | |_) | (_) | |  | |_ 
|___|_| |_| |_| .__/ \___/|_|   \__|
              |_|                   
'''


def import_projects():

    project_files = projects_from_csv()
    
    print ''
    print ''
    
    for p in project_files : 
        
        '''
        project file header
        '''
        print '***************************************'
        print '***************************************'
        print ''
        
        ##################################
        
        '''
        which workspace to import / merge
        this project (or sub-projects) into ? 
        '''
                
        menu_title = ''.join([ 'Choose workspace for  *', 
                                p.project_title,  '*  :'   ])
        
        '''
        choose from a list of worskspace names
        in the command shell
        '''
        ( index, selected_workspace ) = select_from_menu( menu_title, ws_names )
        
        
        print ''
        print 'Importing project data to workspace: ', selected_workspace
        print ''
        
        
        #########################
        
        '''
        now the user must decide whether to import this
        CSV file as a single project, or whether the root
        nodes of this Queue are themselves projects
        '''
        
        menu_title = 'Import this file as a single project, or multiple projects?'
        
        SINGLE     = 'This Queue is a single project.'
        MULTIPLE   = 'Top level nodes in this Queue each represent a project.'
        
        
        ''' choose in cmd
        '''
        ( index, choice ) = select_from_menu( menu_title, [ SINGLE, MULTIPLE ] )
        
        
        ####################
        
        ''' spacer before project imports
        '''      
        print ''
        
        
        #########################
                
        if   choice == SINGLE   : 
            
            '''
            add the current project to the 
            selected workspace
            '''
            
            add_project_to_toggl_workspace( p, selected_workspace )
        
        
        #########################
        
        elif choice == MULTIPLE :
              
            '''
            Add sub-projects to toggl
            one by one
            '''
            sub_projects = p.sub_projects()
            
            for sp in sub_projects :
                        
                add_project_to_toggl_workspace( sp, selected_workspace )
        
        
        #############################
        
        '''
        offer to delete the original file
        '''
        
        menu_title = '\n'.join([ 'File successfully exported to Toggl.',
                                 'Would you like to delete the file?'    ])
        
        DELETE = 'Yes'
        DONT   = 'No'
        
        ( index, choice ) = select_from_menu( menu_title, [ DELETE, DONT ] )
        
        
        ###########################
        
        if choice == DELETE : 
            
            p.delete_file()
            
            print ''
            print 'Deleted File.'
               
        
        ###############
        
        '''
        gap before next queue file
        '''        
        print ''
        print ''
        print ''
        
        
        
###################################################################

def add_project_to_toggl_workspace( p, ws_name ):
    
    '''
    get workspace id from name
    '''
    ws_id = ws_ids[ ws_name ]
    
    
    ##########################
        
    '''
    Should we flattern Queue hierarchy, 
    or should we emulate hierarchy with 
    a naming convention. 
    '''
    
    '''
    if there isn't any hierarchy, 
    don't need to ask
    '''
    if not p.has_hierarchy() :    
        
        gqueues_tasks = p.get_tasks()
    
    
    ###################
    
    else : 
        
        '''
        if there is some hierarchy, we must
        ask the user what to do about this
        '''
        
        menu_title = '\n'.join([ 'This Queue contains some nested tasks.',
                                 'Toggl allows only 1 level of task hierarchy.' ])
        
        EMULATE = 'Emulate hierarchy with naming,  e.g.  Child  [ Grandparent > Parent ]'
        
        FLATTEN = 'Flat hierarchy of leaf-names,   e.g.  Child'
        
        IGNORE  = 'Use top-level tasks only - discarding all nested tasks.'
        
        ( index, choice ) = select_from_menu( menu_title, [ EMULATE, FLATTEN, IGNORE ] )
        
        
        #############################
        
        if   choice == EMULATE :   
            
            gqueues_tasks = p.get_tasks( True )
            
            
        ######################
        
        elif choice == FLATTEN :   

            gqueues_tasks = p.get_tasks( False )
            
        
        ######################
        
        elif choice == IGNORE :   
            
            '''
            get root nodes only
            '''
            gqueues_tasks = p.get_root_tasks()
    
    
    
    
        
    ###############################################################
        
    '''
    see if there is a project with the
    same name in this workspace.
    
    start by getting all projects in 
    this workspace...
    '''
    projects_in_ws  = toggl_API.filter_data( projects, {  "workspace":  { 'name' : ws_name, 
                                                                          'id'   : ws_id     }   })
    
    '''
    Of the projects in the selected
    workspace, do any have the same 
    name as the one we're importing?
    '''
    existing = toggl_API.filter_data( projects_in_ws, {  "name":  p.project_title   }   )
    
    
    
    ########################################
    
    '''
    CASE 1 :  There is no pre-existing project
    '''
    
    if len( existing ) == 0 : 
        
        '''
        make a new project
        '''
        
        project_data = { 'project' : {
            "name"       : p.project_title,
            "is_private" : False,
            "billable"   : False,
            "workspace"  : {  "id": ws_id   }
            }}

        
        ''' create project
        '''
        toggl_project = toggl_API.send_data( "projects", data = project_data )
        
        
        ############################
        
        '''
        add this new project to the 
        rest of the toggle projects
        '''
        projects.append( toggl_project )
        
        
        ############################
        
        ''' notifiy user
        '''
        print ''
        print 'uploaded a new project to Toggl:', p.project_title
        print ''
    
        
        ##########################
        
        '''
        we need to add all of the 
        gqueues tasks, as the projct
        is currently empty
        '''
        new_tasks = gqueues_tasks
        
        ###########################
        
        '''
        if no tasks in this project, 
        inform the user
        '''
        
        if len( new_tasks ) == 0 : 
            
            print 'This project does not contain any tasks.'
        
        
          
    
    
    
    ##################################################################
    
    else : 
        
        '''
        CASE 2 :  a project with this name 
                  already exists
        
        merge the project with the existing one
        adding, but NOT deleting old tasks.
        
        This is because tasks that are completed
        may still have associated time records. 
        '''
        
        toggl_project = existing[0]
        
        
        ####################
        
        ''' notifiy user
        '''
        print ''
        print p.project_title, 'is already a project on Toggl. Merging new tasks...'
        print ''
        
        
        ###################################
        
        '''
        get names all tasks in the project
        on toggl. Match project with object like
        this : 
        
        
        { 'client_project_name': 'To Do', 
          'name': 'To Do', 
          'id'  : 1540962   }
        
        '''            
        toggl_tasks = set([ 
            
            t[ 'name' ] 
                               
            for t in 
                            
            toggl_API.filter_data( tasks, {  "project":  {
                                    
                        'client_project_name' : toggl_project[ 'client_project_name' ],
                                       'name' : toggl_project[ 'name' ],
                                         'id' : toggl_project[ 'id' ]       }}   )])
        
        
        ##########################
        
        '''
        add only the new tasks
        '''
        new_tasks = gqueues_tasks - toggl_tasks
        
        
        ##################
        
        ''' inform if none
        '''
        
        if len( new_tasks ) == 0 : 
            
            print 'There are no new tasks to add to this project.'
        
    
    
    
    #######################################
    
    '''
    add a new tasks to the toggle project
    (whether newly created or existing)
    '''
         
    for task_name in new_tasks :
        
        task_data = { 'task' : {
        "name"      : task_name,
        "is_active" : True,
        "project"   : {  "id": toggl_project[ 'id' ]  }
        }}
        
        ''' create task
        '''
        task = toggl_API.send_data( "tasks", data = task_data )
        
        ''' add to local collection
        '''
        tasks.append( task )
        
        print 'added task: ', task_name
        

     
    
    ###############
    
    '''
    space after project
    '''
    print ''
    



##########################

'''
main
'''
        
import_projects()
        
