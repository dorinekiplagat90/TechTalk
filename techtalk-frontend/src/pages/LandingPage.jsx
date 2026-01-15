import { useState } from 'react';
import { Link } from 'react-router-dom';
import { MessageSquare, Heart, Users, Zap } from 'lucide-react';

const LandingPage = () => {
  const [samplePosts] = useState([
    {
      id: 1,
      username: 'sarah_dev',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=sarah',
      content: 'Just built a real-time chat app with WebSockets and React! The performance is amazing 🚀',
      tags: ['React', 'WebSockets'],
      likes: 42,
      comments: 8,
      timestamp: '2h ago'
    },
    {
      id: 2,
      username: 'tech_mike',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=mike',
      content: 'Pro tip: Use React.memo() to prevent unnecessary re-renders. Saved me 30% render time!',
      tags: ['React', 'Performance'],
      likes: 89,
      comments: 15,
      timestamp: '4h ago'
    },
    {
      id: 3,
      username: 'ai_explorer',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=alex',
      content: 'Trained my first transformer model today. The attention mechanism is fascinating! 🤖',
      tags: ['AI', 'MachineLearning'],
      likes: 156,
      comments: 23,
      timestamp: '6h ago'
    }
  ]);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Zap className="w-8 h-8 text-blue-500" />
              <span className="ml-2 text-2xl font-bold text-gray-900">TechTalk</span>
            </div>
            <div className="flex gap-4">
              <Link
                to="/login"
                className="px-4 py-2 text-gray-700 hover:text-gray-900 font-medium"
              >
                Log In
              </Link>
              <Link
                to="/register"
                className="px-6 py-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 font-medium transition"
              >
                Sign Up
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="bg-gradient-to-br from-blue-500 to-purple-600 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            Where Tech Minds Connect
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-blue-100">
            Share code, discover ideas, and build together with developers worldwide
          </p>
          <Link
            to="/register"
            className="inline-block px-8 py-4 bg-white text-blue-600 rounded-full text-lg font-semibold hover:bg-gray-100 transition"
          >
            Join TechTalk — It's Free
          </Link>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="text-center">
            <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <MessageSquare className="w-8 h-8 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Share Knowledge</h3>
            <p className="text-gray-600">Post tips, tutorials, and tech discoveries</p>
          </div>
          <div className="text-center">
            <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Heart className="w-8 h-8 text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Engage & Learn</h3>
            <p className="text-gray-600">Like, comment, and discuss technical topics</p>
          </div>
          <div className="text-center">
            <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Users className="w-8 h-8 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Build Your Network</h3>
            <p className="text-gray-600">Follow developers with similar interests</p>
          </div>
        </div>

        {/* Sample Posts Section */}
        <div className="max-w-2xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-8">
            What's happening in tech right now
          </h2>
          <div className="space-y-4">
            {samplePosts.map(post => (
              <div key={post.id} className="bg-white rounded-lg shadow p-6 border border-gray-200">
                <div className="flex items-start gap-3 mb-4">
                  <img
                    src={post.avatar}
                    alt={post.username}
                    className="w-12 h-12 rounded-full"
                  />
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-gray-900">@{post.username}</span>
                      <span className="text-gray-500 text-sm">· {post.timestamp}</span>
                    </div>
                    <p className="text-gray-800 mt-2">{post.content}</p>
                    <div className="flex gap-2 mt-3">
                      {post.tags.map(tag => (
                        <span
                          key={tag}
                          className="text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded-full"
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>
                    <div className="flex gap-6 mt-4 text-gray-500">
                      <div className="flex items-center gap-2">
                        <Heart className="w-5 h-5" />
                        <span>{post.likes}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <MessageSquare className="w-5 h-5" />
                        <span>{post.comments}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="text-center mt-8">
            <Link
              to="/register"
              className="inline-block px-8 py-3 bg-blue-500 text-white rounded-full font-semibold hover:bg-blue-600 transition"
            >
              Sign up to see more
            </Link>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-8 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p>&copy; 2025 TechTalk. Built for developers, by developers.</p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;