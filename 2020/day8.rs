use std::collections;
use std::fs;
use std::io::{self, BufRead};

#[derive(Clone)]
enum Op {
    Nop(i64),
    Jmp(i64),
    Acc(i64),
}

struct Cpu {
    ip: u64,
    acc: i64,
}

impl Cpu {
    fn step(&mut self, code: &Vec<Op>) {
        match code[self.ip as usize] {
            Op::Nop(_) => {},
            Op::Jmp(i) => { self.ip = (self.ip as i64 + i) as u64; return }
            Op::Acc(i) => { self.acc += i }
        }
        self.ip += 1;
    }
}

fn main() {
    let file = fs::File::open("day8.txt").unwrap();
    let lines: Vec<String> = io::BufReader::new(file).lines().map(|r| r.unwrap()).collect();
    let mut code: Vec<Op> = lines.iter().map(|line| {
        let inst: Vec<&str> = line.splitn(2, " ").collect();
        match inst[0] {
            "nop" => Op::Nop(inst[1].parse::<i64>().unwrap()),
            "jmp" => Op::Jmp(inst[1].parse::<i64>().unwrap()),
            "acc" => Op::Acc(inst[1].parse::<i64>().unwrap()),
            unk => panic!("Unknown op '{}'", unk),
        }
    }).collect();

    // Part 1.
    let mut visited: collections::HashSet<u64> = collections::HashSet::new();
    let mut cpu = Cpu { ip: 0, acc: 0 };
    while !visited.contains(&cpu.ip) {
        visited.insert(cpu.ip);
        cpu.step(&code);
    }
    println!("Acc after first revisit: {}.", cpu.acc);

    // Part 2.
    for i in 0..code.len() {
        match &code[i] {
            Op::Jmp(val) => {
                let op_backup = code[i].clone();
                code[i] = Op::Nop(*val);
                if let Some(acc) = run(&code) {
                    println!("Acc after non-looping execution: {}.", acc);
                    break
                }
                code[i] = op_backup;
            }
            _ => {}
        }
    }
}

fn run(code: &Vec<Op>) -> Option<i64> {
    let mut visited: collections::HashSet<u64> = collections::HashSet::new();
    let mut cpu = Cpu { ip: 0, acc: 0 };
    while cpu.ip < code.len() as u64 {
        visited.insert(cpu.ip);
        cpu.step(&code);
        if visited.contains(&cpu.ip) {
            return None
        }
    }
    Some(cpu.acc)
}
