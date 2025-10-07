'use client'

import { GoogleMap, LoadScript, Marker, InfoWindow } from '@react-google-maps/api'
import { useState } from 'react'
import { Dog } from '@/types'

interface MapViewProps {
  dogs: Dog[]
  center?: { lat: number; lng: number }
  zoom?: number
  onMarkerClick?: (dog: Dog) => void
}

const defaultCenter = {
  lat: 9.7489,
  lng: -83.7534
} // Costa Rica center

const mapContainerStyle = {
  width: '100%',
  height: '100%'
}

export default function MapView({ dogs, center = defaultCenter, zoom = 8, onMarkerClick }: MapViewProps) {
  const [selectedDog, setSelectedDog] = useState<Dog | null>(null)

  const handleMarkerClick = (dog: Dog) => {
    setSelectedDog(dog)
    if (onMarkerClick) {
      onMarkerClick(dog)
    }
  }

  return (
    <LoadScript googleMapsApiKey={process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || ''}>
      <GoogleMap
        mapContainerStyle={mapContainerStyle}
        center={center}
        zoom={zoom}
      >
        {dogs.map((dog) => (
          <Marker
            key={dog.id}
            position={{ lat: dog.latitude, lng: dog.longitude }}
            onClick={() => handleMarkerClick(dog)}
          />
        ))}

        {selectedDog && (
          <InfoWindow
            position={{ lat: selectedDog.latitude, lng: selectedDog.longitude }}
            onCloseClick={() => setSelectedDog(null)}
          >
            <div className="p-2">
              <h3 className="font-bold">{selectedDog.name}</h3>
              <p className="text-sm">{selectedDog.breed}</p>
              <p className="text-xs text-gray-600">{selectedDog.province}</p>
            </div>
          </InfoWindow>
        )}
      </GoogleMap>
    </LoadScript>
  )
}
