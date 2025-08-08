import { useState, useEffect } from 'react';
import Header from './components/Header';
import FilialSelector from './components/FilialSelector';
import NPSForm from './components/NPSForm';
import ThankYou from './components/ThankYou';
import { getFilialFromUrl } from './lib/filiais';
import './App.css';

// Configuração da API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://csat-backend-production.up.railway.app';

function App() {
  const [currentStep, setCurrentStep] = useState('loading');
  const [selectedFilial, setSelectedFilial] = useState(null);
  const [surveyData, setSurveyData] = useState(null);

  useEffect(() => {
    // Verificar se há filial na URL
    const filialFromUrl = getFilialFromUrl();
    
    if (filialFromUrl) {
      setSelectedFilial(filialFromUrl);
      setCurrentStep('survey');
    } else {
      setCurrentStep('filial-selection');
    }
  }, []);

  const handleFilialSelect = (filial) => {
    setSelectedFilial(filial);
    setCurrentStep('survey');
  };

  const handleSurveySubmit = async (data) => {
    try {
      console.log('Enviando dados da pesquisa:', data);
      
      const response = await fetch(`${API_BASE_URL}/api/nps`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Pesquisa enviada com sucesso:', result);
        setSurveyData(data);
        setCurrentStep('thank-you');
      } else {
        console.error('Erro ao enviar pesquisa:', response.statusText);
        // Em caso de erro, ainda mostra a tela de agradecimento
        setSurveyData(data);
        setCurrentStep('thank-you');
      }
    } catch (error) {
      console.error('Erro na conexão:', error);
      // Em caso de erro, ainda mostra a tela de agradecimento
      setSurveyData(data);
      setCurrentStep('thank-you');
    }
  };

  const handleNewSurvey = () => {
    setSurveyData(null);
    setSelectedFilial(null);
    setCurrentStep('filial-selection');
    
    // Limpar parâmetros da URL
    window.history.pushState({}, '', window.location.pathname);
  };

  if (currentStep === 'loading') {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Carregando...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header filial={selectedFilial} />
      
      <main className="container mx-auto px-4 py-8">
        {currentStep === 'filial-selection' && (
          <div className="flex items-center justify-center min-h-[60vh]">
            <FilialSelector onFilialSelect={handleFilialSelect} />
          </div>
        )}

        {currentStep === 'survey' && selectedFilial && (
          <div className="flex items-center justify-center min-h-[60vh]">
            <NPSForm 
              filial={selectedFilial} 
              onSubmit={handleSurveySubmit}
            />
          </div>
        )}

        {currentStep === 'thank-you' && (
          <div className="flex items-center justify-center min-h-[60vh]">
            <ThankYou onNewSurvey={handleNewSurvey} />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 py-6 mt-12">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <p className="text-gray-600 text-sm">
            © 2025 Digital Sat - Distribuidora de Produtos de Segurança Eletrônica e Conectividade
          </p>
          <p className="text-gray-500 text-xs mt-1">
            Há mais de 25 anos levando soluções tecnológicas aos nossos clientes e parceiros
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;

