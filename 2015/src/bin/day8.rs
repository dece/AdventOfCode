use aoc::input;

fn main() {
    let lines = input::read_lines();

    // Part 1
    let mut used_mem = 0;
    let mut num_chars = 0;
    for line in &lines {
        let chars = line.chars().collect::<Vec<char>>();
        let line_mem = chars.len();
        let mut line_num_chars = line_mem - 2;
        let mut index = 1;
        while index < line_mem - 1 {
            if chars[index] == '\\' {
                if chars[index + 1] == '"' || chars[index + 1] == '\\' {
                    line_num_chars -= 1;
                    index += 1;
                } else if chars[index + 1] == 'x' {
                    line_num_chars -= 3;
                    index += 3;
                }
            }
            index += 1;
        }
        used_mem += line_mem;
        num_chars += line_num_chars;
    }
    println!("{} - {} = {}", used_mem, num_chars, used_mem - num_chars);

    // Part 2
    let mut encoded_size = used_mem;
    for line in &lines {
        for c in line.chars() {
            if c == '\\' || c == '"' { encoded_size += 1 }
        }
        encoded_size += 2; // enclosing quotes
    }
    println!("{} - {} = {}", encoded_size, used_mem, encoded_size - used_mem);
}
