import React from 'react';

const Header = ({ filial }) => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-4xl mx-auto px-4 py-6">
        <div className="flex flex-col items-center text-center">
          {/* Logo Digital Sat */}
          <div className="mb-4">
            <div className="text-3xl font-bold text-red-600 mb-2">
              DIGITAL SAT
            </div>
            <div className="text-sm text-gray-600">
              Distribuidora de Produtos de Segurança Eletrônica e Conectividade
            </div>
          </div>
          
          {/* Título da Pesquisa */}
          <h1 className="text-2xl font-semibold text-gray-800 mb-2">
            Pesquisa de Satisfação
          </h1>
          
          {/* Informações da Filial */}
          {filial && (
            <div className="bg-red-50 px-4 py-2 rounded-lg">
              <span className="text-red-700 font-medium">
                Filial: {filial.nome}
              </span>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;

