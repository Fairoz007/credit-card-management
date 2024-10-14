
// Example of adding an expense
document.getElementById('expense-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const amount = document.getElementById('amount').value;
    const category = document.getElementById('category').value;
    const date = document.getElementById('date').value;
    const payment_method = document.getElementById('payment_method').value;
    const description = document.getElementById('description').value;

    fetch('/expense', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            amount: amount,
            category: category,
            date: date,
            payment_method: payment_method,
            description: description
        })
    }).then(response => response.json()).then(data => {
        alert(data.msg);
    }).catch(error => console.log(error));
});
