use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, ItemFn};

/// A simple procedural macro that extracts the locale from the request
/// and passes it as a `locale: String` parameter to the handler.
#[proc_macro_attribute]
pub fn with_locale(_attr: TokenStream, item: TokenStream) -> TokenStream {
    let mut input = parse_macro_input!(item as ItemFn);
    let fn_name = &input.sig.ident;
    let fn_inputs = &input.sig.inputs; // Preserve parameters
    let fn_body = &input.block;

    // Inject `locale` as an additional parameter
    let output = quote! {
        async fn #fn_name(req: actix_web::HttpRequest, #fn_inputs, locale: String) -> impl actix_web::Responder {
            let locale = req.headers()
                .get("Accept-Language")
                .and_then(|val| val.to_str().ok())
                .map(|val| val.split(',').next().unwrap_or("en"))
                .unwrap_or("en")
                .to_string();

            #fn_body
        }
    };

    output.into()
}
