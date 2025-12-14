import { useState } from 'react'

function App() {
  const [tailwindWorking, setTailwindWorking] = useState(true)

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-pink-900 to-red-900">
      <div className="container mx-auto px-4 py-16">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold text-white mb-4 animate-pulse">
            🍬 Sweet Shop Management
          </h1>
          <p className="text-2xl text-pink-200">
            Tailwind CSS Test Page
          </p>
        </div>
      </div>
    </div>
  )
}

export default App