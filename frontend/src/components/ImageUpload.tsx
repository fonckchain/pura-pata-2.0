'use client'

import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import Image from 'next/image'
import { X, Upload } from 'lucide-react'

interface ImageUploadProps {
  maxFiles?: number
  onFilesChange: (files: File[]) => void
  existingUrls?: string[]
}

export default function ImageUpload({ maxFiles = 5, onFilesChange, existingUrls = [] }: ImageUploadProps) {
  const [files, setFiles] = useState<File[]>([])
  const [previews, setPreviews] = useState<string[]>(existingUrls)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newFiles = [...files, ...acceptedFiles].slice(0, maxFiles)
    setFiles(newFiles)
    onFilesChange(newFiles)

    // Generate previews
    const newPreviews = newFiles.map(file => URL.createObjectURL(file))
    setPreviews([...existingUrls, ...newPreviews])
  }, [files, maxFiles, onFilesChange, existingUrls])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png']
    },
    maxFiles: maxFiles - files.length,
    maxSize: 5 * 1024 * 1024 // 5MB
  })

  const removeFile = (index: number) => {
    const newFiles = files.filter((_, i) => i !== index)
    const newPreviews = previews.filter((_, i) => i !== index)

    setFiles(newFiles)
    setPreviews(newPreviews)
    onFilesChange(newFiles)
  }

  return (
    <div className="space-y-4">
      {/* Preview Grid */}
      {previews.length > 0 && (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {previews.map((preview, index) => (
            <div key={index} className="relative aspect-square">
              <Image
                src={preview}
                alt={`Preview ${index + 1}`}
                fill
                className="object-cover rounded-lg"
              />
              <button
                type="button"
                onClick={() => removeFile(index)}
                className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Upload Area */}
      {files.length < maxFiles && (
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
            ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}`}
        >
          <input {...getInputProps()} />
          <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
          {isDragActive ? (
            <p className="text-blue-500">Suelta las imágenes aquí...</p>
          ) : (
            <div>
              <p className="text-gray-600 mb-2">
                Arrastra imágenes aquí o haz click para seleccionar
              </p>
              <p className="text-sm text-gray-500">
                Máximo {maxFiles} fotos (JPG, PNG - máx 5MB cada una)
              </p>
              <p className="text-sm text-gray-500">
                {files.length} de {maxFiles} fotos cargadas
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
