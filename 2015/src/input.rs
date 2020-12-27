use std::io;

pub fn read_lines() -> Vec<String> {
    let mut lines = vec!();
    loop {
        let mut text = String::new();
        let read_count = io::stdin().read_line(&mut text).unwrap();
        if read_count == 0 {
            break
        }
        if let Some(stripped) = text.strip_suffix("\n") {
            text = stripped.to_string()
        }
        lines.push(text);
    }
    lines
}
