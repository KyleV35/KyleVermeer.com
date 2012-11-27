import webapp2
from webapp2_extras import routes

routes= [
    #webapp2.Route(r'/', handler='main.MainHandler'),
    #For now
    webapp2.Route(r'/',handler='handlers.kyle.FrontPageHandler'),
    webapp2.Route(r'/sara',handler='handlers.kyle.SaraPageHandler'),
    webapp2.Route(r'/examples',handler='handlers.kyle.KyleExamplesHandler'),
    webapp2.Route(r'/contact',handler='handlers.kyle.ContactPageHandler'),
    webapp2.Route(r'/games',handler='handlers.games.GamesPageHandler'),
    routes.PathPrefixRoute(r'/games', [
        webapp2.Route(r'/brickbreaker',handler='handlers.games.BrickBreakerPageHandler'),
        webapp2.Route(r'/brickbreaker/highScore',handler='handlers.games.BrickBreakerHighScoresHandler'),
        webapp2.Route(r'/brickbreaker/init',handler='handlers.games.BrickBreakerInitHandler'),
    ]),
    webapp2.Route(r'/family',handler='handlers.family.FamilyMainPageHandler'),
    webapp2.Route(r'/family/member/<familyMemberName>', handler='handlers.family.FamilyHandler'),
    routes.PathPrefixRoute(r'/family/videos', [
        webapp2.Route(r'/display',handler='handlers.family.VideoHandler'),
        webapp2.Route(r'/like',handler='handlers.family.VideoLikeHandler'), #Ajax handler
    ]),
    webapp2.Route(r'/family/makedummydata', handler='handlers.family.DummyData')
    ]