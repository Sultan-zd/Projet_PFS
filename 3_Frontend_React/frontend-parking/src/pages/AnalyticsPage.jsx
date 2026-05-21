import { useState, useEffect } from 'react';
import api from '../api/axios';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  AreaChart, Area
} from 'recharts';
import {
  HiOutlineTicket, HiOutlineClock, HiOutlineChartBar, HiOutlineSquares2X2
} from 'react-icons/hi2';
import PageTransition from '../components/layout/PageTransition';
import './AnalyticsPage.css';

const tooltipStyle = {
  background: 'var(--bg-card-solid)',
  border: '1px solid var(--glass-border)',
  borderRadius: 8,
  color: 'var(--text-primary)'
};

export default function AnalyticsPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get('/stats/dashboard');
        setStats(res.data);
      } catch (err) {
        console.error('Erreur chargement stats:', err);
        setError('Impossible de charger les statistiques.');
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) {
    return (
      <PageTransition>
        <div className="loading-container">
          <div className="spinner spinner-lg" />
        </div>
      </PageTransition>
    );
  }

  if (error || !stats) {
    return (
      <PageTransition>
        <div className="analytics-page">
          <div className="error-card">
            {error || 'Impossible de charger les statistiques.'}
          </div>
        </div>
      </PageTransition>
    );
  }

  return (
    <PageTransition>
      <div className="analytics-page">
        {/* Page Header */}
        <div className="page-header">
          <h2>Analytique</h2>
          <p>Vue d'ensemble des performances du parking</p>
        </div>

        {/* Summary Bar */}
        <div className="summary-bar">
          <div className="summary-item">
            <div className="summary-icon blue">
              <HiOutlineTicket />
            </div>
            <div>
              <div className="summary-label">Total Sessions</div>
              <div className="summary-value">{stats.totalSessions}</div>
            </div>
          </div>
          <div className="summary-item">
            <div className="summary-icon amber">
              <HiOutlineClock />
            </div>
            <div>
              <div className="summary-label">Durée Moyenne</div>
              <div className="summary-value">{Math.round(stats.dureeMoyenneMinutes || 0)} min</div>
            </div>
          </div>
          <div className="summary-item">
            <div className="summary-icon green">
              <HiOutlineChartBar />
            </div>
            <div>
              <div className="summary-label">Taux d'Occupation</div>
              <div className="summary-value">{stats.tauxOccupation}%</div>
            </div>
          </div>
          <div className="summary-item">
            <div className="summary-icon purple">
              <HiOutlineSquares2X2 />
            </div>
            <div>
              <div className="summary-label">Places Totales</div>
              <div className="summary-value">{stats.totalPlaces}</div>
            </div>
          </div>
        </div>

        {/* Charts Grid */}
        <div className="charts-grid">
          {/* Area Chart — Affluence par Heure */}
          {stats.occupationParHeure && (
            <div className="chart-card">
              <div className="chart-header">
                <HiOutlineChartBar className="chart-icon" />
                <span className="chart-title">Affluence par Heure</span>
              </div>
              <ResponsiveContainer width="100%" height={280}>
                <AreaChart data={stats.occupationParHeure}>
                  <defs>
                    <linearGradient id="gradHour" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                  <XAxis dataKey="heure" tick={{ fill: '#64748b', fontSize: 10 }} />
                  <YAxis tick={{ fill: '#64748b', fontSize: 11 }} />
                  <Tooltip contentStyle={tooltipStyle} />
                  <Area type="monotone" dataKey="count" stroke="#6366f1" fill="url(#gradHour)" strokeWidth={2} name="Stationnements" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Bar Chart — Occupation par Jour */}
          {stats.occupationParJour && (
            <div className="chart-card">
              <div className="chart-header">
                <HiOutlineChartBar className="chart-icon" />
                <span className="chart-title">Occupation par Jour</span>
              </div>
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={stats.occupationParJour}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                  <XAxis dataKey="jour" tick={{ fill: '#64748b', fontSize: 11 }} />
                  <YAxis tick={{ fill: '#64748b', fontSize: 11 }} />
                  <Tooltip contentStyle={tooltipStyle} />
                  <Bar dataKey="count" fill="#3b82f6" radius={[6, 6, 0, 0]} name="Stationnements" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Horizontal Bar Chart — Rotation par Place */}
          {stats.rotationParPlace && stats.rotationParPlace.length > 0 && (
            <div className="chart-card full-width">
              <div className="chart-header">
                <HiOutlineChartBar className="chart-icon" />
                <span className="chart-title">Rotation par Place</span>
              </div>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={stats.rotationParPlace} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                  <XAxis type="number" tick={{ fill: '#64748b', fontSize: 11 }} />
                  <YAxis dataKey="place" type="category" tick={{ fill: '#64748b', fontSize: 10 }} width={50} />
                  <Tooltip contentStyle={tooltipStyle} />
                  <Bar dataKey="count" fill="#10b981" radius={[0, 4, 4, 0]} name="Utilisations" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>
      </div>
    </PageTransition>
  );
}
