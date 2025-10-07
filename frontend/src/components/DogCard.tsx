'use client'

import { Dog } from '@/types'
import Image from 'next/image'
import Link from 'next/link'
import { MapPin, Calendar } from 'lucide-react'

interface DogCardProps {
  dog: Dog
}

export default function DogCard({ dog }: DogCardProps) {
  const getAgeText = () => {
    if (dog.age_years === 0) {
      return `${dog.age_months} meses`
    } else if (dog.age_months === 0) {
      return `${dog.age_years} ${dog.age_years === 1 ? 'año' : 'años'}`
    } else {
      return `${dog.age_years} ${dog.age_years === 1 ? 'año' : 'años'} y ${dog.age_months} meses`
    }
  }

  const getStatusBadge = () => {
    const statusColors = {
      disponible: 'bg-green-100 text-green-800',
      reservado: 'bg-yellow-100 text-yellow-800',
      adoptado: 'bg-gray-100 text-gray-800'
    }

    return (
      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${statusColors[dog.status]}`}>
        {dog.status.charAt(0).toUpperCase() + dog.status.slice(1)}
      </span>
    )
  }

  return (
    <Link href={`/perros/${dog.id}`}>
      <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow cursor-pointer">
        <div className="relative h-48 w-full">
          <Image
            src={dog.photos[0] || '/placeholder-dog.jpg'}
            alt={dog.name}
            fill
            className="object-cover"
          />
          <div className="absolute top-2 right-2">
            {getStatusBadge()}
          </div>
        </div>

        <div className="p-4">
          <h3 className="text-xl font-bold mb-2">{dog.name}</h3>

          <div className="space-y-2 text-sm text-gray-600">
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4" />
              <span>{getAgeText()}</span>
            </div>

            <div className="flex items-center gap-2">
              <MapPin className="w-4 h-4" />
              <span>{dog.province || dog.address || 'Costa Rica'}</span>
            </div>

            <div className="flex gap-2 mt-3">
              <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                {dog.size}
              </span>
              <span className="px-2 py-1 bg-purple-100 text-purple-800 rounded text-xs">
                {dog.gender}
              </span>
              <span className="px-2 py-1 bg-orange-100 text-orange-800 rounded text-xs">
                {dog.breed}
              </span>
            </div>
          </div>

          {dog.description && (
            <p className="mt-3 text-sm text-gray-700 line-clamp-2">
              {dog.description}
            </p>
          )}
        </div>
      </div>
    </Link>
  )
}
