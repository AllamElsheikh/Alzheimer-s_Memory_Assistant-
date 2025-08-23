'use client';

import { useState, useEffect } from 'react';

interface AssessmentStats {
  category: string;
  value: number;
  color: string;
}

export default function CognitiveChart() {
  const [assessmentStats, setAssessmentStats] = useState<AssessmentStats[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeChart, setActiveChart] = useState<'comparison' | 'distribution'>('comparison');

  useEffect(() => {
    loadCognitiveData();
  }, []);

  const loadCognitiveData = async () => {
    try {
      // Simulate API call - replace with actual endpoint
      await new Promise(resolve => setTimeout(resolve, 800));
      
      setAssessmentStats([
        { category: 'الذاكرة', value: 85, color: '#3B82F6' },
        { category: 'الانتباه', value: 90, color: '#10B981' },
        { category: 'اللغة', value: 94, color: '#8B5CF6' },
        { category: 'التنفيذ', value: 82, color: '#F59E0B' }
      ]);
    } catch (error) {
      console.error('Error loading cognitive data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">التقييم المعرفي</h3>
        <div className="animate-pulse">
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900">التقييم المعرفي</h3>
        
        <div className="flex space-x-2 space-x-reverse">
          <button
            onClick={() => setActiveChart('comparison')}
            className={`px-3 py-1 text-sm rounded-lg transition-colors ${
              activeChart === 'comparison'
                ? 'bg-primary-100 text-primary-700'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            المقارنة
          </button>
          <button
            onClick={() => setActiveChart('distribution')}
            className={`px-3 py-1 text-sm rounded-lg transition-colors ${
              activeChart === 'distribution'
                ? 'bg-primary-100 text-primary-700'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            التوزيع
          </button>
        </div>
      </div>

      <div className="h-64">
        {activeChart === 'comparison' && (
          <div className="h-full flex items-end justify-around space-x-4 space-x-reverse">
            {assessmentStats.map((stat, index) => (
              <div key={index} className="flex flex-col items-center flex-1">
                <div className="w-full bg-gray-200 rounded-lg overflow-hidden" style={{ height: '200px' }}>
                  <div 
                    className="w-full rounded-lg transition-all duration-1000 ease-out flex items-end justify-center"
                    style={{ 
                      height: `${stat.value}%`,
                      backgroundColor: stat.color,
                      minHeight: '20px'
                    }}
                  >
                    <span className="text-white text-sm font-medium mb-2">
                      {stat.value}%
                    </span>
                  </div>
                </div>
                <span className="text-sm text-gray-600 mt-2 text-center">
                  {stat.category}
                </span>
              </div>
            ))}
          </div>
        )}

        {activeChart === 'distribution' && (
          <div className="h-full flex items-center justify-center">
            <div className="grid grid-cols-2 gap-6 w-full max-w-md">
              {assessmentStats.map((stat, index) => (
                <div key={index} className="flex items-center space-x-3 space-x-reverse">
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-medium text-gray-700">
                        {stat.category}
                      </span>
                      <span className="text-sm text-gray-600">
                        {stat.value}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3">
                      <div 
                        className="h-3 rounded-full transition-all duration-1000 ease-out"
                        style={{ 
                          width: `${stat.value}%`,
                          backgroundColor: stat.color
                        }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Legend */}
      <div className="flex items-center justify-center space-x-6 space-x-reverse mt-4 pt-4 border-t border-gray-200">
        <div className="flex items-center space-x-2 space-x-reverse">
          <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
          <span className="text-sm text-gray-600">الذاكرة</span>
        </div>
        <div className="flex items-center space-x-2 space-x-reverse">
          <div className="w-3 h-3 bg-green-500 rounded-full"></div>
          <span className="text-sm text-gray-600">الانتباه</span>
        </div>
        <div className="flex items-center space-x-2 space-x-reverse">
          <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
          <span className="text-sm text-gray-600">اللغة</span>
        </div>
        <div className="flex items-center space-x-2 space-x-reverse">
          <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
          <span className="text-sm text-gray-600">التنفيذ</span>
        </div>
      </div>
    </div>
  );
}
