// Login required page
import { Link } from 'react-router-dom';

const LoginRequired = () => {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="card-dark p-12 max-w-md text-center">
        <div className="text-6xl mb-6">🔒</div>
        <h1 className="text-3xl font-bold mb-4">Login Required</h1>
        <p className="text-[#c9d1d9] mb-6">
          You need to be logged in to access this feature.
        </p>
        <div className="flex gap-4 justify-center">
          <Link to="/login" className="btn-primary">
            Login
          </Link>
          <Link to="/register" className="btn-secondary">
            Sign Up
          </Link>
        </div>
      </div>
    </div>
  );
};

export default LoginRequired;
