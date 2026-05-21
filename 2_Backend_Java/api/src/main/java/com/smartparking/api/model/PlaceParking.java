package com.smartparking.api.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * Entité représentant une place de parking dans le système.
 *
 * Chaque place possède un identifiant unique (ex: P1, P2...),
 * un état d'occupation, et un horodatage de début d'occupation.
 */
@Entity
@Table(name = "places_parking")
public class PlaceParking {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "numero_place", unique = true, nullable = false)
    private String numeroPlace;

    @Column(name = "occupee")
    private boolean occupee;

    @Column(name = "debut_occupation")
    private LocalDateTime debutOccupation;

    @Column(name = "zone")
    private String zone;  // Zone du parking (ex: "A", "B", "C")

    // ==========================================
    //           CONSTRUCTEURS
    // ==========================================

    public PlaceParking() {}

    public PlaceParking(String numeroPlace) {
        this.numeroPlace = numeroPlace;
        this.occupee = false;
    }

    public PlaceParking(String numeroPlace, String zone) {
        this.numeroPlace = numeroPlace;
        this.zone = zone;
        this.occupee = false;
    }

    // ==========================================
    //           GETTERS ET SETTERS
    // ==========================================

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getNumeroPlace() { return numeroPlace; }
    public void setNumeroPlace(String numeroPlace) { this.numeroPlace = numeroPlace; }

    public boolean isOccupee() { return occupee; }
    public void setOccupee(boolean occupee) { this.occupee = occupee; }

    public LocalDateTime getDebutOccupation() { return debutOccupation; }
    public void setDebutOccupation(LocalDateTime debutOccupation) { this.debutOccupation = debutOccupation; }

    public String getZone() { return zone; }
    public void setZone(String zone) { this.zone = zone; }
}
