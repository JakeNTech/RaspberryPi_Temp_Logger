---
title: "Numbers"
menu: "numbers"
draft: false
description: "An about section for an about page, Madness I tell you! Madness!"
---
<div id="stats_table">
    <p> Complete the form below to see statistics about that time period!</p>
    <div id="frm_fetch_numbers">
        <!-- Select Date -->
        <label for="start_date">Start Date:</label><br>
        <input type="date" id="start_date" name="start_date"></br>
        <label for="end_date">End Date:</label><br>
        <input type="date" id="end_date" name="end_date"></br>
        <!-- Send -->
        <input type="submit" value="Submit" onclick="get_statistics()">
    </div>
</div>

<script src="/assets/script.js"></script>