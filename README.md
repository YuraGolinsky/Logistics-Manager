



The program contains a calculator for the cost of sleeping on a route with a route, the cost of sleeping for 100 km, the amount of luggage and corrections due to the weather. It was created using the additional Tkinter library for the graphical interface and JSON for saving routes to a file. Axis of main functional capabilities of the programs:

Main functions of the program:
1. Entering the customer's data: the program allows the customer to enter data for the route, such as name, destination, destination, get-up, sleepover, baggage.

2. Weather correction: the program connects to the OpenWeather API to retrieve data about the temperature in Kiev. When the temperature drops below 0°C, the air temperature increases by 15% (like a butt).
· orrection = 0 — correction value equal to 0 is installed on the cob.
· if temperature < 0: — if the temperature is less than 0°C (cold weather), 15% is added to the correction.
· if humidity > 80: - if the humidity is more than 80% (high humidity), 10% is added before correction.
· if wind_speed > 15: — if the wind speed exceeds 15 km/year (strong wind), 5% is added before correction.

Correction logic:
Cold weather (temperature < 0°C): the correction increases by 15%, so in the cold weather you may need more heat or other expenses (for example, for heating the car).
High moisture content (volost content > 80%): the correction increases by 10%, since a high level of moisture content can affect the efficiency of operating systems.
Strong wind (wind speed > 15 km/year): an additional 5% is added, because strong wind can increase the support of the wind, which flows into the weather and other aspects.



3. Restoration of sleeping expenses: the program automatically adjusts the amount of sleep, the insurance of the patient, the amount of sleep, the luggage and the correction for the weather.

4. Saving data to a file: all routes are saved to a JSON file (`routes.json`), and they may be saved when the program is launched.

5. Display of routes: the program displays all saved routes in a table with the following columns:
 - I'm
 - Stars
 - Kudi
 - Vidstan (km)
 - Vitrati pavement (l/100 km)
 - Zagalne bedroom (l)

   ![image](https://github.com/user-attachments/assets/30168f2c-5901-4181-a713-ca00e7a02198)



6. Graphical interface: the program interface allows you to manually enter data, press buttons and view the results table. There are stylish buttons and input fields with fonts that reflect current design benefits.

How the program works:
1. Data storage: when the program starts, it checks the availability of the `routes.json` file to save routes. If the file does not exist, it is created.

2. Calculation of travel expenses: when you press the “Explore route” button, the program will conclude the calculation of your expenses based on the adjustment of the entered data and weather corrections.


3. Displaying the results: after the breakdown, the operator receives notifications with the results, as well as the saving routes are updated in the table.

![image](https://github.com/user-attachments/assets/eda4946f-86cd-41d3-8aa2-cdedaf61a3c6)




Saving data in json
![image](https://github.com/user-attachments/assets/38804be7-2839-4ecf-9de1-1aed60cbeafe)
