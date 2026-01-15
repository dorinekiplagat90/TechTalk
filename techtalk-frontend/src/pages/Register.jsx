// Register page
import { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const Register = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [securityQuestion, setSecurityQuestion] = useState('');
  const [securityAnswer, setSecurityAnswer] = useState('');
  const [error, setError] = useState('');
  const [passwordErrors, setPasswordErrors] = useState([]);
  const { register } = useContext(AuthContext);
  const navigate = useNavigate();

  const securityQuestions = [
    "What was the name of your first pet?",
    "What city were you born in?",
    "What is your mother's maiden name?",
    "What was the name of your elementary school?",
    "What is your favorite book?",
    "What was your childhood nickname?"
  ];

  const validatePassword = (pwd) => {
    const errors = [];
    if (pwd.length < 9) errors.push('At least 9 characters');
    if (!/\d/.test(pwd)) errors.push('At least one number');
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(pwd)) errors.push('At least one special character (!@#$%^&*)');
    setPasswordErrors(errors);
    return errors.length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!validatePassword(password)) {
      setError('Password does not meet requirements');
      return;
    }
    
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    try {
      await register(username, email, password, securityQuestion, securityAnswer);
      navigate('/home');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center py-8">
      <div className="bg-[#0f2a44] p-8 rounded-lg shadow-md w-full max-w-md border border-[#1f3b5c]">
        <h1 className="text-3xl font-bold text-center mb-6 text-white">TechTalk</h1>
        <h2 className="text-xl font-semibold mb-4 text-white">Register</h2>
        
        {error && <div className="bg-red-900/50 text-red-200 p-3 rounded mb-4 border border-red-700">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-[#c9d1d9] mb-2">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-[#0b1c2d] text-white border border-[#1f3b5c] rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#1f6feb]"
              required
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-[#c9d1d9] mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-[#0b1c2d] text-white border border-[#1f3b5c] rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#1f6feb]"
              required
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-[#c9d1d9] mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => { setPassword(e.target.value); validatePassword(e.target.value); }}
              className="w-full bg-[#0b1c2d] text-white border border-[#1f3b5c] rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#1f6feb]"
              required
            />
            {password && passwordErrors.length > 0 && (
              <div className="mt-2 text-sm text-red-400">
                <p className="font-semibold">Password must have:</p>
                <ul className="list-disc list-inside">
                  {passwordErrors.map((err, idx) => <li key={idx}>{err}</li>)}
                </ul>
              </div>
            )}
            {password && passwordErrors.length === 0 && (
              <p className="mt-2 text-sm text-green-400">✓ Password meets all requirements</p>
            )}
          </div>
          
          <div className="mb-4">
            <label className="block text-[#c9d1d9] mb-2">Confirm Password</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full bg-[#0b1c2d] text-white border border-[#1f3b5c] rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#1f6feb]"
              required
            />
            {confirmPassword && password !== confirmPassword && (
              <p className="mt-2 text-sm text-red-400">Passwords do not match</p>
            )}
            {confirmPassword && password === confirmPassword && (
              <p className="mt-2 text-sm text-green-400">✓ Passwords match</p>
            )}
          </div>
          
          <div className="mb-4">
            <label className="block text-[#c9d1d9] mb-2">Security Question</label>
            <select
              value={securityQuestion}
              onChange={(e) => setSecurityQuestion(e.target.value)}
              className="w-full bg-[#0b1c2d] text-white border border-[#1f3b5c] rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#1f6feb]"
              required
            >
              <option value="">Select a security question</option>
              {securityQuestions.map((q, idx) => (
                <option key={idx} value={q}>{q}</option>
              ))}
            </select>
          </div>
          
          <div className="mb-6">
            <label className="block text-[#c9d1d9] mb-2">Security Answer</label>
            <input
              type="text"
              value={securityAnswer}
              onChange={(e) => setSecurityAnswer(e.target.value)}
              className="w-full bg-[#0b1c2d] text-white border border-[#1f3b5c] rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#1f6feb]"
              required
            />
          </div>
          
          <button type="submit" className="w-full bg-[#1f6feb] hover:bg-[#388bfd] text-white py-2 rounded font-medium transition">
            Register
          </button>
        </form>
        
        <p className="mt-4 text-center text-[#c9d1d9]">
          Already have an account? <Link to="/login" className="text-[#1f6feb] hover:underline">Login</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
