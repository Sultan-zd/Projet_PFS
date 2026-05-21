import { useState, useEffect } from 'react';
import api from '../api/axios';
import { useAuth } from '../context/AuthContext';
import PageTransition from '../components/layout/PageTransition';
import StatCard from '../components/dashboard/StatCard';
import OccupancyGauge from '../components/dashboard/OccupancyGauge';
import {
  HiOutlineSquares2X2,
  HiOutlineCheckCircle,
  HiOutlineXCircle,
  HiOutlineClock,
  HiOutlineChartBar,
  HiOutlineChartPie,
  HiOutlineArrowTrendingUp,
  HiOutlineSparkles,
  HiOutlineBolt,
} from 'react-icons/hi2';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, AreaChart, Area
} from 'recharts';
import './DashboardPage.css';

const tooltipStyle = {
  background: 'var(--bg-card-solid)',
  border: '1px solid var(--glass-border)',
  borderRadius: '12px',
  color: 'var(--text-primary)',
  padding: '12px 16px',
  boxShadow: '0 8px 32px rgba(0,0,0,0.2)',
};

export default function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const { isAdmin, user } = useAuth();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const placesRes = await api.get('/parking/places');
        setPlaces(placesRes.data);

        if (isAdmin) {
          const statsRes = await api.get('/stats/dashboard');
          setStats(statsRes.data);
        }
      } catch (error) {
        console.error('Erreur chargement dashboard:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, [isAdmin]);

  const occupied = places.filter(p => p.occupee).length;
  const available = places.filter(p => !p.occupee).length;
  const total = places.length;
  const rate = total > 0 ? Math.round((occupied / total) * 100) : 0;

  const pieData = [
    { name: 'Occupées', value: occupied },
    { name: 'Libres', value: available },
  ];

  const formatDuration = (minutes) => {
    if (minutes == null) return '—';
    if (minutes < 60) return `${minutes} min`;
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    return m > 0 ? `${h}h ${m}min` : `${h}h`;
  };

  // Greeting based on time
  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Bonjour';
    if (hour < 18) return 'Bon après-midi';
    return 'Bonsoir';
  };

  return (
    <PageTransition>
      <div className="dashboard-page">
        {/* ── Hero Banner ── */}
        <div className="hero-banner">
          <div className="hero-content">
            <div className="hero-text">
              <div className="hero-greeting">
                <HiOutlineSparkles className="hero-greeting-icon" />
                <span>{getGreeting()}{user?.username ? `, ${user.username}` : ''}</span>
              </div>
              <h2 className="hero-title">Tableau de Bord</h2>
              <p className="hero-description">
                Surveillance intelligente de votre parking en temps réel avec analyse IA
              </p>
              <div className="hero-tags">
                <span className="hero-tag">
                  <HiOutlineBolt /> IA Active
                </span>
                <span className="hero-tag">
                  <HiOutlineCheckCircle /> {available} places libres
                </span>
              </div>
            </div>
            <div className="hero-gauge">
              <OccupancyGauge percentage={rate} occupied={occupied} total={total} />
            </div>
          </div>
          {/* Decorative elements */}
          <div className="hero-orb hero-orb-1" />
          <div className="hero-orb hero-orb-2" />
          <div className="hero-orb hero-orb-3" />
        </div>

        {/* ── Stats Grid ── */}
        <div className="stats-grid">
          <StatCard
            title="Total Places"
            value={total}
            subtitle="Places configurées"
            icon={<HiOutlineSquares2X2 />}
            color="purple"
            delay={0}
          />
          <StatCard
            title="Libres"
            value={available}
            subtitle="Disponibles maintenant"
            icon={<HiOutlineCheckCircle />}
            color="green"
            delay={0.1}
          />
          <StatCard
            title="Occupées"
            value={occupied}
            subtitle="En cours d'utilisation"
            icon={<HiOutlineXCircle />}
            color="red"
            delay={0.2}
          />
          <StatCard
            title="Taux d'Occupation"
            value={`${rate}%`}
            subtitle={stats ? `Moy. ${Math.round(stats.dureeMoyenneMinutes || 0)} min` : 'Temps réel'}
            icon={<HiOutlineArrowTrendingUp />}
            color="amber"
            delay={0.3}
          />
        </div>

        {/* ── Charts Section ── */}
        <div className="section-title">
          <span className="section-icon"><HiOutlineChartBar /></span>
          Visualisations
        </div>

        <div className="charts-grid">
          {/* Pie Chart (Donut) */}
          <div className="chart-card">
            <div className="chart-header">
              <span className="chart-icon"><HiOutlineChartPie /></span>
              <span className="chart-title">Répartition Actuelle</span>
            </div>
            <div className="pie-chart-container">
              <ResponsiveContainer width="100%" height={240}>
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={90}
                    paddingAngle={5}
                    dataKey="value"
                    stroke="none"
                  >
                    <Cell fill="var(--color-danger)" />
                    <Cell fill="var(--color-success)" />
                  </Pie>
                  <Tooltip contentStyle={tooltipStyle} />
                </PieChart>
              </ResponsiveContainer>
              <div className="pie-legend">
                <div className="legend-item">
                  <span className="legend-dot" style={{ background: 'var(--color-success)' }} />
                  <span>Libres ({available})</span>
                </div>
                <div className="legend-item">
                  <span className="legend-dot" style={{ background: 'var(--color-danger)' }} />
                  <span>Occupées ({occupied})</span>
                </div>
              </div>
            </div>
          </div>

          {/* AreaChart — Affluence par Heure (Admin Only) */}
          {isAdmin && stats?.occupationParHeure && (
            <div className="chart-card">
              <div className="chart-header">
                <span className="chart-icon"><HiOutlineClock /></span>
                <span className="chart-title">Affluence par Heure</span>
              </div>
              <ResponsiveContainer width="100%" height={240}>
                <AreaChart data={stats.occupationParHeure}>
                  <defs>
                    <linearGradient id="colorHour" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="var(--accent-primary)" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="var(--accent-primary)" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" />
                  <XAxis dataKey="heure" tick={{ fill: 'var(--text-muted)', fontSize: 11 }} />
                  <YAxis tick={{ fill: 'var(--text-muted)', fontSize: 11 }} />
                  <Tooltip contentStyle={tooltipStyle} />
                  <Area type="monotone" dataKey="count" stroke="var(--accent-primary)" fill="url(#colorHour)" strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* BarChart — Rotation par Place (Admin Only, Full Width) */}
          {isAdmin && stats?.rotationParPlace && stats.rotationParPlace.length > 0 && (
            <div className="chart-card full-width">
              <div className="chart-header">
                <span className="chart-icon"><HiOutlineChartBar /></span>
                <span className="chart-title">Rotation par Place</span>
              </div>
              <ResponsiveContainer width="100%" height={240}>
                <BarChart data={stats.rotationParPlace}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" />
                  <XAxis dataKey="place" tick={{ fill: 'var(--text-muted)', fontSize: 10 }} />
                  <YAxis tick={{ fill: 'var(--text-muted)', fontSize: 11 }} />
                  <Tooltip contentStyle={tooltipStyle} />
                  <Bar dataKey="count" fill="var(--accent-secondary)" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>

        {/* ── Activity Section (Admin Only) ── */}
        {isAdmin && stats?.activiteRecente && stats.activiteRecente.length > 0 && (
          <div className="activity-section">
            <div className="section-title">
              <span className="section-icon"><HiOutlineClock /></span>
              Activité Récente
            </div>
            <div className="activity-table-wrap">
              <table className="activity-table">
                <thead>
                  <tr>
                    <th>Place</th>
                    <th>Arrivée</th>
                    <th>Départ</th>
                    <th>Durée</th>
                    <th>Statut</th>
                  </tr>
                </thead>
                <tbody>
                  {stats.activiteRecente.slice(0, 8).map((item, i) => (
                    <tr key={i} style={{ animationDelay: `${i * 0.05}s` }}>
                      <td><span className="place-badge">{item.place}</span></td>
                      <td>
                        <div className="cell-with-icon">
                          <span className="cell-dot cell-dot--success" />
                          {item.arrivee
                            ? new Date(item.arrivee).toLocaleString('fr-FR', {
                                hour: '2-digit', minute: '2-digit', day: '2-digit', month: 'short'
                              })
                            : '—'}
                        </div>
                      </td>
                      <td>
                        <div className="cell-with-icon">
                          <span className="cell-dot cell-dot--danger" />
                          {item.depart
                            ? new Date(item.depart).toLocaleString('fr-FR', {
                                hour: '2-digit', minute: '2-digit', day: '2-digit', month: 'short'
                              })
                            : '—'}
                        </div>
                      </td>
                      <td>
                        <span className={`duration-badge ${(item.duree || 0) >= 60 ? 'long' : 'short'}`}>
                          {formatDuration(item.duree)}
                        </span>
                      </td>
                      <td>
                        <span className={`status-pill ${item.depart ? 'completed' : 'active'}`}>
                          {item.depart ? 'Terminé' : 'En cours'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </PageTransition>
  );
}
