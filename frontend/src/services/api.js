const API_BASE_URL = 'https://seqlens.onrender.com';

export const uploadVCF = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Upload failed');
  }

  return response.json();
};

export const analyzeVCF = async (jobId) => {
  const response = await fetch(`${API_BASE_URL}/analyze/${jobId}`, {
    method: 'POST',
  });

  if (!response.ok) {
    throw new Error('Analysis failed');
  }

  return response.json();
};

export const downloadReport = (jobId) => {
  window.open(`${API_BASE_URL}/report/${jobId}`, '_blank');
};