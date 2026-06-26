import React, { useRef } from 'react';
import { FileText, AlertCircle } from 'lucide-react';

const UploadForm = ({ onUpload, isUploading }) => {
  const fileInputRef = useRef(null);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      onUpload(file);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        onClick={handleClick}
        className="border-2 border-dashed border-gray-300 rounded-xl p-12 text-center cursor-pointer hover:border-blue-400 hover:bg-gray-50 transition-all duration-300"
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".vcf,.vcf.gz"
          onChange={handleFileSelect}
          className="hidden"
        />
        
        <div className="flex flex-col items-center gap-4">
          <FileText className="w-16 h-16 text-gray-400" />
          
          <div>
            <p className="text-lg font-semibold text-gray-700">
              Click to upload your VCF file
            </p>
            <p className="text-sm text-gray-500 mt-2">
              Supports .vcf and .vcf.gz files
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs text-gray-400 mt-4">
            <AlertCircle className="w-4 h-4" />
            <span>Max file size: 100MB</span>
          </div>
        </div>
      </div>

      {isUploading && (
        <div className="mt-6 text-center">
          <div className="inline-flex items-center gap-2 text-blue-600">
            <div className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
            <span className="font-medium">Uploading...</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default UploadForm;