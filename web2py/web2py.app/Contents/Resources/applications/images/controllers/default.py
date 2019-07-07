def index():
    images = db().select(db.image.ALL, orderby=db.image.title)
    return dict(images=images)

@auth.requires_login()
def show():
    image = db.image(request.args(0, cast=int)) or redirect(URL('index'))
    db.post.image_id.default = image.id
    form = SQLFORM(db.post)
    if form.process().accepted:
        response.flash = 'your comment is posted'
    comments = db(db.post.image_id == image.id).select(orderby=db.post.id)
    return dict(image=image, comments=comments, form=form)

def download():
    return response.download(request, db)

def user():
    return dict(form=auth())

def manage():
    grid = SQLFORM.smartgrid(db.image, linked_tables=['post'])
    return dict(grid=grid)
