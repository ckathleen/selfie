import React from 'react';

import { Header } from '@/app/components/Header';
import { Sidebar } from '@/app/components/Sidebar';
import { Footer } from "@/app/components/Footer";

import './globals.css';

import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Home',
  description: 'Welcome to Next.js',
}

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html>
    <body>
    <div className="container mx-auto">
      <Header/>
      <div className="flex my-4">
        {/*<Sidebar/>*/}
        <main className="flex-1 p-4">
          {children}
        </main>
      </div>
      <Footer/>
    </div>
    </body>
    </html>
  );
}