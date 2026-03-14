import argparse
import random
import shutil
from pathlib import Path


VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def list_class_folders(source_dir: Path):
    return [path for path in source_dir.iterdir() if path.is_dir()]


def list_images(class_dir: Path):
    return [
        path
        for path in class_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in VALID_EXTENSIONS
    ]


def ensure_split_dirs(target_dir: Path, class_name: str):
    for split_name in ["train", "val", "test"]:
        (target_dir / split_name / class_name).mkdir(parents=True, exist_ok=True)


def clear_split_dirs(target_dir: Path):
    for split_name in ["train", "val", "test"]:
        split_path = target_dir / split_name
        if split_path.exists():
            shutil.rmtree(split_path)


def split_indices(total_items: int, train_ratio: float, val_ratio: float):
    train_count = int(total_items * train_ratio)
    val_count = int(total_items * val_ratio)
    test_count = total_items - train_count - val_count
    return train_count, val_count, test_count


def copy_group(files, output_dir: Path):
    for file_path in files:
        shutil.copy2(file_path, output_dir / file_path.name)


def prepare_dataset(source_dir: str, target_data_dir: str, train_ratio: float, val_ratio: float, seed: int, clean: bool):
    source_path = Path(source_dir)
    target_path = Path(target_data_dir)

    if not source_path.exists() or not source_path.is_dir():
        raise ValueError(f"Invalid source directory: {source_path}")

    if train_ratio <= 0 or val_ratio <= 0 or (train_ratio + val_ratio) >= 1:
        raise ValueError("Use valid ratios where train_ratio > 0, val_ratio > 0, and train_ratio + val_ratio < 1")

    class_folders = list_class_folders(source_path)
    if not class_folders:
        raise ValueError(f"No class folders found in source directory: {source_path}")

    if clean:
        clear_split_dirs(target_path)

    random.seed(seed)
    split_summary = {}

    for class_folder in class_folders:
        class_name = class_folder.name
        images = list_images(class_folder)

        if not images:
            continue

        random.shuffle(images)
        train_count, val_count, test_count = split_indices(
            total_items=len(images),
            train_ratio=train_ratio,
            val_ratio=val_ratio,
        )

        train_files = images[:train_count]
        val_files = images[train_count:train_count + val_count]
        test_files = images[train_count + val_count:train_count + val_count + test_count]

        ensure_split_dirs(target_path, class_name)

        copy_group(train_files, target_path / "train" / class_name)
        copy_group(val_files, target_path / "val" / class_name)
        copy_group(test_files, target_path / "test" / class_name)

        split_summary[class_name] = {
            "total": len(images),
            "train": len(train_files),
            "val": len(val_files),
            "test": len(test_files),
        }

    return split_summary


def parse_args():
    parser = argparse.ArgumentParser(description="Prepare train/val/test split from class-wise image folders.")
    parser.add_argument("--source", required=True, help="Path with class folders containing raw images")
    parser.add_argument("--target", default="data", help="Target data directory where train/val/test are created")
    parser.add_argument("--train-ratio", type=float, default=0.8, help="Train split ratio")
    parser.add_argument("--val-ratio", type=float, default=0.1, help="Validation split ratio")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--clean", action="store_true", help="Delete existing train/val/test folders before split")
    return parser.parse_args()


def main():
    args = parse_args()
    summary = prepare_dataset(
        source_dir=args.source,
        target_data_dir=args.target,
        train_ratio=args.train_ratio,
        val_ratio=args.val_ratio,
        seed=args.seed,
        clean=args.clean,
    )

    if not summary:
        print("No images found in source class folders.")
        return

    print("Dataset split completed.")
    for class_name, stats in sorted(summary.items()):
        print(
            f"{class_name}: total={stats['total']} train={stats['train']} val={stats['val']} test={stats['test']}"
        )


if __name__ == "__main__":
    main()
