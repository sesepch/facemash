from app import app, db, Image

# Wrap operations in application context
with app.app_context():
    # Recreate the database
    db.drop_all()
    db.create_all()

    # Add sample images
    images = ["милый котик.jpg", "супер милый котик.jpg", "котик милаш.jpg", "котенок ми-ми.jpg", "котенок шляпка.jpg"]
    for image_name in images:
        img = Image(name=image_name)
        db.session.add(img)

    db.session.commit()
    print("Database initialized and images added!")
