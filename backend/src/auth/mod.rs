pub mod handlers;
pub mod jwt;
pub mod password;
pub mod queries;

use actix_web::web;

pub fn configure(cfg: &mut web::ServiceConfig) {
    cfg.service(
        web::scope("/auth")
            .service(handlers::login)
            .service(handlers::register)
    );
}