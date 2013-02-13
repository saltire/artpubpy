import os
import re

from flask import Flask, render_template

import markdown


app = Flask(__name__)

content_path = './content'
template_path = './templates'


@app.route('/')
def menu():
    return 'Hello World'


@app.route('/<path:route>')
def article(route):
    path = content_path
    for slug in route.split('/'):
        folders = []
        for entry in os.listdir(path):
            if os.path.isdir(os.path.join(path, entry)):
                m = re.match('(\d+)\.(.*)', entry)
                if m is not None and m.group(2) == slug:
                    folders.append((m.group(2), entry))
                    
        try:
            path = os.path.join(path, sorted(folders)[0][1])
            
        except IndexError:
            #return render_template('404.html')
            return 'Not found.'
        
    cfile = sorted(entry for entry in os.listdir(path)
                   if os.path.splitext(entry)[1] == '.txt'
                   and not os.path.isdir(entry)
                   )[0]
                     
    cvars = {}         
    with open(os.path.join(path, cfile), 'rb') as content:
        for line in content.read().split('\n-\n'):
            var, value = line.split(':', 1)
            cvars[var.strip()] = (value.strip() if '\n' not in value.rstrip()
                                  else markdown.markdown(value.strip(),
                                                         safe_mode='escape'))
            
    tfile = sorted(entry for entry in os.listdir(template_path)
                   if os.path.splitext(entry)[0] == os.path.splitext(cfile)[0])
    
    return render_template(tfile, **cvars)


if __name__ == '__main__':
    app.debug = True
    app.run()