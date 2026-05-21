import { useState, useEffect } from 'react';
import api from '../api/axios';
import ParkingGrid from '../components/parking/ParkingGrid';
import PageTransition from '../components/layout/PageTransition';
import {
  HiOutlineSquares2X2,
  HiOutlineCheckCircle,
  HiOutlineXCircle,
  HiOutlineCpuChip,
} from 'react-icons/hi2';
import './LiveMonitorPage.css';

export default function LiveMonitorPage() {
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [refreshRate, setRefreshRate] = useState(2000);

  useEffect(() => {
    const fetchPlaces = async () => {
      try {
        const res = await api.get('/parking/places');
        setPlaces(res.data);
        setLastUpdate(new Date());
      } catch (error) {
        console.error('Erreur chargement places:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPlaces();
    const interval = setInterval(fetchPlaces, refreshRate);
    return () => clearInterval(interval);
  }, [refreshRate]);

  const occupied = places.filter(p => p.occupee).length;
  const available = places.filter(p => !p.occupee).length;
  const total = places.length;
  const rate = total > 0 ? Math.round((occupied / total) * 100) : 0;

  return (
    <PageTransition>
      <div className="live-page">
        {/* Header */}
        <div className="live-header">
          <div className="live-header-left">
            <h2 className="live-title">Monitoring Temps Réel</h2>
            <div className="live-indicator">
              <span className="live-dot" />
              <span>EN DIRECT</span>
            </div>
          </div>
          <div className="live-controls">
            <div className="ia-status">
              <HiOutlineCpuChip className="ia-status-icon" />
              <span>IA Connectée</span>
            </div>
            {lastUpdate && (
              <span className="last-update">
                MAJ : {lastUpdate.toLocaleTimeString('fr-FR')}
              </span>
            )}
            <select
              className="refresh-select"
              value={refreshRate}
              onChange={(e) => setRefreshRate(Number(e.target.value))}
            >
              <option value={1000}>1s</option>
              <option value={2000}>2s</option>
              <option value={5000}>5s</option>
              <option value={10000}>10s</option>
            </select>
          </div>
        </div>

        {/* Occupation Progress Bar */}
        <div className="occupation-bar-card">
          <div className="occupation-bar-header">
            <span className="occupation-bar-label">Taux d'Occupation</span>
            <span className="occupation-bar-value">{rate}%</span>
          </div>
          <div className="occupation-bar-track">
            <div
              className={`occupation-bar-fill ${rate >= 80 ? 'danger' : rate >= 50 ? 'warning' : 'success'}`}
              style={{ width: `${rate}%` }}
            />
          </div>
          <div className="occupation-bar-labels">
            <span>0%</span>
            <span>50%</span>
            <span>100%</span>
          </div>
        </div>

        {/* Mini Stats */}
        <div className="mini-stats">
          <div className="mini-stat">
            <div className="mini-stat-icon blue">
              <HiOutlineSquares2X2 />
            </div>
            <div>
              <div className="mini-stat-value">{total}</div>
              <div className="mini-stat-label">Total Places</div>
            </div>
          </div>
          <div className="mini-stat">
            <div className="mini-stat-icon green">
              <HiOutlineCheckCircle />
            </div>
            <div>
              <div className="mini-stat-value">{available}</div>
              <div className="mini-stat-label">Places Libres</div>
            </div>
          </div>
          <div className="mini-stat">
            <div className="mini-stat-icon red">
              <HiOutlineXCircle />
            </div>
            <div>
              <div className="mini-stat-value">{occupied}</div>
              <div className="mini-stat-label">Places Occupées</div>
            </div>
          </div>
        </div>

        {/* Parking Grid */}
        <ParkingGrid places={places} loading={loading} />
      </div>
    </PageTransition>
  );
}
