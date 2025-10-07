'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import Image from 'next/image'
import { Dog } from '@/types'
import api from '@/lib/api'
import ShareButtons from '@/components/ShareButtons'
import { MapPin, Calendar, Phone, Mail, Heart, CheckCircle } from 'lucide-react'

export default function DogDetailPage() {
  const params = useParams()
  const [dog, setDog] = useState<Dog | null>(null)
  const [loading, setLoading] = useState(true)
  const [currentImageIndex, setCurrentImageIndex] = useState(0)

  useEffect(() => {
    fetchDog()
  }, [params.id])

  const fetchDog = async () => {
    try {
      const response = await api.get(`/dogs/${params.id}`)
      setDog(response.data)
    } catch (error) {
      console.error('Error fetching dog:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (!dog) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-xl text-gray-600">Perro no encontrado</p>
      </div>
    )
  }

  const getAgeText = () => {
    if (dog.age_years === 0) {
      return `${dog.age_months} meses`
    } else if (dog.age_months === 0) {
      return `${dog.age_years} ${dog.age_years === 1 ? 'año' : 'años'}`
    } else {
      return `${dog.age_years} ${dog.age_years === 1 ? 'año' : 'años'} y ${dog.age_months} meses`
    }
  }

  const whatsappMessage = `Hola! Estoy interesado en adoptar a ${dog.name}. Vi su publicación en Pura Pata.`
  const whatsappUrl = `https://wa.me/${dog.contact_phone.replace(/\D/g, '')}?text=${encodeURIComponent(whatsappMessage)}`

  return (
    <main className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Back button */}
        <button
          onClick={() => window.history.back()}
          className="mb-6 text-blue-600 hover:text-blue-700 flex items-center gap-2"
        >
          ← Volver
        </button>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Image Gallery */}
          <div className="space-y-4">
            <div className="relative aspect-square rounded-lg overflow-hidden bg-gray-200">
              <Image
                src={dog.photos[currentImageIndex] || '/placeholder-dog.jpg'}
                alt={dog.name}
                fill
                className="object-cover"
              />
            </div>

            {dog.photos.length > 1 && (
              <div className="grid grid-cols-5 gap-2">
                {dog.photos.map((photo, index) => (
                  <button
                    key={index}
                    onClick={() => setCurrentImageIndex(index)}
                    className={`relative aspect-square rounded-lg overflow-hidden ${
                      currentImageIndex === index ? 'ring-2 ring-blue-600' : ''
                    }`}
                  >
                    <Image src={photo} alt={`${dog.name} ${index + 1}`} fill className="object-cover" />
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Dog Info */}
          <div className="space-y-6">
            <div>
              <h1 className="text-4xl font-bold mb-2">{dog.name}</h1>
              <div className="flex gap-2 mb-4">
                <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-semibold">
                  {dog.size}
                </span>
                <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-semibold">
                  {dog.gender}
                </span>
                <span className="px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-sm font-semibold">
                  {dog.breed}
                </span>
              </div>
            </div>

            {/* Details */}
            <div className="bg-white rounded-lg p-6 space-y-4">
              <div className="flex items-center gap-3">
                <Calendar className="w-5 h-5 text-gray-600" />
                <div>
                  <p className="text-sm text-gray-600">Edad</p>
                  <p className="font-semibold">{getAgeText()}</p>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <MapPin className="w-5 h-5 text-gray-600" />
                <div>
                  <p className="text-sm text-gray-600">Ubicación</p>
                  <p className="font-semibold">{dog.province || dog.address || 'Costa Rica'}</p>
                </div>
              </div>

              {/* Health Info */}
              <div className="border-t pt-4">
                <p className="text-sm font-semibold text-gray-700 mb-2">Estado de Salud</p>
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    {dog.vaccinated ? (
                      <CheckCircle className="w-5 h-5 text-green-600" />
                    ) : (
                      <div className="w-5 h-5 rounded-full border-2 border-gray-300" />
                    )}
                    <span className={dog.vaccinated ? 'text-green-700' : 'text-gray-600'}>
                      Vacunado
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    {dog.sterilized ? (
                      <CheckCircle className="w-5 h-5 text-green-600" />
                    ) : (
                      <div className="w-5 h-5 rounded-full border-2 border-gray-300" />
                    )}
                    <span className={dog.sterilized ? 'text-green-700' : 'text-gray-600'}>
                      Castrado
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    {dog.dewormed ? (
                      <CheckCircle className="w-5 h-5 text-green-600" />
                    ) : (
                      <div className="w-5 h-5 rounded-full border-2 border-gray-300" />
                    )}
                    <span className={dog.dewormed ? 'text-green-700' : 'text-gray-600'}>
                      Desparasitado
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Description */}
            {dog.description && (
              <div className="bg-white rounded-lg p-6">
                <h2 className="font-semibold text-lg mb-3">Sobre {dog.name}</h2>
                <p className="text-gray-700 whitespace-pre-line">{dog.description}</p>
              </div>
            )}

            {/* Special Needs */}
            {dog.special_needs && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
                <h3 className="font-semibold text-yellow-900 mb-2">Necesidades Especiales</h3>
                <p className="text-yellow-800">{dog.special_needs}</p>
              </div>
            )}

            {/* Contact */}
            <div className="bg-white rounded-lg p-6 space-y-4">
              <h2 className="font-semibold text-lg">Información de Contacto</h2>

              <div className="space-y-3">
                <a
                  href={whatsappUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-3 w-full px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  <Phone className="w-5 h-5" />
                  <span>Contactar por WhatsApp</span>
                </a>

                <div className="flex items-center gap-3 text-gray-700">
                  <Phone className="w-5 h-5" />
                  <span>{dog.contact_phone}</span>
                </div>

                {dog.contact_email && (
                  <div className="flex items-center gap-3 text-gray-700">
                    <Mail className="w-5 h-5" />
                    <span>{dog.contact_email}</span>
                  </div>
                )}
              </div>

              {dog.certificate && (
                <a
                  href={dog.certificate}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block text-center w-full px-4 py-2 border border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition-colors"
                >
                  Ver Certificado Veterinario
                </a>
              )}
            </div>

            {/* Share */}
            <div className="bg-white rounded-lg p-6">
              <h2 className="font-semibold text-lg mb-4">Compartir</h2>
              <ShareButtons
                url={`/perros/${dog.id}`}
                title={`Adopta a ${dog.name}`}
                description={dog.description || `${dog.breed} en adopción`}
              />
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
