import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import NPSScale from './NPSScale';
import { getCnpjFromUrl } from '../lib/filiais';

const NPSForm = ({ filial, onSubmit }) => {
  const [formData, setFormData] = useState({
    score: null,
    nome: '',
    email: '',
    telefone: '',
    cnpj: '',
    comentario: ''
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  // Carregar CNPJ da URL quando o componente for montado
  useEffect(() => {
    const cnpjFromUrl = getCnpjFromUrl();
    if (cnpjFromUrl) {
      setFormData(prev => ({ ...prev, cnpj: cnpjFromUrl }));
    }
  }, []);

  const handleScoreSelect = (score) => {
    setFormData(prev => ({ ...prev, score }));
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (formData.score === null) {
      alert('Por favor, selecione uma nota de 0 a 10.');
      return;
    }

    if (formData.email && !isEmailValid(formData.email)) {
      alert('Por favor, insira um email válido');
      return;
    }

    setIsSubmitting(true);
    
    try {
      // Preparar dados para envio
      const dadosEnvio = {
        filial: filial.id,
        score: formData.score,
        nome: formData.nome || '',
        email: formData.email || '',
        telefone: formData.telefone || '',
        cnpj: formData.cnpj || '',
        comentario: formData.comentario || ''
      };

      // Enviar para o backend
      const response = await fetch('/api/nps', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dadosEnvio)
      });

      const resultado = await response.json();

      if (resultado.success) {
        // Sucesso - chamar callback de sucesso
        await onSubmit({
          ...formData,
          filial: filial.id,
          timestamp: new Date().toISOString()
        });
      } else {
        // Erro do servidor
        console.error('Erro do servidor:', resultado.error);
        alert(`Erro ao enviar avaliação: ${resultado.message}`);
      }
    } catch (error) {
      // Erro de rede ou outro erro
      console.error('Erro ao enviar pesquisa:', error);
      alert('Erro ao enviar pesquisa. Tente novamente.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const isEmailValid = (email) => {
    if (!email) return true; // Email é opcional
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const getCommentLabel = () => {
    if (formData.score !== null && formData.score <= 6) {
      return "Conte-nos o que aconteceu para que possamos melhorar";
    }
    return "Comentários ou sugestões";
  };

  return (
    <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-6 md:p-8">
      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Escala NPS */}
        <NPSScale 
          selectedScore={formData.score}
          onScoreSelect={handleScoreSelect}
        />

        {/* Campo de comentário */}
        <div className="border-t pt-8">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {getCommentLabel()}
            </label>
            <textarea
              value={formData.comentario}
              onChange={(e) => handleInputChange('comentario', e.target.value)}
              rows={4}
              maxLength={500}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-colors resize-none"
              placeholder="Conte-nos sobre sua experiência com a Digital Sat..."
            />
            <div className="text-right text-sm text-gray-500 mt-1">
              {formData.comentario.length}/500 caracteres
            </div>
          </div>
        </div>

        {/* Campos opcionais do cliente */}
        <div className="border-t pt-8">
          <h4 className="text-lg font-semibold text-gray-800 mb-4">
            Informações adicionais (opcional)
          </h4>
          
          <div className="grid md:grid-cols-2 gap-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Nome
              </label>
              <input
                type="text"
                value={formData.nome}
                onChange={(e) => handleInputChange('nome', e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-colors"
                placeholder="Seu nome"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email
              </label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => handleInputChange('email', e.target.value)}
                className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 transition-colors ${
                  isEmailValid(formData.email) 
                    ? 'border-gray-300 focus:ring-red-500 focus:border-red-500' 
                    : 'border-red-300 focus:ring-red-500 focus:border-red-500'
                }`}
                placeholder="seu@email.com"
              />
              {!isEmailValid(formData.email) && (
                <p className="text-red-600 text-sm mt-1">Email inválido</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Telefone
              </label>
              <input
                type="tel"
                value={formData.telefone}
                onChange={(e) => handleInputChange('telefone', e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-colors"
                placeholder="(47) 99999-9999"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                CNPJ
              </label>
              <input
                type="text"
                value={formData.cnpj}
                onChange={(e) => handleInputChange('cnpj', e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-colors"
                placeholder="00.000.000/0000-00"
              />
            </div>
          </div>
        </div>

        {/* Botão de envio */}
        <div className="text-center pt-6">
          <Button
            type="submit"
            disabled={formData.score === null || isSubmitting || !isEmailValid(formData.email)}
            className="bg-red-600 hover:bg-red-700 text-white px-8 py-3 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? 'Enviando...' : 'Enviar Avaliação'}
          </Button>
        </div>
      </form>
    </div>
  );
};

export default NPSForm;

