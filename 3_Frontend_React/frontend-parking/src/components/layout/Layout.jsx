import { useState, useCallback } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';
import PageTransition from './PageTransition';
import './Layout.css';

/**
 * Layout principal avec sidebar collapsible et header.
 * Gère l'état collapsed (persisté dans localStorage) et l'ouverture mobile.
 */
export default function Layout() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(() => {
    const stored = localStorage.getItem('sp-sidebar-collapsed');
    return stored === 'true';
  });

  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  const handleToggleCollapse = useCallback(() => {
    setSidebarCollapsed(prev => {
      const next = !prev;
      localStorage.setItem('sp-sidebar-collapsed', String(next));
      return next;
    });
  }, []);

  return (
    <div className="app-layout">
      <Sidebar
        collapsed={sidebarCollapsed}
        mobileOpen={mobileSidebarOpen}
        onClose={() => setMobileSidebarOpen(false)}
        onToggleCollapse={handleToggleCollapse}
      />

      <div
        className={`sidebar-overlay ${mobileSidebarOpen ? 'active' : ''}`}
        onClick={() => setMobileSidebarOpen(false)}
      />

      <div className={`main-wrapper ${sidebarCollapsed ? 'collapsed' : 'expanded'}`}>
        <Header
          onToggleMobile={() => setMobileSidebarOpen(prev => !prev)}
          collapsed={sidebarCollapsed}
        />
        <main className="main-content">
          <PageTransition>
            <Outlet />
          </PageTransition>
        </main>
      </div>
    </div>
  );
}
