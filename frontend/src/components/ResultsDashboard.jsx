import React from 'react';
import { Download, Activity, Dna, AlertTriangle, CheckCircle } from 'lucide-react';

const COLORS = {
  'Pathogenic': '#ef4444',
  'Likely Pathogenic': '#f97316',
  'Uncertain Significance': '#eab308',
  'Likely Benign': '#22c55e',
  'Benign': '#10b981'
};

const ResultsDashboard = ({ results, onDownloadReport }) => {
  if (!results) return null;

  const chartData = [
    { name: 'Pathogenic', value: results.pathogenic_count },
    { name: 'Likely Pathogenic', value: results.likely_pathogenic_count },
    { name: 'Uncertain Significance', value: results.uncertain_count },
    { name: 'Likely Benign', value: results.likely_benign_count },
    { name: 'Benign', value: results.benign_count }
  ].filter(item => item.value > 0);

  const total = results.total_variants;
  const maxValue = Math.max(...chartData.map(d => d.value), 1);

  return (
    <div className="w-full max-w-6xl mx-auto space-y-6">
      {/* Header Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard 
          icon={<Dna className="w-6 h-6 text-blue-600" />}
          label="Total Variants"
          value={total}
          color="bg-blue-50"
        />
        <StatCard 
          icon={<AlertTriangle className="w-6 h-6 text-red-600" />}
          label="Pathogenic"
          value={results.pathogenic_count}
          color="bg-red-50"
        />
        <StatCard 
          icon={<Activity className="w-6 h-6 text-yellow-600" />}
          label="Uncertain"
          value={results.uncertain_count}
          color="bg-yellow-50"
        />
        <StatCard 
          icon={<CheckCircle className="w-6 h-6 text-green-600" />}
          label="Benign"
          value={results.benign_count}
          color="bg-green-50"
        />
      </div>

      {/* CSS Bar Chart */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Classification Distribution</h3>
        <div className="space-y-4">
          {chartData.map((item) => (
            <div key={item.name} className="flex items-center gap-4">
              <div className="w-32 text-sm font-medium text-gray-700 text-right">{item.name}</div>
              <div className="flex-1 h-8 bg-gray-100 rounded-full overflow-hidden">
                <div 
                  className="h-full rounded-full transition-all duration-500 flex items-center justify-end pr-2"
                  style={{ 
                    width: `${(item.value / maxValue) * 100}%`,
                    backgroundColor: COLORS[item.name]
                  }}
                >
                  <span className="text-white text-xs font-bold">{item.value}</span>
                </div>
              </div>
              <div className="w-16 text-sm text-gray-500">
                {((item.value / total) * 100).toFixed(1)}%
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Variant Table */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-800">Variant Details</h3>
          <button
  onClick={onDownloadReport}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Download className="w-4 h-4" />
            Download PDF Report
          </button>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Chr</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Position</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Gene</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Ref → Alt</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Score</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">ACMG</th>
              </tr>
            </thead>
            <tbody>
              {results.variants.slice(0, 50).map((variant, idx) => (
                <tr key={idx} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4 text-gray-900">{variant.chrom}</td>
                  <td className="py-3 px-4 text-gray-900">{variant.pos.toLocaleString()}</td>
                  <td className="py-3 px-4 text-gray-900">{variant.gene || '-'}</td>
                  <td className="py-3 px-4 text-gray-900">
                    <span className="font-mono text-xs">{variant.ref} → {variant.alt}</span>
                  </td>
                  <td className="py-3 px-4">
                    <span className={`font-mono font-medium ${
                      variant.pathogenicity_score > 0.7 ? 'text-red-600' :
                      variant.pathogenicity_score > 0.3 ? 'text-yellow-600' :
                      'text-green-600'
                    }`}>
                      {variant.pathogenicity_score?.toFixed(3) || '-'}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <span className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${getACMGStyle(variant.acmg_classification)}`}>
                      {variant.acmg_classification}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ icon, label, value, color }) => (
  <div className={`${color} rounded-xl p-4 flex items-center gap-4`}>
    <div className="p-2 bg-white rounded-lg shadow-sm">
      {icon}
    </div>
    <div>
      <p className="text-sm text-gray-600">{label}</p>
      <p className="text-2xl font-bold text-gray-900">{value}</p>
    </div>
  </div>
);

const getACMGStyle = (classification) => {
  const styles = {
    'Pathogenic': 'bg-red-100 text-red-800',
    'Likely Pathogenic': 'bg-orange-100 text-orange-800',
    'Uncertain Significance': 'bg-yellow-100 text-yellow-800',
    'Likely Benign': 'bg-green-100 text-green-800',
    'Benign': 'bg-emerald-100 text-emerald-800'
  };
  return styles[classification] || 'bg-gray-100 text-gray-800';
};

export default ResultsDashboard;