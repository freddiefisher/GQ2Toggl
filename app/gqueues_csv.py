import glob, os, csv
from copy import deepcopy
from collections import deque
from cmd import select_from_menu
from diff_list import DiffList

'''
default path only works on unix
'''
try :  
    
    HOME         = os.path.expanduser( "~" )
    DEFAULT_PATH = os.path.join( HOME, "Downloads" )

except :
    
    DEFAULT_PATH = None


###################################

def get_files_path():

    '''
    if default path is a possiblity,
    give the option. Otherwise, just 
    prompt for path.
    '''

    if DEFAULT_PATH and os.path.exists( DEFAULT_PATH ) :
        
        menu_title = "Where are the GQueues CSV files located?"
        
        
        IN_DEFAULT = ''.join([ 'The files are in the default location : ', 
                                DEFAULT_PATH  ])
    
        
        ELSEWHERE  = "I'd like to enter a path manually."
    
        
        ( index, choice ) = select_from_menu( menu_title, [ IN_DEFAULT, ELSEWHERE ] )
        
        print''
        
        ###############################
        
        '''
        if they chose the default location
        return that path
        '''
        
        if choice == IN_DEFAULT :   return DEFAULT_PATH
           
        '''
        otherwise, enter a path - much as if
        the default had not been an option
        '''
    
    
    ###################
    
    '''
    enter path to CSV files
    '''
    
    FILES_PATH = raw_input( 'Full Path To File(s): ')
    
    
    '''
    check the path is an
    existing directory
    '''
    
    while not os.path.exists( FILES_PATH ) \
       or not os.path.isdir ( FILES_PATH ) :
        
        print ''
        print 'you entered:', FILES_PATH
        print "I'm sorry, that path does not exist, or is not a folder."
        print ''
        
        FILES_PATH = raw_input( 'Full Path To File(s): ')
            
    
    
    ###################################
    
    '''
    we got past the while, and thus have
    a valid path to search for CSV files
    '''
    return FILES_PATH
    
      
        
        
        
        


###################################################################

class Project(object): 
    
    def __init__( self, project_title, fname=None ):
        
        '''
        set with constructor
        '''
        self.project_title = project_title
           
           
        #############################
        
        '''
        queues populated either from 
        CSV file parsing, or by a parent
        Project creating sub-projects
        '''
        self.child_nodes   = deque()
        
        self.parent_nodes  = deque()
        
        
        #############################        
        
        '''
        a dictionary mapping node names
        to a hierarchy mapping ( h_map )
        showing hiearchical layers of 
        tasks.
        
        the node name key is also the 
        leaf node of the h_map.
        
        nodes is populated with a special
        function below, after child / parent
        nodes have been specified 
        '''
        self.nodes         = {}
        
        
        #############################
        
        ''' 
        for deletion after project 
        ( or all sub-projects )
        successfully exported  
        '''
        self.fname = fname
    
    
    
    
    ######################################################
    
    '''
    generates the nodes dictionary
    from the parent nodes, 
    and child nodes queues
    '''
    def populate_nodes( self ):
        
        
        '''
        throw a warning if there are more
        than one tasks with identical names
        '''
        
        all_nodes = deepcopy( self.parent_nodes )
        
        [  all_nodes.append( description ) 
         
           for ( description, parent ) 
          
           in  self.child_nodes            ]
        
        
        ###################
        
        '''
        compare a list of all the nodes to a 
        list of all unique nodes. 
        '''        
        
        uniq_nodes = DiffList(  list(set( all_nodes )) )
        
        all_nodes  = DiffList(  all_nodes  )
        
        '''
        get any 'leftover' nodes
        '''        
        duplicates = all_nodes - uniq_nodes
        
        '''
        stern warning if there are any!
        '''
        if len( duplicates ) != 0 :
            
            title = '\n'.join([ '!!!!!!!!!!!!!!!!!!',
                                '###########',
                                'WARNING!!! ',
                                'WARNING!!! ',
                                'WARNING!!! ',
                                '###########',
                                '!!!!!!!!!!!!!!!!!!',
                                '',
                                'This project contains duplicate task names!',
                                'If you continue, only one task with each name',
                                'will be saved in the project.',
                                '',
                                'In addition, if the duplicate tasks have any', 
                                'sub-tasks, some tasks may end up with incorrect',
                                'ancestors. ',
                                '',
                                'You may be planning to discard the repeated tasks',
                                'anyhow, e.g. because you only wish to import the',
                                'top-level tasks, and none of those are duplicates.',
                                '',
                                'But if not, you may wish to return to GQueues and',
                                'rename the offending duplicate tasks.',
                                '',
                                'The duplicated names are :',
                                '',
                                '\n'.join( set( duplicates )),
                                '',
                                'What would you like to do?'       ])
            
            
            ###########################
            
            QUIT     = 'Delete this CSV file and quit.'
            CONTINUE = 'Continue anyway.'
                        
            '''
            get the user's decision
            '''
            ( index, choice ) = select_from_menu( title, [ QUIT, CONTINUE ] )
            
            print ''
            
            '''
            if they choose quit, quit!
            '''
            if choice == QUIT : 
                
                print 'deleting CSV containing duplicate task-names'
                
                self.delete_file()
                                
                raise SystemExit()
                
            
            '''
            Otherwise, continue onwards.
            You have been warned!
            '''
                
                
        
        ###########################
        
        ''' put root nodes straight into nodes dictionary
        '''
        
        for description in self.parent_nodes : 
        
            self.nodes[ description ] = [ description ]
        
        
        ###########################################
        
        '''
        now parse the children into
        the nodes dictionary  
        '''    
        c_nodes = deepcopy( self.child_nodes )
        
        while len( c_nodes ) > 0 : 
            
            '''
            pop open a node
            '''
            ( description, parent ) = c_nodes.popleft()
            
            '''
            assume we won't find it's parent
            '''
            found = False
            
            
            ################################
            
            for n in self.nodes : 
                
                if n == parent :
                         
                    h_map = deepcopy( self.nodes[ n ] )
                    
                    h_map.append( description )
                    
                    '''
                    add new entry to the nodes dictionary
                    '''
                    self.nodes[ description ] = h_map
                    
                    found = True
                    
                    break
            
            
            ################################
            
            '''
            if we didn't find it's parent yet
            re-add to the end of temp child nodes
            '''
            if not found :   c_nodes.append(  ( description, parent )  )
    
    
    
    
    
    
    ###############################################
    
    def get_tasks( self, emulate_hierarchy=True ):
        
        
        if emulate_hierarchy : 
            
            '''
            each task has it's inheritance hierarchy
            written in brackets afterwards. 
            
            e.g. 
            
            for hierarchy : 
                
                Task A
                    Task B
                        Task C
            
            Task C looks like :  Task C  [ Task A > Task B ]
                
            '''
            
            return set([  self.hierarchical_task_string( task_map )   
                       
                          for task_map 
                       
                          in self.nodes.values()    ]) 
        
        else : 
            
            '''
            otherwise simply flatten any task hierarchy
            '''
            return set( self.nodes.keys() )
              
    
    
    ############################
    
    '''
    return root tasks only
    '''    
    def get_root_tasks(self):
    
        return set( self.parent_nodes )
        
        
    ###############################################
            
    def hierarchical_task_string( self, task_map ):
        
        if len( task_map ) == 0 :  raise ValueError('Task not defined')
        
        if len( task_map ) == 1 :  return task_map[ 0 ]
        
        else : 
            
            return ' '.join([  task_map[ -1 ], '[',
                               ' > '.join( task_map[ : -1 ] ), ']'  ])
        
    
    
    
    
    ###############################################
    
    '''
    test if this project contains 
    any hierarchy or not
    '''
    def has_hierarchy( self ):
        
        if len( self.child_nodes ) != 0 : 
            
            return True
        
        else : return False
        
    
    
    ##########################
    
    '''
    optionally delete original CSV file
    '''
    def delete_file(self):
        
        if self.fname :  os.remove( self.fname )
        
    
    
    ##########################
    
    '''
    returns projects based on
    parent nodes of this project's 
    tasks
    '''
    def sub_projects(self):
        
        projects_list = []
        
        
        for parent in self.parent_nodes : 
            
            '''
            sub project title is the name
            of this task
            '''
            project = Project( parent )
            
            
            ##############################
            
            '''
            parent nodes in the sub projects
            are on the second level in this one
            so have 2 task descriptions in
            hierarchy map
            '''            
            project.parent_nodes = deque([ 
                                          
                description
                
                for  description, h_map 
                
                in   self.nodes.items()
                
                if   len( h_map ) == 2  
                
                and  h_map[ 0 ] == parent    ])
        
            
            ##############################
            
            '''
            child nodes have h_map 
            length 3 or greater
            
            the parent of this node is 
            the penultimate node in 
            the hierarchy map
            '''
            project.child_nodes = deque([ 
                                          
                ( description, h_map[ -2 ] )
                
                for  description, h_map 
                
                in   self.nodes.items()
                
                if   len( h_map ) >= 3  
                
                and  h_map[ 0 ] == parent    ])
            
            
            #############################
            
            '''
            process the nodes
            '''
            project.populate_nodes()
            
            '''
            add to return list
            '''
            projects_list.append( project )
        
        
        #############################
        
        return projects_list
    
    
    
    

#####################################################################

'''
prompt user to enter a path
to search for GQueues csv export
files
'''
GQS_CSV_PATH = get_files_path()


#################

'''
public method
'''

def projects_from_csv():

    '''
    dictionary to store multiple 
    project titles and their tasks
    '''
    projects_to_import = []
    
    
    #####################################################################
    
    for fname in glob.glob( os.path.join( GQS_CSV_PATH, 'gqueues_*.csv') ):
        
        '''
        load the lines
        '''
        
        with open( fname ) as f :   lines = f.readlines()
     
            
        ############################################
        
        if lines[0][:4] == '*GQ*' :
            
            print ''
            print 'skipping complete backup:', fname
            print ''
            
            continue
    
    
        ############################################
        
        '''
        Format looks like this : 
        
        DB Optimization - OPEN ITEMS
        description,notes,tags,dueDate,reminder,repeating,parent item
        Stock DB cluster,,,,,,
        Uses InnoDB,,,,,,Stock DB cluster
        '''
        
        '''
        get the project title
        '''
        project_title = lines[0].split(' - ')[0]
        
        project = Project( project_title, fname )
        
        
        ############################################
        
        '''
        get the list items
        '''
        for l in lines[2:] :
            
            ''' have we got to the end of the items
            '''
            if l.strip() == '""' : break
            
            try:
                
                ( description, notes, 
                  tags, due_date, reminder, 
                  repeating, parent         ) = csv.reader([ l ]).next()
                
                
#                  
#            
#            "Load all ISBN-group links, and all ISBN-advice links into MEMORY",
#            read-only during the day. all cached. ,
#            ,
#            ,
#            ,
#            ,
#            calculate online advice every night
#            
            
            except Exception, e:
                
                print e 
                print l
                
                raise SystemExit()
            
            '''
            strip whitespace from description and parent
            '''
            description = description.strip()
            parent      = parent.strip()
            
            
            ###############################
            
            '''
            if description is empty, skip task
            '''
            if description == '' : continue
            
            
            ###############################
            
            '''
            parse the nodes into parent
            and child node lists
            '''
            
            if parent == '' :
                
                project.parent_nodes.append( description )
              
                
            else : 
                
                project.child_nodes.append(  ( description, parent )  )
                          
                    
        
        ######################################
        
        '''
        process the nodes!
        '''
        project.populate_nodes()
        
        
        ###############################
        
        '''
        finally add the project to import list!
        '''
        projects_to_import.append( project )
    
    
    
    ########################################
    
    '''
    return all projects that were
    found in user's GQS_CSV_PATH folder
    '''
    return projects_to_import






