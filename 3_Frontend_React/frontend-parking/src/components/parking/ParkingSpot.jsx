import './ParkingSpot.css';
import { HiOutlineClock } from 'react-icons/hi2';

/**
 * Place de parking individuelle avec SVG car icon et effets premium.
 */
export default function ParkingSpot({ place, index }) {
  const isAvailable = !place.occupee;

  /* Calcul du temps écoulé depuis l'occupation */
  const getTimeSince = (dateStr) => {
    if (!dateStr) return null;
    const diff = Date.now() - new Date(dateStr).getTime();
    const minutes = Math.floor(diff / 60000);
    if (minutes < 1) return "< 1 min";
    if (minutes < 60) return `${minutes} min`;
    const hours = Math.floor(minutes / 60);
    const remainMin = minutes % 60;
    return `${hours}h${remainMin > 0 ? remainMin.toString().padStart(2, '0') : ''}`;
  };

  return (
    <div
      className={`parking-spot ${isAvailable ? 'available' : 'occupied'}`}
      style={{ animationDelay: `${index * 0.03}s` }}
    >
      {/* Place number */}
      <span className="spot-number">P{place.numero || place.id}</span>

      {/* Status with colored dot */}
      <div className="spot-status">
        <span className="spot-status-dot" />
        <span>{isAvailable ? 'Libre' : 'Occupée'}</span>
      </div>

      {/* Car icon for occupied spots */}
      {!isAvailable && (
        <div className="spot-car">
          <svg width="36" height="20" viewBox="0 0 36 20" fill="none" className="car-svg">
            <path d="M5 13h26c1.1 0 2-.9 2-2V8c0-1.1-.6-2.1-1.5-2.7L28 3.3c-.6-.4-1.2-.8-1.9-1l-2.3-.7c-.5-.2-1-.3-1.6-.3H13.8c-.6 0-1.1.1-1.6.3l-2.3.7c-.7.2-1.3.6-1.9 1L4.5 5.3C3.6 5.9 3 6.9 3 8v3c0 1.1.9 2 2 2z" fill="currentColor" opacity="0.9"/>
            <circle cx="9" cy="15" r="3" fill="currentColor" opacity="0.7"/>
            <circle cx="27" cy="15" r="3" fill="currentColor" opacity="0.7"/>
            <circle cx="9" cy="15" r="1.5" fill="var(--bg-card-solid)"/>
            <circle cx="27" cy="15" r="1.5" fill="var(--bg-card-solid)"/>
            <rect x="7" y="6" width="5" height="3" rx="1" fill="var(--bg-card-solid)" opacity="0.4"/>
            <rect x="24" y="6" width="5" height="3" rx="1" fill="var(--bg-card-solid)" opacity="0.4"/>
          </svg>
        </div>
      )}

      {/* Available check icon */}
      {isAvailable && (
        <div className="spot-available-icon">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
            <circle cx="14" cy="14" r="12" stroke="currentColor" strokeWidth="2" opacity="0.3"/>
            <path d="M9 14.5l3.5 3.5L19 11" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </div>
      )}

      {/* Time since occupation */}
      {!isAvailable && place.heureOccupation && (
        <span className="spot-time">
          <HiOutlineClock className="spot-time-icon" />
          {getTimeSince(place.heureOccupation)}
        </span>
      )}
    </div>
  );
}
