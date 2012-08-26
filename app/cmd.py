import sys, select

def select_from_menu( title, options ):
    
    ''' first, print the title string
    '''
    
    print title
    print ''
    
    ##########################
    
    ''' 
    then, print a numbered 
    menu for the options e.g. : 

    1. Option 1
    2. Option 2

    '''
    
    print '\n'.join([ '. '.join([ str(i+1), 
                                  option    ])                 
                      
                       for i, option 
                       
                       in enumerate( options )   ])
    
    print ''
    
    
    ##########################
    
    '''
    get the user's selection
    '''
    valid_selections = range( 1, len(options)+1 )
    
    selection_index  = get_selection( valid_selections )
    
    '''
    return both the option chosen
    and the index of that option 
    within the option list
    '''
    return ( selection_index, options[ selection_index ] )
    



###########################################

'''
Utility function to get index of 
selected option in a terminal
'''
def get_selection( valid_selections, return_index=True ):
    
    try:
        
        '''
        prompt user for a selection
        '''
        selection = raw_input('Your selection: ')
        
        '''
        this will raise a ValueError 
        if inputted selection is not 
        an integer
        '''
        selection = int( selection )
        
        
        ##############################
        
        '''
        check the selection is one
        of the valid options
        '''        
        if selection not in valid_selections :   
            
            raise ValueError()
        
        
        ########################
        
        '''
        by default, we return a list index
        i.e. starting from zero, instead of
        starting from 1, as selections do
        '''
        if return_index : 
            
            index = selection - 1
            
            if index < 0 : raise ValueError()
            
            return index
        
        
        else :   return selection
    
    
    
    ###############################
    
    except ValueError:
        
        print 'Your selection is invalid.'
        
        '''
        call again, recursively
        '''
        return get_selection( valid_selections, return_index )
    
    



