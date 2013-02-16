import os
import re

from article import Article


class FileTree:
    def __init__(self, content_path):
        self.routes = {}
        
        def add_route_children(path, parent_route=''):
            children = []
            ichildren = []
            i = 1
            for entry in os.listdir(path):
                childpath = os.path.join(path, entry)
                if os.path.isdir(childpath):
                    m = re.match('((\d+)\.)?(.*)', entry)
                    index_num = m.group(2)
                    slug = m.group(3)
                    route = '/'.join((parent_route, slug))
                    
                    child = Article(childpath, i if index_num else None,
                                    add_route_children(childpath))

                    self.routes[route] = child
                    children.append(child)
                    if index_num:
                        ichildren.append(child)
                        i += 1
            
            for child in children:
                child.set_siblings(ichildren)
            
            return ichildren
        
        
        # INCOMPLETE!!!
        def build_routes(path, route=''):
            routes = {}
            
            # build this route
            m = re.match('((\d+)\.)?(.*)', os.path.basename(path))
            index_num = m.group(2)
            slug = m.group(3)
            
            children = []
            ichildren = []
            for entry in os.listdir(path):
                childpath = os.path.join(path, entry)
                if os.path.isdir(childpath):
                    m = re.match('((\d+)\.)?(.*)', entry)
                    index_num = m.group(2) or None
                    slug = m.group(3)
                    childroute = '/'.join((route, slug))
                    
                    # append child's route and its children's
                    routes.update(build_routes(childpath, childroute))
                    
                    children.append(routes[childroute])
                    if index_num is not None:
                        ichildren.append((index_num, routes[childroute]))
                    
            for child in children:
                child.set_siblings(child for _, child in sorted(ichildren))
                
            routes[route] = Article(path, children)
            return routes
                    
        
        self.routes['/'] = Article(content_path, None, add_route_children(content_path))
        #self.routes = build_routes(content_path)
        
    
    def get_article(self, route):
        return self.routes[route] if route in self.routes else None