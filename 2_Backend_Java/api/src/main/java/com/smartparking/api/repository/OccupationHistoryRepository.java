package com.smartparking.api.repository;

import com.smartparking.api.model.OccupationHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface OccupationHistoryRepository extends JpaRepository<OccupationHistory, Long> {

    List<OccupationHistory> findByNumeroPlace(String numeroPlace);

    List<OccupationHistory> findByHeureDepartBetween(LocalDateTime start, LocalDateTime end);

    @Query("SELECT AVG(h.dureeMinutes) FROM OccupationHistory h WHERE h.dureeMinutes IS NOT NULL")
    Double getAverageDuration();

    @Query("SELECT h.numeroPlace, COUNT(h) FROM OccupationHistory h GROUP BY h.numeroPlace ORDER BY COUNT(h) DESC")
    List<Object[]> countByPlace();

    @Query("SELECT HOUR(h.heureArrivee), COUNT(h) FROM OccupationHistory h WHERE h.heureArrivee IS NOT NULL GROUP BY HOUR(h.heureArrivee) ORDER BY HOUR(h.heureArrivee)")
    List<Object[]> countByHour();

    @Query("SELECT DAYOFWEEK(h.heureArrivee), COUNT(h) FROM OccupationHistory h WHERE h.heureArrivee IS NOT NULL GROUP BY DAYOFWEEK(h.heureArrivee) ORDER BY DAYOFWEEK(h.heureArrivee)")
    List<Object[]> countByDayOfWeek();

    @Query("SELECT COUNT(h) FROM OccupationHistory h")
    long getTotalSessions();

    @Query("SELECT h FROM OccupationHistory h ORDER BY h.heureDepart DESC")
    List<OccupationHistory> findRecentActivity();

    List<OccupationHistory> findTop20ByOrderByHeureDepartDesc();
}
