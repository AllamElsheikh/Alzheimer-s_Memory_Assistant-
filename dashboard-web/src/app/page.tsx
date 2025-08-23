'use client';

import { useState, useEffect } from 'react';
import { 
  ChartBarIcon, 
  UserGroupIcon, 
  BellIcon, 
  HeartIcon,
  ClockIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import DashboardLayout from '@/components/layout/DashboardLayout';
import StatsCard from '@/components/dashboard/StatsCard';
import PatientList from '@/components/dashboard/PatientList';
import RecentActivity from '@/components/dashboard/RecentActivity';
import AlertsPanel from '@/components/dashboard/AlertsPanel';
import CognitiveChart from '@/components/dashboard/CognitiveChart';

interface DashboardStats {
  totalPatients: number;
  activeToday: number;
  pendingReminders: number;
  criticalAlerts: number;
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats>({
    totalPatients: 0,
    activeToday: 0,
    pendingReminders: 0,
    criticalAlerts: 0
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      // Connect to actual backend API
      const response = await fetch('http://localhost:8000/health');
      const healthData = await response.json();
      
      // Get patients data
      const patientsResponse = await fetch('http://localhost:8000/api/v1/patients/1');
      const patientData = await patientsResponse.json();
      
      // Get reminders data
      const remindersResponse = await fetch('http://localhost:8000/api/v1/reminders/due');
      const remindersData = await remindersResponse.json();
      
      // Get conversations for activity
      const conversationsResponse = await fetch('http://localhost:8000/api/v1/conversations');
      const conversationsData = await conversationsResponse.json();
      
      setStats({
        totalPatients: 1, // We have one test patient
        activeToday: conversationsData.length > 0 ? 1 : 0,
        pendingReminders: Array.isArray(remindersData) ? remindersData.length : 0,
        criticalAlerts: Array.isArray(remindersData) ? remindersData.filter(r => !r.is_completed).length : 0
      });
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      // Fallback to demo data if API fails
      setStats({
        totalPatients: 1,
        activeToday: 0,
        pendingReminders: 1,
        criticalAlerts: 1
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                لوحة التحكم الرئيسية
              </h1>
              <p className="text-gray-600 mt-1">
                مراقبة ومتابعة حالة المرضى في الوقت الفعلي
              </p>
            </div>
            <div className="flex items-center space-x-4 space-x-reverse">
              <div className="text-sm text-gray-500">
                آخر تحديث: {new Date().toLocaleTimeString('ar-EG')}
              </div>
              <button
                onClick={loadDashboardData}
                className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
              >
                تحديث
              </button>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatsCard
            title="إجمالي المرضى"
            value={stats.totalPatients}
            icon={UserGroupIcon}
            color="blue"
            loading={isLoading}
          />
          <StatsCard
            title="نشط اليوم"
            value={stats.activeToday}
            icon={HeartIcon}
            color="green"
            loading={isLoading}
          />
          <StatsCard
            title="تذكيرات معلقة"
            value={stats.pendingReminders}
            icon={ClockIcon}
            color="yellow"
            loading={isLoading}
          />
          <StatsCard
            title="تنبيهات حرجة"
            value={stats.criticalAlerts}
            icon={ExclamationTriangleIcon}
            color="red"
            loading={isLoading}
          />
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Charts and Analytics */}
          <div className="lg:col-span-2 space-y-6">
            <CognitiveChart />
            <RecentActivity />
          </div>

          {/* Right Column - Patients and Alerts */}
          <div className="space-y-6">
            <AlertsPanel />
            <PatientList />
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
