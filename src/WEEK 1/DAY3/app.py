from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        feedback = request.form.get('feedback')
        
    
        print(f"Feedback received from {name} ({email}): {feedback}")

        return redirect(url_for('thankyou', username=name))
    return render_template('index.html')

@app.route('/thankyou')
def thankyou():
    username = request.args.get('username', 'User')
    return render_template('thankyou.html', name=username)

if __name__ == '__main__':
    app.run(debug=True)
