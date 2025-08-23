'use client';

import { useState, useEffect } from 'react';
import { 
  UserIcon,
  PhoneIcon,
  ClockIcon,
  ExclamationCircleIcon
} from '@heroicons/react/24/outline';
import clsx from 'clsx';

interface Patient {
  id: string;
  name: string;
  age: number;
  lastActivity: string;
  status: 'active' | 'inactive' | 'alert';
  phone?: string;
  riskLevel: 'low' | 'medium' | 'high';
}

export default function PatientList() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPatients();
  }, []);

  const loadPatients = async () => {
    try {
      // Connect to actual backend API
      const response = await fetch('http://localhost:8000/api/v1/patients/1');
      const patientData = await response.json();
      
      // Get conversations to determine activity status
      const conversationsResponse = await fetch('http://localhost:8000/api/v1/conversations');
      const conversationsData = await conversationsResponse.json();
      
      const hasRecentActivity = Array.isArray(conversationsData) && conversationsData.length > 0;
      const lastActivityTime = hasRecentActivity ? 
        conversationsData[conversationsData.length - 1]?.timestamp : 
        new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(); // 24 hours ago
      
      setPatients([
        {
          id: patientData.id.toString(),
          name: patientData.name,
          age: patientData.age,
          lastActivity: lastActivityTime,
          status: hasRecentActivity ? 'active' : 'inactive',
          phone: '+201234567890',
          riskLevel: patientData.condition.includes('مبكر') ? 'medium' : 'high'
        }
      ]);
    } catch (error) {
      console.error('Error loading patients:', error);
      // Fallback to demo data if API fails
      setPatients([
        {
          id: '1',
          name: 'مريض تجريبي',
          age: 70,
          lastActivity: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
          status: 'inactive',
          phone: '+201234567890',
          riskLevel: 'medium'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: Patient['status']) => {
    switch (status) {
      case 'active':
        return 'text-green-600 bg-green-100';
      case 'inactive':
        return 'text-gray-600 bg-gray-100';
      case 'alert':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getRiskLevelColor = (level: Patient['riskLevel']) => {
    switch (level) {
      case 'low':
        return 'text-green-700';
      case 'medium':
        return 'text-yellow-700';
      case 'high':
        return 'text-red-700';
      default:
        return 'text-gray-700';
    }
  };

  const formatLastActivity = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 1) {
      return 'منذ دقائق';
    } else if (diffInHours < 24) {
      return `منذ ${diffInHours} ساعة`;
    } else {
      const diffInDays = Math.floor(diffInHours / 24);
      return `منذ ${diffInDays} يوم`;
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">المرضى</h3>
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="animate-pulse">
              <div className="flex items-center space-x-4 space-x-reverse">
                <div className="w-10 h-10 bg-gray-200 rounded-full"></div>
                <div className="flex-1 space-y-2">
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">المرضى</h3>
        <button 
          onClick={loadPatients}
          className="text-sm text-primary-600 hover:text-primary-700"
        >
          تحديث
        </button>
      </div>
      
      <div className="space-y-4">
        {patients.map((patient) => (
          <div 
            key={patient.id}
            className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
          >
            <div className="flex items-center space-x-3 space-x-reverse">
              <div className="relative">
                <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                  <UserIcon className="w-5 h-5 text-primary-600" />
                </div>
                <div className={clsx(
                  'absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-white',
                  patient.status === 'active' ? 'bg-green-500' :
                  patient.status === 'alert' ? 'bg-red-500' : 'bg-gray-400'
                )}></div>
              </div>
              
              <div className="flex-1">
                <div className="flex items-center space-x-2 space-x-reverse">
                  <h4 className="font-medium text-gray-900">{patient.name}</h4>
                  <span className="text-sm text-gray-500">({patient.age} سنة)</span>
                  {patient.riskLevel === 'high' && (
                    <ExclamationCircleIcon className="w-4 h-4 text-red-500" />
                  )}
                </div>
                
                <div className="flex items-center space-x-4 space-x-reverse mt-1">
                  <div className="flex items-center space-x-1 space-x-reverse">
                    <ClockIcon className="w-3 h-3 text-gray-400" />
                    <span className="text-xs text-gray-500">
                      {formatLastActivity(patient.lastActivity)}
                    </span>
                  </div>
                  
                  <span className={clsx(
                    'text-xs font-medium',
                    getRiskLevelColor(patient.riskLevel)
                  )}>
                    {patient.riskLevel === 'low' ? 'منخفض' :
                     patient.riskLevel === 'medium' ? 'متوسط' : 'عالي'}
                  </span>
                </div>
              </div>
            </div>
            
            <div className="flex items-center space-x-2 space-x-reverse">
              {patient.phone && (
                <button className="p-2 text-gray-400 hover:text-primary-600 transition-colors">
                  <PhoneIcon className="w-4 h-4" />
                </button>
              )}
              
              <span className={clsx(
                'px-2 py-1 text-xs font-medium rounded-full',
                getStatusColor(patient.status)
              )}>
                {patient.status === 'active' ? 'نشط' :
                 patient.status === 'alert' ? 'تنبيه' : 'غير نشط'}
              </span>
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-4 pt-4 border-t border-gray-200">
        <button className="w-full text-center text-sm text-primary-600 hover:text-primary-700 font-medium">
          عرض جميع المرضى
        </button>
      </div>
    </div>
  );
}
