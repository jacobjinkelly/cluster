#!/usr/bin/python3

import argparse
import os
import shutil
import sys
import subprocess
from datetime import datetime

assert sys.version_info.major == 3
assert sys.version_info.minor >= 6


def get_args():
    parser = argparse.ArgumentParser("Launch a sweep of jobs")

    # arguments that will be set for most sweeps
    parser.add_argument("-p", "--partition", type=str, default="t4v2")
    parser.add_argument("-j", "--j_name", type=str, required=True)
    parser.add_argument("-f", "--file", type=str, required=True)
    parser.add_argument("-a", "--args", type=str)
    parser.add_argument("-q", "--q", type=str, required=True)

    # default arguments that will rarely be changed
    parser.add_argument("--experiment_dir", type=str, default="experiments")

    return parser.parse_args()


def setup_dirs(args):
    # create the directory for the sweep
    exp_dir = os.path.join(args.experiment_dir, datetime.now().strftime("%F-%H-%M-%S"))
    os.makedirs(exp_dir)

    # copy files for checking sweeps
    shutil.copy("check.sh", exp_dir)
    shutil.copy("param_check.sh", exp_dir)

    # record git state
    subprocess_kwargs = {
        "shell": True,
        "check": True,
        "capture_output": True
    }
    git_commit_state_file = os.path.join(exp_dir, "commit.state")
    with open(git_commit_state_file, "w") as f:
        subprocess.run("git rev-parse HEAD", stdout=f, stderr=f, **subprocess_kwargs)
    git_diff_patch_file = os.path.join(exp_dir, "diff.patch")
    command = subprocess.run(['ls', '-l'], capture_output=True)

    sys.stdout.buffer.write(command.stdout)
    sys.stderr.buffer.write(command.stderr)
    sys.exit(command.returncode)


def main():
    args = get_args()

    setup_dirs(args)


if __name__ == "__main__":
    main()
