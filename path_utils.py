def get_path_and_distances():
    path = [
        (492, 297),  # Hobbiton
        (588, 319),  # Tom Bombadil's House
        (623, 303),  # Bree
        (717, 293),  # Weathertop
        (928, 285),  # Rivendell
        (928, 353),  # Caradhras
        (890, 414),  # Moria Gate
        (1012, 457),  # Lothlorien
        (1138, 656),  # Falls of Rauros
        (1181, 645),  # Emyn Muil
        (1230, 655),  # Dead Marshes
        (1294, 659),  # Morannon
        (1260, 675),  # North Itlien
        (1263, 735),  # Ithlien
        (1281, 747),  # Minas Morgul
        (1305, 744),  # Stairs of Cirith Ungol
        (1283, 692),  # Shelob's Lair
        (1312, 686),  # Mordor
        (1356, 693),  # Mordor 2
        (1359, 728),  # Mount Doom
    ]

    distances = [
        100,  # Hobbiton to Tom Bombadil's House (in miles)
        50,   # Tom Bombadil's House to Bree (in miles)
        150,  # Bree to Weathertop
        200,  # Weathertop to Rivendell
        100,  # Rivendell to Caradhras
        100,  # Caradhras to Moria Gate
        100,  # Moria Gate to Lothlorien
        200,  # Lothlorien to Falls of Rauros
        100,  # Falls of Rauros to Emyn Muil
        100,  # Emyn Muil to Dead Marshes
        100,  # Dead Marshes to Morannon
        50,   # Morannon to North Itlien
        60,   # North Itlien to Ithlien
        70,   # Ithlien to Minas Morgul
        40,   # Minas Morgul to Stairs of Cirith Ungol
        50,   # Stairs of Cirith Ungol to Shelob's Lair
        30,   # Shelob's Lair to Mordor
        40,   # Mordor to Mordor 2
        30    # Mordor 2 to Mount Doom
    ]

    return path, distances

def scale_coordinates(path, original_size, new_size):
    """
    Scale the coordinates of the path from the original size to the new size.
    """
    original_width, original_height = original_size
    new_width, new_height = new_size
    scale_x = new_width / original_width
    scale_y = new_height / original_height

    return [(int(x * scale_x), int(y * scale_y)) for x, y in path]

def get_current_position(distances, path, total_distance):
    """
    Calculate the current position based on the distance covered.
    """
    distance_covered = 0
    for i, dist in enumerate(distances):
        distance_covered += dist
        if total_distance <= distance_covered:
            ratio = (total_distance - (distance_covered - dist)) / dist
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            x = x1 + (x2 - x1) * ratio
            y = y1 + (y2 - y1) * ratio
            return (x, y)
    return path[-1]  # Return the last point if journey is complete

def get_location_name(index):
    location_names = [
        "Hobbiton", "Tom Bombadil's House", "Bree", "Weathertop", "Rivendell",
        "Caradhras", "Moria Gate", "Lothlorien", "Falls of Rauros", "Emyn Muil",
        "Dead Marshes", "Morannon", "North Itlien", "Ithlien", "Minas Morgul",
        "Stairs of Cirith Ungol", "Shelob's Lair", "Mordor", "Mordor 2", "Mount Doom"
    ]
    return location_names[index]
