package com.smartparking.api.service;

import com.smartparking.api.dto.PlaceUpdateRequest;
import com.smartparking.api.model.OccupationHistory;
import com.smartparking.api.model.PlaceParking;
import com.smartparking.api.repository.OccupationHistoryRepository;
import com.smartparking.api.repository.PlaceParkingRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

/**
 * Service métier pour la gestion des places de parking.
 * Contient toute la logique de mise à jour des états des places
 * et la création automatique de l'historique d'occupation.
 */
@Service
public class ParkingService {

    @Autowired
    private PlaceParkingRepository placeParkingRepository;

    @Autowired
    private OccupationHistoryRepository occupationHistoryRepository;

    /**
     * Récupère toutes les places triées par numéro.
     */
    public List<PlaceParking> getAllPlaces() {
        List<PlaceParking> places = placeParkingRepository.findAll();
        places.sort((a, b) -> {
            // Tri numérique naturel (P1, P2, ... P10, P11)
            String numA = a.getNumeroPlace().replaceAll("\\D", "");
            String numB = b.getNumeroPlace().replaceAll("\\D", "");
            try {
                return Integer.compare(Integer.parseInt(numA), Integer.parseInt(numB));
            } catch (NumberFormatException e) {
                return a.getNumeroPlace().compareTo(b.getNumeroPlace());
            }
        });
        return places;
    }

    /**
     * Met à jour l'état d'une place de parking.
     * Gère automatiquement :
     *   - CAS A : Arrivée d'une voiture (Libre → Occupée) → démarre le chrono
     *   - CAS B : Départ d'une voiture (Occupée → Libre) → crée l'historique
     */
    @Transactional
    public String updatePlace(PlaceUpdateRequest request) {
        PlaceParking place = placeParkingRepository.findByNumeroPlace(request.getNumeroPlace());

        if (place == null) {
            return "Place introuvable : " + request.getNumeroPlace();
        }

        boolean ancienEtat = place.isOccupee();
        boolean nouvelEtat = request.isOccupee();

        // CAS A : La voiture VIENT D'ARRIVER (Libre → Occupée)
        if (!ancienEtat && nouvelEtat) {
            place.setOccupee(true);
            place.setDebutOccupation(LocalDateTime.now());
            placeParkingRepository.save(place);
            return "Place " + request.getNumeroPlace() + " : voiture arrivée";
        }

        // CAS B : La voiture VIENT DE PARTIR (Occupée → Libre)
        if (ancienEtat && !nouvelEtat) {
            LocalDateTime heureArrivee = place.getDebutOccupation();
            LocalDateTime heureDepart = LocalDateTime.now();

            // Créer l'archive dans l'historique
            if (heureArrivee != null) {
                long duree = Duration.between(heureArrivee, heureDepart).toMinutes();

                OccupationHistory archive = new OccupationHistory();
                archive.setNumeroPlace(request.getNumeroPlace());
                archive.setHeureArrivee(heureArrivee);
                archive.setHeureDepart(heureDepart);
                archive.setDureeMinutes(duree);

                occupationHistoryRepository.save(archive);
            }

            // Remettre la place à zéro
            place.setOccupee(false);
            place.setDebutOccupation(null);
            placeParkingRepository.save(place);
            return "Place " + request.getNumeroPlace() + " : voiture partie";
        }

        return "Aucun changement pour " + request.getNumeroPlace();
    }

    /**
     * Récupère le nombre de places occupées.
     */
    public long getOccupiedCount() {
        return placeParkingRepository.countOccupied();
    }

    /**
     * Récupère le nombre de places libres.
     */
    public long getAvailableCount() {
        return placeParkingRepository.countAvailable();
    }
}
