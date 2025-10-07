'use client'

import { Facebook, Instagram, Link as LinkIcon } from 'lucide-react'
import { useState } from 'react'

interface ShareButtonsProps {
  url: string
  title: string
  description: string
}

export default function ShareButtons({ url, title, description }: ShareButtonsProps) {
  const [copied, setCopied] = useState(false)

  const shareUrl = typeof window !== 'undefined' ? window.location.origin + url : url

  const handleCopyLink = async () => {
    try {
      await navigator.clipboard.writeText(shareUrl)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  const handleFacebookShare = () => {
    const facebookUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`
    window.open(facebookUrl, '_blank', 'width=600,height=400')
  }

  const handleInstagramShare = () => {
    // Instagram doesn't have a direct share URL, so we copy the link
    handleCopyLink()
    alert('Link copiado! Pégalo en tu post de Instagram')
  }

  return (
    <div className="flex gap-3">
      <button
        onClick={handleFacebookShare}
        className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        aria-label="Compartir en Facebook"
      >
        <Facebook className="w-5 h-5" />
        <span>Facebook</span>
      </button>

      <button
        onClick={handleInstagramShare}
        className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:from-purple-700 hover:to-pink-700 transition-colors"
        aria-label="Compartir en Instagram"
      >
        <Instagram className="w-5 h-5" />
        <span>Instagram</span>
      </button>

      <button
        onClick={handleCopyLink}
        className="flex items-center gap-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
        aria-label="Copiar enlace"
      >
        <LinkIcon className="w-5 h-5" />
        <span>{copied ? '¡Copiado!' : 'Copiar link'}</span>
      </button>
    </div>
  )
}
