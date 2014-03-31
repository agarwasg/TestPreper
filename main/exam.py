from flask.ext import wtf
import flask

import auth
import model
import util
import logging
from main import app

class ExamForm(wtf.Form):
    name = wtf.StringField('Name', [wtf.validators.required()])
    desc = wtf.StringField('Description', [wtf.validators.required()])

@app.route('/exam/create/', methods=['GET', 'POST'])
@auth.login_required
def exam_create():
  form = ExamForm()
  logging.info("hi")
  logging.info(form.name.data)
  logging.info(form.desc.data)
  if form.validate_on_submit():
     logging.info("helwefwefewfewfwefewfewflo")
     exam_db = model.Exam(
        name=form.name.data,
        desc=form.desc.data,
      )
     exam_db.put()
     flask.flash('New Exam was successfully created!', category='success')
     return flask.redirect(flask.url_for('exam_list', order='-created'))
  else:
     flask.flash('Failed to create the exam!', category='info')
     return flask.render_template(
       'exam_create.html',
       html_class='exam-create',
       title='Create Exam',
       form=form,
     )

@app.route('/exam/')
@auth.login_required
def exam_list():
  exam_dbs, more_cursor = util.retrieve_dbs(
      model.Exam.query(),
      limit=util.param('limit', int),
      cursor=util.param('cursor'),
      order=util.param('order') or 'name',
    )
  return flask.render_template(
      'exam_list.html',
      html_class='exam-list',
      title='Exam List',
      exam_dbs=exam_dbs,
      more_url=util.generate_more_url(more_cursor),
    )

@app.route('/exam/<int:exam_id>/')
@auth.login_required
def exam_view(exam_id):
  exam_db = model.Exam.get_by_id(exam_id)
  if not exam_db:
    flask.abort(404)
  return flask.render_template(
      'exam_view.html',
      html_class='exam-view',
      title=exam_db.name,
      exam_db=exam_db,
    )
