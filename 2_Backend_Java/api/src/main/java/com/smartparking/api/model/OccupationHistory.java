package com.smartparking.api.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.time.Duration;

/**
 * Entité représentant un enregistrement d'historique d'occupation.
 *
 * Chaque fois qu'une voiture quitte une place, un enregistrement
 * est créé avec l'heure d'arrivée, de départ, et la durée calculée.
 */
@Entity
@Table(name = "occupation_history")
public class OccupationHistory {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "numero_place", nullable = false)
    private String numeroPlace;

    @Column(name = "heure_arrivee")
    private LocalDateTime heureArrivee;

    @Column(name = "heure_depart")
    private LocalDateTime heureDepart;

    @Column(name = "duree_minutes")
    private Long dureeMinutes;

    // ==========================================
    //           CONSTRUCTEURS
    // ==========================================

    public OccupationHistory() {}

    public OccupationHistory(String numeroPlace, LocalDateTime arrivee, LocalDateTime depart) {
        this.numeroPlace = numeroPlace;
        this.heureArrivee = arrivee;
        this.heureDepart = depart;
        if (arrivee != null && depart != null) {
            this.dureeMinutes = Duration.between(arrivee, depart).toMinutes();
        }
    }

    // ==========================================
    //           GETTERS ET SETTERS
    // ==========================================

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getNumeroPlace() { return numeroPlace; }
    public void setNumeroPlace(String numeroPlace) { this.numeroPlace = numeroPlace; }

    public LocalDateTime getHeureArrivee() { return heureArrivee; }
    public void setHeureArrivee(LocalDateTime heureArrivee) { this.heureArrivee = heureArrivee; }

    public LocalDateTime getHeureDepart() { return heureDepart; }
    public void setHeureDepart(LocalDateTime heureDepart) { this.heureDepart = heureDepart; }

    public Long getDureeMinutes() { return dureeMinutes; }
    public void setDureeMinutes(Long dureeMinutes) { this.dureeMinutes = dureeMinutes; }
}
