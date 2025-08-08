import React from 'react';
import { Button } from '@/components/ui/button';
import { CheckCircle, Phone, Mail, Clock } from 'lucide-react';

const ThankYou = ({ onNewSurvey }) => {
  return (
    <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-8 text-center">
      {/* Ícone de sucesso */}
      <div className="mb-6">
        <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-800 mb-2">
          Obrigado pela sua avaliação!
        </h2>
        <p className="text-gray-600">
          Sua opinião é muito importante para nós e nos ajuda a melhorar nossos serviços continuamente.
        </p>
      </div>

      {/* Informações de contato */}
      <div className="bg-gray-50 rounded-lg p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          Entre em contato conosco
        </h3>
        
        <div className="space-y-3 text-sm">
          <div className="flex items-center justify-center space-x-2">
            <Phone className="w-4 h-4 text-red-600" />
            <span>(47) 3263-5556 / (47) 3263-5555</span>
          </div>
          
          <div className="flex items-center justify-center space-x-2">
            <Mail className="w-4 h-4 text-red-600" />
            <span>contato@digitalsat.com.br</span>
          </div>
          
          <div className="flex items-center justify-center space-x-2">
            <Clock className="w-4 h-4 text-red-600" />
            <span>Segunda à sexta, das 7h45 às 12h e das 13h30 às 18h</span>
          </div>
        </div>
      </div>

      {/* Mensagem adicional */}
      <div className="mb-6">
        <p className="text-gray-600 text-sm">
          A Digital Sat está há mais de 25 anos no mercado, sempre buscando oferecer 
          as melhores soluções em segurança eletrônica e conectividade.
        </p>
      </div>

      {/* Botão para nova avaliação */}
      <Button
        onClick={onNewSurvey}
        className="bg-red-600 hover:bg-red-700 text-white px-6 py-2"
      >
        Fazer Nova Avaliação
      </Button>

      {/* Link para o site */}
      <div className="mt-6">
        <a 
          href="https://digitalsat.com.br" 
          target="_blank" 
          rel="noopener noreferrer"
          className="text-red-600 hover:text-red-700 text-sm underline"
        >
          Visite nosso site: digitalsat.com.br
        </a>
      </div>
    </div>
  );
};

export default ThankYou;

