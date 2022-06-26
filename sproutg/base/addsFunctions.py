from audioop import reverse
from .models import Game, Transaction
from math import floor
    
def pageHeader(request, page):
    user = request.user 
    userGroups = [x.name for x in user.groups.all()] if user.groups != None else None
    crumbs = (request.path).split('/')[1:-1]
    extraContext = {'curUser': user,
                    'userGroups': userGroups,
                    'crumbs': crumbs,
                    'page': page}
    
    if 'developer' in userGroups:
        pendCount = Game.objects.filter(devUser=user)
        pendCount = pendCount.filter(verified=False).count()
        extraContext |= {'pendCount': pendCount}
    
    print("\n\n\n\n",extraContext)
    return extraContext

def topSold(qty):    
    games = Game.objects.filter(verified=True)
    games = list(games)
    games.sort(reverse=True, key=lambda x: x.sales())
    
    return games[:qty]