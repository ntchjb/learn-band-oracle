use obi::{OBIDeserialize, OBISchema, OBISerialize};
use owasm::{execute_entry_point, ext, oei, prepare_entry_point};

#[derive(OBIDeserialize, OBISchema)]
struct Input {
    symbol: String,
    multiplier: u64,
}

#[derive(OBISerialize, OBISchema)]
struct Output {
    px: u64,
}

#[no_mangle]
fn prepare_impl(input: Input) {
    // Yahoo price data source
    oei::request_external_data(14, 1, &input.symbol.as_bytes());
}

#[no_mangle]
fn execute_impl(input: Input) -> Output {
    let avg: f64 = ext::load_average(1);
    Output { px: (avg * input.multiplier as f64) as u64 }
}

prepare_entry_point!(prepare_impl);
execute_entry_point!(execute_impl);