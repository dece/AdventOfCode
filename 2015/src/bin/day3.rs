use std::collections::HashMap;

use aoc::input;

fn main() {
    let chars = input::read_chars();

    // Part 1
    let mut houses = HashMap::<(i32, i32), u32>::new();
    let (mut x, mut y) = (0, 0);
    houses.insert((0, 0), 1);
    for c in chars.chars() {
        match c {
            '>' => x += 1,
            '<' => x -= 1,
            'v' => y += 1,
            '^' => y -= 1,
            _ => {}
        }
        let presents = houses.entry((x, y)).or_insert(0);
        *presents += 1;
    }
    let num_houses = houses.values().filter(|v| **v > 0).count();
    println!("Houses delivered: {}.", num_houses);

    // Part 2
    let mut houses = HashMap::<(i32, i32), u32>::new();
    let (mut x, mut y, mut rx, mut ry) = (0, 0, 0, 0);
    houses.insert((0, 0), 1);
    let mut is_robot_turn = false;
    for c in chars.chars() {
        match c {
            '>' => if is_robot_turn { rx += 1 } else { x += 1 },
            '<' => if is_robot_turn { rx -= 1 } else { x -= 1 },
            'v' => if is_robot_turn { ry += 1 } else { y += 1 },
            '^' => if is_robot_turn { ry -= 1 } else { y -= 1 },
            _ => {}
        }
        let presents = houses.entry(if is_robot_turn { (rx, ry) } else { (x, y) }).or_insert(0);
        *presents += 1;
        is_robot_turn = !is_robot_turn;
    }
    let num_houses = houses.values().filter(|v| **v > 0).count();
    println!("Houses delivered: {}.", num_houses);
}
