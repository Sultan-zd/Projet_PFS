package com.smartparking.api.service;

import com.smartparking.api.dto.LoginRequest;
import com.smartparking.api.dto.LoginResponse;
import com.smartparking.api.model.AppUser;
import com.smartparking.api.repository.AppUserRepository;
import com.smartparking.api.security.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Optional;

/**
 * Service d'authentification.
 * Gère la vérification des identifiants et la génération des tokens JWT.
 */
@Service
public class AuthService {

    @Autowired
    private AppUserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private JwtUtil jwtUtil;

    /**
     * Authentifie un utilisateur et retourne un token JWT.
     *
     * @return LoginResponse si succès, null si échec
     */
    public LoginResponse authenticate(LoginRequest request) {
        Optional<AppUser> userOptional = userRepository.findByUsername(request.getUsername());

        if (userOptional.isPresent()) {
            AppUser user = userOptional.get();

            if (passwordEncoder.matches(request.getPassword(), user.getPassword())) {
                String token = jwtUtil.generateToken(user.getUsername(), user.getRole());
                return new LoginResponse(token, user.getRole(), user.getUsername());
            }
        }

        return null; // Échec d'authentification
    }
}
