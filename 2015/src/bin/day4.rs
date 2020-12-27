use aoc::input;

fn main() {
    let lines = input::read_lines();
    let mut key = lines[0].to_string();
    let key_len = key.len();

    // Part 1
    let mut n = 0;
    loop {
        key.replace_range(key_len.., &n.to_string());
        let hash = md5::compute(key.as_bytes());
        if &hash[..2] == [0, 0] && hash[2] < 0x10 {
            break
        }
        n += 1
    }
    println!("Found coin with n {}.", n);

    // Part 2
    loop {
        key.replace_range(key_len.., &n.to_string());
        let hash = md5::compute(key.as_bytes());
        if &hash[..3] == [0, 0, 0] {
            break
        }
        n += 1
    }
    println!("Found coin with n {}.", n);
}
