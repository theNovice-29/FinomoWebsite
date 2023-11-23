$(document).ready(function () {
    // Add a click event listener to the sorting icon
    $('.bx-filter').on('click', function () {
        // Get the table body
        const tableBody = $('table tbody');

        // Get all rows in the table body
        const rows = tableBody.find('tr').toArray();

        // Sort the rows based on the User column
        rows.sort(function (a, b) {
            const textA = $(a).find('td:first-child p').text();
            const textB = $(b).find('td:first-child p').text();
            return textA.localeCompare(textB);
        });

        // Clear the table body
        tableBody.empty();

        // Append the sorted rows back to the table body
        $.each(rows, function (index, row) {
            tableBody.append(row);
        });

        // Display a message indicating that the table is sorted
        const sortMessage = $('<p>').text('Table sorted according to users');
        sortMessage.addClass('sort-message');
        $('.sort').append(sortMessage);

        // Remove the message after a few seconds
        setTimeout(function () {
            sortMessage.remove();
        }, 3000); // Remove the message after 3 seconds (adjust as needed)
    });
});

