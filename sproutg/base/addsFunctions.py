from .models import Review
from math import floor

def overallStar(game):
    ratings = [s.star_rating for s in Review.objects.filter(game=game)]
    starsum = 0
    
    for x in ratings:
        starsum += float(x)
    overall_rating = starsum/len(ratings)
    
    fullStars = floor(overall_rating)
    halfStar = (overall_rating % fullStars) >= 0.5
    fullStars = range(fullStars)
    
    return fullStars, halfStar 
    
def pageHeader(request, page):
    user = request.user 
    userGroups = [x.name for x in user.groups.all()] if user.groups != None else None
    crumbs = (request.path).split('/')[1:-1]
    extraContext = {'curUser': user,
                    'userGroups': userGroups,
                    'crumbs': crumbs,
                    'page': page}
    
    return extraContext
