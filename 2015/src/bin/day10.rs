use aoc::input;

fn main() {
    let mut v = input::read_chars();

    // Part 1
    for _ in 0..40 {
        v = step(&v);
    }
    println!("Length after 40 steps: {}", v.len());

    // Part 2
    for _ in 0..10 {
        v = step(&v);
    }
    println!("Length after 50 steps: {}", v.len());
}

fn step(s: &str) -> String {
    let mut count = 1;
    let mut pc = ' ';
    let mut result = String::new();
    for c in s.chars() {
        if c == pc {
            count += 1;
        } else if pc != ' ' {
            result.push_str(&count.to_string());
            result.push(pc);
            count = 1;
        }
        pc = c;
    }
    result.push_str(&count.to_string());
    result.push(pc);
    result
}
