import { NavLink } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useTheme } from '../../context/ThemeContext';
import {
  HiOutlineHome,
  HiOutlineSignal,
  HiOutlineChartBarSquare,
  HiOutlineClock,
  HiOutlineCog6Tooth,
  HiOutlineChevronLeft,
  HiOutlineArrowRightOnRectangle,
} from 'react-icons/hi2';
import { RiParkingBoxLine } from 'react-icons/ri';
import './Sidebar.css';

const navItems = [
  { path: '/', label: 'Dashboard', icon: HiOutlineHome },
  { path: '/live', label: 'Temps Réel', icon: HiOutlineSignal },
  { path: '/analytics', label: 'Analytique', icon: HiOutlineChartBarSquare, adminOnly: true },
  { path: '/history', label: 'Historique', icon: HiOutlineClock, adminOnly: true },
  { path: '/settings', label: 'Paramètres', icon: HiOutlineCog6Tooth, adminOnly: true },
];

/**
 * Sidebar collapsible avec navigation, user card et toggle.
 */
export default function Sidebar({ collapsed, mobileOpen, onClose, onToggleCollapse }) {
  const { user, isAdmin, logout, isAuthenticated } = useAuth();
  const { theme } = useTheme();

  const filteredItems = navItems.filter(item => {
    if (item.adminOnly) return isAdmin;
    return true;
  });

  return (
    <aside className={`sidebar ${collapsed ? 'collapsed' : ''} ${mobileOpen ? 'mobile-open' : ''}`}>
      {/* ── Logo ── */}
      <div className="sidebar-logo">
        <div className="logo-icon">
          <RiParkingBoxLine />
        </div>
        <div className="logo-text">
          <span className="logo-title">SmartParking</span>
          <span className="logo-subtitle">AI Analysis</span>
        </div>
      </div>

      {/* ── Navigation ── */}
      <nav className="sidebar-nav">
        <div className="sidebar-section-label">Menu Principal</div>
        {filteredItems.map(item => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/'}
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
              title={collapsed ? item.label : undefined}
              onClick={() => {
                if (mobileOpen) onClose();
              }}
            >
              <Icon className="nav-icon" />
              <span className="nav-label">{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* ── Footer ── */}
      <div className="sidebar-footer">
        {isAuthenticated && (
          <>
            <div className="user-card">
              <div className="user-avatar">
                {user?.username?.charAt(0).toUpperCase() || 'U'}
              </div>
              <div className="user-info">
                <span className="user-name">{user?.username || 'Utilisateur'}</span>
                <span className="user-role">
                  {isAdmin ? 'Administrateur' : 'Utilisateur'}
                </span>
              </div>
            </div>

            <button
              className="logout-btn"
              onClick={logout}
              title="Déconnexion"
            >
              <HiOutlineArrowRightOnRectangle />
              <span>Déconnexion</span>
            </button>
          </>
        )}

        {!isAuthenticated && (
          <NavLink to="/login" className="nav-item" onClick={() => mobileOpen && onClose()}>
            <HiOutlineArrowRightOnRectangle className="nav-icon" />
            <span className="nav-label">Connexion Admin</span>
          </NavLink>
        )}

        <button
          className="collapse-toggle"
          onClick={onToggleCollapse}
          title={collapsed ? 'Agrandir le menu' : 'Réduire le menu'}
        >
          <HiOutlineChevronLeft className="toggle-icon" />
        </button>
      </div>
    </aside>
  );
}
