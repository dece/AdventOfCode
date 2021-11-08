use serde_json::{self, Value};

use aoc::input;

fn main() {
    let json: Value = serde_json::from_str(&input::read_chars()).unwrap();

    // Part 1
    let sum_num = sum_numbers(&json);
    println!("Sum of numbers: {}", sum_num);

    // Part 2
    let sum_num_2 = sum_numbers_2(&json);
    println!("Sum of un-red numbers: {}", sum_num_2);
}

fn sum_numbers(value: &Value) -> i64 {
    match value {
        Value::Number(number) => number.as_i64().unwrap(),
        Value::Array(array) => array.iter().map(|v| sum_numbers(v)).sum(),
        Value::Object(map) => map.values().map(|v| sum_numbers(v)).sum(),
        _ => 0,
    }
}

fn sum_numbers_2(value: &Value) -> i64 {
    match value {
        Value::Number(number) => number.as_i64().unwrap(),
        Value::Array(array) => array.iter().map(|v| sum_numbers_2(v)).sum(),
        Value::Object(map) => {
            for str_prop in map.values().map(|p| p.as_str()) {
                if str_prop == Some("red") {
                    return 0;
                }
            }
            map.values().map(|v| sum_numbers_2(v)).sum()
        }
        _ => 0,
    }
}
