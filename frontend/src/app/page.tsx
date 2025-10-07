'use client'

import { useEffect, useState } from 'react'
import DogCard from '@/components/DogCard'
import MapView from '@/components/MapView'
import { Dog } from '@/types'
import api from '@/lib/api'
import { Search, MapPin } from 'lucide-react'

export default function Home() {
  const [dogs, setDogs] = useState<Dog[]>([])
  const [loading, setLoading] = useState(true)
  const [viewMode, setViewMode] = useState<'grid' | 'map'>('grid')

  // Filters
  const [filters, setFilters] = useState({
    size: '',
    gender: '',
    province: ''
  })

  useEffect(() => {
    fetchDogs()
  }, [filters])

  const fetchDogs = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams()

      if (filters.size) params.append('size', filters.size)
      if (filters.gender) params.append('gender', filters.gender)
      if (filters.province) params.append('province', filters.province)

      const response = await api.get(`/dogs?${params.toString()}`)
      setDogs(response.data)
    } catch (error) {
      console.error('Error fetching dogs:', error)
    } finally {
      setLoading(false)
    }
  }

  const provinces = [
    'San José', 'Alajuela', 'Cartago', 'Heredia',
    'Guanacaste', 'Puntarenas', 'Limón'
  ]

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Encuentra tu mejor amigo
          </h1>
          <p className="text-xl text-blue-100">
            Ayuda a un perro a encontrar un hogar en Costa Rica
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Filters */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex flex-col md:flex-row gap-4 items-end">
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tamaño
              </label>
              <select
                value={filters.size}
                onChange={(e) => setFilters({ ...filters, size: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Todos</option>
                <option value="pequeño">Pequeño</option>
                <option value="mediano">Mediano</option>
                <option value="grande">Grande</option>
              </select>
            </div>

            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Género
              </label>
              <select
                value={filters.gender}
                onChange={(e) => setFilters({ ...filters, gender: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Todos</option>
                <option value="macho">Macho</option>
                <option value="hembra">Hembra</option>
              </select>
            </div>

            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Provincia
              </label>
              <select
                value={filters.province}
                onChange={(e) => setFilters({ ...filters, province: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Todas</option>
                {provinces.map(province => (
                  <option key={province} value={province}>{province}</option>
                ))}
              </select>
            </div>

            <div className="flex gap-2">
              <button
                onClick={() => setViewMode('grid')}
                className={`px-4 py-2 rounded-md transition-colors ${
                  viewMode === 'grid'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                <Search className="w-5 h-5" />
              </button>
              <button
                onClick={() => setViewMode('map')}
                className={`px-4 py-2 rounded-md transition-colors ${
                  viewMode === 'map'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                <MapPin className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>

        {/* Content */}
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Cargando perros...</p>
          </div>
        ) : viewMode === 'grid' ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {dogs.length > 0 ? (
              dogs.map(dog => <DogCard key={dog.id} dog={dog} />)
            ) : (
              <div className="col-span-full text-center py-12">
                <p className="text-gray-600 text-lg">No se encontraron perros con estos filtros</p>
              </div>
            )}
          </div>
        ) : (
          <div className="h-[600px] rounded-lg overflow-hidden shadow-md">
            <MapView dogs={dogs} />
          </div>
        )}
      </div>
    </main>
  )
}
