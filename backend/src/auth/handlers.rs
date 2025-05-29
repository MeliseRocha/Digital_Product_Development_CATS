use actix_web::{post, web, HttpResponse};
use serde::{Deserialize, Serialize};
use sqlx::PgPool;
use tracing::{instrument, info, warn};

use crate::auth::jwt::create_jwt_token;
use crate::auth::password::verify_password;
use crate::auth::queries::{create_new_user, query_password_hash, query_user_claims};
use crate::errors::AppError;
use crate::models::user::{ NewUser, RegisterRequest };




/// Request format for login
#[derive(Debug, Serialize, Deserialize)]
pub struct LoginRequest {
    pub username: String,
    pub password: String,
}

/// Response format for login
#[derive(Debug, Serialize, Deserialize)]
pub struct LoginResponse {
    pub token: String,
}


#[post("/register")]
#[instrument]
async fn register(
    user: web::Json<RegisterRequest>,
    pool: web::Data<PgPool>
) -> Result<HttpResponse, AppError> {

    // ✅ Convert RegisterRequest -> User (hashes password inside `try_from`)
    let new_user = NewUser::try_from(user.into_inner())?;

    // ✅ Insert new user into DB
    create_new_user(&new_user, pool.get_ref()).await?;

    info!(
        event = "user_registered",
        username = %new_user.username,
        email = %new_user.email,
        "✅ User registered successfully"
    );
    Ok(HttpResponse::Created().json("User registered successfully"))
}

/// Receives a login request and returns a JWT token if the password matches
#[post("/login")]
#[instrument(skip(pool, user))]
async fn login(user: web::Json<LoginRequest>, pool: web::Data<PgPool>) -> Result<HttpResponse, AppError> {
    info!("🔵 Received login request for username: {}", user.username);

    let password_hash: String = query_password_hash(user.username.as_str(), pool.get_ref()).await?;
    
    if let Ok(true) = verify_password(&user.password, &password_hash) {
        // Fetch user details from database
        let user_data = query_user_claims(user.username.as_str(), pool.get_ref()).await?;

        let token = create_jwt_token(
            user_data.sub,
            user_data.roles,
            user_data.clinics_id,
        ).map_err(AppError::JWTError)?;

        info!(
            event = "login_successful",
            username = %user.username,
            user_id = %user_data.sub,
            "✅ Login successful"
        );
        Ok(HttpResponse::Ok().json(LoginResponse { token }))
    } else {
        warn!(
            event = "login_failed",
            username = %user.username,
            reason = "password_mismatch",
            "🚨 Password mismatch"
        );
        Err(AppError::InvalidCredentials)
    }
}