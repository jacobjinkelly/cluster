#!/usr/bin/python3

import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser("Download an experiment directory")

    parser.add_argument("timestamp", type=str, help="Timestamp of experiment")
    parser.add_argument("-r", "--root", type=str, default="/h/jkelly/kfac-pytorch/experiments/",
                        help="Remote root directory")
    parser.add_argument("-s", "--ssh", type=str, default="vd", help="SSH host")
    parser.add_argument("-e", "--exclude", type=str, default="*.pt", help="Exclude files matching this regex")

    args = parser.parse_args()

    # -a: recurse into subdirectories, turn on archive mode and all other options
    # -v: verbose
    # -e: use ssh for encryption
    # --exclude: exclude all checkpoint files (large and unnecessary)

    cmd = f"rsync -av -e ssh --exclude='{args.exclude}' {args.ssh}:{args.root}/{args.timestamp}/ {args.timestamp}/"
    subprocess.run(cmd, shell=True, check=True)


if __name__ == "__main__":
    main()
