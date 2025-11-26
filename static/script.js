document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('generateForm');
    const generateBtn = document.getElementById('generateBtn');
    const resultSection = document.getElementById('resultSection');
    const quoteText = document.getElementById('quoteText');
    const captionText = document.getElementById('captionText');
    const generatedImage = document.getElementById('generatedImage');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const downloadBtn = document.getElementById('downloadBtn');
    const copyQuoteBtn = document.getElementById('copyQuoteBtn');
    const copyCaptionBtn = document.getElementById('copyCaptionBtn');

    const randomBtn = document.getElementById('randomBtn');

    // Reusable generation function
    async function generateContent(promptValue, descriptionValue = "") {
        // UI State: Loading
        generateBtn.disabled = true;
        randomBtn.disabled = true;
        generateBtn.textContent = 'Generating...';
        resultSection.classList.remove('hidden');

        // Reset UI
        quoteText.textContent = 'Thinking...';
        captionText.value = 'Generating caption...';
        generatedImage.classList.add('hidden');
        loadingSpinner.classList.remove('hidden');
        downloadBtn.classList.add('hidden');

        const data = {
            prompt: promptValue,
            description: descriptionValue
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
            captionText.value = result.caption;

            // Handle image loading
            generatedImage.onload = () => {
                loadingSpinner.classList.add('hidden');
                generatedImage.classList.remove('hidden');
                downloadBtn.classList.remove('hidden');
            };
            generatedImage.src = result.image_url;

        } catch (error) {
            console.error('Error:', error);
            quoteText.textContent = 'An error occurred. Please try again.';
            captionText.value = '';
            loadingSpinner.classList.add('hidden');
        } finally {
            generateBtn.disabled = false;
            randomBtn.disabled = false;
            generateBtn.textContent = 'Generate';
        }
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        await generateContent(formData.get('prompt'), formData.get('description'));
    });

    randomBtn.addEventListener('click', async () => {
        document.getElementById('prompt').value = 'random';
        document.getElementById('description').value = '';
        await generateContent('random');
    });

    // Button Handlers
    downloadBtn.addEventListener('click', () => {
        const link = document.createElement('a');
        link.href = generatedImage.src;
        link.download = 'cosmic-quote.png';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });

    copyQuoteBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(quoteText.textContent).then(() => {
            const originalText = copyQuoteBtn.textContent;
            copyQuoteBtn.textContent = '✅ Copied!';
            setTimeout(() => copyQuoteBtn.textContent = originalText, 2000);
        });
    });

    copyCaptionBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(captionText.value).then(() => {
            const originalText = copyCaptionBtn.textContent;
            copyCaptionBtn.textContent = '✅ Copied!';
            setTimeout(() => copyCaptionBtn.textContent = originalText, 2000);
        });
    });
});
