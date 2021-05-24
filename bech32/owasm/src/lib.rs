use obi::{OBIDecode, OBISchema, OBIEncode};
use owasm::{execute_entry_point, ext, oei, prepare_entry_point};

#[derive(OBIDecode, OBISchema)]
struct Input {
    symbols: Vec<String>,
    multiplier: u64,
}

#[derive(OBIEncode, OBISchema)]
struct Output {
    prices: Vec<u64>,
}

// Sources
const COINMARKETCAP_DATA_SOURCE: u64 = 0;

// Data Sources
const COINMARKETCAP_DATA_SOURCE_DS: i64 = 1;

#[no_mangle]
fn prepare_impl(input: Input) {
    oei::ask_external_data(COINMARKETCAP_DATA_SOURCE as i64, COINMARKETCAP_DATA_SOURCE_DS, &input.symbols.join(" ").as_bytes());
}

#[no_mangle]
fn execute_impl(input: Input) -> Output {
    let mut raw_results = Vec::<String>::new();
    raw_results.append(&mut ext::load_input(COINMARKETCAP_DATA_SOURCE as i64).collect());
    let mut output = Output {
        prices: Vec::<u64>::new()
    };

    let num_data_sources = raw_results.len();
    let mut prices = vec![0.0; input.symbols.len()];
    for raw in raw_results {
        let px_list: Vec<f64> = raw
            .split(",")
            .filter_map(|x| x.parse::<f64>().ok())
            .collect();
        for (i, px) in px_list.iter().enumerate() {
            prices[i] += px;
        }
    }

    let final_prices: Vec<u64> = prices.into_iter()
        .map(|x| x / num_data_sources as f64)
        .map(|x| (x * input.multiplier as f64) as u64)
        .collect();

    output.prices = final_prices;

    return output
}

prepare_entry_point!(prepare_impl);
execute_entry_point!(execute_impl);
