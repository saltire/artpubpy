import os
import re

from flask import Flask, render_template, url_for

import markdown

from filetree import FileTree


app = Flask(__name__)

content_path = './content'
template_path = './templates'


@app.route('/articles/')
@app.route('/articles/<path:route>')
def article(route=''):
    filetree = FileTree(content_path)
    
    for route in filetree.routes:
        print route
    
    try:
        article = filetree.routes[route]
    except IndexError:
        return 'Not Found'
    
    tfile = (entry for entry in sorted(os.listdir(template_path))
             if os.path.splitext(entry)[0] == article.template)
    
    return render_template(tfile, **article.get_content_vars())
    
#    path = content_path
#    for slug in route.split('/'):
#        folders = []
#        for entry in os.listdir(path):
#            if os.path.isdir(os.path.join(path, entry)):
#                m = re.match('(\d+)\.(.*)', entry)
#                if m is not None and m.group(2) == slug:
#                    folders.append((m.group(2), entry))
#                    
#        try:
#            path = os.path.join(path, sorted(folders)[0][1])
#            
#        except IndexError:
#            #return render_template('404.html')
#            return 'Not found.'
#        
#    cfile = sorted(entry for entry in os.listdir(path)
#                   if os.path.splitext(entry)[1] == '.txt'
#                   and not os.path.isdir(entry)
#                   )[0]
#                     
#    cvars = {}         
#    with open(os.path.join(path, cfile), 'rb') as content:
#        for line in content.read().split('\n-\n'):
#            var, value = line.split(':', 1)
#            cvars[var.strip()] = (value.strip() if '\n' not in value.rstrip()
#                                  else markdown.markdown(value.strip(),
#                                                         safe_mode='escape'))
#            
#    avars = {'root': url_for('/'),
#            'page_name': folders[-1].split('.', 1)[1].replace('-', ' '),
#            'uri': url_for('/', route=route),
#            'route': route,
#            'index': folders[-1].split('.')[0],
#            'folder_index': '',
#            'slug': folders[-1].split('.', 1)[1]
#            'is_current': 
#            'is_first': 
#            'is_last': 
#            'parent': 
#            'prev_sibling': 
#            'next_sibling': 
#            'first_sibling': 
#            'last_sibling': 
#            'first_child': 
#            'last_child': 
#             }
#            
    


if __name__ == '__main__':
    app.debug = True
    app.run()