# Main FastAPI application with all routes
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List
from datetime import datetime

from database import get_db, init_db
from models import User, Post, Comment, Like, Follower, Notification, Repost, Message
from schemas import (
    UserCreate, UserLogin, UserUpdate, UserResponse,
    PostCreate, PostUpdate, PostResponse,
    CommentCreate, CommentResponse,
    NotificationResponse, Token, MessageCreate, MessageResponse
)
from auth import hash_password, verify_password, create_access_token, get_current_user

app = FastAPI(title="TechTalk API")

# CORS middleware - allows frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Root endpoint
@app.get("/")
def root():
    return {"message": "TechTalk API"}

# Register new user
@app.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username already exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create new user with hashed password
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hash_password(user_data.password),
        security_question=user_data.security_question,
        security_answer=user_data.security_answer
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    token = create_access_token({"sub": new_user.id})
    return {"access_token": token, "token_type": "bearer", "user": new_user}

# Login user
@app.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    # Find user by email or username
    user = db.query(User).filter(
        or_(User.email == credentials.email, User.username == credentials.email)
    ).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create access token
    token = create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer", "user": user}

# Get current user profile
@app.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

# Update user profile
@app.put("/profile", response_model=UserResponse)
def update_profile(
    profile_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if profile_data.bio is not None:
        current_user.bio = profile_data.bio
    if profile_data.profile_pic is not None:
        current_user.profile_pic = profile_data.profile_pic
    
    db.commit()
    db.refresh(current_user)
    return current_user

# Get user by ID (no auth required)
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Search users by username (no auth required)
@app.get("/search/users", response_model=List[UserResponse])
def search_users(q: str, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.username.contains(q)).limit(20).all()
    return users

# Create new post
@app.post("/posts", response_model=PostResponse)
def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_post = Post(
        user_id=current_user.id,
        content=post_data.content,
        image_url=post_data.image_url or "",
        tags=post_data.tags or ""
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    # Add computed fields
    new_post.likes_count = 0
    new_post.comments_count = 0
    new_post.is_liked = False
    return new_post

# Get public feed - all recent posts (no auth required)
@app.get("/feed/public", response_model=List[PostResponse])
def get_public_feed(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    posts = db.query(Post).order_by(Post.timestamp.desc()).offset(skip).limit(limit).all()
    
    result = []
    for post in posts:
        post.likes_count = db.query(func.count(Like.id)).filter(Like.post_id == post.id).scalar()
        post.comments_count = db.query(func.count(Comment.id)).filter(Comment.post_id == post.id).scalar()
        post.is_liked = False
        result.append(post)
    
    return result

# Get feed - posts from followed users
@app.get("/feed", response_model=List[PostResponse])
def get_feed(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    followed_ids = db.query(Follower.followed_id).filter(
        Follower.follower_id == current_user.id
    ).all()
    followed_ids = [f[0] for f in followed_ids]
    followed_ids.append(current_user.id)  # Include own posts
    
    posts = db.query(Post).filter(
        Post.user_id.in_(followed_ids)
    ).order_by(Post.timestamp.desc()).offset(skip).limit(limit).all()
    
    result = []
    for post in posts:
        likes_count = db.query(func.count(Like.id)).filter(Like.post_id == post.id).scalar()
        comments_count = db.query(func.count(Comment.id)).filter(Comment.post_id == post.id).scalar()
        is_liked = db.query(Like).filter(
            Like.post_id == post.id, Like.user_id == current_user.id
        ).first() is not None
        
        post.likes_count = likes_count
        post.comments_count = comments_count
        post.is_liked = is_liked
        result.append(post)
    
    return result

# Get suggested users to follow
@app.get("/users/suggested", response_model=List[UserResponse])
def get_suggested_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 5
):
    # Get users current user is already following
    following_ids = db.query(Follower.followed_id).filter(
        Follower.follower_id == current_user.id
    ).all()
    following_ids = [f[0] for f in following_ids]
    following_ids.append(current_user.id)
    
    # Get users not being followed, ordered by follower count
    suggested = db.query(User).filter(
        User.id.notin_(following_ids)
    ).limit(limit).all()
    
    return suggested

# Get single post by ID
@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Add computed fields
    post.likes_count = db.query(func.count(Like.id)).filter(Like.post_id == post.id).scalar()
    post.comments_count = db.query(func.count(Comment.id)).filter(Comment.post_id == post.id).scalar()
    post.is_liked = db.query(Like).filter(
        Like.post_id == post.id, Like.user_id == current_user.id
    ).first() is not None
    
    return post

# Get posts by user ID (public - no auth required)
@app.get("/users/{user_id}/posts", response_model=List[PostResponse])
def get_user_posts(
    user_id: int,
    db: Session = Depends(get_db)
):
    posts = db.query(Post).filter(Post.user_id == user_id).order_by(Post.timestamp.desc()).all()
    
    result = []
    for post in posts:
        post.likes_count = db.query(func.count(Like.id)).filter(Like.post_id == post.id).scalar()
        post.comments_count = db.query(func.count(Comment.id)).filter(Comment.post_id == post.id).scalar()
        post.is_liked = False  # Default to false for non-authenticated users
        result.append(post)
    
    return result

# Get user's reposts (public - no auth required)
@app.get("/users/{user_id}/reposts", response_model=List[PostResponse])
def get_user_reposts(
    user_id: int,
    db: Session = Depends(get_db)
):
    # Get post IDs that user has reposted
    repost_ids = db.query(Repost.post_id).filter(Repost.user_id == user_id).all()
    repost_ids = [r[0] for r in repost_ids]
    
    # Get the actual posts
    posts = db.query(Post).filter(Post.id.in_(repost_ids)).order_by(Post.timestamp.desc()).all()
    
    result = []
    for post in posts:
        post.likes_count = db.query(func.count(Like.id)).filter(Like.post_id == post.id).scalar()
        post.comments_count = db.query(func.count(Comment.id)).filter(Comment.post_id == post.id).scalar()
        post.is_liked = False
        result.append(post)
    
    return result

# Update post
@app.put("/posts/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_data: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    post.content = post_data.content
    if post_data.image_url is not None:
        post.image_url = post_data.image_url
    
    db.commit()
    db.refresh(post)
    
    post.likes_count = db.query(func.count(Like.id)).filter(Like.post_id == post.id).scalar()
    post.comments_count = db.query(func.count(Comment.id)).filter(Comment.post_id == post.id).scalar()
    post.is_liked = db.query(Like).filter(
        Like.post_id == post.id, Like.user_id == current_user.id
    ).first() is not None
    
    return post

# Delete post
@app.delete("/posts/{post_id}")
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}

# Search posts
@app.get("/search/posts", response_model=List[PostResponse])
def search_posts(
    q: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    posts = db.query(Post).filter(Post.content.contains(q)).order_by(Post.timestamp.desc()).limit(20).all()
    
    result = []
    for post in posts:
        post.likes_count = db.query(func.count(Like.id)).filter(Like.post_id == post.id).scalar()
        post.comments_count = db.query(func.count(Comment.id)).filter(Comment.post_id == post.id).scalar()
        post.is_liked = db.query(Like).filter(
            Like.post_id == post.id, Like.user_id == current_user.id
        ).first() is not None
        result.append(post)
    
    return result

# Create comment on post
@app.post("/posts/{post_id}/comments", response_model=CommentResponse)
def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if post exists
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Create comment
    new_comment = Comment(
        user_id=current_user.id,
        post_id=post_id,
        content=comment_data.content
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    # Create notification for post author
    if post.user_id != current_user.id:
        notification = Notification(
            user_id=post.user_id,
            type="comment",
            message=f"{current_user.username} commented on your post"
        )
        db.add(notification)
        db.commit()
    
    return new_comment

# Get comments for a post (PUBLIC - no auth required)
@app.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.timestamp.desc()).all()
    return comments

# Delete comment
@app.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted"}

# Like a post
@app.post("/posts/{post_id}/likes")
def like_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if post exists
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if already liked
    existing_like = db.query(Like).filter(
        Like.post_id == post_id, Like.user_id == current_user.id
    ).first()
    if existing_like:
        raise HTTPException(status_code=400, detail="Already liked")
    
    # Create like
    new_like = Like(user_id=current_user.id, post_id=post_id)
    db.add(new_like)
    db.commit()
    
    # Create notification for post author
    if post.user_id != current_user.id:
        notification = Notification(
            user_id=post.user_id,
            type="like",
            message=f"{current_user.username} liked your post"
        )
        db.add(notification)
        db.commit()
    
    return {"message": "Post liked"}

# Unlike a post
@app.delete("/posts/{post_id}/likes")
def unlike_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    like = db.query(Like).filter(
        Like.post_id == post_id, Like.user_id == current_user.id
    ).first()
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    
    db.delete(like)
    db.commit()
    return {"message": "Post unliked"}

# Follow a user
@app.post("/users/{user_id}/follow")
def follow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Can't follow yourself
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if already following
    existing_follow = db.query(Follower).filter(
        Follower.follower_id == current_user.id,
        Follower.followed_id == user_id
    ).first()
    if existing_follow:
        raise HTTPException(status_code=400, detail="Already following")
    
    # Create follow relationship
    new_follow = Follower(follower_id=current_user.id, followed_id=user_id)
    db.add(new_follow)
    db.commit()
    
    # Create notification
    notification = Notification(
        user_id=user_id,
        type="follow",
        message=f"{current_user.username} started following you"
    )
    db.add(notification)
    db.commit()
    
    return {"message": "User followed"}

# Unfollow a user
@app.delete("/users/{user_id}/follow")
def unfollow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    follow = db.query(Follower).filter(
        Follower.follower_id == current_user.id,
        Follower.followed_id == user_id
    ).first()
    if not follow:
        raise HTTPException(status_code=404, detail="Not following this user")
    
    db.delete(follow)
    db.commit()
    return {"message": "User unfollowed"}

# Get user's followers
@app.get("/users/{user_id}/followers", response_model=List[UserResponse])
def get_followers(user_id: int, db: Session = Depends(get_db)):
    followers = db.query(User).join(
        Follower, Follower.follower_id == User.id
    ).filter(Follower.followed_id == user_id).all()
    return followers

# Get users that a user is following
@app.get("/users/{user_id}/following", response_model=List[UserResponse])
def get_following(user_id: int, db: Session = Depends(get_db)):
    following = db.query(User).join(
        Follower, Follower.followed_id == User.id
    ).filter(Follower.follower_id == user_id).all()
    return following

# Check if current user is following another user
@app.get("/users/{user_id}/is-following")
def is_following(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    follow = db.query(Follower).filter(
        Follower.follower_id == current_user.id,
        Follower.followed_id == user_id
    ).first()
    return {"is_following": follow is not None}

# Get user notifications
@app.get("/notifications", response_model=List[NotificationResponse])
def get_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(Notification.timestamp.desc()).limit(50).all()
    return notifications

# Mark notification as read
@app.put("/notifications/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    if notification.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    notification.read = True
    db.commit()
    return {"message": "Notification marked as read"}

# Mark all notifications as read
@app.put("/notifications/read-all")
def mark_all_notifications_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.read == False
    ).update({"read": True})
    db.commit()
    return {"message": "All notifications marked as read"}


# Repost a post
@app.post("/posts/{post_id}/repost")
def repost_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    existing_repost = db.query(Repost).filter(
        Repost.post_id == post_id, Repost.user_id == current_user.id
    ).first()
    if existing_repost:
        raise HTTPException(status_code=400, detail="Already reposted")
    
    new_repost = Repost(user_id=current_user.id, post_id=post_id)
    db.add(new_repost)
    db.commit()
    
    if post.user_id != current_user.id:
        notification = Notification(
            user_id=post.user_id,
            type="repost",
            message=f"{current_user.username} reposted your post"
        )
        db.add(notification)
        db.commit()
    
    return {"message": "Post reposted"}

# Unrepost a post
@app.delete("/posts/{post_id}/repost")
def unrepost_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repost = db.query(Repost).filter(
        Repost.post_id == post_id, Repost.user_id == current_user.id
    ).first()
    if not repost:
        raise HTTPException(status_code=404, detail="Repost not found")
    
    db.delete(repost)
    db.commit()
    return {"message": "Repost removed"}

# Send a direct message
@app.post("/messages", response_model=MessageResponse)
def send_message(
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    receiver = db.query(User).filter(User.id == message_data.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_message = Message(
        sender_id=current_user.id,
        receiver_id=message_data.receiver_id,
        content=message_data.content
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    notification = Notification(
        user_id=message_data.receiver_id,
        type="message",
        message=f"{current_user.username} sent you a message"
    )
    db.add(notification)
    db.commit()
    
    return new_message

# Get conversations list
@app.get("/messages/conversations")
def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from sqlalchemy import or_, and_
    
    messages = db.query(Message).filter(
        or_(Message.sender_id == current_user.id, Message.receiver_id == current_user.id)
    ).order_by(Message.timestamp.desc()).all()
    
    conversations = {}
    for msg in messages:
        other_user_id = msg.receiver_id if msg.sender_id == current_user.id else msg.sender_id
        if other_user_id not in conversations:
            other_user = db.query(User).filter(User.id == other_user_id).first()
            unread = db.query(func.count(Message.id)).filter(
                and_(Message.sender_id == other_user_id, Message.receiver_id == current_user.id, Message.read == False)
            ).scalar()
            conversations[other_user_id] = {
                "user": other_user,
                "last_message": msg.content,
                "last_message_time": msg.timestamp,
                "unread_count": unread
            }
    
    return list(conversations.values())

# Get messages with a specific user
@app.get("/messages/{user_id}", response_model=List[MessageResponse])
def get_messages(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from sqlalchemy import or_, and_
    
    messages = db.query(Message).filter(
        or_(
            and_(Message.sender_id == current_user.id, Message.receiver_id == user_id),
            and_(Message.sender_id == user_id, Message.receiver_id == current_user.id)
        )
    ).order_by(Message.timestamp.asc()).all()
    
    db.query(Message).filter(
        and_(Message.sender_id == user_id, Message.receiver_id == current_user.id, Message.read == False)
    ).update({"read": True})
    db.commit()
    
    return messages


# Password reset - verify security question
@app.post("/password-reset/verify")
def verify_security_question(data: dict, db: Session = Depends(get_db)):
    email = data.get("email")
    answer = data.get("security_answer")
    user = db.query(User).filter(User.email == email).first()
    if not user or user.security_answer.lower() != answer.lower():
        raise HTTPException(status_code=400, detail="Invalid email or answer")
    return {"message": "Verified", "security_question": user.security_question}

# Password reset - set new password
@app.post("/password-reset/reset")
def reset_password(data: dict, db: Session = Depends(get_db)):
    email = data.get("email")
    answer = data.get("security_answer")
    new_password = data.get("new_password")
    
    user = db.query(User).filter(User.email == email).first()
    if not user or user.security_answer.lower() != answer.lower():
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    user.password = hash_password(new_password)
    db.commit()
    return {"message": "Password reset successful"}

# Get trending hashtags
@app.get("/trending/tags")
def get_trending_tags(db: Session = Depends(get_db), limit: int = 10):
    posts = db.query(Post).order_by(Post.timestamp.desc()).limit(100).all()
    tag_counts = {}
    for post in posts:
        if post.tags:
            for tag in post.tags.split(','):
                tag = tag.strip()
                if tag:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
    return [{"tag": tag, "count": count} for tag, count in sorted_tags]

# Get trending users
@app.get("/trending/users", response_model=List[UserResponse])
def get_trending_users(db: Session = Depends(get_db), limit: int = 10):
    users = db.query(User).join(Follower, Follower.followed_id == User.id)\
        .group_by(User.id).order_by(func.count(Follower.id).desc()).limit(limit).all()
    return users

# Get unread notification count
@app.get("/notifications/unread-count")
def get_unread_count(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    count = db.query(func.count(Notification.id)).filter(
        Notification.user_id == current_user.id,
        Notification.read == False
    ).scalar()
    return {"unread_count": count}
