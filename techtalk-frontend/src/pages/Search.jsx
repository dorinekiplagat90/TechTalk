// Search page - search for users and posts
import { useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../utils/api';

const Search = () => {
  const [query, setQuery] = useState('');
  const [users, setUsers] = useState([]);
  const [posts, setPosts] = useState([]);
  const [activeTab, setActiveTab] = useState('users');
  const [searched, setSearched] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setSearched(true);
    try {
      if (activeTab === 'users') {
        const response = await api.get(`/search/users?q=${query}`);
        setUsers(response.data);
      } else {
        const response = await api.get(`/search/posts?q=${query}`);
        setPosts(response.data);
      }
    } catch (error) {
      console.error('Error searching:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <h1 className="text-3xl font-bold mb-6 text-gray-800">🔍 Search</h1>

        {/* Search form */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6 border border-blue-100">
          <form onSubmit={handleSearch}>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search for users or posts..."
              className="w-full border-2 border-gray-200 rounded-xl px-4 py-3 mb-4 focus:border-blue-500 focus:outline-none transition text-lg"
            />
            <div className="flex gap-4 mb-4">
              <button
                type="button"
                onClick={() => setActiveTab('users')}
                className={`flex-1 px-6 py-3 rounded-xl font-semibold transition ${
                  activeTab === 'users' 
                    ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-md' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                👥 Users
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('posts')}
                className={`flex-1 px-6 py-3 rounded-xl font-semibold transition ${
                  activeTab === 'posts' 
                    ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-md' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                📝 Posts
              </button>
            </div>
            <button 
              type="submit" 
              className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white px-8 py-3 rounded-xl hover:from-blue-700 hover:to-blue-800 transition font-semibold shadow-md"
            >
              Search
            </button>
          </form>
        </div>

        {/* Results */}
        {searched && (
          <>
            {activeTab === 'users' && (
              <div className="bg-white rounded-2xl shadow-lg border border-blue-100 overflow-hidden">
                {users.length === 0 ? (
                  <div className="p-12 text-center text-gray-500">
                    <div className="text-6xl mb-4">🔍</div>
                    <p className="text-lg">No users found</p>
                  </div>
                ) : (
                  users.map((user) => (
                    <Link
                      key={user.id}
                      to={`/users/${user.id}`}
                      className="flex items-center gap-4 p-6 border-b border-gray-100 hover:bg-blue-50 transition"
                    >
                      <img
                        src={user.profile_pic || 'https://via.placeholder.com/50'}
                        alt={user.username}
                        className="w-16 h-16 rounded-full border-2 border-blue-200"
                      />
                      <div className="flex-1">
                        <p className="font-bold text-lg text-gray-800">{user.username}</p>
                        <p className="text-gray-600">{user.bio || 'No bio'}</p>
                      </div>
                      <span className="text-blue-600 font-semibold">→</span>
                    </Link>
                  ))
                )}
              </div>
            )}

            {activeTab === 'posts' && (
              <div className="space-y-4">
                {posts.length === 0 ? (
                  <div className="bg-white rounded-2xl shadow-lg p-12 text-center border border-blue-100">
                    <div className="text-6xl mb-4">🔍</div>
                    <p className="text-lg text-gray-500">No posts found</p>
                  </div>
                ) : (
                  posts.map((post) => (
                    <div key={post.id} className="bg-white rounded-2xl shadow-lg p-6 border border-blue-100 hover:shadow-xl transition">
                      <Link to={`/users/${post.author.id}`} className="flex items-center gap-3 mb-3 hover:opacity-80">
                        <img
                          src={post.author.profile_pic || 'https://via.placeholder.com/40'}
                          alt={post.author.username}
                          className="w-12 h-12 rounded-full border-2 border-blue-200"
                        />
                        <div>
                          <p className="font-bold text-gray-800">{post.author.username}</p>
                          <p className="text-sm text-gray-500">{post.author.bio}</p>
                        </div>
                      </Link>
                      <p className="text-gray-800 text-lg">{post.content}</p>
                      <div className="flex gap-6 mt-4 text-gray-600">
                        <span>❤️ {post.likes_count}</span>
                        <span>💬 {post.comments_count}</span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </>
        )}

        {!searched && (
          <div className="bg-white rounded-2xl shadow-lg p-12 text-center border border-blue-100">
            <div className="text-6xl mb-4">🔍</div>
            <p className="text-xl text-gray-600">Search for users or posts</p>
            <p className="text-gray-500 mt-2">Enter a keyword and click search</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Search;
