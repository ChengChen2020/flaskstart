from flask import Flask, render_template, request, flash, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, configure_uploads, IMAGES
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import cv2
import os
import pytesseract

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1/flask_books'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

photos = UploadSet('PHOTO')
app.config['UPLOADED_PHOTO_DEST'] = os.path.join(os.path.dirname(__file__), 'static', 'photos')
app.config['UPLOADED_PHOTO_ALLOW'] = IMAGES

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
configure_uploads(app, photos)

app.secret_key = 'you_know_nothing'
db = SQLAlchemy(app)

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True)
    email = db.Column(db.String(32), unique=True)
    books = db.relationship('Book', backref='author')

    def __repr__(self):
        return '<Author: %s %s>' % (self.name, self.email)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __repr__(self):
        return '<Book: %s %s>' % (self.name, self.author_id)


class RegisterForm(FlaskForm):
    author = StringField('作者: ', validators=[DataRequired()])
    email = StringField('邮箱: ', validators=[DataRequired()])
    book = StringField('书名: ', validators=[DataRequired()])
    input = SubmitField('提交')

class AddForm(FlaskForm):
    param1 = StringField('', validators=[DataRequired()])
    param2 = StringField('', validators=[DataRequired()])
    add = SubmitField('求和')

class DiffForm(FlaskForm):
    param3 = StringField('', validators=[DataRequired()])
    param4 = StringField('', validators=[DataRequired()])
    sub = SubmitField('做差')

class MulForm(FlaskForm):
    param5 = StringField('', validators=[DataRequired()])
    param6 = StringField('', validators=[DataRequired()])
    mul = SubmitField('求积')

class DivForm(FlaskForm):
    param7 = StringField('', validators=[DataRequired()])
    param8 = StringField('', validators=[DataRequired()])
    div = SubmitField('求商')

class FileForm(FlaskForm):
    file = FileField('上传文件: ', validators=[FileAllowed(photos, '文件格式不对'), FileRequired()])
    submit = SubmitField('提交')

class GameForm(FlaskForm):
    param1 = StringField('', validators=[DataRequired()])
    param2 = StringField('', validators=[DataRequired()])
    param3 = StringField('', validators=[DataRequired()])
    param4 = StringField('', validators=[DataRequired()])
    submit = SubmitField('求解')

@app.route('/add', methods=['GET', 'POST'])
def add():
    add_form = AddForm()
    c = 0.0000
    if add_form.validate_on_submit():
        a = request.form.get('param1')
        b = request.form.get('param2')
        c = float(a) + float(b)

    diff_form = DiffForm()
    d = 0.0000
    if diff_form.validate_on_submit():
        a = request.form.get('param3')
        b = request.form.get('param4')
        d = float(a) - float(b)

    mul_form = MulForm()
    e = 0.0000
    if mul_form.validate_on_submit():
        a = request.form.get('param5')
        b = request.form.get('param6')
        e = float(a) * float(b)

    div_form = DivForm()
    f = 0.0000
    if div_form.validate_on_submit():
        a = request.form.get('param7')
        b = request.form.get('param8')
        if float(b) == 0.0:
            flash('被除数不能为0')
            f = 0.0
        else:
            f = float(a) / float(b)
    return render_template('arithmetic.html',
                           add_form=add_form,
                           diff_form=diff_form,
                           mul_form=mul_form,
                           div_form=div_form,
                           c=c, d=d, e=e, f=f)


@app.route('/dot24', methods=['GET', 'POST'])
def dot24():
    form = GameForm()
    expr = '请输入四个整数...'
    if form.validate_on_submit():
        a = request.form.get('param1')
        b = request.form.get('param2')
        c = request.form.get('param3')
        d = request.form.get('param4')
        number = [int(a), int(b), int(c), int(d)]
        result = [a, b, c, d]
        if game(4, number, result):
            expr = result[0]
        else:
            expr = '无解'
    return render_template('dot24.html', form=form, expr=expr)


def game(n, number, result):
    if n == 1:
        if abs(number[0] - 24) < 1e-6:
            return True
        return False
    for i in range(0, n):
        for j in range(i + 1, n):
            a = number[i]
            b = number[j]
            number[j] = number[n - 1]

            expr_a = result[i]
            expr_b = result[j]
            result[j] = result[n - 1]

            result[i] = '(' + expr_a + '+' + expr_b + ')'
            number[i] = a + b
            if game(n - 1, number, result):
                return True

            result[i] = '(' + expr_a + '-' + expr_b + ')'
            number[i] = a - b
            if game(n - 1, number, result):
                return True

            result[i] = '(' + expr_b + '-' + expr_a + ')'
            number[i] = b - a
            if game(n - 1, number, result):
                return True

            result[i] = '(' + expr_a + '*' + expr_b + ')'
            number[i] = a * b
            if game(n - 1, number, result):
                return True

            if b != 0:
                result[i] = '(' + expr_a + '/' + expr_b + ')'
                number[i] = a / b
                if game(n - 1, number, result):
                    return True

            if a != 0:
                result[i] = '(' + expr_b + '/' + expr_a + ')'
                number[i] = b / a
                if game(n - 1, number, result):
                    return True

            number[i] = a
            number[j] = b
            result[i] = expr_a
            result[j] = expr_b

    return False

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    file_form = FileForm()
    if request.method == "GET":
        return render_template("extraction.html", form=file_form, error="")
    filename = photos.save(file_form.file.data, name=file_form.file.data.filename)
    return redirect(url_for('show', name=filename))

@app.route('/photo/<name>')
def show(name):

    if name is None:
        os.abort(404)
    url = photos.url(name)

    from aip import AipOcr

    """ 你的 APPID AK SK """
    APP_ID = '17892858'
    API_KEY = 'RTvtQCQDEzX1a0ltdfmx0vq6'
    SECRET_KEY = 'Bx9SU6vfByxI6l47dAPCMEYZZp6NaZTr'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    """ 读取图片 """
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    image = get_file_content(os.path.join(os.path.dirname(__file__), 'static', 'photos', name))

    """ 调用通用文字识别, 图片参数为本地图片 """
    # client.basicGeneral(image)

    """ 如果有可选参数 """
    options = {"language_type": "CHN_ENG", "detect_direction": "true", "probability": "true"}

    """ 带参数调用通用文字识别, 图片参数为本地图片 """
    raw = client.basicAccurate(image, options)['words_result']

    info = ''
    for i in raw:
        text = i['words']
        if text[:2] in ['临时', '姓名', '性别', '出生', '住址', '有效', '签发', '公民']:
            info += '\r\n'
        info += text

    return render_template('show.html', url=url, name=name, info=info)


def preprocess(gray):
    # 1. Sobel算子，x方向求梯度
    sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)
    # 2. 二值化
    ret, binary = cv2.threshold(sobel, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

    # 3. 膨胀和腐蚀操作的核函数
    element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 9))
    element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 6))

    # 4. 膨胀一次，让轮廓突出
    dilation = cv2.dilate(binary, element2, iterations=1)

    # 5. 腐蚀一次，去掉细节，如表格线等。注意这里去掉的是竖直的线
    erosion = cv2.erode(dilation, element1, iterations=1)

    # 6. 再次膨胀，让轮廓明显一些
    dilation2 = cv2.dilate(erosion, element2, iterations=2)

    # 7. 存储中间图片
    # cv2.imwrite("./static/binary.png", binary)
    # cv2.imwrite("./static/dilation.png", dilation)
    # cv2.imwrite("./static/erosion.png", erosion)
    # cv2.imwrite("./static/dilation2.png", dilation2)

    return dilation2

@app.route('/', methods=['GET', 'POST'])
def index():
    authors = Author.query.all()

    register_form = RegisterForm()

    if request.method == 'POST':
        if register_form.validate_on_submit():
            author_name = request.form.get('author')
            book_name = request.form.get('book')
            if Book.query.filter_by(name=book_name).first():
                flash('已存在同名书籍')
            else:
                author = Author.query.filter_by(name=author_name).first()
                if author:
                    try:
                        db.session.add(Book(name=book_name, author_id=author.id))
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        flash('添加书籍失败')
                        db.session.rollback()
                else:
                    try:
                        new_author = Author(name=author_name)
                        db.session.add(new_author)
                        db.session.commit()
                        new_book = Book(name=book_name, author_id=new_author.id)
                        db.session.add(new_book)
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        flash('添加作者和书籍失败')
                        db.session.rollback()
        else:
            flash('参数不全')

    return render_template('index.html',
                           form=register_form,
                           authors=Author.query.all())


@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        try:
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('删除数据出错')
            db.session.rollback()
    else:
        flash('书籍不存在')
    return redirect(url_for('index'))


@app.route('/delete_author/<author_id>')
def delete_author(author_id):
    author = Author.query.get(author_id)
    if author:
        try:
            Book.query.filter_by(author_id=author_id).delete()
            db.session.delete(author)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('删除作者出错')
            db.session.rollback()
    else:
        flash('作者不存在')
    return redirect(url_for('index'))


db.drop_all()
db.create_all()

au1 = Author(name='老王', email='lw@qq.com')
au2 = Author(name='老陈', email='lc@outlook.com')
au3 = Author(name='老刘', email='ll@163.com')

db.session.add_all([au1, au2, au3])
db.session.commit()

bk1 = Book(name='老王回忆录', author_id=au1.id)
bk2 = Book(name='我读书少,你别骗我', author_id=au1.id)
bk3 = Book(name='如何才能让自己更骚', author_id=au2.id)
bk4 = Book(name='怎样征服美丽少女', author_id=au3.id)
bk5 = Book(name='如何征服英俊少男', author_id=au3.id)

db.session.add_all([bk1, bk2, bk3, bk4, bk5])
db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
