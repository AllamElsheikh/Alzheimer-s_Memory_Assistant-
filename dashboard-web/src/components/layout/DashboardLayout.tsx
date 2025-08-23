'use client';

import { useState } from 'react';
import { 
  HomeIcon,
  UserGroupIcon,
  ChartBarIcon,
  BellIcon,
  CogIcon,
  Bars3Icon,
  XMarkIcon
} from '@heroicons/react/24/outline';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import clsx from 'clsx';

const navigation = [
  { name: 'الرئيسية', href: '/', icon: HomeIcon },
  { name: 'المرضى', href: '/patients', icon: UserGroupIcon },
  { name: 'التقارير', href: '/reports', icon: ChartBarIcon },
  { name: 'التنبيهات', href: '/alerts', icon: BellIcon },
  { name: 'الإعدادات', href: '/settings', icon: CogIcon },
];

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const pathname = usePathname();

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        >
          <div className="absolute inset-0 bg-gray-600 opacity-75"></div>
        </div>
      )}

      {/* Sidebar */}
      <div className={clsx(
        'fixed inset-y-0 right-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0',
        sidebarOpen ? 'translate-x-0' : 'translate-x-full'
      )}>
        <div className="flex items-center justify-between h-16 px-6 bg-primary-600">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center">
                <span className="text-primary-600 font-bold text-lg">ف</span>
              </div>
            </div>
            <div className="mr-3">
              <h1 className="text-white font-bold text-lg">فاكر</h1>
              <p className="text-primary-100 text-xs">لوحة التحكم</p>
            </div>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className="lg:hidden text-white hover:text-primary-200"
          >
            <XMarkIcon className="w-6 h-6" />
          </button>
        </div>

        <nav className="mt-8 px-4">
          <ul className="space-y-2">
            {navigation.map((item) => {
              const isActive = pathname === item.href;
              return (
                <li key={item.name}>
                  <Link
                    href={item.href}
                    className={clsx(
                      'flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors',
                      isActive
                        ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                        : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                    )}
                    onClick={() => setSidebarOpen(false)}
                  >
                    <item.icon className={clsx(
                      'ml-3 h-5 w-5',
                      isActive ? 'text-primary-600' : 'text-gray-400'
                    )} />
                    {item.name}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* User info */}
        <div className="absolute bottom-0 w-full p-4 border-t border-gray-200">
          <div className="flex items-center">
            <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
              <span className="text-primary-600 font-medium text-sm">د</span>
            </div>
            <div className="mr-3">
              <p className="text-sm font-medium text-gray-900">د. أحمد محمد</p>
              <p className="text-xs text-gray-500">مقدم رعاية</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top bar */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="flex items-center justify-between px-6 py-4">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden text-gray-500 hover:text-gray-700"
            >
              <Bars3Icon className="w-6 h-6" />
            </button>
            
            <div className="flex items-center space-x-4 space-x-reverse">
              {/* Notifications */}
              <button className="relative p-2 text-gray-400 hover:text-gray-500">
                <BellIcon className="w-6 h-6" />
                <span className="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-400 ring-2 ring-white"></span>
              </button>
              
              {/* Status indicator */}
              <div className="flex items-center space-x-2 space-x-reverse">
                <div className="status-dot status-online"></div>
                <span className="text-sm text-gray-600">متصل</span>
              </div>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
