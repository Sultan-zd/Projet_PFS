import { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import './StatCard.css';

/**
 * Carte de statistique premium avec compteur animé.
 * Props: title, value, subtitle, icon, color ('blue'|'green'|'red'|'purple'|'amber'), delay, trend
 */
export default function StatCard({ title, value, subtitle, icon, color = 'blue', delay = 0, trend }) {
  const [displayValue, setDisplayValue] = useState(0);
  const prevValueRef = useRef(0);

  // Animated count-up for numeric values
  useEffect(() => {
    const numericValue = typeof value === 'string' ? parseInt(value) : value;
    if (isNaN(numericValue)) {
      setDisplayValue(value);
      return;
    }

    const from = prevValueRef.current;
    const to = numericValue;
    prevValueRef.current = to;
    const duration = 800;
    const start = performance.now();

    const animate = (now) => {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setDisplayValue(Math.round(from + (to - from) * eased));
      if (progress < 1) requestAnimationFrame(animate);
    };

    requestAnimationFrame(animate);
  }, [value]);

  const isPercentage = typeof value === 'string' && value.includes('%');
  const formattedValue = isPercentage ? `${displayValue}%` : displayValue;

  return (
    <motion.div
      className={`stat-card stat-card--${color}`}
      initial={{ opacity: 0, y: 24, scale: 0.96 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.5, delay, ease: [0.22, 1, 0.36, 1] }}
    >
      <div className="stat-header">
        <span className="stat-title">{title}</span>
        <div className="stat-icon">
          {icon}
        </div>
      </div>
      <div className="stat-value-row">
        <div className="stat-value">{formattedValue}</div>
        {trend && (
          <span className={`stat-trend ${trend > 0 ? 'up' : 'down'}`}>
            {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}%
          </span>
        )}
      </div>
      {subtitle && <div className="stat-subtitle">{subtitle}</div>}
      {/* Decorative shimmer line */}
      <div className="stat-shimmer" />
    </motion.div>
  );
}
