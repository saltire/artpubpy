import os
import re

from article import Article


class ArticleTree:
    def __init__(self, content_path):
        
        def build_routes(path, route=''):
            routes = {}
            
            children = []
            ichildren = []
            for entry in os.listdir(path):
                childpath = os.path.join(path, entry)
                if os.path.isdir(childpath):
                    # parse the name of the child directory
                    m = re.match('((\d+)\.)?(.*)', entry)
                    index_num = m.group(2) or None
                    slug = m.group(3)
                    childroute = '/'.join((route, slug)).lstrip('/')
                    
                    # add child (and its children) to the routes dict
                    routes.update(build_routes(childpath, childroute))
                    
                    # add child to the children list
                    children.append(routes[childroute])
                    if index_num is not None:
                        # also add to the indexed children list
                        ichildren.append((index_num, routes[childroute]))
                    
            # sort indexed children by number
            ichildren = [child for _, child in sorted(ichildren)]
            
            # make all children aware of their indexed siblings
            for child in children:
                child.set_siblings(ichildren)
                
            # add this article to the routes dict
            routes[route] = Article(path, route, ichildren)
            return routes
        
        
        self.routes = build_routes(content_path)
        
    
    def get_article(self, route):
        return self.routes[route] if route in self.routes else None