import { useState } from 'react';
import { ShoppingCart, Package, Edit, Trash2, Plus, Minus } from 'lucide-react';

const SweetCard = ({ sweet, isAdmin, onEdit, onDelete, onPurchase, onRestock }) => {
  const [purchaseQty, setPurchaseQty] = useState(1);
  const [restockQty, setRestockQty] = useState(10);
  const [showRestock, setShowRestock] = useState(false);

  const isOutOfStock = sweet.quantity_in_stock === 0;
  const isLowStock = sweet.quantity_in_stock < 10;

  return (
    <div 
      className="group relative bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Stock status ribbon */}
      {isOutOfStock && (
        <div className="absolute top-3 right-3 z-10 bg-red-500 text-white px-3 py-1 rounded-full text-xs font-bold shadow-lg">
          Out of Stock
        </div>
      )}
      {!isOutOfStock && isLowStock && (
        <div className="absolute top-3 right-3 z-10 bg-yellow-500 text-white px-3 py-1 rounded-full text-xs font-bold shadow-lg animate-pulse">
          Low Stock
        </div>
      )}

      {/* Header with gradient */}
      <div className="relative h-32 bg-gradient-to-br from-purple-500 via-purple-600 to-pink-600 p-4">
        <div className="absolute inset-0 bg-black opacity-20"></div>
        <div className="relative z-10">
          <h3 className="text-xl font-bold text-white mb-1 drop-shadow-lg">{sweet.sweet_name}</h3>
          <span className="inline-block px-3 py-1 bg-white/20 backdrop-blur-md text-white text-sm rounded-full">
            {sweet.sweet_category}
          </span>
        </div>
        
        {/* Decorative candy icon */}
        <div className="absolute bottom-4 right-4 text-4xl opacity-20 transform rotate-12">
          🍬
        </div>
      </div>

      {/* Body */}
      <div className="p-5">
        <p className="text-gray-600 text-sm mb-4 line-clamp-2 min-h-[2.5rem]">
          {sweet.sweet_description || 'Delicious sweet treat'}
        </p>

        {/* Price and Stock */}
        <div className="flex justify-between items-center mb-4">
          <div className="flex flex-col">
            <span className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              ₹{sweet.sweet_price}
            </span>
            <span className="text-xs text-gray-500">per unit</span>
          </div>
          <div className={`px-4 py-2 rounded-xl text-sm font-bold ${
            isOutOfStock 
              ? 'bg-red-100 text-red-700' 
              : isLowStock 
                ? 'bg-yellow-100 text-yellow-700' 
                : 'bg-green-100 text-green-700'
          }`}>
            <span className="text-lg">{sweet.quantity_in_stock}</span>
            <span className="text-xs block">in stock</span>
          </div>
        </div>

        {/* Purchase Section with better controls */}
        <div className="space-y-3">
          <div className="flex items-center space-x-2">
            <div className="flex items-center border-2 border-purple-200 rounded-lg">
              <button
                onClick={() => setPurchaseQty(Math.max(1, purchaseQty - 1))}
                className="p-2 hover:bg-purple-50 transition-colors"
                disabled={isOutOfStock}
              >
                <Minus className="w-4 h-4" />
              </button>
              <input
                type="number"
                min="1"
                max={sweet.quantity_in_stock}
                value={purchaseQty}
                onChange={(e) => setPurchaseQty(parseInt(e.target.value) || 1)}
                className="w-16 text-center font-semibold"
                disabled={isOutOfStock}
              />
              <button
                onClick={() => setPurchaseQty(Math.min(sweet.quantity_in_stock, purchaseQty + 1))}
                className="p-2 hover:bg-purple-50 transition-colors"
                disabled={isOutOfStock}
              >
                <Plus className="w-4 h-4" />
              </button>
            </div>
            
            <button
              onClick={() => {
                onPurchase(sweet.sweet_id, purchaseQty);
                setPurchaseQty(1);
              }}
              disabled={isOutOfStock}
              className={`flex-1 py-2.5 rounded-xl font-semibold transition-all flex items-center justify-center space-x-2 ${
                isOutOfStock
                  ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                  : 'bg-gradient-to-r from-green-500 to-emerald-600 text-white hover:from-green-600 hover:to-emerald-700 transform hover:scale-105 shadow-lg'
              }`}
            >
              <ShoppingCart className="w-4 h-4" />
              <span>Purchase</span>
            </button>
          </div>

          {/* Admin Actions */}
          {isAdmin && (
            <div className="space-y-2 pt-3 border-t-2 border-gray-100">
              {/* Restock */}
              {showRestock ? (
                <div className="flex items-center space-x-2 animate-slideDown">
                  <div className="flex items-center border-2 border-blue-200 rounded-lg">
                    <button
                      onClick={() => setRestockQty(Math.max(1, restockQty - 5))}
                      className="p-2 hover:bg-blue-50 transition-colors"
                    >
                      <Minus className="w-4 h-4" />
                    </button>
                    <input
                      type="number"
                      min="1"
                      value={restockQty}
                      onChange={(e) => setRestockQty(parseInt(e.target.value) || 1)}
                      className="w-20 text-center font-semibold"
                    />
                    <button
                      onClick={() => setRestockQty(restockQty + 5)}
                      className="p-2 hover:bg-blue-50 transition-colors"
                    >
                      <Plus className="w-4 h-4" />
                    </button>
                  </div>
                  <button
                    onClick={() => {
                      onRestock(sweet.sweet_id, restockQty);
                      setShowRestock(false);
                      setRestockQty(10);
                    }}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    ✓
                  </button>
                  <button
                    onClick={() => setShowRestock(false)}
                    className="px-3 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400"
                  >
                    ✕
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => setShowRestock(true)}
                  className="w-full py-2.5 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl hover:from-blue-600 hover:to-blue-700 transition-all flex items-center justify-center space-x-2 shadow-md hover:shadow-lg transform hover:scale-105"
                >
                  <Package className="w-4 h-4" />
                  <span>Restock</span>
                </button>
              )}

              {/* Edit & Delete */}
              <div className="grid grid-cols-2 gap-2">
                <button
                  onClick={() => onEdit(sweet)}
                  className="py-2.5 bg-gradient-to-r from-yellow-500 to-orange-500 text-white rounded-xl hover:from-yellow-600 hover:to-orange-600 transition-all flex items-center justify-center space-x-1 shadow-md hover:shadow-lg transform hover:scale-105"
                >
                  <Edit className="w-4 h-4" />
                  <span>Edit</span>
                </button>
                <button
                  onClick={() => onDelete(sweet.sweet_id)}
                  className="py-2.5 bg-gradient-to-r from-red-500 to-pink-500 text-white rounded-xl hover:from-red-600 hover:to-pink-600 transition-all flex items-center justify-center space-x-1 shadow-md hover:shadow-lg transform hover:scale-105"
                >
                  <Trash2 className="w-4 h-4" />
                  <span>Delete</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SweetCard;