package com.smartparking.api.security;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import org.springframework.stereotype.Component;

import java.security.Key;
import java.util.Date;

/**
 * Utilitaire JWT pour la génération et la validation des tokens.
 */
@Component
public class JwtUtil {

    // Clé secrète générée cryptographiquement (HMAC-SHA256)
    private final Key key = Keys.secretKeyFor(SignatureAlgorithm.HS256);

    // Durée de validité du token : 10 heures
    private final long EXPIRATION_TIME = 1000 * 60 * 60 * 10;

    /**
     * Génère un token JWT contenant le nom d'utilisateur et son rôle.
     */
    public String generateToken(String username, String role) {
        return Jwts.builder()
                .setSubject(username)
                .claim("role", role)
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + EXPIRATION_TIME))
                .signWith(key)
                .compact();
    }

    /**
     * Extrait le nom d'utilisateur du token.
     */
    public String extractUsername(String token) {
        return Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token)
                .getBody()
                .getSubject();
    }

    /**
     * Vérifie si le token est valide et non altéré.
     */
    public boolean validateToken(String token) {
        try {
            Jwts.parserBuilder().setSigningKey(key).build().parseClaimsJws(token);
            return true;
        } catch (Exception e) {
            return false;
        }
    }
}
