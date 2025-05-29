use actix_web::web;
use actix_web_httpauth::middleware::HttpAuthentication;

use crate::auth;
use crate::auth::jwt::validator;
use crate::handlers;

pub fn config(cfg: &mut web::ServiceConfig) {
    let auth_middleware = HttpAuthentication::with_fn(validator); // ✅ FIX: Use `with_fn`

    auth::configure(cfg); // ✅ Mount auth/password management routes

    cfg.service(handlers::index)
        .service(
            web::scope("/api") // ✅ Protect only `/api/*` routes
                .wrap(auth_middleware) // ✅ Apply auth middleware
                .service(handlers::protected_route),
    );
}

// Future routes

// pub fn config(cfg: &mut web::ServiceConfig) {
//     let auth_middleware = HttpAuthentication::with_fn(validator); // ✅ Use `with_fn`

//     cfg.service(handlers::index)
//         .service(
//             web::scope("/api") // Protect only `/api/*` routes
//                 .wrap(auth_middleware) // Apply auth middleware
//                 .configure(auth::configure) // Configure auth routes
//                 .configure(patients::configure) // Configure patient routes
//                 .configure(records::configure) // Configure record routes
//                 .configure(appointments::configure) // Configure appointment routes
//                 .service(handlers::protected_route),
//         );
// }