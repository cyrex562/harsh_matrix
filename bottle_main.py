from bottle import route, run, static_file

# DEFS #
STATIC_FILE_DIR = 'D:\\dev\\harsh_matrix\\static'
DATA_DIR = 'D:\\dev\\harsh_matrix\\data'


# FUNCTIONS #
@route('/main')
def main():
    return static_file('html/main.html', root=STATIC_FILE_DIR)


@route('/js/<filepath>')
def serve_angular_min(filepath):
    return static_file('/js/' + filepath, root=STATIC_FILE_DIR)


@route('/css/<filepath>')
def serve_bootstrap_min_css(filepath):
    return static_file('/css/' + filepath, root=STATIC_FILE_DIR)


@route('/data/<filepath>')
def serve_data_file(filepath):
    return static_file(filepath, root=DATA_DIR)

# entry point #
run(host='localhost', port=8080, debug=True)

# end of file #
