$(document).ready(function () {
    
  $('#save-button').on('click', function(event) {
        event.preventDefault(); // Prevent the default action of the button

        // Perform an AJAX request to update the transaction
        $.ajax({
            url: '/transactions/',
            method: 'POST',
            data: $('#detail').serialize(), // Serialize the form data
            success: function(data) {
                // Display the success message
                $('.confirmation-message').text('Transaction updated successfully.').addClass('success-message');

                // Clear the message after 3 seconds
                setTimeout(function() {
                    $('.confirmation-message').text('').removeClass('success-message');
                }, 3000);
            },
            error: function(error) {
                console.log('Transaction update failed.'); // Handle error scenario
            }
        });
    });
});
