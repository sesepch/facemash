from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import random
import os
from random import choice


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///facemash.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Image model
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    votes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Image {self.name}>"



# Initialize the database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    # Retrieve all images from the database
    images = Image.query.all()

    # Ensure session exists
    if 'current_image' not in session:
        # Initialize with a random image if no current image is set
        session['current_image'] = choice(images).id

    current_image_id = session['current_image']

    # Get the current image
    current_image = Image.query.get(current_image_id)

    # Select a new opponent (exclude the current image)
    opponent = choice([img for img in images if img.id != current_image_id])

    return render_template('index.html', img1=current_image, img2=opponent)


@app.route('/vote/<int:img_id>')
def vote(img_id):
    # Update the vote count for the selected image
    selected_img = Image.query.get(img_id)
    selected_img.votes += 1
    db.session.commit()

    # Set the chosen image as the current image for the next round
    session['current_image'] = img_id

    return redirect(url_for('index'))



@app.route('/leaderboard')
def leaderboard():
    images = Image.query.order_by(Image.votes.desc()).all()
    # Remove file extensions
    leaderboard_data = [
        {"name": os.path.splitext(img.name)[0], "votes": img.votes}
        for img in images
    ]
    return render_template('leaderboard.html', leaderboard=leaderboard_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

