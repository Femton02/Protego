let customers = [
    { id: 0, name: 'khaled', location: { address: {street: 'Tahrir street'} } },
    { id: 1, name: 'anas' },
    { id: 2, name: 'marwan' },
    { id: 3, name: 'seif', location: { address: {city: 'cairo'} } }
  ];
  let customer = customers.find(cust => cust.location.address.city === 'cairo');
  console.log(customer);