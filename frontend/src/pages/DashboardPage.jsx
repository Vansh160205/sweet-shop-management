import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Plus, Package2, TrendingUp } from 'lucide-react';
import sweetService from '../services/sweetService';
import SweetCard from '../components/sweets/SweetCard';
import SweetForm from '../components/sweets/SweetForm';
import SearchBar from '../components/sweets/SearchBar';
import LoadingSpinner from '../components/common/LoadingSpinner';

const DashboardPage = () => {
  const { isAdmin } = useAuth();
  const [sweets, setSweets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingSweet, setEditingSweet] = useState(null);
  const [searchParams, setSearchParams] = useState({});

  const fetchSweets = async () => {
    setLoading(true);
    try {
      const data = Object.keys(searchParams).length > 0
        ? await sweetService.searchSweets(searchParams)
        : await sweetService.getAllSweets();
      setSweets(data);
    } catch (error) {
      console.error('Failed to fetch sweets:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSweets();
  }, [searchParams]);

  const handleSearch = (params) => {
    setSearchParams(params);
  };

  const handleCreate = () => {
    setEditingSweet(null);
    setShowForm(true);
  };

  const handleEdit = (sweet) => {
    setEditingSweet(sweet);
    setShowForm(true);
  };

  const handleFormClose = () => {
    setShowForm(false);
    setEditingSweet(null);
  };

  const handleFormSuccess = () => {
    handleFormClose();
    fetchSweets();
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this sweet?')) {
      try {
        await sweetService.deleteSweet(id);
        fetchSweets();
      } catch (error) {
        alert('Failed to delete sweet');
      }
    }
  };

  const handlePurchase = async (id, quantity) => {
    try {
      await sweetService.purchaseSweet(id, quantity);
      fetchSweets();
    } catch (error) {
      alert(error.response?.data?.detail || 'Purchase failed');
    }
  };

  const handleRestock = async (id, quantity) => {
    try {
      await sweetService.restockSweet(id, quantity);
      fetchSweets();
    } catch (error) {
      alert(error.response?.data?.detail || 'Restock failed');
    }
  };

  // Calculate stats
  const totalValue = sweets.reduce((sum, sweet) => sum + (sweet.sweet_price * sweet.quantity_in_stock), 0);
  const totalItems = sweets.reduce((sum, sweet) => sum + sweet.quantity_in_stock, 0);
  const outOfStock = sweets.filter(sweet => sweet.quantity_in_stock === 0).length;

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-white">
      <div className="container mx-auto px-4 py-8">
        {/* Header with Stats */}
        <div className="mb-8">
          <div className="flex flex-col md:flex-row justify-between items-center mb-6">
            <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-pink-600 mb-4 md:mb-0 flex items-center space-x-3">
              <Package2 className="w-10 h-10 text-purple-600" />
              <span>Sweet Inventory</span>
            </h1>
            
            {/* Only show Add button for admins */}
            {isAdmin && (
              <button
                onClick={handleCreate}
                className="group relative px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold rounded-2xl hover:from-purple-700 hover:to-pink-700 transition-all transform hover:scale-105 shadow-xl hover:shadow-2xl flex items-center space-x-2"
              >
                <Plus className="w-5 h-5 group-hover:rotate-90 transition-transform" />
                <span>Add New Sweet</span>
              </button>
            )}
          </div>

        </div>

        {/* Search */}
        <SearchBar onSearch={handleSearch} />

        {/* Content */}
        {loading ? (
          <LoadingSpinner />
        ) : sweets.length === 0 ? (
          <div className="text-center py-16 bg-white/80 backdrop-blur-lg rounded-3xl shadow-xl">
            <span className="text-8xl animate-bounce inline-block">🍭</span>
            <p className="text-2xl text-gray-600 mt-6 font-semibold">No sweets found</p>
            <p className="text-gray-500 mt-2">Start by adding your first sweet product</p>
            {isAdmin && (
              <button
                onClick={handleCreate}
                className="mt-6 px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-pink-700 transition-all transform hover:scale-105 shadow-lg"
              >
                + Add Your First Sweet
              </button>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {sweets.map((sweet) => (
              <SweetCard
                key={sweet.sweet_id}
                sweet={sweet}
                isAdmin={isAdmin}
                onEdit={handleEdit}
                onDelete={handleDelete}
                onPurchase={handlePurchase}
                onRestock={handleRestock}
              />
            ))}
          </div>
        )}

        {/* Sweet Form Modal */}
        {showForm && (
          <SweetForm
            sweet={editingSweet}
            onClose={handleFormClose}
            onSuccess={handleFormSuccess}
          />
        )}
      </div>
    </div>
  );
};

export default DashboardPage;