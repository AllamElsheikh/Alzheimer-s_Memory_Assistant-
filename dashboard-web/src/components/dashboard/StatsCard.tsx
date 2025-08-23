'use client';

import { ForwardRefExoticComponent, RefAttributes, SVGProps } from 'react';
import clsx from 'clsx';

interface StatsCardProps {
  title: string;
  value: number;
  icon: ForwardRefExoticComponent<Omit<SVGProps<SVGSVGElement>, "ref"> & {
    title?: string | undefined;
    titleId?: string | undefined;
  } & RefAttributes<SVGSVGElement>>;
  color: 'blue' | 'green' | 'yellow' | 'red';
  loading?: boolean;
  trend?: {
    value: number;
    isPositive: boolean;
  };
}

const colorClasses = {
  blue: {
    bg: 'bg-blue-50',
    icon: 'text-blue-600',
    text: 'text-blue-900'
  },
  green: {
    bg: 'bg-green-50',
    icon: 'text-green-600',
    text: 'text-green-900'
  },
  yellow: {
    bg: 'bg-yellow-50',
    icon: 'text-yellow-600',
    text: 'text-yellow-900'
  },
  red: {
    bg: 'bg-red-50',
    icon: 'text-red-600',
    text: 'text-red-900'
  }
};

export default function StatsCard({ 
  title, 
  value, 
  icon: Icon, 
  color, 
  loading = false,
  trend 
}: StatsCardProps) {
  const colors = colorClasses[color];

  return (
    <div className="bg-white rounded-lg shadow-sm p-6 card-hover">
      <div className="flex items-center">
        <div className={clsx('p-3 rounded-lg', colors.bg)}>
          {loading ? (
            <div className="spinner"></div>
          ) : (
            <Icon className={clsx('w-6 h-6', colors.icon)} />
          )}
        </div>
        <div className="mr-4 flex-1">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <div className="flex items-center mt-1">
            <p className={clsx('text-2xl font-bold arabic-numbers', colors.text)}>
              {loading ? '...' : value.toLocaleString('ar-EG')}
            </p>
            {trend && !loading && (
              <span className={clsx(
                'mr-2 text-sm font-medium',
                trend.isPositive ? 'text-green-600' : 'text-red-600'
              )}>
                {trend.isPositive ? '↗' : '↘'} {Math.abs(trend.value)}%
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
