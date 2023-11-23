$(document).ready(function () {
    // Event delegation for the "Save" button

    $('.todo.add-expense').on('click', '.save-button', function () {
        let valid = true; // Assume all amounts are valid

        // Traverse the DOM to find each expense item and validate
        $('.todo.add-expense .amount').each(function () {
            const amountInput = $(this);
            const label = amountInput.siblings('label').text();
            const amount = parseFloat(amountInput.val());

            if (isNaN(amount) || amount < 0) {
                //alert(`Please enter a valid amount for ${label}`);
                valid = false;
            } else {
                //alert(`Expense added: ${label} - $${amount}`);
            }
        });

        if (valid) {
            // Show a success message
            alert('Budget updated and saved!');

            // Reset all input fields to 0
            $('.todo.add-expense .amount').val('');
        }
        else{
            alert('Pleas enter a valid amount');
        }
    });

    // Event delegation for the "Cancel" button
    $('.todo.add-expense').on('click', '.cancel-button', function () {
        // Reset all input fields to 0
        $('.todo.add-expense .amount').val('');

        // Show a message
        alert('All fields reset. Plan your budget again.');
    });

    // Event delegation for clearing fields when the trash icon is clicked
    $('.todo.add-expense').on('click', '.clear-field', function () {
        const amountInput = $(this).siblings('.amount');
        amountInput.val('');
    });
        hideMessages();

});

function hideMessages() {
    var messages = document.querySelectorAll('.messages li');
    messages.forEach(function(msg) {
        setTimeout(function() {
            msg.style.display = 'none';
        }, 5000); // Hide messages after 5 seconds (adjust as needed)
    });
}