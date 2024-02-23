from flask import (current_app, request, render_template, url_for)
from . import blueprint
from .forms import SearchForm
from app.models import User


## home page
@blueprint.route('/')
@blueprint.route('/index')
def index():
    return render_template('index.html', title='Home')


## explore page
@blueprint.route('/explore', methods=['GET', 'POST'])
def explore():
    form = SearchForm()
    # return search results
    if form.validate_on_submit():
        page = request.args.get('page', 1, type=int)
        users = None
        if form.select.data == 'User':
            users = User.query.filter(User.username.contains(form.search.data)).all()
            total = len(users)
        # paginate results
        next_url = url_for('home_blueprint.results', q=form.search.data, page=page + 1) \
            if total > page * current_app.config['POSTS_PER_PAGE'] else None
        prev_url = url_for('home_blueprint.results', q=form.search.data, page=page - 1) \
            if page > 1 else None
        return render_template('explore.html', title='Results',
                               users=users,
                               next_url=next_url, prev_url=prev_url)
    return render_template('explore.html', title='Search', form=form)
