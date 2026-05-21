package com.smartparking.api.controller;

import com.smartparking.api.dto.PlaceUpdateRequest;
import com.smartparking.api.model.PlaceParking;
import com.smartparking.api.service.ParkingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * Contrôleur principal de gestion du parking.
 * Fournit les endpoints pour :
 *   - Consulter l'état des places en temps réel
 *   - Recevoir les mises à jour depuis le module IA Python
 */
@RestController
@RequestMapping("/api/parking")
public class ParkingController {

    @Autowired
    private ParkingService parkingService;

    /**
     * GET /api/parking/places
     * Retourne la liste de toutes les places avec leur état actuel.
     * Accessible publiquement (temps réel).
     */
    @GetMapping("/places")
    public ResponseEntity<List<PlaceParking>> getPlaces() {
        return ResponseEntity.ok(parkingService.getAllPlaces());
    }

    /**
     * POST /api/parking/update
     * Reçoit une mise à jour d'état depuis le script Python.
     * Accessible publiquement (appelé par le module IA).
     */
    @PostMapping("/update")
    public ResponseEntity<?> updatePlace(@RequestBody PlaceUpdateRequest request) {
        String result = parkingService.updatePlace(request);

        if (result.contains("introuvable")) {
            return ResponseEntity.badRequest().body(Map.of("error", result));
        }

        return ResponseEntity.ok(Map.of("message", result));
    }

    /**
     * GET /api/parking/summary
     * Retourne un résumé rapide (total, occupées, libres).
     * Accessible publiquement.
     */
    @GetMapping("/summary")
    public ResponseEntity<?> getSummary() {
        List<PlaceParking> places = parkingService.getAllPlaces();
        long occupied = parkingService.getOccupiedCount();
        long available = parkingService.getAvailableCount();
        long total = places.size();

        return ResponseEntity.ok(Map.of(
                "total", total,
                "occupied", occupied,
                "available", available,
                "occupancyRate", total > 0 ? Math.round((double) occupied / total * 1000.0) / 10.0 : 0
        ));
    }
}
