import React from 'react'
import WeaponList from './components/WeaponList'

function App() {
  return (
    <div className="min-h-screen bg-black text-white p-8">
      <h1 className="text-4xl font-bold mb-8 text-blue-500">
        Elden Ring Weapons Browser
      </h1>
      <WeaponList />
    </div>
  )
}

export default App