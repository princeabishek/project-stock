from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Dummy user data (you can replace this with a database later)
users = {
    "test@example.com": {"password": "password123"}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if user exists and password matches
        if email in users and users[email]['password'] == password:
            flash('Sign-In Successful', 'success')
            return redirect(url_for('dashboard'))  # Redirect to dashboard after sign-in
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return render_template('signin.html')
    return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Simple validation
        if email in users:
            flash('Email already exists. Please use a different one.', 'danger')
            return render_template('signup.html')
        # Add user to dummy database
        users[email] = {"password": password}
        flash('Sign-Up Successful. You can now sign in.', 'success')
        return redirect(url_for('signin'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # Your dashboard page after successful sign-in

if __name__ == '__main__':
    app.run(debug=True)
