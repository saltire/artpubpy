import os

import markdown


class Article:
    def __init__(self, path, route, children):
        self._path = path
        self._template = next(os.path.splitext(entry)[0]
                             for entry in sorted(os.listdir(self._path))
                             if os.path.splitext(entry)[1] == '.txt'
                             and not os.path.isdir(entry)
                             )
        
        variables = self.get_article_vars(route, children)
        variables.update(self.get_content_vars())
        
        for var, value in variables.items():
            setattr(self, var, value)        
        
        
    def set_siblings(self, siblings):
        self._siblings = siblings
        self.index = siblings.index(self) if self in siblings else None
        
        
    def get_template(self):
        return self._template

    
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
    
    
    def get_article_vars(self, route, children):
        return {'route': route,
                'children': children,
#                'page_name': self.folders[-1].split('.', 1)[1].replace('-', ' '),
#                'index': folders[-1].split('.')[0],
#                'folder_index': '',
#                'slug': folders[-1].split('.', 1)[1],
#                'is_current': 
#                'is_first': 
#                'is_last': 
#                'parent': 
#                'prev_sibling': 
#                'next_sibling': 
#                'first_sibling': 
#                'last_sibling': 
#                'first_child': 
#                'last_child': 
                 }
        