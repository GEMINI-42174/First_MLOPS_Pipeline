import argparse
import numpy as np
from clearml import Dataset
import os


def save_preprocessed_data(data, labels, data_filename, labels_filename):
    import argparse
    import numpy as np
    from clearml import Dataset
    import os

    np.save(data_filename, data)
    np.save(labels_filename, labels)


def preprocess_and_upload_cifar10(
    raw_dataset_id, processed_dataset_project, processed_dataset_name
):
    import argparse
    import numpy as np
    from clearml import Dataset
    import os

    raw_dataset = Dataset.get(dataset_id=raw_dataset_id)
    raw_data_path = raw_dataset.get_local_copy()

    # Load the numpy arrays from the raw dataset
    train_images = np.load(f"{raw_data_path}/train_images.npy")
    train_labels = np.load(f"{raw_data_path}/train_labels.npy")
    test_images = np.load(f"{raw_data_path}/test_images.npy")
    test_labels = np.load(f"{raw_data_path}/test_labels.npy")

    # Preprocess the images (normalize the pixel values)
    train_images, test_images = train_images / 255.0, test_images / 255.0

    # Save the preprocessed arrays to files
    save_preprocessed_data(
        train_images,
        train_labels,
        "train_images_preprocessed.npy",
        "train_labels_preprocessed.npy",
    )
    save_preprocessed_data(
        test_images,
        test_labels,
        "test_images_preprocessed.npy",
        "test_labels_preprocessed.npy",
    )

    # Create a new ClearML dataset for the preprocessed data
    processed_dataset = Dataset.create(
        dataset_name=processed_dataset_name,
        dataset_project=processed_dataset_project,
        parent_datasets=[raw_dataset_id],
    )

    # Add the saved numpy files to the dataset
    processed_dataset.add_files("train_images_preprocessed.npy")
    processed_dataset.add_files("train_labels_preprocessed.npy")
    processed_dataset.add_files("test_images_preprocessed.npy")
    processed_dataset.add_files("test_labels_preprocessed.npy")

    # Upload the dataset to ClearML
    processed_dataset.upload()
    processed_dataset.finalize()

    # Clean up: Remove the numpy files after upload
    os.remove("train_images_preprocessed.npy")
    os.remove("train_labels_preprocessed.npy")
    os.remove("test_images_preprocessed.npy")
    os.remove("test_labels_preprocessed.npy")

    print(f"Preprocessed CIFAR-10 dataset uploaded with ID: {processed_dataset.id}")
    return processed_dataset.id


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Preprocess and Upload CIFAR-10 Data to ClearML"
    )
    parser.add_argument(
        "--raw_dataset_id",
        type=str,
        required=True,
        help="ID of the raw CIFAR-10 dataset in ClearML",
    )
    parser.add_argument(
        "--processed_dataset_project",
        type=str,
        required=True,
        help="ClearML project name for the processed dataset",
    )
    parser.add_argument(
        "--processed_dataset_name",
        type=str,
        required=True,
        help="Name for the processed dataset in ClearML",
    )
    args = parser.parse_args()
    preprocess_and_upload_cifar10(
        args.raw_dataset_id, args.processed_dataset_project, args.processed_dataset_name
    )