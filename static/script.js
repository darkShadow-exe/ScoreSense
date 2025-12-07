// Graph loading function
async function loadGraph(graphType, params = {}) {
    const container = document.getElementById('graph-container');
    
    if (!container) {
        console.error('Graph container not found');
        return;
    }
    
    // Show loading
    container.innerHTML = '<div style="padding: 40px; text-align: center;"><p>Loading graph...</p></div>';
    
    try {
        // Build URL with parameters
        let url = `/graph/${graphType}`;
        const queryParams = new URLSearchParams(params).toString();
        if (queryParams) {
            url += `?${queryParams}`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.error) {
            container.innerHTML = `<div style="padding: 20px; color: #dc3545;">${data.error}</div>`;
            return;
        }
        
        if (data.image) {
            container.innerHTML = `<img src="data:image/png;base64,${data.image}" alt="${graphType} graph">`;
        }
    } catch (error) {
        container.innerHTML = `<div style="padding: 20px; color: #dc3545;">Error loading graph: ${error.message}</div>`;
    }
}

// Load student-specific graph
function loadStudentGraph(studentName) {
    loadGraph('student_bar', { student: studentName });
}

// Load comparison graph for a subject
function loadComparisonGraph(subject) {
    loadGraph('comparison', { subject: subject });
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const inputs = form.querySelectorAll('input[required]');
    let valid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#dc3545';
            valid = false;
        } else {
            input.style.borderColor = '#e0e0e0';
        }
    });
    
    return valid;
}

// Add event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Auto-focus first input in forms
    const firstInput = document.querySelector('input[type="text"]');
    if (firstInput) {
        firstInput.focus();
    }
    
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Number input validation (0-100)
    const scoreInputs = document.querySelectorAll('input[type="number"]');
    scoreInputs.forEach(input => {
        input.addEventListener('input', function() {
            let value = parseInt(this.value);
            if (value < 0) this.value = 0;
            if (value > 100) this.value = 100;
        });
    });
});

// Utility function to format numbers
function formatNumber(num, decimals = 2) {
    return Number(num).toFixed(decimals);
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.textContent = message;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.minWidth = '300px';
    notification.style.animation = 'slideIn 0.3s ease';
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Speech Recognition for Command Input
let recognition = null;
let isListening = false;

function initSpeechRecognition() {
    // Check if browser supports Web Speech API
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        console.warn('Speech recognition not supported in this browser');
        return null;
    }
    
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-US';
    
    return recognition;
}

function startSpeechRecognition() {
    const commandTextarea = document.getElementById('command');
    const micBtn = document.getElementById('mic-btn');
    const statusDiv = document.getElementById('speech-status');
    
    if (!commandTextarea || !micBtn) return;
    
    if (!recognition) {
        recognition = initSpeechRecognition();
        if (!recognition) {
            statusDiv.textContent = '❌ Speech recognition not supported in your browser';
            statusDiv.className = 'speech-status error';
            setTimeout(() => statusDiv.textContent = '', 3000);
            return;
        }
    }
    
    if (isListening) {
        recognition.stop();
        return;
    }
    
    // Start listening
    try {
        recognition.start();
        isListening = true;
        micBtn.classList.add('listening');
        statusDiv.textContent = '🎤 Listening...';
        statusDiv.className = 'speech-status listening';
        
        recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }
            
            // Show interim results
            if (interimTranscript) {
                statusDiv.textContent = `📝 ${interimTranscript}`;
            }
            
            // Set final transcript to textarea
            if (finalTranscript) {
                commandTextarea.value = finalTranscript.trim();
                statusDiv.textContent = '✅ Transcription complete';
                statusDiv.className = 'speech-status success';
                setTimeout(() => statusDiv.textContent = '', 2000);
            }
        };
        
        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            isListening = false;
            micBtn.classList.remove('listening');
            
            let errorMessage = '❌ ';
            switch(event.error) {
                case 'no-speech':
                    errorMessage += 'No speech detected. Please try again.';
                    break;
                case 'audio-capture':
                    errorMessage += 'Microphone not found or not allowed.';
                    break;
                case 'not-allowed':
                    errorMessage += 'Microphone access denied. Please allow microphone access.';
                    break;
                default:
                    errorMessage += `Error: ${event.error}`;
            }
            
            statusDiv.textContent = errorMessage;
            statusDiv.className = 'speech-status error';
            setTimeout(() => statusDiv.textContent = '', 4000);
        };
        
        recognition.onend = () => {
            isListening = false;
            micBtn.classList.remove('listening');
            if (statusDiv.textContent === '🎤 Listening...') {
                statusDiv.textContent = '';
            }
        };
        
    } catch (error) {
        console.error('Error starting speech recognition:', error);
        statusDiv.textContent = '❌ Could not start speech recognition';
        statusDiv.className = 'speech-status error';
        setTimeout(() => statusDiv.textContent = '', 3000);
    }
}

// Initialize speech recognition when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        const micBtn = document.getElementById('mic-btn');
        if (micBtn) {
            micBtn.addEventListener('click', startSpeechRecognition);
        }
    });
} else {
    const micBtn = document.getElementById('mic-btn');
    if (micBtn) {
        micBtn.addEventListener('click', startSpeechRecognition);
    }
}
