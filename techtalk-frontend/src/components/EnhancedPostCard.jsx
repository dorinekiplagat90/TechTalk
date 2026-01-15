import { useState, useContext } from 'react';
import { Heart, MessageCircle, Share2, MoreVertical, Edit2, Trash2, Bookmark } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { formatDistanceToNow } from 'date-fns';
import { AuthContext } from '../context/AuthContext';
import CommentSection from './CommentSection';
import api from '../utils/api';

const EnhancedPostCard = ({ post, onUpdate }) => {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  const [showComments, setShowComments] = useState(false);
  const [showMenu, setShowMenu] = useState(false);
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [comments, setComments] = useState([]);
  const [isLiked, setIsLiked] = useState(post.is_liked);
  const [likesCount, setLikesCount] = useState(post.likes_count);

  const isOwnPost = user && post.author.id === user.id;

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

  const handleAddComment = async (postId, content) => {
    try {
      const response = await api.post(`/posts/${postId}/comments`, { content });
      setComments([response.data, ...comments]);
      if (onUpdate) onUpdate();
      return response.data;
    } catch (error) {
      console.error('Error adding comment:', error);
      throw error;
    }
  };

  const handleDeleteComment = async (commentId) => {
    try {
      await api.delete(`/comments/${commentId}`);
      setComments(comments.filter(c => c.id !== commentId));
      if (onUpdate) onUpdate();
    } catch (error) {
      console.error('Error deleting comment:', error);
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

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: `Post by @${post.author.username}`,
        text: post.content,
        url: window.location.href
      });
    } else {
      navigator.clipboard.writeText(window.location.href);
      alert('Link copied to clipboard!');
    }
  };

  const handleBookmark = () => {
    setIsBookmarked(!isBookmarked);
  };

  return (
    <div className="bg-white rounded-lg shadow border border-gray-200 overflow-hidden">
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-start gap-3 flex-1">
            <Link to={`/users/${post.author.id}`}>
              <img
                src={post.author.profile_pic || `https://api.dicebear.com/7.x/avataaars/svg?seed=${post.author.username}`}
                alt={post.author.username}
                className="w-12 h-12 rounded-full cursor-pointer hover:opacity-90 transition"
              />
            </Link>
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <Link 
                  to={`/users/${post.author.id}`}
                  className="font-semibold text-gray-900 hover:underline"
                >
                  @{post.author.username}
                </Link>
                <span className="text-gray-500 text-sm">·</span>
                <span className="text-gray-500 text-sm">
                  {formatDistanceToNow(new Date(post.timestamp), { addSuffix: true })}
                </span>
              </div>
              {post.author.bio && (
                <p className="text-sm text-gray-600 mt-0.5">{post.author.bio}</p>
              )}
            </div>
          </div>

          {/* More Menu */}
          {isOwnPost && (
            <div className="relative">
              <button
                onClick={() => setShowMenu(!showMenu)}
                className="p-2 hover:bg-gray-100 rounded-full transition"
              >
                <MoreVertical className="w-5 h-5 text-gray-600" />
              </button>

              {showMenu && (
                <div className="absolute right-0 mt-1 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-10 min-w-[150px]">
                  {onUpdate && (
                    <button
                      onClick={() => {
                        setShowMenu(false);
                      }}
                      className="w-full px-4 py-2 text-left text-sm hover:bg-gray-100 flex items-center gap-2"
                    >
                      <Edit2 className="w-4 h-4" />
                      Edit
                    </button>
                  )}
                  <button
                    onClick={() => {
                      handleDelete();
                      setShowMenu(false);
                    }}
                    className="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-gray-100 flex items-center gap-2"
                  >
                    <Trash2 className="w-4 h-4" />
                    Delete
                  </button>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Content */}
        <div className="mb-4">
          <p className="text-gray-900 whitespace-pre-wrap">{post.content}</p>
        </div>

        {/* Image */}
        {post.image_url && (
          <div className="mb-4 rounded-lg overflow-hidden">
            <img
              src={post.image_url}
              alt="Post content"
              className="w-full max-h-96 object-cover"
            />
          </div>
        )}

        {/* Tags */}
        {post.tags && (
          <div className="flex flex-wrap gap-2 mb-4">
            {post.tags.split(',').map((tag, idx) => (
              <Link
                key={idx}
                to={`/search?q=${encodeURIComponent(tag.trim())}`}
                className="text-sm bg-blue-100 text-blue-700 px-3 py-1 rounded-full hover:bg-blue-200 transition"
              >
                #{tag.trim()}
              </Link>
            ))}
          </div>
        )}

        {/* Actions */}
        <div className="flex items-center gap-6 pt-4 border-t border-gray-200">
          <button
            onClick={handleLike}
            className={`flex items-center gap-2 transition ${
              isLiked 
                ? 'text-red-500 hover:text-red-600' 
                : 'text-gray-600 hover:text-red-500'
            }`}
          >
            <Heart 
              className={`w-5 h-5 ${isLiked ? 'fill-current' : ''}`}
            />
            <span className="text-sm font-medium">{likesCount}</span>
          </button>

          <button
            onClick={loadComments}
            className="flex items-center gap-2 text-gray-600 hover:text-blue-500 transition"
          >
            <MessageCircle className="w-5 h-5" />
            <span className="text-sm font-medium">{post.comments_count || 0}</span>
          </button>

          <button
            onClick={handleShare}
            className="flex items-center gap-2 text-gray-600 hover:text-green-500 transition"
          >
            <Share2 className="w-5 h-5" />
          </button>

          <button
            onClick={handleBookmark}
            className={`flex items-center gap-2 ml-auto transition ${
              isBookmarked 
                ? 'text-blue-500' 
                : 'text-gray-600 hover:text-blue-500'
            }`}
          >
            <Bookmark className={`w-5 h-5 ${isBookmarked ? 'fill-current' : ''}`} />
          </button>
        </div>

        {/* Comments Section */}
        {showComments && (
          <CommentSection
            postId={post.id}
            comments={comments}
            onAddComment={handleAddComment}
            onDeleteComment={handleDeleteComment}
            onEditComment={() => {}}
            currentUserId={user?.id}
          />
        )}
      </div>
    </div>
  );
};

export default EnhancedPostCard;