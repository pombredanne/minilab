from flask import Blueprint, render_template, make_response, jsonify
import multiprocessing as mp


mod = Blueprint('home', __name__, url_prefix='/home')


def square(n):
    return n**2

@mod.route('/')
def home():
    return 'Worked!'


@mod.route('/hello/')
@mod.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@mod.route('/square')
def mp_test():
    pool = mp.Pool(10)

    result = sum(pool.map(square, range(10000)))

    pool.close()
    pool.join()

    return render_template('home/square.html', result=result)


# This route will prompt a file download with the csv lines
@mod.route('/download')
def download():
    csv = """"REVIEW_DATE","AUTHOR","ISBN","DISCOUNTED_PRICE"
"1985/01/21","Douglas Adams",0345391802,5.95
"1990/01/12","Douglas Hofstadter",0465026567,9.95
"1998/07/15","Timothy ""The Parser"" Campbell",0968411304,18.99
"1999/12/03","Richard Friedman",0060630353,5.95
"2004/10/04","Randel Helms",0879755725,4.50"""
    # We need to modify the response, so the first thing we
    # need to do is create a response out of the CSV string
    response = make_response(csv)
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers["Content-Disposition"] = "attachment; filename=books.csv"
    #response.headers["Content-Length: %s" % len(csv)]
    return response


@mod.route('/json')
def result_client(name=None):
    return jsonify({'test': True})


from flask.ext.admin import BaseView, expose

class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')