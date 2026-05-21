package com.smartparking.api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Point d'entrée principal de l'application Smart Parking API.
 *
 * Architecture :
 *   - config/      → Configuration (Security, CORS)
 *   - model/       → Entités JPA (PlaceParking, OccupationHistory, AppUser)
 *   - repository/  → Repositories Spring Data JPA
 *   - service/     → Couche service (logique métier)
 *   - controller/  → Contrôleurs REST
 *   - dto/         → Data Transfer Objects
 *   - security/    → JWT (JwtUtil, JwtRequestFilter)
 *   - init/        → Initialisation des données
 */
@SpringBootApplication
public class ApiApplication {

	public static void main(String[] args) {
		SpringApplication.run(ApiApplication.class, args);
		System.out.println("═══════════════════════════════════════════════");
		System.out.println("  🚗 Smart Parking API — Démarré avec succès !");
		System.out.println("  📡 API     : http://localhost:8080/api");
		System.out.println("  📖 Swagger : http://localhost:8080/swagger-ui.html");
		System.out.println("═══════════════════════════════════════════════");
	}
}
