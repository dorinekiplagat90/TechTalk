# Seed database with example data
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import User, Post, Comment, Like, Follower
from auth import hash_password

def seed_database():
    init_db()
    db = SessionLocal()
    
    db.query(Follower).delete()
    db.query(Like).delete()
    db.query(Comment).delete()
    db.query(Post).delete()
    db.query(User).delete()
    db.commit()
    
    # Create 15 users
    users_data = [
        {"username": "alice_dev", "email": "alice@example.com", "password": "password123", "bio": "Full-stack developer | Python & React enthusiast", "profile_pic": "https://i.pravatar.cc/150?img=1"},
        {"username": "bob_coder", "email": "bob@example.com", "password": "password123", "bio": "Backend engineer | Love building APIs", "profile_pic": "https://i.pravatar.cc/150?img=2"},
        {"username": "charlie_tech", "email": "charlie@example.com", "password": "password123", "bio": "DevOps | Cloud architecture", "profile_pic": "https://i.pravatar.cc/150?img=3"},
        {"username": "diana_js", "email": "diana@example.com", "password": "password123", "bio": "Frontend developer | JavaScript ninja", "profile_pic": "https://i.pravatar.cc/150?img=4"},
        {"username": "eve_data", "email": "eve@example.com", "password": "password123", "bio": "Data Scientist | ML enthusiast", "profile_pic": "https://i.pravatar.cc/150?img=5"},
        {"username": "frank_mobile", "email": "frank@example.com", "password": "password123", "bio": "Mobile dev | Flutter & React Native", "profile_pic": "https://i.pravatar.cc/150?img=6"},
        {"username": "grace_ui", "email": "grace@example.com", "password": "password123", "bio": "UI/UX Designer | Making apps beautiful", "profile_pic": "https://i.pravatar.cc/150?img=7"},
        {"username": "henry_security", "email": "henry@example.com", "password": "password123", "bio": "Security researcher | Ethical hacker", "profile_pic": "https://i.pravatar.cc/150?img=8"},
        {"username": "iris_ai", "email": "iris@example.com", "password": "password123", "bio": "AI researcher | Deep learning", "profile_pic": "https://i.pravatar.cc/150?img=9"},
        {"username": "jack_blockchain", "email": "jack@example.com", "password": "password123", "bio": "Blockchain developer | Web3 builder", "profile_pic": "https://i.pravatar.cc/150?img=10"},
        {"username": "kate_product", "email": "kate@example.com", "password": "password123", "bio": "Product Manager | Tech strategy", "profile_pic": "https://i.pravatar.cc/150?img=11"},
        {"username": "leo_game", "email": "leo@example.com", "password": "password123", "bio": "Game developer | Unity & Unreal", "profile_pic": "https://i.pravatar.cc/150?img=12"},
        {"username": "mia_cloud", "email": "mia@example.com", "password": "password123", "bio": "Cloud architect | AWS certified", "profile_pic": "https://i.pravatar.cc/150?img=13"},
        {"username": "noah_startup", "email": "noah@example.com", "password": "password123", "bio": "Startup founder | Building the future", "profile_pic": "https://i.pravatar.cc/150?img=14"},
        {"username": "olivia_qa", "email": "olivia@example.com", "password": "password123", "bio": "QA Engineer | Breaking things professionally", "profile_pic": "https://i.pravatar.cc/150?img=15"},
    ]
    
    users = []
    for user_data in users_data:
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            password=hash_password(user_data["password"]),
            bio=user_data["bio"],
            profile_pic=user_data["profile_pic"],
            security_question="What is your favorite color?",
            security_answer="blue"
        )
        db.add(user)
        users.append(user)
    
    db.commit()
    
    # Create 30+ posts with longer content and code images
    posts_data = [
        {"user_idx": 0, "content": "Just deployed my first FastAPI app to production! 🚀\n\nThe performance is incredible - handling 10k requests/second with ease. Here's what I learned:\n\n1. Use async/await everywhere\n2. Pydantic validation is a lifesaver\n3. Auto-generated docs are amazing\n\n#FastAPI #Python #WebDev", "image_url": "https://i.imgur.com/8YzKQ5M.png"},
        {"user_idx": 0, "content": "React hooks have completely changed how I write components. useEffect is a game changer! No more class components for me.", "tags": "react,javascript,webdev"},
        {"user_idx": 1, "content": "Debugging a race condition in production... 😅\n\nSpent 6 hours tracking down a bug that only happened under high load. Turns out it was a shared state issue between async tasks.\n\nLesson learned: Always use proper locking mechanisms!\n\n#DevLife #Debugging", "image_url": "https://i.imgur.com/9nohQh4.png"},
        {"user_idx": 1, "content": "SQLAlchemy ORM makes database operations so much cleaner. Highly recommend for any Python project!", "tags": "python,database,orm"},
        {"user_idx": 2, "content": "Setting up CI/CD pipeline with GitHub Actions 🔄\n\nAutomated:\n✅ Testing\n✅ Linting\n✅ Building\n✅ Deployment\n\nDevelopment velocity increased by 300%!\n\n#DevOps #Automation", "image_url": "https://i.imgur.com/5ChkzcU.png"},
        {"user_idx": 2, "content": "Docker containers have saved me so many times. 'Works on my machine' is no longer an excuse 🐳", "tags": "docker,devops,containers"},
        {"user_idx": 3, "content": "TailwindCSS is the best thing that happened to CSS. Change my mind! 💅\n\nNo more writing custom CSS for every component. Utility classes make styling so fast and consistent.\n\n#TailwindCSS #CSS #Frontend", "tags": "tailwind,css,frontend"},
        {"user_idx": 3, "content": "Just learned about Web Workers. Parallel processing in the browser is amazing! Heavy computations no longer block the UI.", "tags": "javascript,webworkers,performance"},
        {"user_idx": 4, "content": "Training a neural network to recognize cat breeds 🐱\n\nDataset: 10,000 images\nModel: ResNet-50\nAccuracy: 95.3%\n\nNext step: Deploy as a web API!\n\n#MachineLearning #AI #DeepLearning", "image_url": "https://i.imgur.com/xKQYZQZ.png"},
        {"user_idx": 4, "content": "Pandas + NumPy = Data science magic ✨\n\nProcessed 10GB of data in under 2 minutes. Vectorization is key!", "tags": "python,datascience,pandas"},
        {"user_idx": 5, "content": "Flutter's hot reload is a game changer for mobile development! See changes instantly without losing app state.", "tags": "flutter,mobile,dart"},
        {"user_idx": 5, "content": "Cross-platform development has never been easier. React Native FTW! One codebase, iOS + Android.", "tags": "reactnative,mobile,javascript"},
        {"user_idx": 6, "content": "Figma is revolutionizing how designers and developers collaborate 🎨\n\nReal-time collaboration\nComponent libraries\nDev handoff tools\n\nDesign-to-code workflow is seamless!", "tags": "figma,design,uiux"},
        {"user_idx": 6, "content": "Dark mode isn't just a trend, it's a necessity for modern apps. Users expect it, and it reduces eye strain.", "tags": "design,darkmode,ux"},
        {"user_idx": 7, "content": "Found a critical XSS vulnerability today 🔒\n\nAlways sanitize user inputs!\nUse Content Security Policy\nValidate on both client AND server\n\nSecurity is not optional.\n\n#CyberSecurity #WebSecurity", "image_url": "https://i.imgur.com/TKNpfeq.png"},
        {"user_idx": 7, "content": "Two-factor authentication should be mandatory for all apps in 2024. Password-only auth is not enough anymore.", "tags": "security,2fa,authentication"},
        {"user_idx": 8, "content": "GPT-4 is mind-blowing 🤖\n\nBuilding an AI assistant that:\n- Writes code\n- Debugs errors\n- Explains concepts\n\nThe future of development is here!\n\n#AI #GPT4 #MachineLearning", "tags": "ai,gpt4,openai"},
        {"user_idx": 8, "content": "Working on a computer vision project. OpenCV is incredibly powerful for image processing and real-time video analysis!", "tags": "opencv,computervision,python"},
        {"user_idx": 9, "content": "Smart contracts are changing how we think about trust in applications. Decentralized, transparent, and immutable.", "tags": "blockchain,smartcontracts,web3"},
        {"user_idx": 9, "content": "Ethereum gas fees are still too high 💸\n\nLayer 2 solutions like Polygon and Arbitrum can't come soon enough!\n\n#Ethereum #Blockchain", "tags": "ethereum,blockchain,layer2"},
        {"user_idx": 10, "content": "Product-market fit is everything. Build what users actually need, not what you think they need!\n\nTalk to customers daily\nIterate quickly\nMeasure everything", "tags": "product,startup,business"},
        {"user_idx": 10, "content": "User feedback is gold 💎\n\nEvery complaint is an opportunity to improve. Always listen to your customers.", "tags": "product,feedback,ux"},
        {"user_idx": 11, "content": "Unity's new rendering pipeline is a massive improvement 🎮\n\nBetter graphics\nHigher performance\nEasier to optimize\n\nGame development just got better!\n\n#Unity #GameDev", "image_url": "https://i.imgur.com/mV7iV8k.png"},
        {"user_idx": 11, "content": "Indie game development is tough but so rewarding! Just shipped my first game on Steam. 1000+ wishlists!", "tags": "gamedev,indie,unity"},
        {"user_idx": 12, "content": "Kubernetes orchestration makes scaling apps so much easier ☸️\n\nAuto-scaling\nLoad balancing\nSelf-healing\n\nCloud-native architecture at its best!", "tags": "kubernetes,cloud,devops"},
        {"user_idx": 12, "content": "AWS Lambda + API Gateway = Serverless heaven ☁️\n\nNo servers to manage\nPay only for what you use\nInfinite scalability\n\n#Serverless #AWS", "tags": "aws,serverless,cloud"},
        {"user_idx": 13, "content": "Launched our MVP today! 🚀\n\nBuilt in 3 months\n50 beta users signed up\nExcited to see feedback\n\nStartup journey begins!\n\n#Startup #MVP", "tags": "startup,mvp,launch"},
        {"user_idx": 13, "content": "Startup life: 20% coding, 80% talking to customers. Understanding the problem is more important than the solution.", "tags": "startup,entrepreneurship,business"},
        {"user_idx": 14, "content": "Found 15 bugs before production 🐛\n\nQA saves the day again!\n\nAutomated tests caught:\n- 8 edge cases\n- 4 race conditions\n- 3 memory leaks\n\n#QA #Testing", "tags": "qa,testing,quality"},
        {"user_idx": 14, "content": "Automated testing is not optional. It's essential for quality software. Write tests, save time debugging later.", "tags": "testing,automation,qa"},
    ]
    
    posts = []
    for post_data in posts_data:
        post = Post(
            user_id=users[post_data["user_idx"]].id,
            content=post_data["content"],
            image_url=post_data.get("image_url", ""),
            tags=post_data.get("tags", "")
        )
        db.add(post)
        posts.append(post)
    
    db.commit()
    
    # Create comments
    comments_data = [
        {"user_idx": 1, "post_idx": 0, "content": "FastAPI is awesome! What hosting service did you use?"},
        {"user_idx": 2, "post_idx": 0, "content": "Congrats! FastAPI + Docker is my go-to stack"},
        {"user_idx": 3, "post_idx": 1, "content": "useState and useEffect are essential. Have you tried useReducer?"},
        {"user_idx": 0, "post_idx": 3, "content": "Totally agree! The relationship system is so intuitive"},
        {"user_idx": 1, "post_idx": 6, "content": "Tailwind is great but the bundle size can get large. Tree-shaking helps!"},
        {"user_idx": 5, "post_idx": 8, "content": "That's impressive! What dataset are you using?"},
        {"user_idx": 7, "post_idx": 14, "content": "Security first! Thanks for sharing"},
        {"user_idx": 9, "post_idx": 16, "content": "Have you tried the new GPT-4 Turbo? Even better!"},
    ]
    
    for comment_data in comments_data:
        comment = Comment(
            user_id=users[comment_data["user_idx"]].id,
            post_id=posts[comment_data["post_idx"]].id,
            content=comment_data["content"]
        )
        db.add(comment)
    
    db.commit()
    
    # Create likes
    likes_data = [
        {"user_idx": 1, "post_idx": 0}, {"user_idx": 2, "post_idx": 0}, {"user_idx": 3, "post_idx": 0},
        {"user_idx": 0, "post_idx": 2}, {"user_idx": 2, "post_idx": 2},
        {"user_idx": 0, "post_idx": 4}, {"user_idx": 1, "post_idx": 4},
        {"user_idx": 0, "post_idx": 6}, {"user_idx": 1, "post_idx": 6}, {"user_idx": 2, "post_idx": 6},
        {"user_idx": 4, "post_idx": 8}, {"user_idx": 5, "post_idx": 8},
        {"user_idx": 6, "post_idx": 12}, {"user_idx": 7, "post_idx": 12},
        {"user_idx": 8, "post_idx": 16}, {"user_idx": 9, "post_idx": 16},
    ]
    
    for like_data in likes_data:
        like = Like(
            user_id=users[like_data["user_idx"]].id,
            post_id=posts[like_data["post_idx"]].id
        )
        db.add(like)
    
    db.commit()
    
    # Create follow relationships
    follows_data = [
        {"follower_idx": 0, "followed_idx": 1}, {"follower_idx": 0, "followed_idx": 2}, {"follower_idx": 0, "followed_idx": 3},
        {"follower_idx": 1, "followed_idx": 0}, {"follower_idx": 1, "followed_idx": 2},
        {"follower_idx": 2, "followed_idx": 0}, {"follower_idx": 2, "followed_idx": 1},
        {"follower_idx": 3, "followed_idx": 0}, {"follower_idx": 4, "followed_idx": 0},
        {"follower_idx": 5, "followed_idx": 1}, {"follower_idx": 6, "followed_idx": 2},
        {"follower_idx": 7, "followed_idx": 3}, {"follower_idx": 8, "followed_idx": 4},
    ]
    
    for follow_data in follows_data:
        follow = Follower(
            follower_id=users[follow_data["follower_idx"]].id,
            followed_id=users[follow_data["followed_idx"]].id
        )
        db.add(follow)
    
    db.commit()
    db.close()
    
    print("✅ Database seeded successfully with 15 users and 30+ posts!")
    print("\nTest accounts:")
    for user_data in users_data[:4]:
        print(f"Email: {user_data['email']} | Password: password123")

if __name__ == "__main__":
    seed_database()
