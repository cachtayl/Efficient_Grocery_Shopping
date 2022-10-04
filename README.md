# Groceries List Generator
<div>
    <h3>Description:</h3> <p>Wouldn't it be nice if your grocery shopping list was automatically sorted by your item's aisle number.
    With a sorted list you would never again wander throughout the store looking for items, traversing back and forth, wasting precious time.
    This application will generate a sorted grocery shopping list for you, so you can be in and checking out ASAP!</p>
    <p><b>How to run:</b>
    <ol type="1">
    <li>Click on Groceries-List-Generator-Installer.exe</li>
    <li>Download the Groceries-List-Generator-Installer.exe</li>
    <li>Follow the Installer instructions</li>
    <li>Open Groceries List Generator.exe</li>
    <li>Reference this page for help</li>
    </ol>
    </p>
    <p><b>Note: </b>Currently the application will come with an example store, "Vons / Laurel Canyon Blvd, Los Angeles, CA".</p>
    <p><b>Features: </b>
    <li>Add your local store for later use</li>
    <li>Delete a store from your database</li>
    <li>Edit a store from your database</li>
    <li>Make a shopping list by inputing an item and selecting the aisle it would be in from the dropdown box</li>
    <p>
    <!-- <img src="media/screenshot.PNG" alt="MainMenu" width="900" height="800"><br> -->
    <p><b>Current Limitations(Will be fixed in later versions):</b>
    <li>User runs their own database of stores, should be sharable or pulling from a greater database</li>
    <li>No export feature of the sorted list</li>
    <li>Database is run through a json file</li>
    <li>Dropdown list for the associated aisle should be searchable, should be easier to find the aisle your item would be in</li>
    <p>
    <p><b>High-level GUI Architecture:</b> There is a stacked layout that populates the main window of this application. Within that stacked layout there are three pages that can visually overwrite eachother, main menu page, register a store page, and generate sorted list page. The menu and register pages are created at startup and will update their contents everytime the user changes page. However, the generate sorted list page will be dynamically created and deleted on a need basis. It will delete itself after it's event loop has ended, i.e goes back to main menu.</p>
    <h1> Contributors </h1>
    <p>If you'd like to contribute, please fork the repository and make changes as you'd like. <br><b>Pull requests are warmly welcome.</b></p>
    <h1> License </h1>
    <p>MIT License 2022 - Cameron Taylor</p>
</div>
