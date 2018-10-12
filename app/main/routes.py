from datetime import datetime

from flask import g, current_app
from flask import render_template, flash, redirect, url_for, request
from flask_babel import _
from flask_babel import get_locale
from flask_login import current_user, logout_user
from flask_login import login_required

from app import db

from app.main.forms import ChangePasswordForm
from app.main.forms import EditPorfileForm
from app.main.forms import PostForm
from app.main.forms import Searchform
from app.main.forms import MessageForm
from app.main import bp

from app.models import Post
from app.models import User
from app.models import Message
from app.models import Notification

from guess_language import guess_language

from flask import jsonify
from app.translate import translate

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

        # search_from is visible because of Elasticserarch  service is not start...
        g.search_form = Searchform() if current_app.elasticsearch else None

    #define locale language
    g.locale = str(get_locale())

@bp.route('/')
def home():
    if current_app.dbconnect:
        return redirect(url_for('main.index'))
    else:
        return render_template('error/DBError.html')



@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author = current_user, language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.index', page = posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page = posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html', title=_('Home Page'),
        form=form , posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1 ,type = int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page = posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page = posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html', title=_('Explore'),
                           posts = posts.items, next_url=next_url,
                           prev_url=prev_url)


# =====================================================================================
# 可以使用内置的path转换器告诉Flask框架改变这一默认行为。path转换器允许 规则匹配包含 / 的字符串：
#
# @app.route('/file/<path: name>')
# </path: name>
# 在Flask中，转换器/converter用来对从URL中提取的变量进行预处理，这个过程
# 发生在调用视图函数之前。Flask预置了四种转换器：
#   string - 匹配不包含/的字符串，这是默认的转换器
#   path - 匹配包含/的字符串
#   int - 只有当URL中的变量是整型值时才匹配，并将变量转换为整型
#   float - 只有当URL中的变量是浮点值时才匹配，并将变量转换为浮点型
# =====================================================================================
@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    page = request.args.get('page', 1, type= int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=username, page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('user.html', user=user,
                           posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_popup.html', user=user)



@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditPorfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved!'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username = username).first()

    if user is None:
        flash(_('user %(username)s not found!', username = username))

        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('user %(username)s can not follow yourself!', username = username))
        return redirect(url_for('main.user', username = username))
    current_user.follow(user)
    db.session.commit()
    flash(_('you are following %(username)s', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        flash(_('user %(username)s not found!', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('user %(username)s can not unfollow yourself!',username= username))
        return redirect(url_for('main.user', username = username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('you are not following %(username)s', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/Change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    form = ChangePasswordForm()

    """ Check which button is click """
    if form.submitcancle.data:
        return redirect(url_for('main.user', username=current_user.username))

    if form.validate_on_submit():
        """ check user old password is valid """
        oldpassword_is_valid = current_user.check_password(form.oldpassword.data)

        if oldpassword_is_valid:
            current_user.set_password(form.password.data)
            db.session.commit()
            flash(_("Yes! Your password has been changed!"))
            logout_user()
            return redirect(url_for('auth.login'))
        else:
            flash(_("Oh! Your original password hasn't correct!"))

    return render_template('change_password.html', form=form)


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))

    page = request.args.get('page', 1, type=int)

    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])

    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None

    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None

    return render_template('search.html', title=_('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/translate', methods = [ 'POST' ])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})

@bp.route('/send_message/<recipient>', methods = ['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                    body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash(_('Your message has benn sent.'))
        return redirect(url_for('main.user', username=recipient))
    return render_template('send_message.html', title=_('Send message'),
                    form=form, recipient=recipient)


@bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('main.messages', page=messages.prev_num) \
        if messages.has_prev else None

    return render_template('messages.html', messages=messages.items, next_url=next_url, prev_url=prev_url)


@bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])