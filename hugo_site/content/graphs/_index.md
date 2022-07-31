---
title: "Graphs"
menu: "graphs"
draft: false
description: "An about section for an about page, Madness I tell you! Madness!"
---
<p> Complete the form below to generate a graph showing that information!</p>
<form action="">
    <!-- Select Date -->
    <label for="start_date">Start Date:</label><br>
    <input type="date" id="start_date" name="start_date"></br>
    <label for="end_date">End Date:</label><br>
    <input type="date" id="end_date" name="end_date"></br>
    <!-- Select Sensor -->
    <p>Sensor</p>
    <input type="checkbox" id="indoor_sensor" name="indoor_sensor" value="Indoor">
    <label for="indoor_sensor">Indoor</label><br>
    <input type="checkbox" id="outdoor_sensor" name="outdoor_sensor" value="Indoor">
    <label for="sensor">Outdoor</label><br>
    <!-- Send -->
    <input type="submit" value="Submit">
</form>