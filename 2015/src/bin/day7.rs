use std::collections::HashMap;

use aoc::input;

#[derive(Debug)]
enum Op {
    And(String, String), // left-hand can be an int
    Or(String, String),
    Not(String),
    Lshift(String, u16),
    Rshift(String, u16),
    Value(String), // either int or wire
}

fn main() {
    let lines = input::read_lines();
    let mut wiring: HashMap<String, Op> = HashMap::new();
    for line in lines {
        let mut parts = line.split(" -> ");
        let op_text = parts.next().unwrap();
        let target = parts.next().unwrap();
        let op_parts: Vec<&str> = op_text.split_whitespace().collect();
        let op = match op_parts.len() {
            1 => { Op::Value(op_parts[0].to_string()) }
            2 => { Op::Not(op_parts[1].to_string()) }
            3 => { match op_parts[1] {
                "AND" => { Op::And(op_parts[0].to_string(), op_parts[2].to_string()) }
                "OR" => { Op::Or(op_parts[0].to_string(), op_parts[2].to_string()) }
                "LSHIFT" => { Op::Lshift(op_parts[0].to_string(), op_parts[2].parse::<u16>().unwrap()) }
                "RSHIFT" => { Op::Rshift(op_parts[0].to_string(), op_parts[2].parse::<u16>().unwrap()) }
                _ => panic!()
            } }
            _ => panic!()
        };
        wiring.insert(target.to_string(), op);
    }

    // Part 1
    let mut cache: HashMap<String, u16> = HashMap::new();
    let part1 = solve(&wiring, "a", &mut cache);
    println!("Wire a: {}", part1);

    // Part 2
    wiring.insert("b".to_string(), Op::Value(part1.to_string()));
    let mut cache: HashMap<String, u16> = HashMap::new();
    println!("Wire a with b overridden: {}", solve(&wiring, "a", &mut cache));
}

fn solve(wiring: &HashMap<String, Op>, name: &str, cache: &mut HashMap<String, u16>) -> u16 {
    if cache.contains_key(name) {
        return *cache.get(name).unwrap()
    }
    let value = if let Ok(value) = name.parse::<u16>() {
        return value
    } else {
        match wiring.get(name).unwrap() {
            Op::And(lh, rh) => { solve(wiring, lh, cache) & solve(wiring, rh, cache) }
            Op::Or(lh, rh) => { solve(wiring, lh, cache) | solve(wiring, rh, cache) }
            Op::Not(op) => { !solve(wiring, op, cache) }
            Op::Lshift(lh, rh) => { solve(wiring, lh, cache) << rh }
            Op::Rshift(lh, rh) => { solve(wiring, lh, cache) >> rh }
            Op::Value(v) => { solve(wiring, v, cache) }
        }
    };
    cache.insert(name.to_string(), value);
    value
}
