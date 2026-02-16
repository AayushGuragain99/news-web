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
    
    # Categories and News Data (Added is_trending flag)
    # Format: (Title, Content, IsTrending)
    news_data = {
        "Business": [
            ("Global Markets Rally on Tech Surge", "NVIDIA and Apple reach record highs.", True),
            ("New Startup Unicorn Emerges", "A local fintech firm raises $200M.", False)
        ],
        "Politics": [
            ("Elections 2026: What to Expect", "Analysts weigh in on legislative changes.", True),
            ("New Trade Agreement Signed", "Ten nations agree on digital trade.", False)
        ],
        "Sports": [
            ("Championship Finals Set", "The top two teams prepare for a showdown.", True),
            ("New World Record in Athletics", "A 19-year-old sprinter breaks the record.", False)
        ],
        "Agriculture": [
            ("Sustainable Farming on the Rise", "New tech helps reduce water usage.", False),
            ("Global Grain Supply Stabilizes", "Harvest reports show better yields.", False)
        ]
    }

    for cat_name, posts in news_data.items():
        category = Category(name=cat_name)
        db.session.add(category)
        db.session.flush() 
        for title, content, trending in posts:
            p = Post(title=title, content=content, author=admin, category=category, is_trending=trending)
            db.session.add(p)
    
    db.session.commit()
    print("SUCCESS: Database recreated with 'is_trending' column!")