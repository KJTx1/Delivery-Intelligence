import { create } from 'zustand';

export interface Alert {
  id: string;
  severity: 'critical' | 'warning' | 'info';
  type: string;
  driver: {
    id: string;
    name: string;
  };
  route: string;
  timestamp: string;
  message: string;
  details: Record<string, unknown>;
}

interface AlertStore {
  alerts: Alert[];
  addAlert: (alert: Alert) => void;
  removeAlert: (alertId: string) => void;
  clearAlerts: () => void;
}

export const useAlertStore = create<AlertStore>((set) => ({
  alerts: [],

  addAlert: (alert) =>
    set((state) => ({
      alerts: [alert, ...state.alerts],
    })),

  removeAlert: (alertId) =>
    set((state) => ({
      alerts: state.alerts.filter((a) => a.id !== alertId),
    })),

  clearAlerts: () => set({ alerts: [] }),
}));

