import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { ChevronDown } from 'lucide-react';
import { filiais } from '../lib/filiais';

const FilialSelector = ({ onFilialSelect }) => {
  const [selectedFilial, setSelectedFilial] = useState('');
  const [isOpen, setIsOpen] = useState(false);

  const handleFilialSelect = (filial) => {
    setSelectedFilial(filial);
    setIsOpen(false);
  };

  const handleContinue = () => {
    if (selectedFilial) {
      onFilialSelect(selectedFilial);
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-6">
      <div className="text-center mb-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-2">
          Selecione sua filial
        </h2>
        <p className="text-gray-600">
          Para continuar com a pesquisa, selecione a filial onde você foi atendido.
        </p>
      </div>

      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Filial
        </label>
        <div className="relative">
          <button
            type="button"
            onClick={() => setIsOpen(!isOpen)}
            className="w-full bg-white border border-gray-300 rounded-lg px-4 py-3 text-left focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-colors"
          >
            <span className={selectedFilial ? 'text-gray-900' : 'text-gray-500'}>
              {selectedFilial ? selectedFilial.nome : 'Selecione uma filial'}
            </span>
            <ChevronDown 
              className={`absolute right-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400 transition-transform ${
                isOpen ? 'rotate-180' : ''
              }`}
            />
          </button>

          {isOpen && (
            <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-auto">
              {filiais.map((filial) => (
                <button
                  key={filial.id}
                  type="button"
                  onClick={() => handleFilialSelect(filial)}
                  className="w-full px-4 py-3 text-left hover:bg-gray-50 focus:bg-gray-50 focus:outline-none transition-colors"
                >
                  {filial.nome}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      <Button 
        onClick={handleContinue}
        disabled={!selectedFilial}
        className="w-full bg-red-600 hover:bg-red-700 text-white py-3"
      >
        Continuar
      </Button>
    </div>
  );
};

export default FilialSelector;

