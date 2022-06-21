from .models import Review
from math import floor
    
def pageHeader(request, page):
    user = request.user 
    userGroups = [x.name for x in user.groups.all()] if user.groups != None else None
    crumbs = (request.path).split('/')[1:-1]
    extraContext = {'curUser': user,
                    'userGroups': userGroups,
                    'crumbs': crumbs,
                    'page': page}
    
    return extraContext
