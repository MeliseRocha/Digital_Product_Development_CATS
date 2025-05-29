use actix_web::{HttpResponse, ResponseError};
use derive_more::Display;
use sqlx::Error as SqlxError;


#[derive(Debug, Display)] // ✅ Ensures `Display` is implemented
pub enum AppError {
    #[display("Database error: {}", _0)] 
    DatabaseError(String),

    #[display("Invalid Credentials")]  
    InvalidCredentials,

    #[display("Internal error")]  
    InternalError,

    #[display("Serialization error: {}", _0)]
    SerializationError(String),

    #[display("Configuration error")]
    ConfigError,

    JWTError(jsonwebtoken::errors::Error), // ✅ New variant for JWT errors



}

// ✅ Convert `AppError` to Actix-web HTTP response
impl ResponseError for AppError {
    fn error_response(&self) -> HttpResponse {
        match self {
            AppError::DatabaseError(msg) => HttpResponse::InternalServerError().body(format!("Database error: {}", msg)),
            AppError::InvalidCredentials => HttpResponse::Unauthorized().body("Invalid credentials"),
            AppError::InternalError => HttpResponse::InternalServerError().body("Internal error"),
            AppError::SerializationError(msg   ) => HttpResponse::InternalServerError().body(format!("Serialization error: {}", msg)),
            AppError::ConfigError => HttpResponse::InternalServerError().body("Configuration error"),
            AppError::JWTError(err) => HttpResponse::Unauthorized().body(format!("JWT error: {}", err)),
        }
    }
}


// ✅ Convert `sqlx::Error` into `AppError`
impl From<SqlxError> for AppError {
    fn from(err: SqlxError) -> Self {
        match err {
            SqlxError::RowNotFound => AppError::InvalidCredentials, // Prevent user enumeration

            SqlxError::Io(ref io_err) if io_err.kind() == std::io::ErrorKind::BrokenPipe => {
                AppError::DatabaseError("Database connection lost. Please try again.".to_string())
            }

            SqlxError::PoolTimedOut => {
                AppError::DatabaseError("Database connection pool is full. Try again later.".to_string())
            }

            SqlxError::Database(ref db_err) => {
                AppError::DatabaseError(format!("Database error: {}", db_err.message()))
            }

            SqlxError::Configuration(_) => AppError::InternalError,

            SqlxError::TypeNotFound { .. } => AppError::InternalError,

            _ => AppError::DatabaseError(format!("Unexpected DB error: {:?}", err)),
        }
    }
}
