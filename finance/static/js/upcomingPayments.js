$(document).ready(function () {
    // Get the search query parameter from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const searchQuery = urlParams.get("payment");
 
    // Get the table body element where transaction data will be displayed
    const tableBody = $("table tbody");
 
    // Sample transaction data 
    const transactions = [
        { purpose: "Water Bill", amount: "$50.00" },
        { purpose: "Wi-Fi Bill", amount: "$30.00" },
        { purpose: "Electricity Bill", amount: "$75.00" },
        { purpose: "Mobile Plan Bill", amount: "$50.00" },
        { purpose: "Car Insurance", amount: "$30.00" },
        { purpose: "Home Rent", amount: "$75.00" },
        { purpose: "Utilities ", amount: "$50.00" },
        { purpose: "Water Bill 2", amount: "$30.00" },
        { purpose: "Amenities Bill", amount: "$75.00" },
    
    ];
 
    // Function to display transactions in the table
    function displayTransactions(data) {
        // Clear the table body
        tableBody.empty();
 
        // Check if there are matching transactions
        if (data.length === 0) {
            $("#error-message").show(); // Show error message
        } else {
            $("#error-message").hide(); // Hide error message
 
            // Loop through the transaction data and create table rows
            $.each(data, function (index, transaction) {
                const row = $("<tr>").html(`
                    <td>${transaction.purpose}</td>
                    <td>${transaction.amount}</td>
                `);
                tableBody.append(row);
            });
        }
    }
 
    // Simulated search logic
    if (searchQuery) {
        const matchingTransactions = transactions.filter((transaction) =>
            transaction.purpose.toLowerCase().includes(searchQuery.toLowerCase())
        );
        displayTransactions(matchingTransactions);
    } else {
        // If no search query provided, display all transactions
        displayTransactions(transactions);
    }
 });


