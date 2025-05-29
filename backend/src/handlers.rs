use actix_web::{get, HttpResponse, Responder, HttpRequest, HttpMessage};
use tracing::{info, warn, instrument};

use crate::models::user::Claim as UserClaim;


/// Protected route that requires authentication
#[get("/protected")]
#[instrument(skip(req))]
async fn protected_route(req: HttpRequest) -> impl Responder {
    let extensions = req.extensions();
    let claims = extensions.get::<UserClaim>();

    if claims.is_none() {
        warn!("🚨 No JWT claims found in request!");
    } else {
        info!("✅ JWT claims found: {:?}", claims);
    }

    match claims {
        Some(claims) => HttpResponse::Ok().json(format!("Welcome, {}!", claims.sub)),
        _ => HttpResponse::Unauthorized().body("Invalid or missing token"),
    }
}
/// Public index route
#[get("/")]
async fn index() -> impl Responder {
    HttpResponse::Ok().body("Hello World!")
}
