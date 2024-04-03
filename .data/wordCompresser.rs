use std::fs::{self, File};
use std::io::{self, BufRead, BufReader, Write};
use std::path::Path;

fn compress(folder: &Path) -> io::Result<()> {
    // Iterate over files in the specified folder
    for entry in fs::read_dir(folder)? {
        let entry = entry?;
        let path = entry.path();

        // Skip directories
        if path.is_dir() {
            continue;
        }

        let file = File::open(&path)?;
        let reader = BufReader::new(file);
        let mut lines_to_write = Vec::new();

        for line in reader.lines() {
            let line = line?;
            // Split the line by whitespace and collect into a vector
            let parts: Vec<&str> = line.split_whitespace().collect();
            // Check if there's at least 2 parts and the second part is a year
            if parts.len() > 1 {
                if let Ok(year) = parts[1].parse::<i32>() {
                    // If the year is >= 1970, keep the line
                    if year >= 1900 {
                        lines_to_write.push(line);
                    }
                }
            } else {
                // If there's no year, keep the line as is
                lines_to_write.push(line);
            }
        }

        // Rewrite the file with the filtered and modified lines
        let mut file = File::create(&path)?;
        for line in lines_to_write {
            writeln!(file, "{}", line)?;
        }
    }
    Ok(())
}

fn main() {
    let folder = Path::new("ngram"); // Replace with your folder path
    if let Err(e) = compress(folder) {
        eprintln!("Error compressing files: {}", e);
    }
}
