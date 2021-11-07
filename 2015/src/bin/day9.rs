use std::collections::{HashMap, HashSet};

use aoc::input;

type Dists = HashMap<String, HashMap<String, u32>>;

fn main() {
    let lines = input::read_lines();
    let mut places: HashSet<String> = HashSet::new();
    let mut dists: Dists = HashMap::new();
    for line in lines {
        let parts = line.split_whitespace().collect::<Vec<&str>>();
        let from = parts[0];
        let to = parts[2];
        let dist = parts[4].parse::<u32>().unwrap();
        if !dists.contains_key(from) {
            dists.insert(from.to_string(), HashMap::new());
        }
        if !dists.contains_key(to) {
            dists.insert(to.to_string(), HashMap::new());
        }
        dists.get_mut(from).unwrap().insert(to.to_string(), dist);
        dists.get_mut(to).unwrap().insert(from.to_string(), dist);
        places.insert(from.to_string());
        places.insert(to.to_string());
    }
    let path_len = places.len();

    // Part 1
    let mut min: u32 = u32::MAX;
    for place in &places {
        let shortest_dist =
            find_shortest_path(&dists, &places, &mut vec![place.to_owned()], 0, path_len);
        if shortest_dist < min {
            min = shortest_dist
        }
    }
    println!("Shortest distance: {}", min);

    // Part 2
    let mut max: u32 = 0;
    for place in &places {
        let longest_dist =
            find_longest_path(&dists, &places, &mut vec![place.to_owned()], 0, path_len);
        if longest_dist > max {
            max = longest_dist
        }
    }
    println!("Longest distance: {}", max);
}

fn find_shortest_path(
    dists: &Dists,
    places: &HashSet<String>,
    cur_path: &mut Vec<String>,
    cur_dist: u32,
    max_places: usize,
) -> u32 {
    if cur_path.len() == max_places {
        return cur_dist;
    }
    // get next unexplored places
    let dists_from_here = dists.get(cur_path.last().unwrap()).unwrap();
    let mut min: u32 = u32::MAX;
    for next_place in places {
        if cur_path.contains(next_place) {
            continue;
        }
        cur_path.push(next_place.to_string());
        let next_place_dist = dists_from_here.get(next_place).unwrap();
        let shortest_dist = find_shortest_path(
            dists,
            places,
            cur_path,
            cur_dist + next_place_dist,
            max_places,
        );
        cur_path.pop();
        if shortest_dist < min {
            min = shortest_dist;
        }
    }
    min
}

fn find_longest_path(
    dists: &Dists,
    places: &HashSet<String>,
    cur_path: &mut Vec<String>,
    cur_dist: u32,
    max_places: usize,
) -> u32 {
    if cur_path.len() == max_places {
        return cur_dist;
    }
    // get next unexplored places
    let dists_from_here = dists.get(cur_path.last().unwrap()).unwrap();
    let mut max: u32 = 0;
    for next_place in places {
        if cur_path.contains(next_place) {
            continue;
        }
        cur_path.push(next_place.to_string());
        let next_place_dist = dists_from_here.get(next_place).unwrap();
        let longest_dist = find_longest_path(
            dists,
            places,
            cur_path,
            cur_dist + next_place_dist,
            max_places,
        );
        cur_path.pop();
        if longest_dist > max {
            max = longest_dist;
        }
    }
    max
}
