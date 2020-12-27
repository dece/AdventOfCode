use aoc::input;

fn main() {
    let lines = input::read_lines();
    let line = lines[0].to_owned();

    // Part 1
    let mut floor = 0;
    for c in line.chars() {
        match c {
            '(' => floor += 1,
            ')' => floor -= 1,
            _ => {}
        }
    }
    println!("Floor: {}", floor);

    // Part 2
    floor = 0;
    for (i, c) in line.chars().enumerate() {
        match c {
            '(' => floor += 1,
            ')' => floor -= 1,
            _ => {}
        }
        if floor == -1 {
            println!("Entered -1 at {}.", i + 1);
            return
        }
    }
}
