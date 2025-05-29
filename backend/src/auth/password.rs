use argon2::{Argon2, PasswordHasher, PasswordVerifier, password_hash::{SaltString, rand_core::OsRng, PasswordHash}};
use tracing::{instrument, warn, error, debug};

use crate::errors::AppError;

#[instrument(skip(password))]
pub fn hash_it(password: &str) -> Result<String, AppError> {
    let salt = SaltString::generate(&mut OsRng); // Generate a random salt
    let argon2 = Argon2::default();

    let hashed_password = argon2.hash_password(password.as_bytes(), &salt)
        .map_err(|e| {
            error!("Failed to hash password: {}", e);
            AppError::InternalError
        })?;

    let hashed_password_str = hashed_password.to_string();
    debug!("Password hashed successfully");
    
    Ok(hashed_password_str)
}

#[instrument(skip(typed_password, hash))]
pub fn verify_password(typed_password: &str, hash: &str) -> Result<bool, AppError> {
    let parsed_hash = PasswordHash::new(hash)
        .map_err(|e| {
            error!("Failed to parse password hash: {}", e);
            AppError::InternalError
        })?;

    match Argon2::default().verify_password(typed_password.as_bytes(), &parsed_hash) {
        Ok(_) => {
            debug!("Password verified successfully");
            Ok(true)
        },
        Err(e) => {
            debug!("Password verification failed: {}", e);
            Err(AppError::InvalidCredentials)
        }
    }
}