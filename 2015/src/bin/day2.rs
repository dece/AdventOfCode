use aoc::input;

fn main() {
    let lines = input::read_lines();
    let dimensions: Vec<Vec<u32>> = lines.iter().map(|line| {
        line.split('x').map(|dim| dim.parse::<u32>().unwrap()).collect()
    }).collect();

    // Part 1
    let total: u32 = dimensions.iter().map(|dim| {
        let (l, w, h) = (dim[0], dim[1], dim[2]);
        let areas = vec!(l * w, w * h, h * l);
        let slack = areas.iter().min().unwrap();
        areas.iter().map(|a| 2 * a).sum::<u32>() + slack
    }).sum();
    println!("Needed paper: {}.", total);

    // Part 2
    let total: u32 = dimensions.iter().map(|dim| {
        let mut sdim = dim.clone();
        sdim.sort();
        let (d1, d2, d3) = (sdim[0], sdim[1], sdim[2]);
        let wrap = 2 * d1 + 2 * d2;
        let bow = d1 * d2 * d3;
        wrap + bow
    }).sum();
    println!("Needed ribbon: {}.", total);
}
