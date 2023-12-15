import shutil
import os
import argparse

source_dir = "./templates"
dest_dir = "."

files = os.listdir(source_dir)


def main(problem_id):
    for file in files:
        src_path = os.path.join(source_dir, file)
        dest_path = os.path.join(dest_dir, file.replace("template", problem_id))
        shutil.copy2(src_path, dest_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem-id")
    args = parser.parse_args()
    if not args.problem_id:
        raise Exception("precise problem # -> --problem-id [id]")
    main(args.problem_id)