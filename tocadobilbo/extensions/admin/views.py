from flask import flash, redirect, request, render_template, Response, url_for
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView

from tocadobilbo.extensions.admin import forms
from tocadobilbo.extensions.database import db
from tocadobilbo.extensions.database.models import Post, PostThumbnail, User
from tocadobilbo.controllers.post import CreatePostController, UpdatePostController

from tocadobilbo.controllers.postthumbnail import (
    CreatePostThumbnailController, 
    DeletePostThumbnailController, 
    UpdatePostThumbnailController
)

from tocadobilbo.controllers.user import CreateUserController, UpdateUserController


class UserModelView(ModelView):
    # column_exclude_list = ['password']
    
    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self) -> Response:
        form = forms.UserForm(request.form)

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            fields = {'username': username, 'password': password}
            
            controller = CreateUserController()
            result = controller.post(fields)

            if result['success'] == False:
                flash(result['message'], 'danger')
            
            else:
                flash(result['message'], 'success')
                return redirect(url_for('user.index_view'))
        
        return self.render(self.create_template, form=form, return_url=url_for('user.index_view'))
    
    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self) -> Response:
        user = db.session.query(User).filter(User.id == request.args.get('id')).first()
        form = forms.UserForm(request.form, obj=user)

        if user is None:
            flash('User not found.', 'danger')
            return redirect(url_for('user.index_view'))

        if request.method == 'POST':
            id = request.args['id']
            username = request.form['username']
            password = request.form['password']
            fields = {'id': id, 'username': username, 'password': password}

            controller = UpdateUserController()
            response = controller.post(fields)

            if response['success'] == False:
                flash(response['message'], 'danger')

            else:
                flash(response['message'], 'success')
                return redirect(url_for('user.index_view'))

        return self.render(self.edit_template, form=form, return_url=url_for('user.index_view'))
        

class PostModelView(ModelView):
    column_exclude_list = ['body', 'body_html']
    create_template = 'admin/post/create.html'
    edit_template = 'admin/post/edit.html'

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self) -> Response:
        form = forms.PostForm(request.form)

        if request.method == 'POST':
            id_user = request.form['user']
            title = request.form['title']
            slug = request.form['slug']
            body = request.form['body']
            fields = {'id_user': id_user, 'title': title, 'body': body, 'slug': slug}

            controller = CreatePostController()
            response = controller.post(fields)
            
            if response['success'] == False:
                flash(response['message'], 'danger')
            
            else:
                flash(response['message'], 'success')
                return redirect(url_for('post.index_view'))
        
        return self.render(self.create_template, form=form, return_url=url_for('post.index_view'))
    
    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self) -> Response:
        post = db.session.query(Post).filter(Post.id == request.args.get('id')).first()
        form = forms.PostForm(request.form, obj=post)
        
        if post is None:
            flash('Post not found.', 'danger')
            return redirect(url_for('post.index_view'))

        if request.method == 'POST':
            id = post.id
            id_user = request.form['user']
            title = request.form['title']
            slug = request.form['slug']
            body = request.form['body']
            fields = {'id': id, 'id_user': id_user, 'title': title, 'slug': slug, 'body': body}

            controller = UpdatePostController()
            response = controller.post(fields)

            if response['success'] == False:
                flash(response['message'], 'danger')

            else:
                flash(response['message'], 'success')
                return redirect(url_for('post.index_view'))
        
        return self.render(self.edit_template, form=form, return_url=url_for('post.index_view'))


class PostThumbnailModelView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = ['post', 'secure_url', 'public_id']


    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self) -> Response:
        form = forms.PostThumbnailForm(request.form)

        if request.method == 'POST':
            id_post = request.form['post']
            source = request.files['source']
            values = {'id_post': id_post, 'source': source}
            
            controller = CreatePostThumbnailController()
            response = controller.post(values)

            if response['success'] == False:
                flash(response['message'], 'danger')

            else:
                flash(response['message'], 'success')
                return redirect(url_for('postthumbnail.index_view'))

        return self.render(self.create_template, form=form, return_url=url_for('postthumbnail.index_view'))

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self) -> Response:
        id = request.args.get('id')
        postthumbnail = db.session.query(PostThumbnail).filter(PostThumbnail.id == id).first()
        form = forms.PostThumbnailForm(request.form, obj=postthumbnail)

        if postthumbnail is None:
            flash('Post Thumbnail not found.', 'danger')
            return redirect(url_for('postthumbnail.index_view'))

        if request.method == 'POST':
            id_post = request.form['post']
            source = request.files['source']
            fields = {'id': id, 'id_post': id_post, 'source': source}

            controller = UpdatePostThumbnailController()
            response = controller.post(fields)

            if response['success'] == False:
                flash(response['message'], 'danger')

            else:
                flash(response['message'], 'success')
                return redirect(url_for('postthumbnail.index_view'))

        return self.render(self.edit_template, form=form, return_url=url_for('postthumbnail.index_view'))
    
    @expose('/delete/', methods=('POST',))
    def delete_view(self) -> None:
        id = request.form.get('id')
        fields = {'id': id}

        controller = DeletePostThumbnailController()
        response = controller.post(fields)

        if response['success'] == False:
            flash(response['message'], 'danger')
        else:
            flash(response['message'], 'success')

        return redirect(url_for('postthumbnail.index_view'))
