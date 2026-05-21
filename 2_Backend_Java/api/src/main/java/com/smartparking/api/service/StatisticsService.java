package com.smartparking.api.service;

import com.smartparking.api.dto.DashboardStatsResponse;
import com.smartparking.api.model.OccupationHistory;
import com.smartparking.api.repository.OccupationHistoryRepository;
import com.smartparking.api.repository.PlaceParkingRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;

/**
 * Service de statistiques et d'analytique.
 * Calcule toutes les métriques pour le Dashboard d'administration.
 */
@Service
public class StatisticsService {

    @Autowired
    private PlaceParkingRepository placeParkingRepository;

    @Autowired
    private OccupationHistoryRepository occupationHistoryRepository;

    /**
     * Construit le résumé complet du Dashboard.
     */
    public DashboardStatsResponse getDashboardStats() {
        DashboardStatsResponse stats = new DashboardStatsResponse();

        // --- Métriques principales ---
        long total = placeParkingRepository.count();
        long occupied = placeParkingRepository.countOccupied();
        long available = placeParkingRepository.countAvailable();

        stats.setTotalPlaces(total);
        stats.setPlacesOccupees(occupied);
        stats.setPlacesLibres(available);
        stats.setTauxOccupation(total > 0 ? Math.round((double) occupied / total * 1000.0) / 10.0 : 0);
        stats.setDureeMoyenneMinutes(occupationHistoryRepository.getAverageDuration());
        stats.setTotalSessions(occupationHistoryRepository.getTotalSessions());

        // --- Graphique : Occupation par heure ---
        stats.setOccupationParHeure(getHourlyStats());

        // --- Graphique : Occupation par jour ---
        stats.setOccupationParJour(getDailyStats());

        // --- Graphique : Rotation par place ---
        stats.setRotationParPlace(getRotationStats());

        // --- Activité récente ---
        stats.setActiviteRecente(getRecentActivity());

        return stats;
    }

    /**
     * Statistiques horaires (nombre de stationnements par heure de la journée).
     */
    public List<Map<String, Object>> getHourlyStats() {
        List<Object[]> rawData = occupationHistoryRepository.countByHour();
        String[] heures = {"00h", "01h", "02h", "03h", "04h", "05h", "06h", "07h",
                "08h", "09h", "10h", "11h", "12h", "13h", "14h", "15h",
                "16h", "17h", "18h", "19h", "20h", "21h", "22h", "23h"};

        // Initialiser toutes les heures à 0
        Map<Integer, Long> hourMap = new LinkedHashMap<>();
        for (int i = 0; i < 24; i++) hourMap.put(i, 0L);

        // Remplir avec les vraies données
        for (Object[] row : rawData) {
            int hour = ((Number) row[0]).intValue();
            long count = ((Number) row[1]).longValue();
            hourMap.put(hour, count);
        }

        List<Map<String, Object>> result = new ArrayList<>();
        for (Map.Entry<Integer, Long> entry : hourMap.entrySet()) {
            Map<String, Object> item = new LinkedHashMap<>();
            item.put("heure", heures[entry.getKey()]);
            item.put("count", entry.getValue());
            result.add(item);
        }

        return result;
    }

    /**
     * Statistiques par jour de la semaine.
     */
    public List<Map<String, Object>> getDailyStats() {
        List<Object[]> rawData = occupationHistoryRepository.countByDayOfWeek();
        String[] jours = {"", "Dimanche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"};

        // Initialiser tous les jours à 0
        Map<Integer, Long> dayMap = new LinkedHashMap<>();
        for (int i = 1; i <= 7; i++) dayMap.put(i, 0L);

        for (Object[] row : rawData) {
            int day = ((Number) row[0]).intValue();
            long count = ((Number) row[1]).longValue();
            if (day >= 1 && day <= 7) dayMap.put(day, count);
        }

        List<Map<String, Object>> result = new ArrayList<>();
        for (Map.Entry<Integer, Long> entry : dayMap.entrySet()) {
            Map<String, Object> item = new LinkedHashMap<>();
            item.put("jour", jours[entry.getKey()]);
            item.put("count", entry.getValue());
            result.add(item);
        }

        return result;
    }

    /**
     * Taux de rotation par place (nombre de stationnements).
     */
    public List<Map<String, Object>> getRotationStats() {
        List<Object[]> rawData = occupationHistoryRepository.countByPlace();
        List<Map<String, Object>> result = new ArrayList<>();

        for (Object[] row : rawData) {
            Map<String, Object> item = new LinkedHashMap<>();
            item.put("place", (String) row[0]);
            item.put("count", ((Number) row[1]).longValue());
            result.add(item);
        }

        return result;
    }

    /**
     * 20 dernières activités (arrivées/départs).
     */
    public List<Map<String, Object>> getRecentActivity() {
        List<OccupationHistory> recent = occupationHistoryRepository.findTop20ByOrderByHeureDepartDesc();
        List<Map<String, Object>> result = new ArrayList<>();

        for (OccupationHistory h : recent) {
            Map<String, Object> item = new LinkedHashMap<>();
            item.put("id", h.getId());
            item.put("place", h.getNumeroPlace());
            item.put("arrivee", h.getHeureArrivee() != null ? h.getHeureArrivee().toString() : null);
            item.put("depart", h.getHeureDepart() != null ? h.getHeureDepart().toString() : null);
            item.put("duree", h.getDureeMinutes());
            result.add(item);
        }

        return result;
    }

    /**
     * Historique complet.
     */
    public List<OccupationHistory> getFullHistory() {
        return occupationHistoryRepository.findAll();
    }
}
