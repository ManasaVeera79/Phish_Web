document.addEventListener('DOMContentLoaded', () => {
  const checkButton = document.getElementById('checkButton');
  const urlInput = document.getElementById('urlInput');
  const resultDiv = document.getElementById('result');

  async function handleCheckButtonClick() {
    const url = urlInput.value.trim();

    if (!url) {
      resultDiv.textContent = ' Please enter a URL.';
      resultDiv.style.color = 'orange';
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
      });

      if (!response.ok) {
        throw new Error('Server responded with error');
      }

      const data = await response.json();

      if (data.prediction === 'unsafe') {
        resultDiv.textContent = ` Prediction: ${data.prediction}`;
        resultDiv.style.color = 'red';
      } else {
        resultDiv.textContent = ` Prediction: ${data.prediction}`;
        resultDiv.style.color = 'green';
      }
    } catch (error) {
      console.error('Error:', error);
      resultDiv.textContent = ' Error: Could not connect to the API. Is the Flask app running?';
      resultDiv.style.color = 'red';
    }
  }

  checkButton.addEventListener('click', handleCheckButtonClick);
});
