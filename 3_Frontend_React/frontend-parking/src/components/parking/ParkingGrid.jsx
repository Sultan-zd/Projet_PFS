import ParkingSpot from './ParkingSpot';
import './ParkingGrid.css';

/**
 * Grille de toutes les places de parking, groupées par zone.
 */
export default function ParkingGrid({ places, loading }) {
  /* ── Loading: 12 skeleton cards ─────────────────────────── */
  if (loading) {
    return (
      <div className="parking-grid">
        {[...Array(12)].map((_, i) => (
          <div key={i} className="skeleton-spot" />
        ))}
      </div>
    );
  }

  /* ── Empty state ────────────────────────────────────────── */
  if (!places || places.length === 0) {
    return (
      <div className="empty-state">
        <p>Aucune donnée disponible.</p>
        <span>Démarrez le backend pour voir les places.</span>
      </div>
    );
  }

  /* ── Group places by zone ───────────────────────────────── */
  const zones = {};
  places.forEach(place => {
    const zone = place.zone || 'Général';
    if (!zones[zone]) zones[zone] = [];
    zones[zone].push(place);
  });

  return (
    <div>
      {Object.entries(zones).map(([zoneName, zonePlaces]) => {
        const freeCount = zonePlaces.filter(p => !p.occupee).length;
        return (
          <div key={zoneName} className="zone-section">
            <div className="zone-header">
              <span className="zone-title">Zone {zoneName}</span>
              <span className="zone-count">
                {freeCount}/{zonePlaces.length} libres
              </span>
            </div>
            <div className="parking-grid">
              {zonePlaces.map((place, index) => (
                <ParkingSpot key={place.id} place={place} index={index} />
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}
