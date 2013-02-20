import os
import re

from article import Article


class ArticleTree:
    def __init__(self, content_path):
        
        def build_routes(parent_path, parent_route=''):
            routes = {}
            
            for entry in os.listdir(parent_path):
                path = os.path.join(parent_path, entry)
                if os.path.isdir(path):
                    # parse the name of the child directory
                    m = re.match('((\d+)\.)?(.*)', entry)
                    index_num = int(m.group(2)) if m.group(2) else None
                    slug = m.group(3)
                    route = '/'.join((parent_route, slug))
                    
                    # add article (and its children) to the routes dict
                    routes[route] = index_num, Article(path, route, self)
                    routes.update(build_routes(path, route))
                    
            return routes
        
        
        self.routes = build_routes(content_path)
        
        # generate variables for all articles
        # note: let's find a way to avoid this
        for _, article in self.routes.values():
            article.generate_vars()
        
    
    def get_article(self, route):
        try:
            return self.routes['/' + route][1]
        except KeyError:
            return None
    

    def get_child_articles(self, parent_route):
        articleinfo = (ainfo for route, ainfo in self.routes.items()
                       if route.rsplit('/', 1)[0] == parent_route)
        
        return [article for index_num, article in sorted(articleinfo)
                if index_num is not None]
        