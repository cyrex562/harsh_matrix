from bottle import route, run


@route('/hello')
def hello():
    return "hello world!"

# entry point #
run(host='localhost', port=8080, debug=True)

# end of file #