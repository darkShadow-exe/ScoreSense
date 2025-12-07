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
