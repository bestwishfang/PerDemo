import web

render = web.template.render('templates/')

urls = (
    '/', 'hello',
    'task/\d', 'task',
    '/(.*)', 'anyd',
)


class anyd:
    def GET(self, name):
        i = web.input(name=None)
        return render.index(name)


class hello:
    def GET(self):
        return "Hello World! This is Web.py Frame!"


class task:
    def GET(self):
        name = 'Bob'
        return render.index(name)


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
