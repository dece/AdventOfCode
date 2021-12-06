use std::io;

fn main() {
    let mut text = String::new();
    io::stdin().read_line(&mut text).unwrap();
    let mut data = vec![0u64; 9];
    for c in text.strip_suffix("\n").unwrap().split(",") {
        data[str::parse::<usize>(c).unwrap()] += 1;
    }
    for _ in 0..80 {
        step(&mut data);
    }
    println!("{}", data.iter().sum::<u64>());
    for _ in 80..256 {
        step(&mut data);
    }
    println!("{}", data.iter().sum::<u64>());
}

fn step(data: &mut Vec<u64>) {
    let d0 = data[0];
    for d in 0..=7 {
        data[d] = data[d + 1];
    }
    data[6] += d0;
    data[8] = d0;
}
