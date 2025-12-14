import api from './api';

const sweetService = {
  // Get all sweets
  async getAllSweets() {
    const response = await api.get('/api/sweets');
    return response.data;
  },

  // Search sweets
  async searchSweets(params) {
    const response = await api.get('/api/sweets/search', { params });
    return response.data;
  },

  // Create sweet
  async createSweet(sweetData) {
    const response = await api.post('/api/sweets', sweetData);
    return response.data;
  },

  // Update sweet
  async updateSweet(id, sweetData) {
    const response = await api.put(`/api/sweets/${id}`, sweetData);
    return response.data;
  },

  // Delete sweet (admin only)
  async deleteSweet(id) {
    const response = await api.delete(`/api/sweets/${id}`);
    return response.data;
  },

  // Purchase sweet
  async purchaseSweet(id, quantity) {
    const response = await api.post(`/api/sweets/${id}/purchase`, {
      quantity_to_purchase: quantity
    });
    return response.data;
  },

  // Restock sweet (admin only)
  async restockSweet(id, quantity) {
    const response = await api.post(`/api/sweets/${id}/restock`, {
      quantity_to_add: quantity
    });
    return response.data;
  },
};

export default sweetService;