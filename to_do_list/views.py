from flask import render_template, url_for, redirect, g, request, abort, flash
from to_do_list import app
from to_do_list.forms import TaskForm

import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, ReqlDriverError


# rethink config
RDB_HOST = 'localhost'
RDB_PORT = 28015
TODO_DB = 'to_do_list'


# rdb = r.RethinkDB()
# rdb.connect("localhost", 28015).repl()
# rdb.table('to_do_list').insert({'name':'sail to the moon'})
# h = rdb.table('to_do_list')
# print(type(h))


@app.before_request
def before_request():
    try:
        rdb = r.RethinkDB()
        rdb.connect("localhost", 28015).repl()
        g.rdb_conn = rdb
    except ReqlDriverError:
        abort(503, "Database not connected")


@app.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.connect().close()
    except AttributeError:
        pass


@app.route("/", methods=["GET", "POST"])
def index():
    form = TaskForm()
    if form.validate_on_submit() and request.form['btn'] == 'Save':
        do = g.rdb_conn.table('to_do_list').insert({"name": form.label.data}).run()
        if do:
            flash("添加 {} 成功".format(form.label.data), category="message")
        return redirect(url_for('index'))
    elif form.validate_on_submit() and request.form['btn'] == 'Delete':
        item = form.label.data
        do = g.rdb_conn.table('to_do_list').filter({"name": item}).delete().run()
        if do['deleted'] == 1:
            flash("删除 {} 成功".format(form.label.data), category="warning")
        else:
            flash("你不能删除一个并不存在的东西", category="warning")
        return redirect(url_for('index'))
    to_do_s = list(g.rdb_conn.table('to_do_list').run())
    return render_template('index.html', form=form, tasks=to_do_s)