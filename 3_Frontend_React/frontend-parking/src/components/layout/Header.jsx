import { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useTheme } from '../../context/ThemeContext';
import { useAuth } from '../../context/AuthContext';
import {
  HiOutlineBars3,
  HiOutlineBell,
  HiOutlineSun,
  HiOutlineMoon,
  HiOutlineMagnifyingGlass,
  HiOutlineXMark,
} from 'react-icons/hi2';
import './Header.css';

const pageTitles = {
  '/': 'Dashboard',
  '/live': 'Monitoring Temps Réel',
  '/analytics': 'Analytique & Statistiques',
  '/history': "Historique d'Occupation",
  '/settings': 'Paramètres',
  '/login': 'Connexion',
};

const pageDescriptions = {
  '/': 'Vue d\'ensemble en temps réel',
  '/live': 'Surveillance des places en direct',
  '/analytics': 'Analyse des performances',
  '/history': 'Historique complet des sessions',
  '/settings': 'Configuration du système',
  '/login': 'Accès administrateur',
};

const mockNotifications = [
  { id: 1, type: 'info', text: 'Système IA connecté et opérationnel', time: 'Il y a 2 min' },
  { id: 2, type: 'warning', text: 'Place P12 occupée depuis 4h', time: 'Il y a 15 min' },
  { id: 3, type: 'success', text: 'Analyse terminée — 98% précision', time: 'Il y a 1h' },
];

/**
 * Header sticky avec titre de page, recherche, statut, thème et notifications.
 */
export default function Header({ onToggleMobile, collapsed }) {
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();
  const { isAuthenticated } = useAuth();
  const [showNotifications, setShowNotifications] = useState(false);
  const [showSearch, setShowSearch] = useState(false);

  const title = pageTitles[location.pathname] || 'Smart Parking';
  const description = pageDescriptions[location.pathname] || '';

  // Current date
  const formattedDate = new Date().toLocaleDateString('fr-FR', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
  });

  // Clock
  const [currentTime, setCurrentTime] = useState(() =>
    new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
  );

  useState(() => {
    const timer = setInterval(() => {
      setCurrentTime(
        new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
      );
    }, 60000);
    return () => clearInterval(timer);
  });

  return (
    <header className="header">
      <div className="header-left">
        <button
          className="hamburger-btn"
          onClick={onToggleMobile}
          aria-label="Ouvrir le menu"
        >
          <HiOutlineBars3 />
        </button>
        <div className="header-titles">
          <h1 className="page-title">{title}</h1>
          <span className="breadcrumb">{description}</span>
        </div>
      </div>

      <div className="header-right">
        {/* Search Bar */}
        <div className={`header-search ${showSearch ? 'expanded' : ''}`}>
          <HiOutlineMagnifyingGlass className="search-trigger-icon" />
          <input
            type="text"
            className="header-search-input"
            placeholder="Rechercher..."
            onFocus={() => setShowSearch(true)}
            onBlur={() => setShowSearch(false)}
          />
        </div>

        <span className="header-date">
          {formattedDate} — {currentTime}
        </span>

        <div className="status-badge">
          <span className="status-dot" />
          <span className="status-text">Système Actif</span>
        </div>

        <button
          className="header-icon-btn theme-toggle"
          onClick={toggleTheme}
          aria-label="Changer le thème"
          title={theme === 'dark' ? 'Mode clair' : 'Mode sombre'}
        >
          {theme === 'dark' ? <HiOutlineSun /> : <HiOutlineMoon />}
        </button>

        {/* Notifications */}
        <div className="notification-wrapper">
          <button
            className="header-icon-btn notification-btn"
            aria-label="Notifications"
            title="Notifications"
            onClick={() => setShowNotifications(!showNotifications)}
          >
            <HiOutlineBell />
            <span className="notification-dot" />
          </button>

          {showNotifications && (
            <>
              <div className="notification-backdrop" onClick={() => setShowNotifications(false)} />
              <div className="notification-panel">
                <div className="notification-panel-header">
                  <span className="notification-panel-title">Notifications</span>
                  <button className="notification-panel-close" onClick={() => setShowNotifications(false)}>
                    <HiOutlineXMark />
                  </button>
                </div>
                <div className="notification-list">
                  {mockNotifications.map(n => (
                    <div key={n.id} className={`notification-item notification-item--${n.type}`}>
                      <div className="notification-item-dot" />
                      <div className="notification-item-body">
                        <span className="notification-item-text">{n.text}</span>
                        <span className="notification-item-time">{n.time}</span>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="notification-panel-footer">
                  <span>Tout marquer comme lu</span>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
