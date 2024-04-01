use std::fs::{self, File, OpenOptions};
use std::io::{self, BufRead, BufReader, Write};
use std::path::Path;

fn append_files(folder: &Path, output_file_name: &str) -> io::Result<()> {
    let output_path = folder.join(output_file_name);
    let mut output_file = OpenOptions::new()
        .create(true)
        .write(true)
        .append(true)
        .open(&output_path)?;

    for entry in fs::read_dir(folder)? {
        let entry = entry?;
        let path = entry.path();

        // Skip if it is a directory or the output file itself
        if path.is_dir() || path.file_name() == Some(output_file_name.as_ref()) {
            continue;
        }

        let file = File::open(&path)?;
        let reader = BufReader::new(file);

        for line in reader.lines() {
            let line = line?;
            writeln!(output_file, "{}", line)?;
        }
    }
    Ok(())
}

fn main() {
    let folder_path = Path::new("ngram");
    let output_file_name = "combined.txt";

    if let Err(e) = append_files(folder_path, output_file_name) {
        eprintln!("Failed to append files: {}", e);
    } else {
        println!("Files successfully appended to '{}'", output_file_name);
    }
}
