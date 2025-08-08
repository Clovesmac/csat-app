export const filiais = [
  { id: 'balneario-camboriu', nome: 'Balneário Camboriú' },
  { id: 'blumenau', nome: 'Blumenau' },
  { id: 'brusque', nome: 'Brusque' },
  { id: 'centro-distribuicao', nome: 'Centro de Distribuição' },
  { id: 'gravatai', nome: 'Gravataí - RS' },
  { id: 'itajai', nome: 'Itajaí' },
  { id: 'itapema', nome: 'Itapema' },
  { id: 'joinville', nome: 'Joinville' },
  { id: 'lages', nome: 'Lages' },
  { id: 'rio-do-sul', nome: 'Rio do Sul' },
  { id: 'sao-jose', nome: 'São José' },
  { id: 'tubarao', nome: 'Tubarão' }
];

export const getFilialById = (id) => {
  return filiais.find(filial => filial.id === id);
};

export const getFilialFromUrl = () => {
  const urlParams = new URLSearchParams(window.location.search);
  const filialParam = urlParams.get('filial');
  
  if (filialParam) {
    return getFilialById(filialParam);
  }
  
  return null;
};

export const getCnpjFromUrl = () => {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('cnpj') || '';
};

export const getNPSCategory = (score) => {
  if (score >= 9) return { category: 'promotor', color: 'green' };
  if (score >= 7) return { category: 'neutro', color: 'yellow' };
  return { category: 'detrator', color: 'red' };
};

