# middle_earth_tracker
# Middle-earth Walking Tracker

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [How It Works](#how-it-works)
- [Scaling and Distance Calculation](#scaling-and-distance-calculation)
- [Things In Progress](#things-in-progress)
- [Future Features](#future-features)
- [Current Bugs](#current-bugs)
- [Adjustments and Customization](#adjustments-and-customization)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

Welcome to the Middle-earth Walking Tracker! This program helps you visualize and track your walking or running progress on a map of Middle-earth. It's designed to motivate and inspire users by allowing them to embark on a virtual journey through the iconic locations from J.R.R. Tolkien's legendary universe.

## Features

- **Interactive Map**: An engaging, zoomable, and pannable map of Middle-earth.
- **Distance Tracking**: Enter your daily walking or running distance to progress on your journey.
- **Save and Load Progress**: Save your progress and load it later to continue your adventure.
- **Day Tracking**: Track the number of days since you started your journey.
- **Visual Indicators**: See your path, current location, and progress on the map.
- **Responsive UI**: User-friendly interface with easy-to-use controls.

## How It Works

1. **Map Display**: The program displays a map of Middle-earth, allowing users to zoom, pan, and interact with it.
2. **Distance Entry**: Users enter the distance they walked or ran into the input field, and the program updates their total distance covered.
3. **Save Progress**: Users can save their progress by entering a username. This saves the total distance and start date in an SQLite database.
4. **Load Progress**: Users can load their saved progress by selecting their username from a list. This retrieves the saved data and updates the map and distance accordingly.
5. **Day Tracking**: The program tracks the number of days elapsed since the user's journey started.

## Scaling and Distance Calculation

### Map Scaling

The map image is dynamically scaled based on the user's zoom level. This is achieved using the following steps:
1. The original image is loaded and displayed on the canvas.
2. When the user zooms in or out, the `self.image_scale` is adjusted.
3. The image is resized to match the new scale using the `PIL.Image.resize` method.
4. The resized image is then displayed on the canvas, and the scroll region is updated to match the new image size.
5. Path and location points are scaled accordingly to maintain accuracy.

### Distance Calculation

The total distance covered by the user is calculated by summing up the daily distances entered by the user. This total distance is then used to update the user's position on the map:
1. The user's total distance is compared to the distances between predefined locations on the map.
2. The user's current position is calculated by determining where the total distance fits within the cumulative distances between locations.
3. The map is updated to visually indicate the user's progress.

## Things In Progress

- **Improved Location Markers**: Enhancing the visibility and design of location markers on the map.
- **Refined Distance Updates**: Optimizing the distance entry and update mechanism for smoother performance.
- **Error Handling**: Implementing more robust error handling to manage unexpected inputs and scenarios.

## Future Features

- **Images for Locations**: Displaying images when reaching certain locations.
- **Text Displays for Points of Interest**: Showing text descriptions for points of interest.
- **Better Map Quality**: Improving the quality of the map image.
- **Random Encounters and Events**: Introducing random encounters and events that can help or hinder progress.
- **Light RPG Gameplay Elements**: Adding optional light RPG-style gameplay elements.
- **More Accurate Fellowship Path**: Mapping a more accurate path followed by the Fellowship.
- **Total Distance**: Tracking the total distance, which is approximately 1800 miles.

## Current Bugs

- **Resetting Progress**: Resetting progress can sometimes behave unexpectedly.
- **Location Colors**: Location colors may not always update correctly.

## Adjustments and Customization

- **Changing the Map Image**: Replace the `map-of-mearth.jpeg` file with another image of Middle-earth to customize the map. Ensure the image path is correctly set in the code.
- **Adjusting Zoom Levels**: Modify the `self.image_scale` value in the `zoom_in` and `zoom_out` methods to change the zoom sensitivity.
- **Customizing UI Elements**: Modify the Tkinter widget properties in the code to change the appearance and behavior of the UI elements.
- **Database Adjustments**: Update the `database.py` file to include additional fields or modify existing ones as needed.

## Getting Started

### Prerequisites

- Python 3.x
- SQLite3
- PIL (Pillow)
- Tkinter (comes with Python)

### Installation

1. Clone the repository or download the source code.
2. Ensure you have the required dependencies installed.
3. Run the `tracker.py` script to start the application.

### Usage

1. Open the application.
2. Enter your walking or running distance in the input field and click "Submit Distance."
3. Save your progress by entering a username.
4. Load your progress by selecting your username from the list.

## Contributing

Contributions are welcome! If you'd like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.


## Contact

For any questions or suggestions, please contact the project maintainer at [dtrefun@gmail.com].
