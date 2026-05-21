package com.smartparking.api.controller;

import com.smartparking.api.dto.DashboardStatsResponse;
import com.smartparking.api.model.OccupationHistory;
import com.smartparking.api.service.StatisticsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * Contrôleur de statistiques et d'analytique.
 * Fournit les données pour le Dashboard d'administration.
 * Tous les endpoints nécessitent le rôle ADMIN.
 */
@RestController
@RequestMapping("/api/stats")
public class StatisticsController {

    @Autowired
    private StatisticsService statisticsService;

    /**
     * GET /api/stats/dashboard
     * Retourne le résumé complet du Dashboard.
     */
    @GetMapping("/dashboard")
    public ResponseEntity<DashboardStatsResponse> getDashboard() {
        return ResponseEntity.ok(statisticsService.getDashboardStats());
    }

    /**
     * GET /api/stats/hourly
     * Retourne les statistiques d'occupation par heure de la journée.
     */
    @GetMapping("/hourly")
    public ResponseEntity<List<Map<String, Object>>> getHourlyStats() {
        return ResponseEntity.ok(statisticsService.getHourlyStats());
    }

    /**
     * GET /api/stats/daily
     * Retourne les statistiques d'occupation par jour de la semaine.
     */
    @GetMapping("/daily")
    public ResponseEntity<List<Map<String, Object>>> getDailyStats() {
        return ResponseEntity.ok(statisticsService.getDailyStats());
    }

    /**
     * GET /api/stats/rotation
     * Retourne le taux de rotation par place.
     */
    @GetMapping("/rotation")
    public ResponseEntity<List<Map<String, Object>>> getRotationStats() {
        return ResponseEntity.ok(statisticsService.getRotationStats());
    }

    /**
     * GET /api/stats/recent
     * Retourne les 20 dernières activités.
     */
    @GetMapping("/recent")
    public ResponseEntity<List<Map<String, Object>>> getRecentActivity() {
        return ResponseEntity.ok(statisticsService.getRecentActivity());
    }

    /**
     * GET /api/stats/history
     * Retourne l'historique complet d'occupation.
     */
    @GetMapping("/history")
    public ResponseEntity<List<OccupationHistory>> getFullHistory() {
        return ResponseEntity.ok(statisticsService.getFullHistory());
    }
}
