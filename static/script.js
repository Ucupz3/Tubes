document.getElementById('predictBtn').addEventListener('click', async () => {
    const text = document.getElementById('reviewInput').value;
    const resultContainer = document.getElementById('result');
    const sentimentResult = document.getElementById('sentimentResult');
    const processedText = document.getElementById('processedText');
    const btn = document.getElementById('predictBtn');

    if (!text.trim()) {
        alert('Please enter a review.');
        return;
    }

    btn.disabled = true;
    btn.textContent = 'Analyzing...';

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text }),
        });

        const data = await response.json();

        if (response.ok) {

            resultContainer.classList.remove('hidden');
            sentimentResult.textContent = data.sentiment;

            // FIX DI SINI
            updateCharts(data.positive_prob / 100, data.negative_prob / 100);

            processedText.textContent = data.processed_text;

            sentimentResult.className = 'sentiment-badge';
            if (data.sentiment === 'positive') {
                sentimentResult.classList.add('positive');
            } else {
                sentimentResult.classList.add('negative');
            }

        } else {
            alert('Error: ' + data.error);
        }

    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Analyze Sentiment';
    }
});
