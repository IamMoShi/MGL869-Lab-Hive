def display_version_tree(version, level=0, visited=None):
    """
    Recursively display the version tree starting from a given version,
    showing only the version IDs in an indented tree structure.

    Args:
        version (Version): The starting version to display.
        level (int): The current depth in the tree (used for indentation).
        visited (set): A set to track visited versions to prevent infinite loops.
    """
    if visited is None:
        visited = set()

    # Prevent infinite recursion in case of cyclic relationships
    if version in visited:
        print(" " * (level * 4) + f"└── [Cyclic: {version.id}]")
        return
    visited.add(version)

    # Print the current version ID with proper indentation
    prefix = "└── " if level > 0 else ""  # Add "└── " only for non-root nodes
    print(" " * (level * 4) + prefix + f"{version.id} {version.getDate().date()}")

    # Recursively print each next version
    for next_version in sorted(version.next_versions, key=lambda v: v.id):
        display_version_tree(next_version, level + 1, visited)
