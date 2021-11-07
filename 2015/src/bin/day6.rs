use std::cmp;

use aoc::input;

fn main() {
    let lines = input::read_lines();
    let mut grid = vec![false; 1_000_000];

    // Part 1
    for line in &lines {
        let mut parts = line.split_whitespace();
        let state = if parts.next() == Some("turn") {
            parts.next().and_then(|s| Some(s == "on"))
        } else { // toggle
            None
        };
        let s: Vec<usize> = parts.next().unwrap().split(",")
            .map(|p| p.parse::<usize>().unwrap()).collect();
        let e: Vec<usize> = parts.nth(1).unwrap().split(",")
            .map(|p| p.parse::<usize>().unwrap()).collect();
        for i in s[0]..=e[0] {
            for j in s[1]..=e[1] {
                grid[i * 1000 + j] = match state {
                    Some(c) => c,
                    None => !grid[i * 1000 + j]
                }
            }
        }
    }
    println!("Lights on: {}", grid.iter().map(|s| if *s { 1 } else { 0 }).sum::<u32>());

    // Part 2
    let mut grid = vec![0; 1_000_000];
    for line in &lines {
        let mut parts = line.split_whitespace();
        let change: i32 = if parts.next() == Some("turn") {
            if parts.next().unwrap() == "on" { 1 } else { -1 }
        } else { // toggle
            2
        };
        let s: Vec<usize> = parts.next().unwrap().split(",")
            .map(|p| p.parse::<usize>().unwrap()).collect();
        let e: Vec<usize> = parts.nth(1).unwrap().split(",")
            .map(|p| p.parse::<usize>().unwrap()).collect();
        for i in s[0]..=e[0] {
            for j in s[1]..=e[1] {
                let current = grid[i * 1000 + j];
                grid[i * 1000 + j] = cmp::max(current + change, 0);
            }
        }
    }
    println!("Brightness: {}", grid.iter().sum::<i32>());
}
