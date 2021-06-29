use obi::{OBIDecode, OBISchema, OBIEncode};
use owasm::{execute_entry_point, ext, oei, prepare_entry_point};

// endpoint field is for testing purpose only
#[derive(OBIDecode, OBISchema)]
struct Input {
    endpoint: String,
    symbols: Vec<String>,
    multiplier: u64,
}

#[derive(OBIEncode, OBISchema)]
struct Output {
    prices: Vec<u64>,
}

// External IDs
const COINGECKO_DATA_SOURCE: i64 = 0;

// Data Source Script IDs
const COINGECKO_DATA_SOURCE_DS: i64 = 1;

#[no_mangle]
fn prepare_impl(input: Input) {
    // Calldata should be something like "https://gateway-endpoint.example BTC,ETH,UNI"
    oei::ask_external_data(COINGECKO_DATA_SOURCE, COINGECKO_DATA_SOURCE_DS, &[input.endpoint, input.symbols.join(",")].join(" ").as_bytes());
}

#[no_mangle]
fn execute_impl(input: Input) -> Output {
    let mut raw_results = Vec::<String>::new();
    let mut output = Output {
        prices: Vec::<u64>::new()
    };

    // Collect unprocessed results from each validator
    raw_results.append(&mut ext::load_input(COINGECKO_DATA_SOURCE).collect());

    let num_responses = raw_results.len();
    let mut prices = vec![0.0; input.symbols.len()];
    // Get response from each validator
    for response in raw_results {
        // Convert a response to a list of float (coin prices list)
        // We assume that datasource returns a string of comma-separated coin prices
        let px_list: Vec<f64> = response
            .split(",")
            .filter_map(|x| x.parse::<f64>().ok())
            .collect();
        // add each coin to prices array in proper order
        for (i, px) in px_list.iter().enumerate() {
            prices[i] += px;
        }
    }

    // Get sum of each coin and find average of each coin
    // , then multiply by multiplier
    let final_prices: Vec<u64> = prices.into_iter()
        .map(|x| x / num_responses as f64)
        .map(|x| (x * input.multiplier as f64) as u64)
        .collect();

    output.prices = final_prices;

    return output
}

prepare_entry_point!(prepare_impl);
execute_entry_point!(execute_impl);
