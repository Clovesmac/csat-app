import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Star, CheckCircle, MessageCircle, ShoppingCart, RotateCcw, Headphones, HelpCircle } from 'lucide-react'
import './App.css'

function App() {
  const [rating, setRating] = useState(0)
  const [hoveredRating, setHoveredRating] = useState(0)
  const [context, setContext] = useState('')
  const [otherContext, setOtherContext] = useState('')
  const [comment, setComment] = useState('')
  const [submitted, setSubmitted] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const contextOptions = [
    { value: 'compra', label: 'Compra', icon: ShoppingCart },
    { value: 'devolucao', label: 'Devolução', icon: RotateCcw },
    { value: 'suporte', label: 'Suporte/Assistência', icon: Headphones },
    { value: 'outro', label: 'Outro', icon: HelpCircle }
  ]

  const handleStarClick = (starValue) => {
    setRating(starValue)
  }

  const handleStarHover = (starValue) => {
    setHoveredRating(starValue)
  }

  const handleStarLeave = () => {
    setHoveredRating(0)
  }

  const handleContextChange = (value) => {
    setContext(value)
    if (value !== 'outro') {
      setOtherContext('')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // Validações
    if (rating === 0) {
      alert('Por favor, selecione uma avaliação de 1 a 5 estrelas.')
      return
    }
    
    if (!context) {
      alert('Por favor, selecione o que você está avaliando.')
      return
    }
    
    if (context === 'outro' && !otherContext.trim()) {
      alert('Por favor, especifique o que você está avaliando no campo "Outro".')
      return
    }

    setIsSubmitting(true)
    
    // Determinar o contexto final
    const finalContext = context === 'outro' ? otherContext : contextOptions.find(opt => opt.value === context)?.label
    
    try {
      const response = await fetch('/api/csat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          rating,
          context: finalContext,
          comment,
          timestamp: new Date().toISOString()
        })
      })

      if (response.ok) {
        setSubmitted(true)
        setIsSubmitting(false)
      } else {
        throw new Error('Erro ao enviar avaliação')
      }
    } catch (error) {
      console.error('Erro:', error)
      setIsSubmitting(false)
      alert('Erro ao enviar avaliação. Tente novamente.')
    }
  }

  const getRatingText = (stars) => {
    switch (stars) {
      case 1: return 'Muito Insatisfeito'
      case 2: return 'Insatisfeito'
      case 3: return 'Neutro'
      case 4: return 'Satisfeito'
      case 5: return 'Muito Satisfeito'
      default: return 'Selecione uma avaliação'
    }
  }

  if (submitted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
        <Card className="w-full max-w-md mx-auto shadow-lg">
          <CardContent className="pt-6">
            <div className="text-center space-y-4">
              <CheckCircle className="w-16 h-16 text-green-500 mx-auto" />
              <h2 className="text-2xl font-bold text-gray-900">Obrigado!</h2>
              <p className="text-gray-600">
                Sua avaliação foi enviada com sucesso. Agradecemos seu feedback!
              </p>
              <Button 
                onClick={() => {
                  setSubmitted(false)
                  setRating(0)
                  setContext('')
                  setOtherContext('')
                  setComment('')
                  setIsSubmitting(false)
                }}
                className="w-full"
              >
                Nova Avaliação
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <Card className="w-full max-w-md mx-auto shadow-lg">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-bold text-gray-900">
            Avaliação de Atendimento
          </CardTitle>
          <CardDescription className="text-gray-600">
            Como foi sua experiência conosco hoje?
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Sistema de Estrelas */}
            <div className="space-y-3">
              <label className="block text-sm font-medium text-gray-700">
                Qual sua satisfação geral com o atendimento hoje?
              </label>
              <div className="flex justify-center space-x-1">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => handleStarClick(star)}
                    onMouseEnter={() => handleStarHover(star)}
                    onMouseLeave={handleStarLeave}
                    className="p-1 transition-transform hover:scale-110 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded"
                  >
                    <Star
                      className={`w-8 h-8 transition-colors ${
                        star <= (hoveredRating || rating)
                          ? 'text-yellow-400 fill-yellow-400'
                          : 'text-gray-300'
                      }`}
                    />
                  </button>
                ))}
              </div>
              <p className="text-center text-sm text-gray-600">
                {getRatingText(hoveredRating || rating)}
              </p>
            </div>

            {/* Pergunta de Contexto */}
            <div className="space-y-3">
              <label className="block text-sm font-medium text-gray-700">
                Você está avaliando:
              </label>
              <div className="space-y-2">
                {contextOptions.map((option) => {
                  const IconComponent = option.icon
                  return (
                    <label
                      key={option.value}
                      className={`flex items-center p-3 border rounded-lg cursor-pointer transition-colors ${
                        context === option.value
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <input
                        type="radio"
                        name="context"
                        value={option.value}
                        checked={context === option.value}
                        onChange={(e) => handleContextChange(e.target.value)}
                        className="sr-only"
                      />
                      <IconComponent className="w-5 h-5 mr-3 text-gray-600" />
                      <span className="text-sm font-medium text-gray-700">
                        {option.label}
                      </span>
                    </label>
                  )
                })}
              </div>
              
              {/* Campo de texto para "Outro" */}
              {context === 'outro' && (
                <div className="mt-3">
                  <Input
                    type="text"
                    placeholder="Especifique o que você está avaliando..."
                    value={otherContext}
                    onChange={(e) => setOtherContext(e.target.value)}
                    className="w-full"
                    maxLength={50}
                  />
                  <p className="text-xs text-gray-500 text-right mt-1">
                    {otherContext.length}/50 caracteres
                  </p>
                </div>
              )}
            </div>

            {/* Campo de Comentário */}
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">
                <MessageCircle className="w-4 h-4 inline mr-1" />
                Comentários (opcional)
              </label>
              <Textarea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Conte-nos mais sobre sua experiência..."
                className="min-h-[100px] resize-none"
                maxLength={500}
              />
              <p className="text-xs text-gray-500 text-right">
                {comment.length}/500 caracteres
              </p>
            </div>

            {/* Botão de Envio */}
            <Button
              type="submit"
              disabled={rating === 0 || !context || isSubmitting || (context === 'outro' && !otherContext.trim())}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400"
            >
              {isSubmitting ? 'Enviando...' : 'Enviar Avaliação'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

export default App

