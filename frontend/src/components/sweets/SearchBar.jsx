import { useState } from 'react';
import { Search, Filter, X } from 'lucide-react';

const SearchBar = ({ onSearch }) => {
  const [filters, setFilters] = useState({
    name: '',
    category: '',
    min_price: '',
    max_price: '',
  });
  const [isExpanded, setIsExpanded] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  };

  const handleSearch = (e) => {
    e.preventDefault();
    const params = {};
    if (filters.name) params.name = filters.name;
    if (filters.category) params.category = filters.category;
    if (filters.min_price) params.min_price = parseFloat(filters.min_price);
    if (filters.max_price) params.max_price = parseFloat(filters.max_price);
    onSearch(params);
  };

  const handleClear = () => {
    setFilters({ name: '', category: '', min_price: '', max_price: '' });
    onSearch({});
  };

  return (
    <form onSubmit={handleSearch} className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-xl p-6 mb-8 border border-purple-100">
      <div className="flex items-center mb-4">
        <Search className="w-5 h-5 text-purple-600 mr-2" />
        <h3 className="text-lg font-semibold text-gray-800">Search & Filter</h3>
        <button
          type="button"
          onClick={() => setIsExpanded(!isExpanded)}
          className="ml-auto text-purple-600 hover:text-purple-700"
        >
          <Filter className="w-5 h-5" />
        </button>
      </div>
      
      <div className={`grid grid-cols-1 md:grid-cols-5 gap-4 ${!isExpanded && 'md:grid-cols-2'}`}>
        <div className="relative">
          <input
            type="text"
            name="name"
            placeholder="Search sweets..."
            value={filters.name}
            onChange={handleChange}
            className="w-full px-4 py-3 pl-10 border-2 border-purple-100 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all bg-white/50"
          />
          <Search className="w-4 h-4 text-gray-400 absolute left-3 top-3.5" />
        </div>
        
        {(isExpanded || window.innerWidth < 768) && (
          <>
            <input
              type="text"
              name="category"
              placeholder="Category..."
              value={filters.category}
              onChange={handleChange}
              className="px-4 py-3 border-2 border-purple-100 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all bg-white/50"
            />
            <input
              type="number"
              name="min_price"
              placeholder="Min price (₹)"
              value={filters.min_price}
              onChange={handleChange}
              className="px-4 py-3 border-2 border-purple-100 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all bg-white/50"
            />
            <input
              type="number"
              name="max_price"
              placeholder="Max price (₹)"
              value={filters.max_price}
              onChange={handleChange}
              className="px-4 py-3 border-2 border-purple-100 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all bg-white/50"
            />
          </>
        )}
        
        <div className="flex space-x-2">
          <button
            type="submit"
            className="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-pink-700 transition-all transform hover:scale-105 shadow-lg flex items-center justify-center space-x-2 py-3"
          >
            <Search className="w-4 h-4" />
            <span>Search</span>
          </button>
          <button
            type="button"
            onClick={handleClear}
            className="px-4 bg-gray-200 hover:bg-gray-300 rounded-xl transition-all hover:shadow-md"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>
    </form>
  );
};

export default SearchBar;