import os

import markdown


class Article:
    def __init__(self, path, route, tree, template):
        self._path = path
        self._route = route
        self._tree = tree
        
        # find the first .txt in the path to use as the template
        self._template = next(os.path.splitext(entry)[0]
                              for entry in sorted(os.listdir(path))
                              if os.path.splitext(entry)[1] == '.txt'
                              and not os.path.isdir(entry)
                              )


#    def __getattr__(self, var):
#        if not hasattr(self, var):
#            self.vars = self.get_article_vars()
#            self.vars.update(self.get_content_vars())
#            
#        return self.vars[var] if var in self.vars else None


    def generate_vars(self):
        vrs = self.get_article_vars()
        vrs.update(self.get_content_vars())
        
        for var, value in vrs.items():
            setattr(self, var, value)
        
        
    def get_template(self):
        return self._template
    
    
    def get_article_vars(self):
        parent_route = self._route.rsplit('/', 1)[0]
        
        parent = self._tree.get_article(parent_route) if parent_route != '' else None
        siblings = self._tree.get_child_articles(parent_route)
        index = siblings.index(self) if self in siblings else None
        
        return {'route': self._route,
                'parent': parent,
                'siblings': siblings,
                'index': index,
                'is_first': index == 0,
                'is_last': index == len(siblings) - 1,
                'children': self._tree.get_child_articles(self._route),
                'slug': self._route.rsplit('/', 1)[-1],
                }
        

    def get_content_vars(self):
        cvars = {}
        with open(os.path.join(self._path, '{0}.txt'.format(self._template)), 'rb') as content:
            for line in content.read().replace('\r', '').split('\n-\n'):
                try:
                    var, value = line.split(':', 1)
                except ValueError:
                    continue
                
                cvars[var.strip()] = (value.strip() if '\n' not in value.rstrip()
                                      else markdown.markdown(value.strip(),
                                                             safe_mode='escape'))
        return cvars
    
        