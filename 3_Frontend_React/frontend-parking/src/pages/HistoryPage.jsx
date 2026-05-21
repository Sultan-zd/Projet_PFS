import { useState, useEffect } from 'react';
import api from '../api/axios';
import { HiOutlineMagnifyingGlass, HiOutlineCalendarDays, HiOutlineArrowDown, HiOutlineArrowUp } from 'react-icons/hi2';
import PageTransition from '../components/layout/PageTransition';
import './HistoryPage.css';

export default function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const perPage = 15;

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await api.get('/stats/history');
        // Trier par date de départ (plus récent en premier)
        const sorted = res.data.sort((a, b) => {
          if (!b.heureDepart || !a.heureDepart) return 0;
          return new Date(b.heureDepart) - new Date(a.heureDepart);
        });
        setHistory(sorted);
      } catch (error) {
        console.error('Erreur chargement historique:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  // Filtrage par numéro de place
  const filtered = history.filter(h =>
    h.numeroPlace?.toLowerCase().includes(search.toLowerCase())
  );

  // Pagination
  const totalPages = Math.ceil(filtered.length / perPage);
  const paginated = filtered.slice((page - 1) * perPage, page * perPage);

  const formatDate = (dateStr) => {
    if (!dateStr) return '—';
    return new Date(dateStr).toLocaleString('fr-FR', {
      day: '2-digit', month: 'short', year: 'numeric',
      hour: '2-digit', minute: '2-digit'
    });
  };

  return (
    <PageTransition>
      <div className="history-page">
        {/* Page Header */}
        <div className="page-header">
          <h2>Historique</h2>
          <p>Consultez l'historique complet des sessions de stationnement</p>
        </div>

        {/* Filters Bar */}
        <div className="filters-bar">
          <div className="search-bar">
            <HiOutlineMagnifyingGlass className="search-icon" />
            <input
              type="text"
              className="search-input"
              placeholder="Rechercher une place (ex: P5)..."
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(1); }}
            />
          </div>
          <div className="filter-actions">
            <span className="search-count">
              {filtered.length} résultat{filtered.length > 1 ? 's' : ''}
            </span>
          </div>
        </div>

        {/* Table */}
        <div className="table-card">
          {loading ? (
            <div className="loading-container">
              <div className="spinner spinner-lg" />
            </div>
          ) : (
            <table className="history-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Place</th>
                  <th>
                    <div className="th-with-icon">
                      <HiOutlineArrowDown className="th-icon success" />
                      Arrivée
                    </div>
                  </th>
                  <th>
                    <div className="th-with-icon">
                      <HiOutlineArrowUp className="th-icon danger" />
                      Départ
                    </div>
                  </th>
                  <th>Durée</th>
                </tr>
              </thead>
              <tbody>
                {paginated.length > 0 ? (
                  paginated.map((item, i) => (
                    <tr key={item.id || i} style={{ animationDelay: `${i * 0.03}s` }}>
                      <td className="row-number">{(page - 1) * perPage + i + 1}</td>
                      <td>
                        <span className="place-badge">{item.numeroPlace}</span>
                      </td>
                      <td>{formatDate(item.heureArrivee)}</td>
                      <td>{formatDate(item.heureDepart)}</td>
                      <td>
                        {item.dureeMinutes != null ? (
                          <span className={`duration-badge ${item.dureeMinutes >= 60 ? 'long' : 'short'}`}>
                            {item.dureeMinutes < 60
                              ? `${item.dureeMinutes} min`
                              : `${Math.floor(item.dureeMinutes / 60)}h ${item.dureeMinutes % 60}min`
                            }
                          </span>
                        ) : '—'}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="5" className="empty-row">Aucun résultat trouvé</td>
                  </tr>
                )}
              </tbody>
            </table>
          )}

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="pagination">
              <button
                className="pagination-btn"
                disabled={page <= 1}
                onClick={() => setPage(page - 1)}
              >
                ← Précédent
              </button>
              <div className="pagination-pages">
                {Array.from({ length: Math.min(totalPages, 5) }, (_, i) => {
                  const pageNum = i + 1;
                  return (
                    <button
                      key={pageNum}
                      className={`pagination-page ${page === pageNum ? 'active' : ''}`}
                      onClick={() => setPage(pageNum)}
                    >
                      {pageNum}
                    </button>
                  );
                })}
                {totalPages > 5 && <span className="pagination-ellipsis">...</span>}
              </div>
              <button
                className="pagination-btn"
                disabled={page >= totalPages}
                onClick={() => setPage(page + 1)}
              >
                Suivant →
              </button>
            </div>
          )}
        </div>
      </div>
    </PageTransition>
  );
}
