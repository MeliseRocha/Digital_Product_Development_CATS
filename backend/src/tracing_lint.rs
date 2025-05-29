// src/tracing.rs
use std::path::Path;
use tracing_appender::rolling::{RollingFileAppender, Rotation};
use tracing_subscriber::{fmt, prelude::*, EnvFilter};

pub fn init(crate_name: &str) -> Result<(), Box<dyn std::error::Error>> {
    let logs_dir = Path::new("logs");
    if !logs_dir.exists() {
        std::fs::create_dir_all(logs_dir)?;
    }

    let file_appender = RollingFileAppender::new(Rotation::DAILY, logs_dir, "redcore.log");
    let (non_blocking, _guard) = tracing_appender::non_blocking(file_appender);

    let env_filter = EnvFilter::from_default_env()
        .add_directive(format!("{crate_name}=info").parse()?)
        .add_directive(format!("{crate_name}::db=debug").parse()?)
        .add_directive(format!("{crate_name}::auth=debug").parse()?)
        .add_directive("sqlx=warn".parse()?)
        .add_directive("actix_web=warn".parse()?)
        .add_directive("actix_server=warn".parse()?);

    let stdout_layer = fmt::layer()
        .with_writer(std::io::stdout)
        .with_ansi(true)
        .with_thread_ids(false)
        .with_thread_names(false)
        .with_file(true)
        .with_line_number(true)
        .with_target(true)
        .compact()
        .pretty();

    let file_layer = fmt::layer()
        .with_writer(non_blocking)
        .with_ansi(false)
        .with_thread_ids(true)
        .with_thread_names(true)
        .with_file(true)
        .with_line_number(true)
        .with_target(true);

    tracing_subscriber::registry()
        .with(env_filter)
        .with(stdout_layer)
        .with(file_layer)
        .init();

    Ok(())
}
