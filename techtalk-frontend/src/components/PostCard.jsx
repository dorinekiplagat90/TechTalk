// Post card component - displays a single post with actions
import { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { formatDate } from '../utils/date';
import api from '../utils/api';

const PostCard = ({ post, onUpdate }) => {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  const [isLiked, setIsLiked] = useState(post.is_liked);
  const [likesCount, setLikesCount] = useState(post.likes_count);
  const [showComments, setShowComments] = useState(false);
  const [comments, setComments] = useState([]);
  const [commentText, setCommentText] = useState('');

  const renderContentWithHashtags = (content) => {
    const parts = content.split(/(#\w+)/);
    return parts.map((part, idx) => 
      part.startsWith('#') ? (
        <span key={idx} className="text-blue-600 font-semibold hover:underline cursor-pointer">{part}</span>
      ) : part
    );
  };

  const handleLike = async () => {
    if (!user) {
      navigate('/login');
      return;
    }
    
    try {
      if (isLiked) {
        await api.delete(`/posts/${post.id}/likes`);
        setIsLiked(false);
        setLikesCount(likesCount - 1);
      } else {
        await api.post(`/posts/${post.id}/likes`);
        setIsLiked(true);
        setLikesCount(likesCount + 1);
      }
    } catch (error) {
      console.error('Error toggling like:', error);
    }
  };

  const loadComments = async () => {
    if (!showComments) {
      try {
        const response = await api.get(`/posts/${post.id}/comments`);
        setComments(response.data);
      } catch (error) {
        console.error('Error loading comments:', error);
      }
    }
    setShowComments(!showComments);
  };

  const handleComment = async (e) => {
    e.preventDefault();
    if (!user) {
      navigate('/login');
      return;
    }
    if (!commentText.trim()) return;

    try {
      const response = await api.post(`/posts/${post.id}/comments`, { content: commentText });
      setComments([response.data, ...comments]);
      setCommentText('');
      if (onUpdate) onUpdate();
    } catch (error) {
      console.error('Error adding comment:', error);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Delete this post?')) {
      try {
        await api.delete(`/posts/${post.id}`);
        if (onUpdate) onUpdate();
      } catch (error) {
        console.error('Error deleting post:', error);
      }
    }
  };

  return (
    <div className="post">
      {/* Post header */}
      <div className="flex items-center justify-between mb-4">
        <Link to={`/users/${post.author.id}`} className="flex items-center gap-3 hover:opacity-80 transition">
          <img
            src={post.author.profile_pic || 'https://via.placeholder.com/40'}
            alt={post.author.username}
            className="avatar w-12 h-12"
          />
          <div>
            <p className="font-bold">{post.author.username}</p>
            <p className="text-sm text-[#8b949e]">{formatDate(post.timestamp)}</p>
          </div>
        </Link>
        {user?.id === post.author.id && (
          <button onClick={handleDelete} className="text-red-400 hover:text-red-300 font-medium">
            Delete
          </button>
        )}
      </div>

      {/* Post content */}
      <p className="mb-4 text-lg whitespace-pre-wrap">{renderContentWithHashtags(post.content)}</p>
      {post.tags && (
        <div className="mb-3 flex flex-wrap gap-2">
          {post.tags.split(',').map((tag, idx) => (
            <span key={idx} className="bg-[#1f6feb]/20 text-[#1f6feb] px-3 py-1 rounded-full text-sm font-medium">
              {tag.trim()}
            </span>
          ))}
        </div>
      )}
      {post.image_url && (
        <img src={post.image_url} alt="Post" className="w-full rounded-xl mb-4 max-h-96 object-cover" />
      )}

      {/* Post actions */}
      <div className="post-actions border-t border-[#1f3b5c] pt-4">
        <button 
          onClick={handleLike} 
          className={`flex items-center gap-2 hover:scale-110 transition ${
            isLiked ? 'text-red-400' : 'hover:text-red-400'
          }`}
        >
          <span className="text-xl">{isLiked ? '❤️' : '🤍'}</span>
          <span className="font-semibold">{likesCount}</span>
        </button>
        <button 
          onClick={loadComments} 
          className="flex items-center gap-2 hover:scale-110 hover:text-[#1f6feb] transition"
        >
          <span className="text-xl">💬</span>
          <span className="font-semibold">{post.comments_count}</span>
        </button>
      </div>

      {/* Comments section */}
      {showComments && (
        <div className="mt-4 border-t border-[#1f3b5c] pt-4">
          {user ? (
            <form onSubmit={handleComment} className="mb-4">
              <input
                type="text"
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
                placeholder="Write a comment..."
                className="input"
              />
            </form>
          ) : (
            <div className="mb-4 text-center py-3 bg-[#1f3b5c]/50 rounded-xl">
              <Link to="/login" className="text-[#1f6feb] hover:underline font-semibold">Login</Link>
              <span className="text-[#c9d1d9]"> to comment</span>
            </div>
          )}
          <div className="space-y-3">
            {comments.map((comment) => (
              <div key={comment.id} className="flex gap-3">
                <img
                  src={comment.author.profile_pic || 'https://via.placeholder.com/32'}
                  alt={comment.author.username}
                  className="avatar w-10 h-10"
                />
                <div className="flex-1 bg-[#1f3b5c]/50 rounded-xl px-4 py-3">
                  <Link to={`/users/${comment.author.id}`} className="font-semibold text-sm hover:text-[#1f6feb]">
                    {comment.author.username}
                  </Link>
                  <p className="text-sm mt-1">{comment.content}</p>
                  <p className="text-xs text-[#8b949e] mt-1">{formatDate(comment.timestamp)}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default PostCard;
