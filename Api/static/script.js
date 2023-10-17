let style = document.createElement('style');
style.innerHTML = `
#subtlesplice{
    color: red;
    
}

`;
document.head.appendChild(style);




document.addEventListener("DOMContentLoaded", async function() {
    try {
        // Get all the <p> elements on the page.
        let paragraphs = document.getElementsByTagName("p");

        // Choose a random <p> element.
        let randomIndex = Math.floor(Math.random() * paragraphs.length);
        let textElement = paragraphs[randomIndex];

        // Get the text content of the selected <p> element.
        let inputText = textElement.innerText;

        // Send the text content to the server for processing.
        let response = await fetch('http://127.0.0.1:5000/process_words', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ words: inputText })
        });

        if (response.ok) {
            let data = await response.json();
            let processedWords = data.processed_words;

            // Replace the original <p> element's text content with the processed text.
            textElement.innerHTML = processedWords;
        } else {
            // Handle the case where the response is not OK (e.g., HTTP error)
            console.error('Server returned an error:', response.statusText);
        }
    } catch (error) {
        // Handle any unexpected errors during fetch or processing
        console.error('Error during fetch operation', error);
    }
});
