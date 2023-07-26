import json
import os


# function merging .json files (firefox bookmarks default format)
def merge(addition, masterfile):
    for bookmark in addition:
        if 'children' in bookmark and isinstance(bookmark['children'], list):
            nested = []
            merge(bookmark['children'], nested)
            bookmark['children'] = nested

        masterfile.append(bookmark)


if __name__ == "__main__":

    workdir = os.path.dirname(os.path.realpath(__file__))
    listdir = os.listdir(workdir)
    detected = [file for file in listdir if file.endswith(".json")]

    while not detected:
        print("No \'json\' files found in working directory, move files to scipts\' directory and re-run the script or provide paths manually.")
        user_input = input("Enter file paths, separated by spaces ('q' to quit):")
        if user_input.lower() == 'q':
            exit()
        detected = user_input.split()

    masterfile = []

    for file in detected:
        with open(file, 'r') as data:
            bookmarks = json.load(data)

            # checks if children are present and wether
            if 'children' in bookmarks and isinstance(bookmarks['children'], list):
                merge(bookmarks['children'], masterfile)

    masterfile.sort(key=lambda bookmark: bookmark.get('title', '').lower())

    output = os.path.join(workdir, "merged-bookmarks.json")

    with open(output, 'w') as output_file:
        json.dump({"title": "Merged Bookmarks", "children": masterfile}, output_file)


