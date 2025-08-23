'use client';

import { useState, useEffect } from 'react';
import { 
  ExclamationTriangleIcon,
  ClockIcon,
  HeartIcon,
  BellIcon,
  XMarkIcon
} from '@heroicons/react/24/outline';
import clsx from 'clsx';

interface Alert {
  id: string;
  type: 'critical' | 'warning' | 'info';
  title: string;
  message: string;
  patientName: string;
  timestamp: string;
  acknowledged: boolean;
}

export default function AlertsPanel() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAlerts();
  }, []);

  const loadAlerts = async () => {
    try {
      // Simulate API call - replace with actual endpoint
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setAlerts([
        {
          id: '1',
          type: 'critical',
          title: 'عدم تناول الدواء',
          message: 'لم يتم تناول دواء الضغط منذ 8 ساعات',
          patientName: 'محمد علي',
          timestamp: '2024-01-15T10:00:00Z',
          acknowledged: false
        },
        {
          id: '2',
          type: 'warning',
          title: 'انخفاض النشاط',
          message: 'لم يتم تسجيل أي نشاط منذ 6 ساعات',
          patientName: 'عائشة محمود',
          timestamp: '2024-01-15T09:30:00Z',
          acknowledged: false
        },
        {
          id: '3',
          type: 'info',
          title: 'موعد قادم',
          message: 'موعد مع الطبيب خلال ساعتين',
          patientName: 'فاطمة أحمد',
          timestamp: '2024-01-15T09:00:00Z',
          acknowledged: true
        }
      ]);
    } catch (error) {
      console.error('Error loading alerts:', error);
    } finally {
      setLoading(false);
    }
  };

  const acknowledgeAlert = (alertId: string) => {
    setAlerts(prev => 
      prev.map(alert => 
        alert.id === alertId 
          ? { ...alert, acknowledged: true }
          : alert
      )
    );
  };

  const dismissAlert = (alertId: string) => {
    setAlerts(prev => prev.filter(alert => alert.id !== alertId));
  };

  const getAlertIcon = (type: Alert['type']) => {
    switch (type) {
      case 'critical':
        return ExclamationTriangleIcon;
      case 'warning':
        return ClockIcon;
      case 'info':
        return BellIcon;
      default:
        return BellIcon;
    }
  };

  const getAlertColor = (type: Alert['type']) => {
    switch (type) {
      case 'critical':
        return 'text-red-600 bg-red-100 border-red-200';
      case 'warning':
        return 'text-yellow-600 bg-yellow-100 border-yellow-200';
      case 'info':
        return 'text-blue-600 bg-blue-100 border-blue-200';
      default:
        return 'text-gray-600 bg-gray-100 border-gray-200';
    }
  };

  const formatTimestamp = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));
    
    if (diffInMinutes < 60) {
      return `منذ ${diffInMinutes} دقيقة`;
    } else {
      const diffInHours = Math.floor(diffInMinutes / 60);
      return `منذ ${diffInHours} ساعة`;
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">التنبيهات</h3>
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="animate-pulse">
              <div className="flex items-start space-x-3 space-x-reverse p-3 border rounded-lg">
                <div className="w-8 h-8 bg-gray-200 rounded-lg"></div>
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

  const unacknowledgedAlerts = alerts.filter(alert => !alert.acknowledged);

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2 space-x-reverse">
          <h3 className="text-lg font-semibold text-gray-900">التنبيهات</h3>
          {unacknowledgedAlerts.length > 0 && (
            <span className="bg-red-100 text-red-800 text-xs font-medium px-2 py-1 rounded-full">
              {unacknowledgedAlerts.length}
            </span>
          )}
        </div>
        <button 
          onClick={loadAlerts}
          className="text-sm text-primary-600 hover:text-primary-700"
        >
          تحديث
        </button>
      </div>
      
      {alerts.length === 0 ? (
        <div className="text-center py-8">
          <HeartIcon className="w-12 h-12 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-500">لا توجد تنبيهات حالياً</p>
        </div>
      ) : (
        <div className="space-y-3">
          {alerts.map((alert) => {
            const Icon = getAlertIcon(alert.type);
            return (
              <div 
                key={alert.id}
                className={clsx(
                  'flex items-start space-x-3 space-x-reverse p-3 border rounded-lg transition-all',
                  getAlertColor(alert.type),
                  alert.acknowledged ? 'opacity-60' : 'opacity-100'
                )}
              >
                <div className="flex-shrink-0">
                  <Icon className="w-5 h-5" />
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <h4 className="text-sm font-medium">{alert.title}</h4>
                    <button
                      onClick={() => dismissAlert(alert.id)}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      <XMarkIcon className="w-4 h-4" />
                    </button>
                  </div>
                  
                  <p className="text-sm mt-1">{alert.message}</p>
                  
                  <div className="flex items-center justify-between mt-2">
                    <div className="flex items-center space-x-2 space-x-reverse">
                      <span className="text-xs font-medium">{alert.patientName}</span>
                      <span className="text-xs text-gray-500">
                        {formatTimestamp(alert.timestamp)}
                      </span>
                    </div>
                    
                    {!alert.acknowledged && (
                      <button
                        onClick={() => acknowledgeAlert(alert.id)}
                        className="text-xs bg-white bg-opacity-50 hover:bg-opacity-75 px-2 py-1 rounded transition-colors"
                      >
                        تأكيد
                      </button>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
      
      {alerts.length > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <button className="w-full text-center text-sm text-primary-600 hover:text-primary-700 font-medium">
            عرض جميع التنبيهات
          </button>
        </div>
      )}
    </div>
  );
}
