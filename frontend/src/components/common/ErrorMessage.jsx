import { XCircle, AlertTriangle } from 'lucide-react';
import { useState } from 'react';

const ErrorMessage = ({ message, type = 'error' }) => {
  const [isVisible, setIsVisible] = useState(true);
  
  if (!message || !isVisible) return null;

  const styles = {
    error: 'bg-red-50 border-red-200 text-red-700',
    warning: 'bg-yellow-50 border-yellow-200 text-yellow-700',
    success: 'bg-green-50 border-green-200 text-green-700',
  };

  const icons = {
    error: <XCircle className="w-5 h-5" />,
    warning: <AlertTriangle className="w-5 h-5" />,
    success: '✅',
  };

  return (
    <div className={`${styles[type]} border-l-4 px-4 py-3 rounded-lg mb-4 shadow-md animate-slideDown relative`}>
      <div className="flex items-center">
        <span className="mr-2">{icons[type]}</span>
        <p className="text-sm font-medium flex-1">{message}</p>
        <button 
          onClick={() => setIsVisible(false)}
          className="ml-2 hover:opacity-70 transition-opacity"
        >
          ✕
        </button>
      </div>
    </div>
  );
};

export default ErrorMessage;