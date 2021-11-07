use aoc::input;

fn main() {
    let mut pass = input::read_chars();

    // Part 1
    get_next_pass(&mut pass);
    println!("Next pass: {}", pass);

    // Part 2
    get_next_pass(&mut pass);
    println!("Next pass: {}", pass);
}

fn get_next_pass(pass: &mut String) {
    loop {
        unsafe { inc(pass.as_bytes_mut()) }
        let pb = pass.as_bytes();
        if has_seq(pb) && !has_banned_chars(pb) && has_pairs(&pass) {
            break;
        }
    }
}

fn has_seq(pass: &[u8]) -> bool {
    for i in 0..(pass.len() - 2) {
        if pass[i] == pass[i + 1] - 1 && pass[i + 1] == pass[i + 2] - 1 {
            return true;
        }
    }
    false
}

fn has_banned_chars(pass: &[u8]) -> bool {
    for b in b"iol".iter() {
        if pass.contains(b) {
            return true;
        }
    }
    false
}

fn has_pairs(pass: &str) -> bool {
    let mut num_pairs = 0;
    let mut pc = ' ';
    let mut skip_next = false;
    for c in pass.chars() {
        if skip_next {
            skip_next = false;
            pc = c;
            continue
        }
        if c == pc {
            num_pairs += 1;
            skip_next = true;
        }
        pc = c;
    }
    num_pairs >= 2
}

fn inc(pass: &mut [u8]) {
    let mut i = pass.len() - 1;
    loop {
        let lc = pass[i];
        if lc < b'z' {
            let offset = if lc == b'i' || lc == b'o' || lc == b'l' { 2 } else { 1 };
            pass[i] = pass[i] + offset;
            break;
        } else {
            pass[i] = b'a';
            i -= 1;
        }
    }
}
