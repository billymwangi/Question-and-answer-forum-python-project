from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import generate_password_hash, check_password_hash
from database_and_tables_file import User, Question

app = Flask(__name__)
app.secret_key="hkiojo"

@app.route('/' , methods=["GET", "POST"])
def register():  # put application's code here
    if request.method == "POST":
        userName = request.form["u_name"]
        userEmail = request.form["u_email"]
        userPassword = request.form["u_pass"]
        encryptedUserPassword = generate_password_hash(userPassword)
        User.create(name=userName, email=userEmail, password=encryptedUserPassword)
        flash("User created successfully")
    return render_template("register.html")

@app.route('/login' , methods=["GET", "POST"])
def login():
    if request.method == "POST":
        userEmail = request.form["u_email"]
        userPassword = request.form["u_pass"]
        try:
            user = User.get(User.email == userEmail)
            encryptedPassword = user.password
            if check_password_hash(encryptedPassword, userPassword):
                flash("Login sucessful")
                session["loggedIn"]= True
                session["userName"] = user.name
                #redirect the user to home.html
                return redirect(url_for("home"))
        except:
            flash("wrong email or password")

    return render_template("login.html")

@app.route("/home")
def home():
    if not session["loggedIn"]:
        return redirect(url_for(login))
    return render_template("home.html")

@app.route("/add_questions", methods=['GET', 'POST'])
def addQuestion(): 
    if not session["loggedIn"]:
        return redirect(url_for(login))
    if request.method == "POST":
        questionName = request.form["name"]
        Question.create(question=questionName)
        flash("Question created successfully") 
    return render_template("add_questions.html")

@app.route("/questions")
def questions():
    if not session["loggedIn"]:
        return redirect(url_for(login))
    questions = Question.select()
    return render_template("questions.html", questions=questions)

@app.route("/questionsandanswers")
def questionsandanswers():
    if not session["loggedIn"]:
        return redirect(url_for(login))
    questions = Question.select()
    return render_template("questions_and_answers.html", questions=questions)

@app.route("/delete/<int:id>")
def delete(id):
    if not session["loggedIn"]:
        return redirect(url_for(login))
    Question.delete().where(Question.id ==id).execute()
    flash("Question deleted successfully")
    return redirect(url_for("products"))

@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    if not session["loggedIn"]:
        return redirect(url_for(login))
    question = Question.get(Question.id == id)
    if request.method == 'POST':
        updatedQuestion = request.form['name']
        updatedAnswer = request.form['answer']
        question.name = updatedQuestion
        question.answer = updatedAnswer
        question.save()
        flash('Question answered successfully')
        return redirect(url_for("questions"))
    return render_template("answer_question.html", question=question)

if __name__ == '__main__':
    app.run()
