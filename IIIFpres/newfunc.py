     
     
def check(selfx,classx,obj):   
    #TODO: CHECK IF ALLOWED
    if unused(selfx):
        selfx = []
    if obj is None:
        obj = classx()
        selfx.append(obj)
        return obj
    else:
        if isinstance(obj,classx):
            selfx.append(obj)
        else:
            ValueError("Trying to add wrong object to partOf")
   
def unused(attr):
    """
    This function check if an attribute is not set (has no value in it).
    """
    if attr is None:
        return True
    else:
        return False


