document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('generateForm');
    const generateBtn = document.getElementById('generateBtn');
    const resultSection = document.getElementById('resultSection');
    const quoteText = document.getElementById('quoteText');
    const generatedImage = document.getElementById('generatedImage');
    const loadingSpinner = document.getElementById('loadingSpinner');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // UI State: Loading
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';
        resultSection.classList.remove('hidden');
        quoteText.textContent = 'Thinking...';
        generatedImage.classList.add('hidden');
        loadingSpinner.classList.remove('hidden');

        const formData = new FormData(form);
        const data = {
            prompt: formData.get('prompt'),
            description: formData.get('description')
        };

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json();

            // UI State: Success
            quoteText.textContent = `"${result.quote}"`;
            
            // Handle image loading
            generatedImage.onload = () => {
                loadingSpinner.classList.add('hidden');
                generatedImage.classList.remove('hidden');
            };
            generatedImage.src = result.image_url;

        } catch (error) {
            console.error('Error:', error);
            quoteText.textContent = 'An error occurred. Please try again.';
            loadingSpinner.classList.add('hidden');
        } finally {
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate';
        }
    });
});
