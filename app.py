from flask import Flask, render_template, request, redirect, url_for, flash, \
    Response, session     
from flask_bootstrap import Bootstrap  
from filters import datetimeformat, file_type
from resources import get_bucket, get_buckets_list

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'secret'
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        bucket = request.form['bucket']
        session['bucket'] = bucket
        return redirect(url_for('files'))
    else:
        buckets = get_buckets_list()
        return render_template("index.html", buckets=buckets)


@app.route('/files')
def files():
    my_bucket = get_bucket()
    summaries = my_bucket.objects.all()

    objects = []
    for obj in summaries:
        if not obj.key.endswith('/'):
            objects.append(obj)

    return render_template('files.html', files=objects)



@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']
    my_bucket = get_bucket()

    file_obj = my_bucket.Object(key).get()
    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )


if __name__ == "__main__":
    app.run()
