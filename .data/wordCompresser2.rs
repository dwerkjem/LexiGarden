use std::collections::HashMap;
use std::fs::{self, File};
use std::io::{self, BufRead, BufReader, Write};
use std::path::Path;

fn compress_and_aggregate(folder: &Path) -> io::Result<()> {
    for entry in fs::read_dir(folder)? {
        let entry = entry?;
        let path = entry.path();

        if path.is_dir() {
            continue;
        }

        let file = File::open(&path)?;
        let reader = BufReader::new(file);
        let mut word_counts = HashMap::new();

        for line in reader.lines() {
            let line = line?;
            // Assuming there can be multiple whitespace characters as separators
            let parts: Vec<&str> = line.split_whitespace().collect();
            if parts.len() == 4 {
                // Change the parsing to i64
                if let (Ok(n), Ok(n2)) = (parts[2].parse::<i64>(), parts[3].parse::<i64>()) {
                    *word_counts.entry(parts[0].to_string()).or_insert(0) += n + n2;
                }
            }
        }

        let mut file = File::create(&path)?;
        for (word, count) in word_counts {
            writeln!(file, "{} {}", word, count)?;
        }
    }
    Ok(())
}

fn main() {
    let folder = Path::new("ngram");
    if let Err(e) = compress_and_aggregate(folder) {
        eprintln!("Error processing files: {}", e);
    }
}
