import { useState, useEffect } from 'react';
import { UserPlus, Check } from 'lucide-react';
import { Link } from 'react-router-dom';
import api from '../utils/api';

const SuggestedUsers = ({ onFollow }) => {
  const [users, setUsers] = useState([]);
  const [following, setFollowing] = useState(new Set());
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchSuggestedUsers();
  }, []);

  const fetchSuggestedUsers = async () => {
    setLoading(true);
    try {
      const response = await api.get('/users/suggested?limit=10');
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching suggested users:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFollow = async (userId) => {
    try {
      await api.post(`/users/${userId}/follow`);
      setFollowing(new Set(following).add(userId));
      if (onFollow) onFollow(userId);
    } catch (error) {
      console.error('Error following user:', error);
    }
  };

  const handleUnfollow = async (userId) => {
    try {
      await api.delete(`/users/${userId}/follow`);
      const newFollowing = new Set(following);
      newFollowing.delete(userId);
      setFollowing(newFollowing);
    } catch (error) {
      console.error('Error unfollowing user:', error);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-4">
        <h2 className="text-lg font-semibold mb-4">Suggested Users</h2>
        <div className="space-y-4">
          {[1, 2, 3].map(i => (
            <div key={i} className="animate-pulse flex gap-3">
              <div className="w-12 h-12 bg-gray-300 rounded-full"></div>
              <div className="flex-1">
                <div className="h-4 bg-gray-300 rounded w-3/4 mb-2"></div>
                <div className="h-3 bg-gray-300 rounded w-full"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Who to Follow</h2>
      </div>
      
      <div className="divide-y divide-gray-200">
        {users.map(user => (
          <div key={user.id} className="p-4 hover:bg-gray-50 transition">
            <div className="flex gap-3">
              <Link to={`/users/${user.id}`}>
                <img
                  src={user.profile_pic || `https://api.dicebear.com/7.x/avataaars/svg?seed=${user.username}`}
                  alt={user.username}
                  className="w-12 h-12 rounded-full cursor-pointer hover:opacity-90 transition"
                />
              </Link>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <Link 
                      to={`/users/${user.id}`}
                      className="font-semibold text-gray-900 hover:underline block truncate"
                    >
                      @{user.username}
                    </Link>
                    <p className="text-sm text-gray-600 line-clamp-2 mt-1">
                      {user.bio || 'Tech enthusiast'}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      {user.followers_count || 0} followers
                    </p>
                  </div>
                  
                  {following.has(user.id) ? (
                    <button
                      onClick={() => handleUnfollow(user.id)}
                      className="ml-2 px-3 py-1.5 bg-gray-200 text-gray-800 rounded-full text-sm font-medium hover:bg-gray-300 transition flex items-center gap-1 flex-shrink-0"
                    >
                      <Check className="w-4 h-4" />
                      Following
                    </button>
                  ) : (
                    <button
                      onClick={() => handleFollow(user.id)}
                      className="ml-2 px-3 py-1.5 bg-blue-500 text-white rounded-full text-sm font-medium hover:bg-blue-600 transition flex items-center gap-1 flex-shrink-0"
                    >
                      <UserPlus className="w-4 h-4" />
                      Follow
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      <div className="p-4 border-t border-gray-200">
        <Link
          to="/explore"
          className="text-blue-500 hover:text-blue-600 text-sm font-medium"
        >
          Show more
        </Link>
      </div>
    </div>
  );
};

export default SuggestedUsers;