use actix_web::{App, HttpServer, web};
use dotenv::dotenv;
use tracing::info;
use db::connect_to_db;

mod auth;
mod db;
mod tracing_lint;
mod handlers;
mod routes;
mod errors;
mod models;

#[actix_web::main]
async fn main() -> std::io::Result<()> {

    // Environment setup    
    dotenv().ok(); 

    // To make logging pretty
    tracing_lint::init(env!("CARGO_PKG_NAME"))
        .expect("Failed to initialize tracing");

    // Get the host and port from the environment, or use defaults
    let host = std::env::var("HOST").unwrap_or_else(|_| "127.0.0.1".to_string());

    println!("{}", host);


    let port: u16 = std::env::var("PORT")
        .ok()
        .and_then(|port_str| port_str.parse::<u16>().ok())
        .unwrap_or(8080);

    // Connect to the database
    let pool = connect_to_db().await.map_err(|e| {
        tracing::error!("❌ Database connection failed: {:?}", e);
        std::io::Error::new(std::io::ErrorKind::Other, e.to_string())
    })?;

    // Create the Actix server
    let server = HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(pool.clone()))
            .wrap(tracing_actix_web::TracingLogger::default())
            .configure(routes::config)
    })
    .bind((host.as_str(), port));

    info!("🚀 Server starting on http://{}:{}", host, port);

    server.expect("Failed to bind server").run().await?;

    Ok(())
}
