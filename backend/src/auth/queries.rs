use sqlx::PgPool;
use tracing::{instrument, debug, info, warn, error};

use crate::errors::AppError;
use crate::models::user:: { NewUser, Claim }; // Import the User type from the models module

#[instrument(skip(pool))]
pub async fn query_password_hash(username: &str, pool: &PgPool) -> Result<String, AppError> {
    let result = sqlx::query_scalar::<_, String>(
        "SELECT password_hash FROM users WHERE username = $1"
    )
    .bind(username)  // ✅ Use .bind() for parameters
    .fetch_optional(pool)
    .await?;

    match result {
        Some(hash) => {
            debug!("Password hash found for user: {}", username);
            Ok(hash)
        },
        None => {
            warn!("No password hash found for username: {}", username);
            Err(AppError::InvalidCredentials) // Prevents user enumeration
        }
    }
}


#[instrument(skip(user, pool))]
pub async fn create_new_user(user: &NewUser, pool: &PgPool) -> Result<(), AppError> {
    sqlx::query(
        "INSERT INTO users (username, name, email, phone, password_hash, status, created_at, roles)
         VALUES ($1, $2, $3, $4, $5, $6::status_enum, $7, $8::jsonb)" // ✅ `::jsonb` works fine here
    )
    .bind(&user.username)
    .bind(&user.name)
    .bind(&user.email)
    .bind(&user.phone)
    .bind(&user.password_hash)
    .bind(&user.status.to_string().to_lowercase())
    .bind(&user.created_at)
    .bind(serde_json::to_value(&user.roles).unwrap()) // ✅ Proper JSON handling
    .execute(pool)
    .await
    .map_err(|e| {
        error!("Failed to create new user: {}", e);
        AppError::DatabaseError(e.to_string())
    })?;

    info!("User created successfully: {}", user.username);
    Ok(())
}



#[instrument(skip(pool))]
pub async fn query_user_claims(username: &str, pool: &PgPool) -> Result<Claim, AppError> {

    let row = sqlx::query!(
        "
        SELECT 
            u.id AS user_id, 
            u.username AS sub, 
            u.roles AS roles,  
            COALESCE(ARRAY_REMOVE(ARRAY_AGG(c.id), NULL), ARRAY[]::UUID[]) AS clinics_id
        FROM users u
        LEFT JOIN clinics c ON u.id = c.user_id
        WHERE u.username = $1
        GROUP BY u.id, u.username, u.roles;
        ",
        username
    )
    .fetch_one(pool)
    .await?;


    let roles: Vec<String> = serde_json::from_value(row.roles)
    .map_err(|e| {
        error!("Failed to deserialize roles for user: {}", username);
        AppError::SerializationError(e.to_string()) 
    })?;


    let claim = Claim {
        sub: row.user_id,
        exp: 0, // Example expiration time
        clinics_id: row.clinics_id.unwrap_or_default(),
        roles: roles,
    };


    Ok(claim)
}
