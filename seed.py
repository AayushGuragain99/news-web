from app import create_app, db
from app.models import User, Post, Category
from app import bcrypt

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    
    # Create Admin
    hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
    admin = User(username='Admin', email='admin@news.com', password=hashed_pw, is_admin=True)
    db.session.add(admin)
    
    # Categories and News Data
    news_data = {
        "Business": [
            ("Global Markets Rally on Tech Surge", "NVIDIA and Apple reach record highs as AI demand skyrockets."),
            ("New Startup Unicorn Emerges in Fintech", "A local fintech firm raises $200M in Series C funding.")
        ],
        "Politics": [
            ("Elections 2026: What to Expect", "Political analysts weigh in on the upcoming legislative changes."),
            ("New Trade Agreement Signed", "Ten nations agree on a new digital trade framework.")
        ],
        "Sports": [
            ("Championship Finals Set for Sunday", "The league's top two teams prepare for a historic showdown."),
            ("New World Record in Athletics", "A 19-year-old sprinter breaks the 100m record in Zurich.")
        ],
        "Agriculture": [
            ("Sustainable Farming Practices on the Rise", "New tech helps farmers reduce water usage by 40%."),
            ("Global Grain Supply Stabilizes", "Harvest reports from the Midwest show better-than-expected yields.")
        ]
    }

    for cat_name, posts in news_data.items():
        category = Category(name=cat_name)
        db.session.add(category)
        db.session.flush() # Gets the category ID
        for title, content in posts:
            p = Post(title=title, content=content, author=admin, category=category)
            db.session.add(p)
    
    db.session.commit()
    print("SUCCESS: Real Categories and 8 News Stories created!")