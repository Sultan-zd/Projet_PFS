import { useState, useEffect, useRef } from 'react';
import './OccupancyGauge.css';

/**
 * Jauge circulaire SVG animée pour le taux d'occupation.
 * Change de couleur dynamiquement : vert → jaune → rouge.
 */
export default function OccupancyGauge({ percentage = 0, occupied = 0, total = 0 }) {
  const [animatedPercent, setAnimatedPercent] = useState(0);
  const rafRef = useRef(null);

  // Animated count-up
  useEffect(() => {
    const duration = 1200;
    const start = performance.now();
    const from = animatedPercent;
    const to = percentage;

    const animate = (now) => {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      // ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      setAnimatedPercent(Math.round(from + (to - from) * eased));
      if (progress < 1) {
        rafRef.current = requestAnimationFrame(animate);
      }
    };

    rafRef.current = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(rafRef.current);
  }, [percentage]);

  // SVG circle params
  const size = 180;
  const strokeWidth = 12;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (animatedPercent / 100) * circumference;

  // Dynamic color based on percentage
  const getColor = (pct) => {
    if (pct < 50) return 'var(--color-success)';
    if (pct < 80) return 'var(--color-warning)';
    return 'var(--color-danger)';
  };

  const getGlowColor = (pct) => {
    if (pct < 50) return 'rgba(var(--color-success-rgb), 0.3)';
    if (pct < 80) return 'rgba(251, 191, 36, 0.3)';
    return 'rgba(var(--color-danger-rgb), 0.3)';
  };

  const strokeColor = getColor(animatedPercent);

  return (
    <div className="gauge-container">
      <div className="gauge-ring">
        <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
          {/* Background track */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke="var(--border-subtle)"
            strokeWidth={strokeWidth}
          />
          {/* Animated progress arc */}
          <circle
            className="gauge-progress"
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke={strokeColor}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            style={{
              filter: `drop-shadow(0 0 8px ${getGlowColor(animatedPercent)})`,
            }}
          />
        </svg>
        {/* Center content */}
        <div className="gauge-center">
          <span className="gauge-value" style={{ color: strokeColor }}>
            {animatedPercent}
          </span>
          <span className="gauge-unit">%</span>
          <span className="gauge-label">Occupé</span>
        </div>
      </div>

      {/* Legend below */}
      <div className="gauge-legend">
        <div className="gauge-legend-item">
          <span className="gauge-legend-dot" style={{ background: 'var(--color-danger)' }} />
          <span className="gauge-legend-text">{occupied} occupées</span>
        </div>
        <div className="gauge-legend-item">
          <span className="gauge-legend-dot" style={{ background: 'var(--color-success)' }} />
          <span className="gauge-legend-text">{total - occupied} libres</span>
        </div>
      </div>
    </div>
  );
}
