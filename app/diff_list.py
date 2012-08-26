'''
Special list subclass which can 
make use of the ' - ' operator
'''
class DiffList(list):
    
    '''
    when subtracting two diff lists 
    subtract is similar to 'discard' for
    sets, I.E. remove if exists, otherwise
    just carry on
    '''
    def __sub__(self, b):
        result = self[:]
        b = b[:]
        
        while b:
            try:
                result.remove(b.pop())
            
            except ValueError:
                pass
        
        return result


#a = DiffList([1,1,2,3])
#
#b = DiffList([1,3,4])
#
#print a - b 
