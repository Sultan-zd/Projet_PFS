import { createContext, useContext, useState, useCallback } from 'react';
import { HiOutlineCheckCircle, HiOutlineXCircle, HiOutlineInformationCircle, HiOutlineExclamationTriangle, HiOutlineXMark } from 'react-icons/hi2';

const ToastContext = createContext(null);

let toastId = 0;

const ICONS = {
  success: <HiOutlineCheckCircle />,
  error: <HiOutlineXCircle />,
  info: <HiOutlineInformationCircle />,
  warning: <HiOutlineExclamationTriangle />,
};

/**
 * Système de toast notifications global.
 * Usage: const { addToast } = useToast();
 *        addToast({ type: 'success', title: 'Succès', message: 'Action réussie' });
 */
export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const removeToast = useCallback((id) => {
    setToasts(prev => prev.map(t => t.id === id ? { ...t, exiting: true } : t));
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, 300);
  }, []);

  const addToast = useCallback(({ type = 'info', title, message, duration = 4000 }) => {
    const id = ++toastId;
    setToasts(prev => [...prev, { id, type, title, message, duration, exiting: false }]);

    if (duration > 0) {
      setTimeout(() => removeToast(id), duration);
    }

    return id;
  }, [removeToast]);

  return (
    <ToastContext.Provider value={{ addToast, removeToast }}>
      {children}
      <div className="toast-container">
        {toasts.map(toast => (
          <div
            key={toast.id}
            className={`toast toast--${toast.type} ${toast.exiting ? 'exiting' : ''}`}
          >
            <span className="toast-icon">{ICONS[toast.type]}</span>
            <div className="toast-body">
              {toast.title && <span className="toast-title">{toast.title}</span>}
              {toast.message && <span className="toast-message">{toast.message}</span>}
            </div>
            <button className="toast-close" onClick={() => removeToast(toast.id)}>
              <HiOutlineXMark />
            </button>
            {toast.duration > 0 && (
              <div
                className="toast-progress"
                style={{ animationDuration: `${toast.duration}ms` }}
              />
            )}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) throw new Error('useToast must be used within ToastProvider');
  return context;
}
