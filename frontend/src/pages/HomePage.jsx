import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-pink-900 to-red-900 flex items-center justify-center">
      <div className="text-center text-white px-4">
        <h1 className="text-5xl md:text-7xl font-bold mb-6 animate-pulse">
          🍬 Sweet Shop
        </h1>
        <p className="text-xl md:text-2xl mb-8 text-pink-200">
          Manage your candy store inventory with ease
        </p>

        <div className="space-x-4">
          <Link
            to="/login"
            className="inline-block px-8 py-3 bg-white text-purple-900 font-bold rounded-lg hover:bg-gray-100 transition-all transform hover:scale-105"
          >
            Login
          </Link>
          <Link
            to="/register"
            className="inline-block px-8 py-3 bg-purple-600 text-white font-bold rounded-lg hover:bg-purple-700 transition-all transform hover:scale-105 border-2 border-purple-400"
          >
            Register
          </Link>
        </div>

        <p className="mt-12 text-pink-300 text-sm">
          Built with ❤️ using React + FastAPI
        </p>
      </div>
    </div>
  );
};

export default HomePage;