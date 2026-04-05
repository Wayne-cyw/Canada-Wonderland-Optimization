# Canada Wonderland Optimization Program

## Included Rides

Rides are organized by park zone. All zones and rides below are supported by the program.

| **Grande World Expo** | Antique Carrousel, Flight Deck, Swing of the Century

| **Action Zone** | Backlot Stunt Coaster, Behemoth, Psyclone, Skyhawk, Sledge Hammer, SlingShot, WindSeeker

| **Alpenfest** | AlpenFury, Klockwerks, Krachenwagen, Shockwave, The Fly, Thunder Run, Wonder Mountain's Guardian 

| **Frontier Canada** | Flying Canoes, Lumberjack, Mighty Canadian Minebuster, Soaring Timbers, Timberwolf Falls, Tundra Twister, Vortex, White Water Canyon, Yukon Striker

| **Planet Snoopy** | Beagle Brigade Airfield, Boo Blasters on Boo Hill, Character Carousel, Ghoster Coaster, Joe Cool's Dodgem School, Lucy's Tugboat, PEANUTS 500, Sally's Love Buggies, SNOOPY vs Red Baron, SNOOPY's Revolution, SNOOPY's Racing Railway, SNOOPY's Space Race, Swan Lake, The Pumpkin Patch, Woodstock Whirlybirds

| **KidZville** | Blast Off!, Flying Eagles, Frequent Flyers, Jokey's Jalopies, Jumpin' Jet, KidZville Station, Maple Park Treehouse, Silver Streak, Sugar Shack, Swing Time, Taxi Jam, Treetop Adventure

| **Medieval Faire** | Dragon Fyre, Drop Tower, Leviathan, Riptide, Speed City Raceway, Spinovator, The Bat, Viking's Rage, Wilde Beast, Wilde Knight Mares

| **Splash Works** | Barracuda Blaster, Black Hole, Lakeside Lagoon Pool, Lakeside Lagoon Slides, Lazy River, Moosehorn Falls, Mountain Bay Cliffs, Muskoka Plunge, Pumphouse, Riptide Racer, Splash Station, Super Soaker, The Plunge, Typhoon, Waterways, Whirlwinds, White Water Bay


## Setup

**Step 1 — Download the project**

Download or clone the repository folder to your computer.

**Step 2 — Install the required dependency**

```bash
pip install pick
```

**Step 3 — Open a terminal and navigate to the project folder**

```bash
cd path/to/Canada Wonderland Optimization
```

> **Important:** The program uses a full-screen terminal interface. Maximize or full-screen your terminal window before running, otherwise the display may not render correctly and an error may occur.


## How to Use

**Step 1 — Run the program**

```bash
python main.py
```
or 
```bash
python3 main.py
```

A splash screen will appear briefly, then the program will guide you through three steps.


**Step 2 — Select your rides**

A multi-column menu will appear showing all available rides organized by zone.

- Use the **arrow keys** to navigate between rides and zones
- Press **SPACE** to select or deselect a ride (`[x]` means selected)
- Press **ENTER** to confirm your selections and continue

Select only the rides you are interested in visiting. You are not required to select rides from every zone.

**Step 3 — Choose your time window**

You will be asked to pick your **arrival time** and then your **departure time** from a list of 30-minute intervals (10:00 AM to 8:00 PM).

- Use the **arrow keys** to highlight a time
- Press **ENTER** to confirm

The program will use the difference between these two times as your total available budget.


**Step 4 — View your optimal route**

The program will calculate and display the optimal order to visit your selected rides, maximizing the number of rides you can complete within your time window. Rides are listed in the recommended visit order.

Press any key to exit when done.


## Limitations

- **Performance with many rides selected.** The optimization algorithm runs in O(2^n × n²) time. Selecting more than approximately 20 rides may cause the program to run slowly.

- **Time intervals are 30 minutes.** Arrival and departure times can only be set in 30-minute increments between 10:00 AM and 8:00 PM. This is to avoid user maunal inputing time causing formatting error.

- **Terminal window size.** The program requires a sufficiently large terminal window. If the window is too small, the interface may raise an error. Full-screening the terminal is recommended.

- **Ride availability not accounted for.** The program assumes all selected rides are open and operating. It does not account for ride closures, seasonal availability, or height/age restrictions.
