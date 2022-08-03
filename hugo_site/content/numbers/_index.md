---
title: "Numbers"
menu: "numbsres"
draft: false
description: "An about section for an about page, Madness I tell you! Madness!"
---
<p> Complete the form below to see statistics about that time period!</p>
<form action="/numbers">
    <!-- Select Date -->
    <label for="start_date">Start Date:</label><br>
    <input type="date" id="start_date" name="start_date"></br>
    <label for="end_date">End Date:</label><br>
    <input type="date" id="end_date" name="end_date"></br>
    <!-- Select Sensor -->
    <p>Sensor</p>
    <input type="radio" id="indoor" name="sensor" value="HTML">
    <label for="sensor">Indoor</label><br>
    <input type="radio" id="outdoor" name="sensor" value="HTML">
    <label for="sensor">Outdoor</label><br>
    <!-- Send -->
    <input type="submit" value="Submit">
</form>