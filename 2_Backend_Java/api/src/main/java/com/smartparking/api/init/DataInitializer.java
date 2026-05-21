package com.smartparking.api.init;

import com.smartparking.api.model.AppUser;
import com.smartparking.api.model.PlaceParking;
import com.smartparking.api.repository.AppUserRepository;
import com.smartparking.api.repository.PlaceParkingRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

/**
 * Initialiseur de données au démarrage de l'application.
 * Crée le compte administrateur par défaut et les places de parking.
 */
@Component
public class DataInitializer implements CommandLineRunner {

    @Autowired
    private AppUserRepository userRepository;

    @Autowired
    private PlaceParkingRepository placeParkingRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) throws Exception {
        // --- Création du compte admin par défaut ---
        if (userRepository.count() == 0) {
            AppUser admin = new AppUser();
            admin.setUsername("admin");
            admin.setPassword(passwordEncoder.encode("admin123"));
            admin.setRole("ROLE_ADMIN");
            userRepository.save(admin);

            System.out.println("═══════════════════════════════════════════════");
            System.out.println("  ✅ COMPTE ADMIN CRÉÉ AVEC SUCCÈS !");
            System.out.println("  📧 Utilisateur : admin");
            System.out.println("  🔑 Mot de passe : admin123");
            System.out.println("═══════════════════════════════════════════════");
        }

        // --- Création des places de parking (38 places) ---
        if (placeParkingRepository.count() == 0) {
            String[][] placesConfig = {
                    // Zone A — Rangée du bas (P1 à P11)
                    {"P1", "A"}, {"P2", "A"}, {"P3", "A"}, {"P4", "A"}, {"P5", "A"},
                    {"P6", "A"}, {"P7", "A"}, {"P8", "A"}, {"P9", "A"}, {"P10", "A"},
                    {"P11", "A"},
                    // Zone B — Rangée du milieu (P12 à P22)
                    {"P12", "B"}, {"P13", "B"}, {"P14", "B"}, {"P15", "B"}, {"P16", "B"},
                    {"P17", "B"}, {"P18", "B"}, {"P19", "B"}, {"P20", "B"}, {"P21", "B"},
                    {"P22", "B"},
                    // Zone C — Rangée du haut (P23 à P35)
                    {"P23", "C"}, {"P24", "C"}, {"P25", "C"}, {"P26", "C"}, {"P27", "C"},
                    {"P28", "C"}, {"P29", "C"}, {"P30", "C"}, {"P31", "C"}, {"P32", "C"},
                    {"P33", "C"}, {"P34", "C"}, {"P35", "C"},
                    // Zone D — Rangée latérale (P36 à P38)
                    {"P36", "D"}, {"P37", "D"}, {"P38", "D"}
            };

            for (String[] config : placesConfig) {
                PlaceParking place = new PlaceParking(config[0], config[1]);
                placeParkingRepository.save(place);
            }

            System.out.println("  ✅ " + placesConfig.length + " PLACES DE PARKING CRÉÉES !");
            System.out.println("  📍 Zones : A (11), B (11), C (13), D (3)");
            System.out.println("═══════════════════════════════════════════════");
        }
    }
}
