// Telugu Q&A Generator JavaScript

// Global variables
let currentQAPairs = [];
let originalParagraph = '';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Set up event listeners
    const form = document.getElementById('qaForm');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
    
    // Add clear form functionality
    const clearBtn = document.querySelector('[onclick="clearForm()"]');
    if (clearBtn) {
        clearBtn.addEventListener('click', clearForm);
    }
}

// Handle form submission
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const paragraph = document.getElementById('teluguParagraph').value.trim();
    const numQuestions = document.getElementById('numQuestions').value;
    const difficulty = document.getElementById('difficulty').value;
    
    if (!paragraph) {
        showAlert('దయచేసి తెలుగు పేరాగ్రాఫ్ ను ఎంటర్ చేయండి', 'warning');
        return;
    }
    
    if (!validateTeluguText(paragraph)) {
        showAlert('దయచేసి తెలుగు భాషలో పేరాగ్రాఫ్ ను ఎంటర్ చేయండి', 'warning');
        return;
    }
    
    // Show the section and the spinner
    showResultsSection(true);
    showLoading(true);
    scrollToResults();
    
    try {
        const response = await fetch('/api/generate-qa', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                paragraph: paragraph,
                num_questions: numQuestions,
                difficulty: difficulty
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentQAPairs = data.qa_pairs;
            originalParagraph = paragraph;
            displayResults(data.qa_pairs);
        } else {
            showAlert(data.error || 'ప్రశ్నలు రూపొందించడంలో లోపం', 'danger');
            showResultsSection(false); // Hide on error
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('సర్వర్ లోపం. దయచేసి తిరిగి ప్రయత్నించండి', 'danger');
        showResultsSection(false); // Hide on error
    } finally {
        showLoading(false); // This will now only hide the spinner
    }
}

// Display results
function displayResults(qaPairs) {
    const resultsContent = document.getElementById('resultsContent');
    if (!resultsContent) return;
    
    if (qaPairs.length === 0) {
        resultsContent.innerHTML = `
            <div class="alert alert-info">
                <i class="fas fa-info-circle me-2"></i>
                ప్రస్తుతానికి ప్రశ్నలు లేవు. దయచేసి మరో పేరాగ్రాఫ్ ప్రయత్నించండి.
            </div>
        `;
        return;
    }
    
    let html = `
        <div class="mb-3">
            <h5 class="text-primary">మొత్తం ప్రశ్నలు: ${qaPairs.length}</h5>
        </div>
        <div class="row">
    `;
    
    qaPairs.forEach((qa, index) => {
        html += `
            <div class="col-12 mb-4">
                <div class="card border-primary">
                    <div class="card-header bg-primary text-white">
                        <h6 class="mb-0">
                            <i class="fas fa-question-circle me-2"></i>
                            ప్రశ్న ${index + 1}
                        </h6>
                    </div>
                    <div class="card-body">
                        <p class="card-text">
                            <strong>ప్రశ్న:</strong> <span class="text-telugu">${qa.question}</span>
                        </p>
                        <p class="card-text">
                            <strong>ఉత్తరం:</strong> <span class="text-telugu">${qa.answer}</span>
                        </p>
                        <small class="text-muted">
                            <i class="fas fa-tag me-1"></i>
                            రకం: ${qa.type}
                        </small>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    resultsContent.innerHTML = html;
}

// Utility functions
function validateTeluguText(text) {
    const teluguPattern = /[\u0C00-\u0C7F]/;
    return teluguPattern.test(text);
}

function showAlert(message, type) {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the page
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function showLoading(show) {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.classList.toggle('d-none', !show);
    }
}

function showResultsSection(show) {
    const resultsSection = document.getElementById('results');
    if (resultsSection) {
        resultsSection.classList.toggle('d-none', !show);
    }
}

function scrollToGenerator() {
    const generator = document.getElementById('generator');
    if (generator) {
        generator.scrollIntoView({ behavior: 'smooth' });
    }
}

function scrollToResults() {
    const results = document.getElementById('results');
    if (results) {
        results.scrollIntoView({ behavior: 'smooth' });
    }
}

function clearForm() {
    const textarea = document.getElementById('teluguParagraph');
    if (textarea) {
        textarea.value = '';
    }
    showResultsSection(false);
}

// Export functions
function exportResults(format) {
    if (!currentQAPairs || currentQAPairs.length === 0) {
        showAlert('ఎగుమతి చేయడానికి ప్రశ్నలు లేవు', 'warning');
        return;
    }
    
    switch (format) {
        case 'json':
            exportAsJSON();
            break;
        case 'text':
            exportAsText();
            break;
        default:
            showAlert('అమాన్యమైన ఎగుమతి ఫార్మాట్', 'danger');
    }
}

function exportAsJSON() {
    const data = {
        original_paragraph: originalParagraph,
        qa_pairs: currentQAPairs,
        generated_at: new Date().toISOString(),
        total_questions: currentQAPairs.length
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `telugu-qa-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
}

function exportAsText() {
    let text = `తెలుగు ప్రశ్నోత్తరాలు\n`;
    text += `==================\n\n`;
    text += `అసలు పేరాగ్రాఫ్:\n${originalParagraph}\n\n`;
    text += `రూపొందించిన ప్రశ్నలు:\n\n`;
    
    currentQAPairs.forEach((qa, index) => {
        text += `${index + 1}. ${qa.question}\n`;
        text += `   ఉత్తరం: ${qa.answer}\n`;
        text += `   రకం: ${qa.type}\n\n`;
    });
    
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `telugu-qa-${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
}

function printResults() {
    if (!currentQAPairs || currentQAPairs.length === 0) {
        showAlert('ప్రింట్ చేయడానికి ప్రశ్నలు లేవు', 'warning');
        return;
    }
    
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
        <head>
            <title>తెలుగు ప్రశ్నోత్తరాలు</title>
            <style>
                body { font-family: 'Noto Sans Telugu', sans-serif; margin: 20px; }
                .question { font-weight: bold; color: #0d6efd; margin-top: 20px; }
                .answer { margin-left: 20px; margin-bottom: 10px; }
                .type { font-size: 0.9em; color: #6c757d; }
            </style>
        </head>
        <body>
            <h1>తెలుగు ప్రశ్నోత్తరాలు</h1>
            <p><strong>అసలు పేరాగ్రాఫ్:</strong> ${originalParagraph}</p>
            <hr>
            ${currentQAPairs.map((qa, i) => `
                <div class="question">${i + 1}. ${qa.question}</div>
                <div class="answer">${qa.answer}</div>
                <div class="type">రకం: ${qa.type}</div>
            `).join('')}
        </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.print();
}
