import os

import markdown


class Article:
    def __init__(self, path, index, children):
        self.path = path
        self.index = index
        self.children = children
        
        self.template = next(os.path.splitext(entry)[0]
                             for entry in sorted(os.listdir(self.path))
                             if os.path.splitext(entry)[1] == '.txt'
                             and not os.path.isdir(entry)
                             )

        
    def set_siblings(self, siblings):
        self.siblings = siblings
        
        
    def get_content_vars(self):
        cvars = {}         
        with open(os.path.join(self.path, '{0}.txt'.format(self.template)), 'rb') as content:
            for line in content.read().split('\n-\n'):
                try:
                    var, value = line.split(':', 1)
                    cvars[var.strip()] = (value.strip() if '\n' not in value.rstrip()
                                          else markdown.markdown(value.strip(),
                                                                 safe_mode='escape'))
                except ValueError:
                    continue
                    
        return cvars
        
        
    def generate_vars(self):
        return {}
                       
        
        
        
#        self.route = route.split('/')
#        self.folders = []
#        
#        path = content_path
#        for slug in self.route:
#            for entry in os.listdir(path):
#                if os.path.isdir(os.path.join(path, entry)):
#                    m = re.match('(\d+)\.(.*)', entry)
#                    if m is not None and m.group(2) == slug:
#                        self.folders.append((m.group(2), entry))
#        
#        self.vars = {'root': web_root,
#                     'page_name': self.folders[-1].split('.', 1)[1].replace('-', ' '),
#                     'uri': '/'.join((web_root, route)),
#                     'route': route,
#                     'index': folders[-1].split('.')[0],
#                     'folder_index': '',
#                     'slug': folders[-1].split('.', 1)[1]
#                     'is_current': 
#                     'is_first': 
#                     'is_last': 
#                     'parent': 
#                     'prev_sibling': 
#                     'next_sibling': 
#                     'first_sibling': 
#                     'last_sibling': 
#                     'first_child': 
#                     'last_child': 
#                      }
        
        