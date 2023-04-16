const businesses = [
    { BusinessId: 1, BusinessName: 'Business 1' },
    { BusinessId: 2, BusinessName: 'Business 2' },
    { BusinessId: 3, BusinessName: 'Business 3' },
  ];
  
  export default function handleGet() {
    // Simulate fetching businesses from a database or API
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(businesses);
      }, 1000);
    });
  }
  