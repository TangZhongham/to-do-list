from to_do_list import app, manager


if __name__ == '__main__':
    app.run('0.0.0.0', port=5017, debug=True)
    # manager.run()