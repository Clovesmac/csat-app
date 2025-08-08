import React from 'react';
import { getNPSCategory } from '../lib/filiais';

const NPSScale = ({ selectedScore, onScoreSelect }) => {
  const scores = Array.from({ length: 11 }, (_, i) => i);

  const handleScoreSelect = (score) => {
    onScoreSelect(score);
    
    // Rolagem automática para o fim da página após selecionar nota
    setTimeout(() => {
      window.scrollTo({
        top: document.documentElement.scrollHeight,
        behavior: 'smooth'
      });
    }, 100);
  };

  const getScoreColor = (score) => {
    const { color } = getNPSCategory(score);
    
    switch (color) {
      case 'green':
        return 'bg-green-500 hover:bg-green-600 text-white';
      case 'yellow':
        return 'bg-yellow-500 hover:bg-yellow-600 text-white';
      case 'red':
        return 'bg-red-500 hover:bg-red-600 text-white';
      default:
        return 'bg-gray-200 hover:bg-gray-300 text-gray-700';
    }
  };

  const getSelectedColor = (score) => {
    const { color } = getNPSCategory(score);
    
    switch (color) {
      case 'green':
        return 'bg-green-600 ring-green-300';
      case 'yellow':
        return 'bg-yellow-600 ring-yellow-300';
      case 'red':
        return 'bg-red-600 ring-red-300';
      default:
        return 'bg-gray-300 ring-gray-200';
    }
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="text-lg font-semibold text-gray-800 mb-2">
          Em uma escala de 0 a 10, qual a probabilidade de você recomendar a Digital Sat para um amigo ou colega?
        </h3>
        <div className="flex justify-between text-sm text-gray-600 mb-4">
          <span>Muito improvável</span>
          <span>Muito provável</span>
        </div>
      </div>

      {/* Layout responsivo: uma linha única */}
      <div className="grid grid-cols-11 gap-1 sm:gap-2 max-w-5xl mx-auto">
        {scores.map((score) => (
          <button
            key={score}
            type="button"
            onClick={() => handleScoreSelect(score)}
            className={`
              w-6 h-8 sm:w-14 sm:h-14 rounded-lg font-bold text-xs sm:text-xl transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-4 shadow-md hover:shadow-lg
              ${selectedScore === score 
                ? `${getSelectedColor(score)} ring-4 scale-105` 
                : getScoreColor(score)
              }
            `}
          >
            {score}
          </button>
        ))}
      </div>

      {selectedScore !== null && (
        <div className="text-center mt-6">
          <div className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium">
            {selectedScore >= 9 && (
              <span className="text-green-700 bg-green-100 px-3 py-1 rounded-full">
                🎉 Obrigado pela confiança!
              </span>
            )}
            {selectedScore >= 7 && selectedScore <= 8 && (
              <span className="text-yellow-700 bg-yellow-100 px-3 py-1 rounded-full">
                😊 Vamos melhorar ainda mais!
              </span>
            )}
            {selectedScore <= 6 && (
              <span className="text-red-700 bg-red-100 px-3 py-1 rounded-full">
                😔 Conte-nos o que aconteceu para que possamos melhorar nossos serviços.
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default NPSScale;

