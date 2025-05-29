use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;
use std::convert::TryFrom; 

use derive_more::Display; 

use crate::errors::AppError; 
use crate::auth::password::hash_it;

#[derive(Debug, Serialize, Deserialize)]
pub struct NewUser {
    pub username: String,
    pub name: String,
    pub email: String,
    pub phone: String,
    pub password_hash: String,
    pub status: StatusEnum,
    pub created_at: DateTime<Utc>,
    pub roles: Vec<String>,
}

#[derive(Debug, sqlx::Type, Serialize, Deserialize)]
#[derive(Display)] 
#[sqlx(type_name = "status_enum", rename_all = "lowercase")]
pub enum StatusEnum {
    Active,
    Inactive    
}

pub struct _User {
     pub username: String,
    pub name: String,
    pub email: String,
    pub phone: String,
    pub status: StatusEnum,
    pub created_at: DateTime<Utc>,
    pub roles: Vec<String>
}

#[derive(Debug, Serialize, Deserialize)]
pub struct RegisterRequest {
    pub username: String,
    pub name: String,
    pub email: String,
    pub phone: String,
    pub password: String,
    pub roles: Vec<String>,
}
#[derive(Debug, Serialize, Deserialize)]
pub struct Claim {
    pub sub: Uuid,
    pub exp: i64,
    pub clinics_id: Vec<Uuid>,
    pub roles: Vec<String>
}

// ✅ Corrected implementation of `TryFrom<RegisterRequest>` for `User`
impl TryFrom<RegisterRequest> for NewUser {
    type Error = AppError;

    fn try_from(request: RegisterRequest) -> Result<Self, Self::Error> {
        
        let hashed_password = hash_it(&request.password)?; // ✅ Hash password securely

        Ok(NewUser {
            username: request.username,
            name: request.name,
            email: request.email,
            phone: request.phone,
            password_hash: hashed_password, // ✅ Now stored securely
            status: StatusEnum::Active, // ✅ Default for new users
            created_at: Utc::now(),
            roles: request.roles,
        })
    }
}

