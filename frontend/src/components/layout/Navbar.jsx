import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { LogOut, Crown, User, ShoppingBag } from 'lucide-react';

const Navbar = () => {
  const { user, logout, isAdmin } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-white/90 backdrop-blur-lg shadow-xl sticky top-0 z-50 border-b border-purple-100">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo with animation */}
          <Link to="/dashboard" className="flex items-center space-x-3 group">
            <div className="relative">
              <span className="text-3xl group-hover:animate-spin inline-block">🍬</span>
              <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full blur opacity-30 group-hover:opacity-100 transition duration-200"></div>
            </div>
            <div>
              <span className="font-bold text-xl bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                Sweet Shop
              </span>
              <p className="text-xs text-gray-500">Inventory Management</p>
            </div>
          </Link>

          {/* User Info with better styling */}
          <div className="flex items-center space-x-6">
            {/* User profile card */}
            <div className="hidden md:flex items-center space-x-3 px-4 py-2 bg-gradient-to-r from-purple-50 to-pink-50 rounded-full">
              <div className="w-8 h-8 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full flex items-center justify-center text-white text-sm font-bold">
                {user?.full_name?.charAt(0).toUpperCase()}
              </div>
              <div>
                <p className="text-sm font-semibold text-gray-700">{user?.full_name}</p>
                <p className="text-xs text-gray-500">{user?.email_address}</p>
              </div>
            </div>

            {/* Admin badge with animation */}
            {isAdmin && (
              <div className="relative group">
                <div className="px-4 py-2 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-full text-sm font-bold flex items-center space-x-2 shadow-lg transform hover:scale-105 transition-all">
                  <Crown className="w-4 h-4 animate-pulse" />
                  <span>Admin</span>
                </div>
                <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full blur opacity-50 group-hover:opacity-75 transition duration-200"></div>
              </div>
            )}

            {/* Logout button with hover effect */}
            <button
              onClick={handleLogout}
              className="group relative px-5 py-2.5 overflow-hidden bg-red-500 text-white font-semibold rounded-xl hover:bg-red-600 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            >
              <span className="relative z-10 flex items-center space-x-2">
                <LogOut className="w-4 h-4" />
                <span>Logout</span>
              </span>
              <div className="absolute inset-0 bg-gradient-to-r from-red-600 to-pink-600 opacity-0 group-hover:opacity-100 transition-opacity duration-200"></div>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;