use std::env;
use chrono::Utc; 

use actix_web::{dev::ServiceRequest, Error, HttpMessage};
use actix_web_httpauth::extractors::bearer::BearerAuth;
use jsonwebtoken::{encode, decode, Header, Validation, EncodingKey, DecodingKey, Algorithm};
use tracing::{info, warn, error, instrument};
use uuid::Uuid;

use crate::models::user::Claim;


/// Load JWT secret key from the environment
fn get_secret_key() -> String {
    env::var("JWT_SECRET_KEY").unwrap_or_else(|_| "secretkey".to_string())
}

/// Generate JWT token
const EXPIRATION_HOURS: i64 = 24; // Token valid for 24 hours

#[instrument(skip(roles, clinics_id))]
pub fn create_jwt_token(user_id: Uuid, roles: Vec<String>, clinics_id: Vec<Uuid>) -> Result<String, jsonwebtoken::errors::Error> {
    let expiration = Utc::now()
    .checked_add_signed(chrono::Duration::hours(EXPIRATION_HOURS)) // ✅ Correct method
    .map(|t| t.timestamp()) // Convert to Unix timestamp safely
    .unwrap_or_else(|| Utc::now().timestamp()); // Fallback: current timestamp

    let claims = Claim {
        sub: user_id,
        exp: expiration,
        clinics_id,
        roles
    };

    let secret = env::var("JWT_SECRET_KEY").expect("JWT_SECRET must be set");
    encode(
        &Header { alg: Algorithm::HS256, ..Default::default() }, // ✅ Explicitly set HS256
        &claims,
        &EncodingKey::from_secret(secret.as_ref())
    )
}


/// Validate JWT token
#[instrument(skip(token))]
pub fn validate_token(token: &str) -> Result<Claim, jsonwebtoken::errors::Error> {
    let decoded = decode::<Claim>(
        token,
        &DecodingKey::from_secret(get_secret_key().as_bytes()),
        &Validation::default(),
    )?;
    Ok(decoded.claims)
}

#[instrument(skip(req, credentials))]
pub async fn validator(req: ServiceRequest, credentials: BearerAuth) -> Result<ServiceRequest, (Error, ServiceRequest)> {

    if credentials.token().is_empty() {
        warn!("🚨 Authentication failed: Missing token");
        return Err((actix_web::error::ErrorUnauthorized("Missing token"), req));
    }


    match validate_token(credentials.token()) {
        Ok(claims) => {
            info!(
                event = "authentication_successful",
                user_id = %claims.sub,
                roles = ?claims.roles,
                "✅ Authentication successful"
            );
            req.extensions_mut().insert(claims); // Store claims inside request
            Ok(req)
        }
        Err(err) => {
            error!(
                event = "authentication_failed",
                error = %err,
                "🚨 Authentication failed"
            );
            Err((actix_web::error::ErrorUnauthorized("Invalid or missing token"), req))
        }
    }
}