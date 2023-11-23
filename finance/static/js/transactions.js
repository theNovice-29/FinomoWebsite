$(document).ready(function() {
  $('#search-form').on('submit', function(event) {
    event.preventDefault();

    var searchQuery = $('#search-input').val();

    $.ajax({
      url: '/transactions/search_transactions/',
      method: 'GET',
      data: { query: searchQuery },
      success: function(data) {
        // Clear the search results table
        $('tbody').empty();
        if (data.transactions.length === 0) {
          $('#error-message').text('No matching transactions found.').show();
          setTimeout(function() {
            $('#error-message').fadeOut();
            window.location.href = '/dashboard/transactions/';
          }, 3000); // Hides the error message after 3 seconds
        } else {
          $('#error-message').hide();
        // Append the search results to the table
        data.transactions.forEach(function(transaction) {
          console.log(transaction)
          var row = "<tr>";
          row += "<td><a href='/finance/updateTransaction/" + transaction.transaction_number + "'>" + transaction.transaction_number + "</a></td>";
          row += "<td>" + transaction.purpose + "</td>";
          row += "<td>" + transaction.category + "</td>";
          row += "<td>" + transaction.date + "</td>";
          row += "<td class='amount'>" + transaction.amount + "</td>";
          row += "</tr>";

          $('tbody').append(row);
        });
        }
      },
            error: function(error) {
                console.log('Search request failed'); // Handle error
      }
    });
  });

  function checkFormFields() {
            var purpose = $('#purpose').val();
            var amount = $('#amount').val();
            var category = $('input[name="category"]:checked').val();

            // Check if any of the fields are empty
            if (!purpose || !amount || !category) {
                showErrorBox(); // Display the error message box
                return false;   // Return false to prevent form submission
            }
            else{
              showConfirmationBox();
              return true;
            }

        }

        // Function to display the error response box with a timeout
        function showErrorBox() {
            $('#error-message-expense').fadeIn();
            setTimeout(function() {
                $('#error-message-expense').fadeOut();
            }, 3000);  // Timeout after 3 seconds (3000 milliseconds)
        }

        // Event listener for form submission
        $('#expense-form').on('submit', function(event) {
            if (!checkFormFields()) {
                event.preventDefault(); // Prevent form submission if fields are not filled
            }
        });

  function showConfirmationBox() {
            $('#confirmation-box').fadeIn();
            setTimeout(function() {
                $('#confirmation-box').fadeOut();
            }, 3000);

            // Move messages to the confirmation box
            var messages = $('.messages');
            messages.find('.success-message').appendTo('#confirmation-box');
        }

        $('#expense-form').on('submit', function(event) {
            if (!checkFormFields()) {
                event.preventDefault();
            } else {
                showConfirmationBox();
            }
        });
});