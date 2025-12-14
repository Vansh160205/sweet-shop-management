import { useState } from 'react';
import { X, Save, Package } from 'lucide-react';
import sweetService from '../../services/sweetService';

const SweetForm = ({ sweet, onClose, onSuccess }) => {
  const isEditing = !!sweet;
  
  const [formData, setFormData] = useState({
    sweet_name: sweet?.sweet_name || '',
    sweet_category: sweet?.sweet_category || '',
    sweet_price: sweet?.sweet_price || '',
    quantity_in_stock: sweet?.quantity_in_stock || 0,
    sweet_description: sweet?.sweet_description || '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const data = {
        ...formData,
        sweet_price: parseFloat(formData.sweet_price),
        quantity_in_stock: parseInt(formData.quantity_in_stock),
      };

      if (isEditing) {
        await sweetService.updateSweet(sweet.sweet_id, data);
      } else {
        await sweetService.createSweet(data);
      }
      
      onSuccess();
    } catch (err) {
      setError(err.response?.data?.detail || 'Operation failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-fadeIn">
      <div className="bg-white rounded-3xl shadow-2xl w-full max-w-lg transform animate-slideUp">
        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600 to-pink-600 px-6 py-5 rounded-t-3xl relative overflow-hidden">
          <div className="absolute inset-0 bg-white/10 backdrop-blur-sm"></div>
          <div className="relative z-10 flex items-center justify-between">
            <h2 className="text-2xl font-bold text-white flex items-center space-x-2">
              <Package className="w-6 h-6" />
              <span>{isEditing ? 'Edit Sweet' : 'Add New Sweet'}</span>
            </h2>
            <button
              onClick={onClose}
              className="text-white/80 hover:text-white transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-5">
          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 text-red-700 px-4 py-3 rounded-lg text-sm animate-shake">
              {error}
            </div>
          )}

          {/* Name Field */}
          <div className="group">
            <label className="block text-gray-700 font-semibold mb-2 group-focus-within:text-purple-600 transition-colors">
              Sweet Name
            </label>
            <input
              type="text"
              name="sweet_name"
              value={formData.sweet_name}
              onChange={handleChange}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
              placeholder="e.g., Kaju Katli"
              required
            />
          </div>

          {/* Category Field */}
          <div className="group">
            <label className="block text-gray-700 font-semibold mb-2 group-focus-within:text-purple-600 transition-colors">
              Category
            </label>
            <input
              type="text"
              name="sweet_category"
              value={formData.sweet_category}
              onChange={handleChange}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
              placeholder="e.g., Traditional"
              required
            />
          </div>

          {/* Price and Stock Grid */}
          <div className="grid grid-cols-2 gap-4">
            <div className="group">
              <label className="block text-gray-700 font-semibold mb-2 group-focus-within:text-purple-600 transition-colors">
                Price (₹)
              </label>
              <div className="relative">
                <span className="absolute left-3 top-3 text-gray-500">₹</span>
                <input
                  type="number"
                  step="0.01"
                  min="0.01"
                  name="sweet_price"
                  value={formData.sweet_price}
                  onChange={handleChange}
                  className="w-full pl-8 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                  placeholder="299.00"
                  required
                />
              </div>
            </div>
            <div className="group">
              <label className="block text-gray-700 font-semibold mb-2 group-focus-within:text-purple-600 transition-colors">
                Stock Quantity
              </label>
              <input
                type="number"
                min="0"
                name="quantity_in_stock"
                value={formData.quantity_in_stock}
                onChange={handleChange}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                placeholder="50"
                required
              />
            </div>
          </div>

          {/* Description Field */}
          <div className="group">
            <label className="block text-gray-700 font-semibold mb-2 group-focus-within:text-purple-600 transition-colors">
              Description
            </label>
            <textarea
              name="sweet_description"
              value={formData.sweet_description}
              onChange={handleChange}
              rows="3"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all resize-none"
              placeholder="Describe this sweet treat..."
            />
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 py-3 bg-gray-200 text-gray-700 font-semibold rounded-xl hover:bg-gray-300 transition-all transform hover:scale-105"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-pink-700 transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl flex items-center justify-center space-x-2"
            >
              <Save className="w-5 h-5" />
              <span>{loading ? 'Saving...' : isEditing ? 'Update' : 'Create'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SweetForm;