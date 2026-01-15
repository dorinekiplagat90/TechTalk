// Single post view page
import { useState, useEffect, useContext } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { formatDate } from '../utils/date';
import api from '../utils/api';

const SinglePost = () => {
  const { postId } = useParams();
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [commentText, setCommentText] = useState('');
  const [isLiked, setIsLiked] = useState(false);
  const [likesCount, setLikesCount] = useState(0);

  useEffect(() => {
    loadPost();
    loadComments();
  }, [postId]);

  const loadPost = async () => {
    try {
      const response = await api.get(`/posts/${postId}`);
      setPost(response.data);
      setIsLiked(response.data.is_liked);
      setLikesCount(response.data.likes_count);
    } catch (error) {
      console.error('Error loading post:', error);
    }
  };

  const loadComments = async () => {
    try {
      const response = await api.get(`/posts/${postId}/comments`);
      setComments(response.data);
    } catch (error) {
      console.error('Error loading comments:', error);
    }
  };

  const handleLike = async () => {
    if (!user) {
      navigate('/login');
      return;
    }
    
    try {
      if (isLiked) {
        await api.delete(`/posts/${postId}/likes`);
        setIsLiked(false);
        setLikesCount(likesCount - 1);
      } else {
        await api.post(`/posts/${postId}/likes`);
        setIsLiked(true);
        setLikesCount(likesCount + 1);
      }
    } catch (error) {
      console.error('Error toggling like:', error);
    }
  };

  const handleComment = async (e) => {
    e.preventDefault();
    if (!user) {
      navigate('/login');
      return;
    }
    if (!commentText.trim()) return;

    try {
      const response = await api.post(`/posts/${postId}/comments`, { content: commentText });
      setComments([response.data, ...comments]);
      setCommentText('');
    } catch (error) {
      console.error('Error adding comment:', error);
    }
  };

  if (!post) {
    return <div className="flex justify-center items-center h-screen text-white">Loading...</div>;
  }

  return (
    <div className="app-bg min-h-screen">
      <div className="container mx-auto px-4 py-6 max-w-3xl">
        <Link to="/home" className="text-blue-400 hover:underline mb-4 inline-block">&larr; Back to Feed</Link>
        
        {/* Post */}
        <div className="post mb-6">
          <div className="flex items-center gap-3 mb-4">
            <Link to={`/users/${post.author.id}`}>
              <img
                src={post.author.profile_pic || 'https://via.placeholder.com/50'}
                alt={post.author.username}
                className="avatar w-12 h-12"
              />
            </Link>
            <div>
              <Link to={`/users/${post.author.id}`} className="font-bold text-black hover:text-blue-600">
                {post.author.username}
              </Link>
              <p className="text-sm text-gray-500">{formatDate(post.timestamp)}</p>
            </div>
          </div>

          <p className="text-lg mb-4 whitespace-pre-wrap text-black">{post.content}</p>
          
          {post.tags && (
            <div className="mb-3 flex flex-wrap gap-2">
              {post.tags.split(',').map((tag, idx) => (
                <span key={idx} className="bg-blue-100 text-blue-600 px-3 py-1 rounded-full text-sm font-medium">
                  {tag.trim()}
                </span>
              ))}
            </div>
          )}
          
          {post.image_url && (
            <img src={post.image_url} alt="Post" className="w-full rounded-xl mb-4 max-h-96 object-cover" />
          )}

          <div className="flex gap-6 pt-4 border-t border-gray-300">
            <button 
              onClick={handleLike} 
              className={`flex items-center gap-2 hover:scale-110 transition ${
                isLiked ? 'text-red-500' : 'text-gray-600 hover:text-red-500'
              }`}
            >
              <span className="text-xl">{isLiked ? '❤️' : '🤍'}</span>
              <span className="font-semibold">{likesCount}</span>
            </button>
            <div className="flex items-center gap-2 text-gray-600">
              <span className="text-xl">💬</span>
              <span className="font-semibold">{comments.length}</span>
            </div>
          </div>
        </div>

        {/* Comments Section */}
        <div className="post">
          <h2 className="text-xl font-bold mb-4 text-black">Comments ({comments.length})</h2>
          
          {user ? (
            <form onSubmit={handleComment} className="mb-6">
              <textarea
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
                placeholder="Write a comment..."
                className="w-full border-2 border-gray-300 rounded-xl px-4 py-3 resize-none focus:border-blue-500 focus:outline-none text-black"
                rows="3"
              />
              <button type="submit" className="mt-2 btn-primary">
                Post Comment
              </button>
            </form>
          ) : (
            <div className="mb-6 text-center py-4 bg-gray-100 rounded-xl">
              <Link to="/login" className="text-blue-600 hover:underline font-semibold">Login</Link>
              <span className="text-gray-700"> to comment</span>
            </div>
          )}

          <div className="space-y-4">
            {comments.map((comment) => (
              <div key={comment.id} className="flex gap-3 pb-4 border-b border-gray-200">
                <Link to={`/users/${comment.author.id}`}>
                  <img
                    src={comment.author.profile_pic || 'https://via.placeholder.com/40'}
                    alt={comment.author.username}
                    className="avatar w-10 h-10"
                  />
                </Link>
                <div className="flex-1">
                  <Link to={`/users/${comment.author.id}`} className="font-semibold text-black hover:text-blue-600">
                    {comment.author.username}
                  </Link>
                  <p className="text-sm text-gray-500">{formatDate(comment.timestamp)}</p>
                  <p className="mt-2 text-black">{comment.content}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SinglePost;
