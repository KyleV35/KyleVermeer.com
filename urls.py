import webapp2
from webapp2_extras import routes

routes= [
    #webapp2.Route(r'/', handler='main.MainHandler'),
    #For now
    webapp2.Route(r'/',handler='handlers.kyle.FrontPageHandler'),
    webapp2.Route(r'/about',handler='handlers.kyle.AboutPageHandler'),
    webapp2.Route(r'/sara',handler='handlers.kyle.SaraPageHandler'),
    
    #Examples
    webapp2.Route(r'/examples',handler='handlers.kyle.KyleExamplesHandler'),
    routes.PathPrefixRoute(r'/examples', [
        webapp2.Route(r'/whats_up',handler='handlers.kyle.WhatsUpHandler'),
    ]),
    
    #Contact
    webapp2.Route(r'/contact',handler='handlers.kyle.ContactPageHandler'),
    
    #Games
    webapp2.Route(r'/games',handler='handlers.games.GamesPageHandler'),
    routes.PathPrefixRoute(r'/games', [
        webapp2.Route(r'/brickbreaker',handler='handlers.games.BrickBreakerPageHandler'),
        webapp2.Route(r'/brickbreaker/highScore',handler='handlers.games.BrickBreakerHighScoresHandler'),
        webapp2.Route(r'/brickbreaker/init',handler='handlers.games.BrickBreakerInitHandler'),
    ]),
    
    #Blog
    webapp2.Route(r'/blog',handler='handlers.kyle.BlogHandlerLatest'),
    routes.PathPrefixRoute(r'/blog', [
        webapp2.Route(r'/',handler='handlers.kyle.BlogHandler'),
        webapp2.Route(r'/<year>/<month>/<day>/<title>',handler='handlers.kyle.BlogHandler'),       
        webapp2.Route(r'/create_new',handler='handlers.kyle.NewBlogPostHandler'),
    ]),
    
    #Family
    webapp2.Route(r'/family',handler='handlers.family.FamilyMainPageHandler'),
    webapp2.Route(r'/family/member/<familyMemberName>', handler='handlers.family.FamilyHandler'),
    routes.PathPrefixRoute(r'/family/videos', [
        webapp2.Route(r'/display',handler='handlers.family.VideoHandler'),
        webapp2.Route(r'/like',handler='handlers.family.VideoLikeHandler'), #Ajax handler
    ]),
    webapp2.Route(r'/family/makedummydata', handler='handlers.family.DummyData'),
    
    #Book Reviews
    webapp2.Route(r'/reviews',handler='handlers.book_reviews_handler.BookReviewHandler')
    ]