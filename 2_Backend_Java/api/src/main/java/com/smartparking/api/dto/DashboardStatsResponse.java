package com.smartparking.api.dto;

import java.util.List;
import java.util.Map;

/**
 * DTO pour le résumé du dashboard principal.
 * Contient toutes les statistiques affichées en page d'accueil.
 */
public class DashboardStatsResponse {

    private long totalPlaces;
    private long placesOccupees;
    private long placesLibres;
    private double tauxOccupation;
    private Double dureeMoyenneMinutes;
    private long totalSessions;

    // Graphiques
    private List<Map<String, Object>> occupationParHeure;
    private List<Map<String, Object>> occupationParJour;
    private List<Map<String, Object>> rotationParPlace;
    private List<Map<String, Object>> activiteRecente;

    // ==========================================
    //           GETTERS ET SETTERS
    // ==========================================

    public long getTotalPlaces() { return totalPlaces; }
    public void setTotalPlaces(long totalPlaces) { this.totalPlaces = totalPlaces; }

    public long getPlacesOccupees() { return placesOccupees; }
    public void setPlacesOccupees(long placesOccupees) { this.placesOccupees = placesOccupees; }

    public long getPlacesLibres() { return placesLibres; }
    public void setPlacesLibres(long placesLibres) { this.placesLibres = placesLibres; }

    public double getTauxOccupation() { return tauxOccupation; }
    public void setTauxOccupation(double tauxOccupation) { this.tauxOccupation = tauxOccupation; }

    public Double getDureeMoyenneMinutes() { return dureeMoyenneMinutes; }
    public void setDureeMoyenneMinutes(Double dureeMoyenneMinutes) { this.dureeMoyenneMinutes = dureeMoyenneMinutes; }

    public long getTotalSessions() { return totalSessions; }
    public void setTotalSessions(long totalSessions) { this.totalSessions = totalSessions; }

    public List<Map<String, Object>> getOccupationParHeure() { return occupationParHeure; }
    public void setOccupationParHeure(List<Map<String, Object>> occupationParHeure) { this.occupationParHeure = occupationParHeure; }

    public List<Map<String, Object>> getOccupationParJour() { return occupationParJour; }
    public void setOccupationParJour(List<Map<String, Object>> occupationParJour) { this.occupationParJour = occupationParJour; }

    public List<Map<String, Object>> getRotationParPlace() { return rotationParPlace; }
    public void setRotationParPlace(List<Map<String, Object>> rotationParPlace) { this.rotationParPlace = rotationParPlace; }

    public List<Map<String, Object>> getActiviteRecente() { return activiteRecente; }
    public void setActiviteRecente(List<Map<String, Object>> activiteRecente) { this.activiteRecente = activiteRecente; }
}
