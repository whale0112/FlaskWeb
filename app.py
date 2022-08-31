from flask import Flask, request, redirect
import random

app = Flask(__name__)

nextId = 4
topics = [
    {'id':1, 'title': 'html', 'body':'html is....'},
    {'id':2, 'title': 'css', 'body':'css is....'},
    {'id':3, 'title': 'javascript', 'body':'javascript is....'},
]

def template(contents, content, id=None):
    needIdUI=''
    if id != None:
        needIdUI = f'''
        <li><a href="/update/{id}/">update</a></li>
        <li><form action="/delete/{id}/" method="POST">
            <input type="submit" value="delete"></form></li>
        '''
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                <li><a href="/create/">create</a></li>
                {needIdUI}
            </ul>
        </body>
    </html>
    '''

def getContents():
    liTags = ''
    for topic in topics:
        id = topic['id']
        title = topic['title']
        liTags = liTags + f'<li><a href="/read/{id}/">{title}</a></li>'
    return liTags

@app.route('/')
def index():
    return template(getContents(), '<h2>Welcome</h2>Hello, WEB')

@app.route('/create/', methods=['GET', 'POST'])
def create():
    print('request', request.method)
    if request.method == 'GET':
        content = '''
        <form action='/create/' method="POST">
            <p><input type="text" name="title" placeholder="title"></p>
            <p><textarea placeholder="body" name="body"></textarea></p>
            <p><input type="submit" value="create"></p>
        </form>
        '''
        return template(getContents(), content)
    elif request.method == 'POST':
        global nextId
        title = request.form['title']
        body = request.form['body']
        newTopic = {'id':nextId, 'title':title, 'body':body}
        topics.append(newTopic)
        url = f'/read/{nextId}/'
        nextId += 1
        return redirect(url)

@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET':
        title = ''
        body = ''
        for topic in topics:
            if id == topic['id']:
                title = topic['title']
                body = topic['body']
                break
        content = f'''
        <form action='/update/{id}' method="POST">
            <p><input type="text" name="title" placeholder="title" value="{title}"></p>
            <p><textarea placeholder="body" name="body">{body}</textarea></p>
            <p><input type="submit" value="update"></p>
        </form>
        '''
        return template(getContents(), content)
    elif request.method =='POST':
        title = request.form['title']
        body = request.form['body']
        for topic in topics:
            if id == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break
        url = f'/read/{id}/'
        return redirect(url)

@app.route('/read/<int:id>/')
def read(id):
    for topic in topics:
        if id == topic['id']:
            title = topic['title']
            body = topic['body']
            break
    return template(getContents(), f'<h2>{title}</h2>{body}',id)

@app.route('/delete/<int:id>/', methods=['POST'])
def deleat(id):
    for topic in topics:
        if id == topic['id']:
            topics.remove(topic)
            break
    return redirect('/')

if __name__ == '__main__'
    app.run(debug=True)
