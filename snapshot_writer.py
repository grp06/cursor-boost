import os

def write_snapshot(snapshot):
    with open("snapshot.txt", "w") as f:
        f.write(snapshot)
