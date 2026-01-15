// Topic page - shows posts by hashtag
import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import PostCard from '../components/PostCard';
import api from '../utils/api';

const Topic = () => {
  const { tag } = useParams();
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTopicPosts();
  }, [tag]);

  const loadTopicPosts = async () => {
    try {
      // Search for posts containing the tag
      const response = await api.get(`/search/posts?q=${tag}`);
      setPosts(response.data);
    } catch (error) {
      console.error('Error loading topic posts:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-screen text-white">Loading...</div>;
  }

  return (
    <div className="app-bg min-h-screen">
      <div className="container mx-auto px-4 py-6 max-w-3xl">
        <Link to="/home" className="text-blue-400 hover:underline mb-4 inline-block">&larr; Back to Feed</Link>
        
        <div className="post mb-6">
          <h1 className="text-3xl font-bold text-black mb-2">#{tag}</h1>
          <p className="text-gray-600">{posts.length} posts about this topic</p>
        </div>

        {posts.length === 0 ? (
          <div className="post text-center py-12">
            <div className="text-6xl mb-4">🔍</div>
            <p className="text-gray-600 text-lg">No posts found for #{tag}</p>
          </div>
        ) : (
          <div className="space-y-4">
            {posts.map((post) => (
              <PostCard key={post.id} post={post} onUpdate={loadTopicPosts} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Topic;
