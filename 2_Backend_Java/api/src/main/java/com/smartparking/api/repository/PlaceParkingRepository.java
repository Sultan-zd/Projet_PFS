package com.smartparking.api.repository;

import com.smartparking.api.model.PlaceParking;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface PlaceParkingRepository extends JpaRepository<PlaceParking, Long> {

    PlaceParking findByNumeroPlace(String numeroPlace);

    @Query("SELECT COUNT(p) FROM PlaceParking p WHERE p.occupee = true")
    long countOccupied();

    @Query("SELECT COUNT(p) FROM PlaceParking p WHERE p.occupee = false")
    long countAvailable();

    List<PlaceParking> findByZone(String zone);

    List<PlaceParking> findByOccupee(boolean occupee);
}
