use obi::{OBIDecode, OBISchema, OBIEncode};
use owasm::{execute_entry_point, ext, oei, prepare_entry_point};

#[derive(OBIDecode, OBISchema)]
struct Input {
    multiplier: u64,
}

#[derive(OBIEncode, OBISchema)]
struct Output {
    price: u64,
}

// Sources
const FREEFOREXAPI_DATA_SOURCE: u64 = 0;
const GOLDPRICEORG_DATA_SOURCE: u64 = 1;

// Data Sources
const FREEFOREXAPI_DATA_SOURCE_DS: i64 = 4;
const GOLDPRICEORG_DATA_SOURCE_DS: i64 = 5;

#[no_mangle]
fn prepare_impl(_input: Input) {
    oei::ask_external_data(FREEFOREXAPI_DATA_SOURCE as i64, FREEFOREXAPI_DATA_SOURCE_DS, "GOLD".as_bytes());
    oei::ask_external_data(GOLDPRICEORG_DATA_SOURCE as i64, GOLDPRICEORG_DATA_SOURCE_DS, "GOLD".as_bytes());
}

#[no_mangle]
fn execute_impl(input: Input) -> Output {
    let mut results = Vec::<f64>::new();
    results.append(&mut ext::load_input(FREEFOREXAPI_DATA_SOURCE as i64).collect());
    results.append(&mut ext::load_input(GOLDPRICEORG_DATA_SOURCE as i64).collect());

    match ext::stats::average(results) {
        Some(result) => {
            Output { price: (result * input.multiplier as f64) as u64 }
        }
        None => {
            panic!("No data provided by data sources")
        }
    }
}

prepare_entry_point!(prepare_impl);
execute_entry_point!(execute_impl);

#[cfg(test)]
mod tests {
    use super::*;
    use obi::get_schema;
    use std::collections::*;

    #[test]
    fn test_get_schema() {
        let mut schema = HashMap::new();
        Input::add_definitions_recursively(&mut schema);
        Output::add_definitions_recursively(&mut schema);
        let input_schema = get_schema(String::from("Input"), &schema);
        let output_schema = get_schema(String::from("Output"), &schema);
        println!("{}/{}", input_schema, output_schema);
        assert_eq!(
            "{multiplier:u64}/{price:u64}",
            format!("{}/{}", input_schema, output_schema),
        );
    }
}
