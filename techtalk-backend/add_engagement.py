#!/usr/bin/env python3
# Add realistic engagement numbers to existing data
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Post, Comment, Like, Follower, Repost
from auth import hash_password
import random

def add_realistic_engagement():
    db = SessionLocal()
    
    # Get all users and posts
    users = db.query(User).all()
    posts = db.query(Post).all()
    
    if not users or not posts:
        print("No users or posts found. Run seed.py first!")
        return
    
    print(f"Found {len(users)} users and {len(posts)} posts")
    
    # Make first 3 users "influencers" with high follower counts
    influencer_indices = [0, 1, 2]
    
    # Add massive follower counts for influencers
    print("\nCreating influencer followers...")
    follower_count = 0
    for influencer_idx in influencer_indices:
        influencer = users[influencer_idx]
        # Each influencer gets followed by most other users
        for follower in users:
            if follower.id != influencer.id:
                existing = db.query(Follower).filter(
                    Follower.follower_id == follower.id,
                    Follower.followed_id == influencer.id
                ).first()
                if not existing:
                    db.add(Follower(follower_id=follower.id, followed_id=influencer.id))
                    follower_count += 1
    
    db.commit()
    print(f"Added {follower_count} new follower relationships")
    
    # Add likes to ALL posts
    print("\nAdding likes to ALL posts...")
    popular_posts = posts[:5]  # First 5 posts are viral
    like_count = 0
    
    # Popular posts get ALL users liking
    for post in popular_posts:
        for user in users:
            existing = db.query(Like).filter(
                Like.user_id == user.id,
                Like.post_id == post.id
            ).first()
            if not existing:
                db.add(Like(user_id=user.id, post_id=post.id))
                like_count += 1
    
    # ALL other posts get at least 5-15 likes
    for post in posts[5:]:
        num_likes = random.randint(5, 15)
        likers = random.sample(users, min(num_likes, len(users)))
        for user in likers:
            existing = db.query(Like).filter(
                Like.user_id == user.id,
                Like.post_id == post.id
            ).first()
            if not existing:
                db.add(Like(user_id=user.id, post_id=post.id))
                like_count += 1
    
    db.commit()
    print(f"Added {like_count} likes to ALL posts")
    
    # Add comments to ALL posts
    print("\nAdding comments to ALL posts...")
    comment_templates = [
        "This is amazing! 🔥",
        "Great insight, thanks for sharing!",
        "I learned so much from this",
        "Bookmarking this for later",
        "Can you share more details?",
        "This helped me solve my problem!",
        "Exactly what I needed",
        "Mind blown 🤯",
        "Thanks for the tutorial!",
        "Following for more content like this",
        "This is gold!",
        "Saved me hours of work",
        "Best explanation I've seen",
        "You're a legend!",
        "More people need to see this",
        "Sharing with my team",
        "This changed my perspective",
        "Incredible work!",
        "Keep these coming!",
        "Absolutely brilliant",
    ]
    
    comment_count = 0
    # Popular posts get 50-100 comments
    for post in popular_posts:
        num_comments = random.randint(50, 100)
        for i in range(num_comments):
            user = random.choice(users)
            comment_text = random.choice(comment_templates)
            db.add(Comment(
                user_id=user.id,
                post_id=post.id,
                content=f"{comment_text} #{i+1}"
            ))
            comment_count += 1
    
    # ALL other posts get at least 3-10 comments
    for post in posts[5:]:
        num_comments = random.randint(3, 10)
        for i in range(num_comments):
            user = random.choice(users)
            comment_text = random.choice(comment_templates)
            db.add(Comment(
                user_id=user.id,
                post_id=post.id,
                content=comment_text
            ))
            comment_count += 1
    
    db.commit()
    print(f"Added {comment_count} comments to ALL posts")
    
    # Add reposts
    print("\nAdding reposts...")
    repost_count = 0
    for post in popular_posts:
        # Each popular post gets 50-100 reposts
        num_reposts = random.randint(50, 100)
        for i in range(num_reposts):
            user = random.choice(users)
            existing = db.query(Repost).filter(
                Repost.user_id == user.id,
                Repost.post_id == post.id
            ).first()
            if not existing:
                db.add(Repost(user_id=user.id, post_id=post.id))
                repost_count += 1
    
    db.commit()
    print(f"Added {repost_count} reposts")
    
    db.close()
    
    print("\n✅ Realistic engagement added!")
    print(f"\nInfluencers (high follower count):")
    db2 = SessionLocal()
    for idx in influencer_indices:
        user = db2.query(User).filter(User.id == idx + 1).first()
        if user:
            followers = db2.query(Follower).filter(Follower.followed_id == user.id).count()
            print(f"  {user.username}: {followers} followers")
    
    print(f"\nPopular posts (high engagement):")
    for post in popular_posts[:3]:
        likes = db2.query(Like).filter(Like.post_id == post.id).count()
        comments = db2.query(Comment).filter(Comment.post_id == post.id).count()
        reposts = db2.query(Repost).filter(Repost.post_id == post.id).count()
        print(f"  Post {post.id}: {likes} likes, {comments} comments, {reposts} reposts")
    
    db2.close()

if __name__ == "__main__":
    add_realistic_engagement()
