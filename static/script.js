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
            
            document.getElementById('positiveProb').textContent = `${data.positive_prob}%`;
            document.getElementById('negativeProb').textContent = `${data.negative_prob}%`;
            
            processedText.textContent = data.processed_text;

            sentimentResult.className = 'sentiment-badge'; // Reset classes
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
