#!/usr/bin/env python3
import os
import shutil
import argparse
import hashlib
import logging
from datetime import datetime
from rich.console import Console
from rich.text import Text

console = Console()

# Setup logging
def setup_logging(debug=False):
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"phoenix_{timestamp}.log")
    
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("Phoenix")

def print_ascii_banner():
    # Rainbow colors
    rainbow_colors = [
        "red",
        "yellow",
        "green",
        "cyan",
        "blue",
        "magenta",
        "red"  # Complete the rainbow cycle
    ]
    banner = Text()
    
    # Phoenix text banner with rainbow effect
    text_banner = [
        "██████╗ ██╗  ██╗ ██████╗ ███████╗███╗   ██╗██╗██╗  ██╗",
        "██╔══██╗██║  ██║██╔═══██╗██╔════╝████╗  ██║██║╚██╗██╔╝",
        "██████╔╝███████║██║   ██║█████╗  ██╔██╗ ██║██║ ╚███╔╝ ",
        "██╔═══╝ ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║██║ ██╔██╗ ",
        "██║     ██║  ██║╚██████╔╝███████╗██║ ╚████║██║██╔╝ ██╗",
        "╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝"
    ]
    
    # Print each line with rainbow gradient
    for i, line in enumerate(text_banner):
        # Calculate color positions for smooth transition
        color_pos = i / len(text_banner) * (len(rainbow_colors) - 1)
        color1 = rainbow_colors[int(color_pos)]
        color2 = rainbow_colors[int(color_pos) + 1]
        
        # Print each character with gradient color
        for j, char in enumerate(line):
            pos = j / len(line)
            color = color1 if pos < 0.5 else color2
            banner.append(char, style=color)
        banner.append("\n")
    
    # Add credits with special styling
    banner.append("\n")
    banner.append("Created by ", style="cyan")
    banner.append("Pakagrong Lebel", style="bright_cyan bold")
    banner.append(" | Data Recovery Tool", style="cyan")
    banner.append("\n\n")
    
    console.print(banner)

def calculate_hash(filepath):
    try:
        with open(filepath, "rb") as f:
            hash_value = hashlib.sha256(f.read()).hexdigest()
            logging.debug(f"Calculated hash for {filepath}: {hash_value}")
            return hash_value
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        return None
    except Exception as e:
        logging.error(f"Error calculating hash for {filepath}: {str(e)}")
        return None

def list_backup_files(backup_dir):
    logging.info(f"Listing backup files in {backup_dir}")
    backups = []
    for root, dirs, files in os.walk(backup_dir):
        for file in files:
            full_path = os.path.join(root, file)
            backups.append(full_path)
            logging.debug(f"Found backup file: {full_path}")
    return backups

def recover_file(corrupted_path, backup_path, dry_run=False):
    if dry_run:
        logging.info(f"[DRY RUN] Would restore {corrupted_path} from backup")
        console.print(f"[cyan]Simulated recovery:[/cyan] Would restore [bold]{corrupted_path}[/bold] from backup.")
    else:
        try:
            shutil.copy2(backup_path, corrupted_path)
            logging.info(f"Successfully recovered {corrupted_path} from backup")
            console.print(f"[green]✔ Recovered:[/green] {corrupted_path} from backup.")
        except Exception as e:
            logging.error(f"Failed to recover {corrupted_path}: {str(e)}")
            console.print(f"[red]✘ Failed to recover:[/red] {corrupted_path}")

def find_and_recover(original_dir, backup_dir, dry_run=False):
    logging.info(f"Starting recovery process - Original: {original_dir}, Backup: {backup_dir}, Dry Run: {dry_run}")
    files_restored = 0
    for root, _, files in os.walk(original_dir):
        for file in files:
            original_path = os.path.join(root, file)
            rel_path = os.path.relpath(original_path, original_dir)
            backup_path = os.path.join(backup_dir, rel_path)
            
            logging.debug(f"Checking file: {original_path}")
            original_hash = calculate_hash(original_path)
            backup_hash = calculate_hash(backup_path)

            if original_hash and backup_hash and original_hash != backup_hash:
                logging.info(f"Hash mismatch detected for {original_path}")
                recover_file(original_path, backup_path, dry_run)
                files_restored += 1
    
    if files_restored == 0:
        logging.info("No corrupted files found or all files are up-to-date")
        console.print("[yellow]No corrupted files were found or all are up-to-date.[/yellow]")
    else:
        logging.info(f"Recovery completed. Files restored: {files_restored}")

def main():
    print_ascii_banner()
    parser = argparse.ArgumentParser(
        description="Phoenix: Advanced Data Recovery After Ransomware or Corruption",
        epilog="Example: phoenix.py -o ./original_data -b ./backup --dry-run"
    )
    parser.add_argument("-o", "--original", required=True, help="Path to original (corrupted) directory")
    parser.add_argument("-b", "--backup", required=True, help="Path to backup directory")
    parser.add_argument("--dry-run", action="store_true", help="Simulate recovery without modifying files")
    parser.add_argument("--list", action="store_true", help="List backup files without restoring")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(args.debug)
    logging.info("Phoenix Data Recovery Tool Started")

    if args.list:
        console.print("[bold yellow]Available backup files:[/bold yellow]")
        for f in list_backup_files(args.backup):
            console.print(f"- {f}")
        return

    find_and_recover(args.original, args.backup, args.dry_run)
    logging.info("Phoenix Data Recovery Tool Completed")

if __name__ == "__main__":
    main()
