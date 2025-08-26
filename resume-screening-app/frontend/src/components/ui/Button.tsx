import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', children, ...props }, ref) => {
    return (
      <button
        className={twMerge(
          clsx(
            'inline-flex items-center justify-center rounded-lg font-semibold transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none',
            {
              'bg-purple-600 hover:bg-purple-700 text-white focus:ring-purple-500': variant === 'primary',
              'bg-gray-600 hover:bg-gray-700 text-white focus:ring-gray-500': variant === 'secondary',
              'border border-gray-300 bg-transparent hover:bg-gray-50 text-gray-700 focus:ring-gray-500': variant === 'outline',
              'bg-transparent hover:bg-gray-100 text-gray-700 focus:ring-gray-500': variant === 'ghost',
              'px-3 py-1.5 text-sm': size === 'sm',
              'px-4 py-2 text-base': size === 'md',
              'px-6 py-3 text-lg': size === 'lg',
            }
          ),
          className
        )}
        ref={ref}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';

export { Button };
