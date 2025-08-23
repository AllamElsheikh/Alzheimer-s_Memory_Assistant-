'use client';

import { useState, useEffect } from 'react';
import { 
  ChatBubbleLeftRightIcon,
  CameraIcon,
  BellIcon,
  ClipboardDocumentCheckIcon,
  ClockIcon
} from '@heroicons/react/24/outline';
import clsx from 'clsx';

interface Activity {
  id: string;
  type: 'conversation' | 'photo_analysis' | 'reminder' | 'assessment';
  patientName: string;
  description: string;
  timestamp: string;
  status: 'completed' | 'pending' | 'failed';
}

export default function RecentActivity() {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRecentActivity();
  }, []);

  const loadRecentActivity = async () => {
    try {
      // Simulate API call - replace with actual endpoint
      await new Promise(resolve => setTimeout(resolve, 600));
      
      setActivities([
        {
          id: '1',
          type: 'conversation',
          patientName: 'فاطمة أحمد',
          description: 'محادثة صوتية حول الذكريات العائلية',
          timestamp: '2024-01-15T10:30:00Z',
          status: 'completed'
        },
        {
          id: '2',
          type: 'photo_analysis',
          patientName: 'محمد علي',
          description: 'تحليل صورة عائلية قديمة',
          timestamp: '2024-01-15T09:45:00Z',
          status: 'completed'
        },
        {
          id: '3',
          type: 'reminder',
          patientName: 'عائشة محمود',
          description: 'تذكير بموعد الدواء',
          timestamp: '2024-01-15T09:00:00Z',
          status: 'pending'
        },
        {
          id: '4',
          type: 'assessment',
          patientName: 'أحمد حسن',
          description: 'اختبار الذاكرة قصيرة المدى',
          timestamp: '2024-01-15T08:30:00Z',
          status: 'completed'
        },
        {
          id: '5',
          type: 'conversation',
          patientName: 'فاطمة أحمد',
          description: 'محادثة حول الأنشطة اليومية',
          timestamp: '2024-01-15T08:00:00Z',
          status: 'failed'
        }
      ]);
    } catch (error) {
      console.error('Error loading recent activity:', error);
    } finally {
      setLoading(false);
    }
  };

  const getActivityIcon = (type: Activity['type']) => {
    switch (type) {
      case 'conversation':
        return ChatBubbleLeftRightIcon;
      case 'photo_analysis':
        return CameraIcon;
      case 'reminder':
        return BellIcon;
      case 'assessment':
        return ClipboardDocumentCheckIcon;
      default:
        return ClockIcon;
    }
  };

  const getActivityColor = (type: Activity['type']) => {
    switch (type) {
      case 'conversation':
        return 'text-blue-600 bg-blue-100';
      case 'photo_analysis':
        return 'text-purple-600 bg-purple-100';
      case 'reminder':
        return 'text-yellow-600 bg-yellow-100';
      case 'assessment':
        return 'text-green-600 bg-green-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusColor = (status: Activity['status']) => {
    switch (status) {
      case 'completed':
        return 'text-green-700 bg-green-50 border-green-200';
      case 'pending':
        return 'text-yellow-700 bg-yellow-50 border-yellow-200';
      case 'failed':
        return 'text-red-700 bg-red-50 border-red-200';
      default:
        return 'text-gray-700 bg-gray-50 border-gray-200';
    }
  };

  const formatTimestamp = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('ar-EG', { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: true 
    });
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">النشاط الأخير</h3>
        <div className="space-y-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="animate-pulse">
              <div className="flex items-start space-x-4 space-x-reverse">
                <div className="w-10 h-10 bg-gray-200 rounded-lg"></div>
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
        <h3 className="text-lg font-semibold text-gray-900">النشاط الأخير</h3>
        <button 
          onClick={loadRecentActivity}
          className="text-sm text-primary-600 hover:text-primary-700"
        >
          تحديث
        </button>
      </div>
      
      <div className="space-y-4">
        {activities.map((activity) => {
          const Icon = getActivityIcon(activity.type);
          return (
            <div 
              key={activity.id}
              className="flex items-start space-x-4 space-x-reverse p-3 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <div className={clsx(
                'p-2 rounded-lg',
                getActivityColor(activity.type)
              )}>
                <Icon className="w-5 h-5" />
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {activity.patientName}
                  </p>
                  <span className="text-xs text-gray-500">
                    {formatTimestamp(activity.timestamp)}
                  </span>
                </div>
                
                <p className="text-sm text-gray-600 mt-1">
                  {activity.description}
                </p>
                
                <div className="flex items-center justify-between mt-2">
                  <span className={clsx(
                    'inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border',
                    getStatusColor(activity.status)
                  )}>
                    {activity.status === 'completed' ? 'مكتمل' :
                     activity.status === 'pending' ? 'معلق' : 'فشل'}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
      
      <div className="mt-4 pt-4 border-t border-gray-200">
        <button className="w-full text-center text-sm text-primary-600 hover:text-primary-700 font-medium">
          عرض جميع الأنشطة
        </button>
      </div>
    </div>
  );
}
