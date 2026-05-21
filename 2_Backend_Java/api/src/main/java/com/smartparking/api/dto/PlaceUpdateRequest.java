package com.smartparking.api.dto;

/**
 * DTO pour les mises à jour de places depuis le script Python.
 */
public class PlaceUpdateRequest {
    private String numeroPlace;
    private boolean occupee;
    private Double confiance;

    public PlaceUpdateRequest() {}

    public String getNumeroPlace() { return numeroPlace; }
    public void setNumeroPlace(String numeroPlace) { this.numeroPlace = numeroPlace; }

    public boolean isOccupee() { return occupee; }
    public void setOccupee(boolean occupee) { this.occupee = occupee; }

    public Double getConfiance() { return confiance; }
    public void setConfiance(Double confiance) { this.confiance = confiance; }
}
