import os

from flask import Flask, redirect, render_template, url_for

from tree import ArticleTree


app = Flask(__name__)

CONTENT_PATH = './content/'
TEMPLATE_PATH = './templates/'

tree = ArticleTree(CONTENT_PATH)


@app.route('/')
def menu():
    return render_template('menu.html', root=url_for('menu', _external=True),
                           articles=tree.get_child_articles(''))
    
    
@app.route('/<path:route>')
def article(route=''):
    route = route.rstrip('/')
    
    print 'Trying route:', route,
    
    article = tree.get_article(route)
    if article is None:
        return redirect(url_for('menu'))
    
    print article.children
    
    tfile = next(entry for entry in sorted(os.listdir(TEMPLATE_PATH))
                 if os.path.splitext(entry)[0] == article.get_template())
    
    return render_template(tfile, root=url_for('article', route='', _external=True),
                           **vars(article))
    
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