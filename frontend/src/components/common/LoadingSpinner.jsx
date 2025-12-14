const LoadingSpinner = () => {
  return (
    <div className="flex flex-col items-center justify-center p-8">
      <div className="relative w-24 h-24">
        {/* Outer ring */}
        <div className="absolute inset-0 border-4 border-purple-200 rounded-full animate-pulse"></div>
        
        {/* Spinning gradient ring */}
        <div className="absolute inset-0 border-4 border-transparent border-t-purple-600 border-r-pink-600 rounded-full animate-spin"></div>
        
        {/* Inner dot */}
        <div className="absolute inset-6 bg-gradient-to-br from-purple-600 to-pink-600 rounded-full animate-pulse"></div>
        
        {/* Center candy icon */}
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-2xl animate-bounce">🍬</span>
        </div>
      </div>
      <p className="mt-6 text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-pink-600 font-bold text-lg animate-pulse">
        Loading Sweet Shop...
      </p>
    </div>
  );
};

export default LoadingSpinner;