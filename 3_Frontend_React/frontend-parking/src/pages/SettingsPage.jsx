import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import {
  HiOutlineInformationCircle,
  HiOutlineGlobeAlt,
  HiOutlinePaintBrush,
  HiOutlineSun,
  HiOutlineMoon,
  HiOutlineBell,
  HiOutlineCpuChip,
} from 'react-icons/hi2';
import PageTransition from '../components/layout/PageTransition';
import './SettingsPage.css';

export default function SettingsPage() {
  const { user } = useAuth();
  const { theme, toggleTheme } = useTheme();

  const endpoints = [
    { method: 'GET', path: '/api/parking/places', desc: 'Places temps réel' },
    { method: 'POST', path: '/api/parking/update', desc: 'Mise à jour depuis IA' },
    { method: 'GET', path: '/api/stats/dashboard', desc: 'Statistiques dashboard' },
    { method: 'GET', path: '/api/stats/history', desc: 'Historique sessions' },
    { method: 'POST', path: '/api/auth/login', desc: 'Authentification JWT' },
  ];

  return (
    <PageTransition>
      <div className="settings-page">
        {/* Page Header */}
        <div className="page-header">
          <h2>Paramètres</h2>
          <p>Informations système et configuration de l'application</p>
        </div>

        <div className="settings-grid">
          {/* System Info Card */}
          <div className="settings-card">
            <div className="card-title">
              <HiOutlineInformationCircle className="card-title-icon" />
              Informations Système
            </div>
            <div className="info-grid">
              <div className="info-item">
                <span className="info-label">Version</span>
                <span className="info-value">2.0.0</span>
              </div>
              <div className="info-item">
                <span className="info-label">Utilisateur</span>
                <span className="info-value">{user?.username || '—'}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Rôle</span>
                <span className="info-value">
                  <span className={`role-badge ${user?.role === 'ROLE_ADMIN' ? 'admin' : 'user'}`}>
                    {user?.role === 'ROLE_ADMIN' ? 'Administrateur' : user?.role || '—'}
                  </span>
                </span>
              </div>
              <div className="info-item">
                <span className="info-label">Frontend</span>
                <span className="info-value">React 19 + Vite</span>
              </div>
              <div className="info-item">
                <span className="info-label">Backend</span>
                <span className="info-value">Spring Boot 3.2</span>
              </div>
              <div className="info-item">
                <span className="info-label">IA</span>
                <span className="info-value">YOLOv8 + FastAPI</span>
              </div>
            </div>
          </div>

          {/* Appearance Card */}
          <div className="settings-card">
            <div className="card-title">
              <HiOutlinePaintBrush className="card-title-icon" />
              Apparence
            </div>

            <div className="settings-options">
              <div className="settings-option">
                <div className="settings-option-info">
                  <div className="settings-option-icon">
                    {theme === 'dark' ? <HiOutlineMoon /> : <HiOutlineSun />}
                  </div>
                  <div>
                    <div className="settings-option-title">Mode sombre</div>
                    <div className="settings-option-desc">Basculer entre le thème clair et sombre</div>
                  </div>
                </div>
                <label className="toggle-switch">
                  <input type="checkbox" checked={theme === 'dark'} onChange={toggleTheme} />
                  <span className="toggle-slider" />
                </label>
              </div>

              <div className="settings-option">
                <div className="settings-option-info">
                  <div className="settings-option-icon">
                    <HiOutlineBell />
                  </div>
                  <div>
                    <div className="settings-option-title">Notifications</div>
                    <div className="settings-option-desc">Alertes sonores lors de changements</div>
                  </div>
                </div>
                <label className="toggle-switch">
                  <input type="checkbox" defaultChecked />
                  <span className="toggle-slider" />
                </label>
              </div>

              <div className="settings-option">
                <div className="settings-option-info">
                  <div className="settings-option-icon">
                    <HiOutlineCpuChip />
                  </div>
                  <div>
                    <div className="settings-option-title">Auto-refresh</div>
                    <div className="settings-option-desc">Mise à jour automatique des données</div>
                  </div>
                </div>
                <label className="toggle-switch">
                  <input type="checkbox" defaultChecked />
                  <span className="toggle-slider" />
                </label>
              </div>
            </div>

            {/* Theme Preview */}
            <div className="theme-preview">
              <div
                className={`theme-card ${theme === 'dark' ? 'selected' : ''}`}
                onClick={() => theme !== 'dark' && toggleTheme()}
              >
                <div className="theme-card-preview dark-preview">
                  <div className="preview-bar" />
                  <div className="preview-content">
                    <div className="preview-line" />
                    <div className="preview-line short" />
                  </div>
                </div>
                <span className="theme-card-label">Sombre</span>
              </div>
              <div
                className={`theme-card ${theme === 'light' ? 'selected' : ''}`}
                onClick={() => theme !== 'light' && toggleTheme()}
              >
                <div className="theme-card-preview light-preview">
                  <div className="preview-bar" />
                  <div className="preview-content">
                    <div className="preview-line" />
                    <div className="preview-line short" />
                  </div>
                </div>
                <span className="theme-card-label">Clair</span>
              </div>
            </div>
          </div>
        </div>

        {/* API Endpoints Card */}
        <div className="settings-card">
          <div className="card-title">
            <HiOutlineGlobeAlt className="card-title-icon" />
            API Endpoints
          </div>
          <div className="endpoint-list">
            {endpoints.map((ep, i) => (
              <div key={i} className="endpoint-item" style={{ animationDelay: `${i * 0.05}s` }}>
                <span className={`method-badge ${ep.method.toLowerCase()}`}>
                  {ep.method}
                </span>
                <span className="endpoint-path">{ep.path}</span>
                <span className="endpoint-desc">{ep.desc}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </PageTransition>
  );
}
