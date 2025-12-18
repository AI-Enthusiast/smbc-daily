import os
import glob
from pathlib import Path


def get_most_recent_comic():
    """
    Find the most recent SMBC comic in the data directory.
    Returns: tuple of (date, comic_title, image_path, metadata) or None if no comic found
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(project_root, 'data')

    if not os.path.exists(data_dir):
        print(f"data directory not found: {data_dir}")
        return None

    # Get all date directories, sorted in reverse order (most recent first)
    date_dirs = sorted([d for d in os.listdir(data_dir)
                       if os.path.isdir(os.path.join(data_dir, d))],
                      reverse=True)

    if not date_dirs:
        print("No date directories found in data folder")
        return None

    # Get the most recent date directory
    most_recent_date = date_dirs[0]
    most_recent_dir = os.path.join(data_dir, most_recent_date)

    # Find PNG files in that directory
    png_files = glob.glob(os.path.join(most_recent_dir, '*.png'))

    if not png_files:
        print(f"No PNG files found in {most_recent_dir}")
        return None

    # Get the first PNG file (there should typically be only one)
    image_path = png_files[0]
    comic_title = Path(image_path).stem  # Get filename without extension

    # Read metadata file if it exists
    metadata_file = os.path.join(most_recent_dir, f"{comic_title}_metadata.txt")
    metadata = {}
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()

    # Return relative path from project root
    rel_image_path = os.path.relpath(image_path, project_root)

    # URL-encode spaces for GitHub compatibility
    rel_image_path = rel_image_path.replace(' ', '%20')

    return (most_recent_date, comic_title, rel_image_path, metadata)


def update_readme():
    """
    Update the README.md file with the most recent SMBC comic.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    readme_path = os.path.join(project_root, 'README.md')

    comic_info = get_most_recent_comic()

    if not comic_info:
        print("No comic found to update README")
        return

    date, title, image_path, metadata = comic_info

    # Extract metadata fields
    publish_date = metadata.get('Date', date)
    hover_text = metadata.get('Hover Text', '')

    # Create the README content
    readme_content = f"""# SMBC Daily

#### {publish_date}

## {title}

![{title}]({image_path})

"""

    # Add hover text if available
    if hover_text:
        readme_content += f"**Hover Text:** {hover_text}\n\n"

    readme_content += """---

*This README is automatically updated with the latest SMBC comic.*
"""

    # Write to README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"README updated successfully with comic: {title}")


if __name__ == "__main__":
    update_readme()

