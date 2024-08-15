import os
import secrets

from flask import render_template, url_for, flash, redirect, request
from LMS import app, db, bcrypt
from LMS.forms import RegistrationForm, LoginForm, UpdateAccountForm,UpdateFacultyAccountForm
from LMS.models import User,Faculty
from flask_login import login_user, current_user, logout_user, login_required
from LMS.forms import FacultyForm

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register as User', form=form)

from flask import request, jsonify

from flask import jsonify

@app.route('/search_faculty')
def search_faculty():
    name = request.args.get('name')
    faculties = None
    try:
        faculties = Faculty.query.filter(Faculty.name.ilike(f'%{name}%')).all()
    except Exception as e:
        print(e)
    if faculties is not None:
        faculty_list = [{
            'name': faculty.name,
            'designation': faculty.designation,
            'school': faculty.school,
            'cabin': faculty.cabin,
            'availability': faculty.availability,
            'remark': faculty.remark
        } for faculty in faculties]
        return jsonify(faculty_list)
    else:
        return jsonify([])



from flask_login import login_user, current_user, logout_user

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        if form.user_type.data == 'student':
            user = User.query.filter_by(email=form.email.data).first()
        elif form.user_type.data == 'faculty':
            user = Faculty.query.filter_by(name=form.email.data).first()  
        else:
            abort(403)

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if form.user_type.data == 'student':
                return redirect(url_for('student'))
            elif form.user_type.data == 'faculty':
                return redirect(url_for('faculty'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html', title='Login', form=form)


from LMS.models import Faculty  

@app.route("/student")
@login_required
def student():
    faculties = Faculty.query.all()  
    return render_template('student.html', faculties=faculties)

@app.route("/faculty")
@login_required
def faculty():
    return render_template('faculty.html')



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))




@app.route('/facultyregister', methods=['GET', 'POST'])
def register_faculty():
    form = FacultyForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_faculty = Faculty(
            name=form.name.data,
            designation=form.designation.data,
            school=form.school.data,
            cabin=form.cabin.data,
            availability=form.availability.data,
            remark=form.remark.data,
            password=hash_password
        )
        db.session.add(new_faculty)
        db.session.commit()
        flash('Faculty registered successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('faculty-register.html', title='Register', form=form)



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# route.py
from flask import render_template

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    if current_user.is_authenticated:
        if current_user.type == 1:
            return redirect(url_for('account_user'))
        else:
            return redirect(url_for('account_faculty'))
    else:
        # Handle unauthenticated users here, maybe redirect them to the login page
        pass


@app.route("/account_user", methods=['GET', 'POST'])
@login_required
def account_user():
    if current_user.type != 1:
        return redirect(url_for('account'))
    form = UpdateAccountForm()

    if form.validate_on_submit():
        # Your update logic here
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account_user'))

    elif request.method == 'GET':
        # Populate form with current user data
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/account_faculty", methods=['GET', 'POST'])
@login_required
def account_faculty():
    if current_user.type != 0:
        return redirect(url_for('account'))
    form = UpdateFacultyAccountForm()

    if form.validate_on_submit():
        # Your update logic here
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account_faculty'))

    elif request.method == 'GET':
        # Populate form with current user data
        form.name.data = current_user.name
        form.designation.data = current_user.designation
        form.school.data = current_user.school
        form.cabin.data = current_user.cabin

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account_faculty.html', title='Faculty Account', image_file=image_file, form=form)

@app.route("/AdminDashboard")
@login_required
def AdminDashboard():
    return render_template('home.html')



@app.route("/home")
@login_required
def homeUser():
    return render_template('home.html')

@app.route("/Book1")
@login_required
def book():
    return render_template('book.html')



from flask import request, jsonify
from flask_login import current_user

from flask_login import current_user

# Route to handle updating availability
@app.route('/update_availability/<int:faculty_id>', methods=['POST'])
def update_availability(faculty_id):
    if current_user.is_authenticated and current_user.id == faculty_id:
        availability = request.json.get('availability')
        faculty = Faculty.query.get(faculty_id)
        if faculty:
            faculty.availability = availability
            db.session.commit()
            return jsonify({'message': 'Availability updated successfully'}), 200
        else:
            return jsonify({'message': 'Faculty not found'}), 404
    else:
        return jsonify({'message': 'Unauthorized'}), 401

# Route to handle adding a remark
@app.route('/add_remark/<int:faculty_id>', methods=['POST'])
def add_remark(faculty_id):
    if current_user.is_authenticated and current_user.id == faculty_id:
        remark = request.json.get('remark')
        faculty = Faculty.query.get(faculty_id)
        if faculty:
            faculty.remark = remark
            db.session.commit()
            return jsonify({'message': 'Remark added successfully'}), 200
        else:
            return jsonify({'message': 'Faculty not found'}), 404
    else:
        return jsonify({'message': 'Unauthorized'}), 401
