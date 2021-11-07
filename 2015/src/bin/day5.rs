use aoc::input;

fn main() {
    let lines = input::read_lines();

    // Part 1
    let mut goods = 0;
    let bad_pairs = vec!("ab", "cd", "pq", "xy");
    for line in &lines {
        let mut has_bad_pair = false;
        for p in &bad_pairs {
            if line.contains(p) { has_bad_pair = true; break }
        }
        if has_bad_pair { continue }
        let mut num_vowels = 0;
        let mut cc = ' ';
        let mut has_doubled = false;
        for c in line.chars() {
            if "aeiou".contains(c) { num_vowels += 1 }
            if c == cc { has_doubled = true }
            cc = c;
        }
        if num_vowels < 3 { continue }
        if !has_doubled { continue }
        goods += 1;
    }
    println!("Good strings: {}", goods);

    // Part 2
    goods = 0;
    for line in &lines {
        let mut cond1 = false;
        let chars: Vec<char> = line.chars().collect();
        for i in 0..(chars.len() - 2) {
            let c1 = chars[i];
            let c2 = chars[i + 1];
            for j in (i + 2)..(chars.len() - 1) {
                if chars[j] == c1 && chars[j + 1] == c2 {
                    cond1 = true;
                    break
                }
            }
            if cond1 { break }
        }
        if !cond1 { continue }
        
        let mut cond2 = false;
        let mut cm2 = ' ';
        let mut cm1 = ' ';
        for c in line.chars() {
            if c == cm2 { cond2 = true }
            cm2 = cm1;
            cm1 = c;
        }
        if !cond2 { continue }
        goods += 1;
    }
    println!("Best strings: {}", goods);
}
