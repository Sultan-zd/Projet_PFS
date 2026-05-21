import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { motion } from 'framer-motion';
import { RiParkingBoxLine } from 'react-icons/ri';
import {
  HiOutlineUser,
  HiOutlineLockClosed,
  HiOutlineEye,
  HiOutlineEyeSlash,
  HiOutlineCpuChip,
  HiOutlineSignal,
  HiOutlineChartBar,
  HiOutlineShieldCheck,
} from 'react-icons/hi2';
import './LoginPage.css';

const cardVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: [0.22, 1, 0.36, 1], staggerChildren: 0.08 },
  },
};

const childVariants = {
  hidden: { opacity: 0, y: 14 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4, ease: [0.22, 1, 0.36, 1] } },
};

const features = [
  { icon: <HiOutlineCpuChip />, title: 'IA YOLOv8', desc: 'Détection en temps réel des véhicules' },
  { icon: <HiOutlineSignal />, title: 'Temps Réel', desc: 'Mise à jour automatique des places' },
  { icon: <HiOutlineChartBar />, title: 'Analytique', desc: 'Statistiques et rapports détaillés' },
  { icon: <HiOutlineShieldCheck />, title: 'Sécurisé', desc: 'Authentification JWT et chiffrement' },
];

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8080/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        login(data.token, data.role, data.username || username);
        navigate('/');
      } else {
        setError('Identifiant ou mot de passe incorrect.');
      }
    } catch (err) {
      setError('Serveur injoignable. Vérifiez votre connexion.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      {/* ── Left Panel — Branding ── */}
      <div className="login-branding">
        <div className="branding-content">
          <motion.div
            className="branding-logo"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          >
            <div className="branding-logo-icon">
              <RiParkingBoxLine />
            </div>
            <h1 className="branding-title">Smart Parking</h1>
            <p className="branding-subtitle">Système de Gestion Intelligent</p>
          </motion.div>

          <motion.div
            className="branding-features"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.6 }}
          >
            {features.map((f, i) => (
              <motion.div
                key={i}
                className="branding-feature"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + i * 0.1, duration: 0.5 }}
              >
                <div className="branding-feature-icon">{f.icon}</div>
                <div>
                  <div className="branding-feature-title">{f.title}</div>
                  <div className="branding-feature-desc">{f.desc}</div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>

        {/* Decorative elements */}
        <div className="branding-orb branding-orb-1" />
        <div className="branding-orb branding-orb-2" />
        <div className="branding-orb branding-orb-3" />
        <div className="branding-grid-overlay" />
      </div>

      {/* ── Right Panel — Form ── */}
      <div className="login-form-panel">
        <motion.div
          className="login-card"
          variants={cardVariants}
          initial="hidden"
          animate="visible"
        >
          {/* Mobile Logo */}
          <motion.div className="login-logo-mobile" variants={childVariants}>
            <div className="login-logo-icon">
              <RiParkingBoxLine />
            </div>
          </motion.div>

          <motion.div className="login-header" variants={childVariants}>
            <h2 className="login-title">Bienvenue</h2>
            <p className="login-subtitle">Connectez-vous à votre espace administrateur</p>
          </motion.div>

          {/* Form */}
          <motion.form
            className="login-form"
            onSubmit={handleSubmit}
            variants={childVariants}
          >
            <div className="form-group">
              <label className="form-label" htmlFor="login-username">
                Identifiant
              </label>
              <div className="input-wrapper">
                <input
                  id="login-username"
                  className="form-input"
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                  placeholder="admin"
                  autoComplete="username"
                />
                <HiOutlineUser className="input-icon" />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="login-password">
                Mot de passe
              </label>
              <div className="input-wrapper">
                <input
                  id="login-password"
                  className="form-input"
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  placeholder="••••••••"
                  autoComplete="current-password"
                />
                <HiOutlineLockClosed className="input-icon" />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword(!showPassword)}
                  tabIndex={-1}
                >
                  {showPassword ? <HiOutlineEyeSlash /> : <HiOutlineEye />}
                </button>
              </div>
            </div>

            {error && (
              <motion.div
                className="login-error"
                initial={{ opacity: 0, y: -6 }}
                animate={{ opacity: 1, y: 0 }}
              >
                {error}
              </motion.div>
            )}

            <button type="submit" className="login-btn" disabled={loading}>
              {loading ? (
                <>
                  <span className="btn-spinner" />
                  Vérification…
                </>
              ) : (
                'Se connecter'
              )}
            </button>
          </motion.form>

          {/* Feature tags */}
          <motion.div className="login-features" variants={childVariants}>
            <span className="feature-tag">🤖 IA YOLOv8</span>
            <span className="feature-tag">⚡ Temps Réel</span>
            <span className="feature-tag">📊 Analytique</span>
          </motion.div>

          {/* Credential hint */}
          <motion.p className="login-hint" variants={childVariants}>
            Identifiants par défaut : <code>admin / admin123</code>
          </motion.p>
        </motion.div>
      </div>
    </div>
  );
}
