/**
 * Voice Input Feature for Expense Tracker
 * Uses Web Speech API (Free - No API key required)
 * Features: Dictation, Voice Commands, Real-time transcription
 */

class VoiceInputManager {
    constructor() {
        // Browser speech recognition API
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            console.warn('Speech Recognition not supported in this browser');
            this.supported = false;
            return;
        }
        
        this.recognition = new SpeechRecognition();
        this.supported = true;
        this.isListening = false;
        this.transcript = '';
        this.finalTranscript = '';
        
        // Configuration
        this.recognition.continuous = false;
        this.recognition.interimResults = true;
        this.recognition.language = 'en-US';
        
        // Event listeners
        this.setupEventListeners();
        this.registerCommands();
    }
    
    setupEventListeners() {
        this.recognition.onstart = () => {
            this.isListening = true;
            this.transcript = '';
            this.finalTranscript = '';
            this.updateUI('listening');
            console.log('Voice recognition started');
        };
        
        this.recognition.onresult = (event) => {
            this.transcript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                
                if (event.results[i].isFinal) {
                    this.finalTranscript += transcript + ' ';
                } else {
                    this.transcript += transcript;
                }
            }
            
            // Show interim results
            const interimText = this.finalTranscript + this.transcript;
            this.updateTranscriptDisplay(interimText);
        };
        
        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.updateUI('error', `Error: ${event.error}`);
        };
        
        this.recognition.onend = () => {
            this.isListening = false;
            
            // Process the final transcript
            if (this.finalTranscript) {
                this.processVoiceInput(this.finalTranscript.trim());
            }
            
            this.updateUI('idle');
            console.log('Voice recognition ended');
        };
    }
    
    registerCommands() {
        // Voice commands for quick expense entry
        this.commands = {
            'add': this.handleAddCommand.bind(this),
            'expense': this.handleAddCommand.bind(this),
            'spend': this.handleAddCommand.bind(this),
            'record': this.handleAddCommand.bind(this),
            'clear': this.handleClearCommand.bind(this),
            'cancel': this.handleClearCommand.bind(this),
            'reset': this.handleClearCommand.bind(this),
            'help': this.handleHelpCommand.bind(this),
        };
    }
    
    startListening(targetField = 'description') {
        if (!this.supported) {
            alert('Voice input is not supported in your browser. Please use Chrome, Firefox, or Edge.');
            return;
        }
        
        if (this.isListening) {
            this.stopListening();
            return;
        }
        
        this.targetField = targetField;
        this.recognition.start();
    }
    
    stopListening() {
        if (this.isListening) {
            this.recognition.stop();
        }
    }
    
    processVoiceInput(text) {
        // Try to match voice commands first
        const lowerText = text.toLowerCase();
        
        for (const [command, handler] of Object.entries(this.commands)) {
            if (lowerText.includes(command)) {
                handler(text);
                return;
            }
        }
        
        // If no command matched, try to parse as structured input
        this.parseStructuredInput(text);
    }
    
    /**
     * Parse structured voice input: "amount description [category] [date]"
     * Examples:
     * - "500 coffee"
     * - "1500 grocery food"
     * - "200 taxi transport"
     * - "100 movie entertainment today"
     */
    parseStructuredInput(text) {
        const normalizedText = text
            .replace(/[,.]/g, ' ')
            .replace(/\s+/g, ' ')
            .trim();

        let amount = null;
        let description = normalizedText;

        // Extract a leading amount like "500", "500 PKR", "PKR 500"
        const leadingAmountMatch = normalizedText.match(/^(?:pkr\s*)?(\d+(?:\.\d+)?)\b(?:\s*(?:pkr|rs|rupees?|usd|\$))?/i);
        if (leadingAmountMatch) {
            amount = parseFloat(leadingAmountMatch[1]);
            description = normalizedText.slice(leadingAmountMatch[0].length).trim();
        }

        // If nothing follows the amount, keep the description empty instead of reusing the amount text
        const hasDescription = Boolean(description);
        
        // Fill form fields
        if (amount && amount > 0) {
            const amountField = document.getElementById('amount');
            if (amountField) {
                amountField.value = amount;
                amountField.dispatchEvent(new Event('change'));
            }
        }
        
        if (hasDescription) {
            this.fillField('description-input', description);
            this.triggerPrediction();
        } else {
            this.fillField('description-input', '');
        }

        const categorySource = description || normalizedText;
        const category = this.detectCategory(categorySource);
        if (category) {
            this.fillField('category-input', category);
        }
        
        this.showNotification(`Parsed: Amount ${amount || 'n/a'}${hasDescription ? `, Description: ${description}` : ''}${category ? `, Category: ${category}` : ''}`);
    }

    detectCategory(text) {
        const categoryKeywords = {
            'Food': ['food', 'coffee', 'lunch', 'dinner', 'breakfast', 'restaurant', 'cafe', 'pizza', 'burger', 'snack'],
            'Transport': ['taxi', 'uber', 'bus', 'fuel', 'petrol', 'parking', 'gas', 'train', 'metro', 'car'],
            'Entertainment': ['movie', 'cinema', 'game', 'gaming', 'show', 'concert', 'netflix', 'spotify'],
            'Shopping': ['shopping', 'buy', 'clothes', 'shoes', 'dress', 'shirt', 'pants', 'mall', 'store'],
            'Health': ['doctor', 'medicine', 'pharmacy', 'hospital', 'health', 'medical', 'gym', 'fitness'],
            'Utilities': ['electricity', 'water', 'bill', 'internet', 'phone', 'utility'],
        };

        const lowerText = text.toLowerCase();
        for (const [category, keywords] of Object.entries(categoryKeywords)) {
            if (keywords.some(keyword => lowerText.includes(keyword))) {
                return category;
            }
        }

        return null;
    }
    
    handleAddCommand(text) {
        // User said "add/expense/spend" - extract details
        const withoutCommand = text.replace(/^(add|expense|spend|record)\s+/i, '').trim();
        this.parseStructuredInput(withoutCommand);
    }
    
    handleClearCommand(text) {
        // Clear form fields
        document.getElementById('amount').value = '';
        document.getElementById('description-input').value = '';
        document.getElementById('category-input').value = '';
        this.showNotification('Form cleared');
    }
    
    handleHelpCommand(text) {
        const helpText = `
Voice commands available:
1. "500 coffee" - Amount and description
2. "1500 grocery food" - With category
3. "add 200 taxi" - Explicit add command
4. "clear" or "cancel" - Clear form
5. Say just description - it will be added
        `;
        this.showNotification(helpText);
    }
    
    fillField(fieldId, value) {
        const field = document.getElementById(fieldId);
        if (field) {
            field.value = value;
            field.dispatchEvent(new Event('input', { bubbles: true }));
            field.focus();
        }
    }
    
    triggerPrediction() {
        // Trigger ML category prediction if available
        const descriptionField = document.getElementById('description-input');
        if (descriptionField && typeof predictCategory === 'function') {
            setTimeout(() => {
                predictCategory();
            }, 300);
        }
    }
    
    updateTranscriptDisplay(text) {
        const display = document.getElementById('voice-transcript');
        if (display) {
            display.value = text;
        }
    }
    
    updateUI(state, message = '') {
        const button = document.getElementById('voice-btn');
        const status = document.getElementById('voice-status');
        
        if (!button || !status) return;
        
        switch(state) {
            case 'listening':
                button.classList.remove('btn-outline-primary');
                button.classList.add('btn-danger');
                button.innerHTML = '<i class="fas fa-microphone"></i> Listening...';
                status.textContent = 'Listening...';
                status.style.color = 'red';
                break;
            case 'error':
                button.classList.add('btn-outline-primary');
                button.classList.remove('btn-danger');
                button.innerHTML = '<i class="fas fa-microphone"></i> Error';
                status.textContent = message;
                status.style.color = 'red';
                break;
            case 'idle':
            default:
                button.classList.add('btn-outline-primary');
                button.classList.remove('btn-danger');
                button.innerHTML = '<i class="fas fa-microphone"></i> Voice Input';
                status.textContent = 'Ready';
                status.style.color = 'green';
        }
    }
    
    showNotification(message) {
        // Create bootstrap alert
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-info alert-dismissible fade show';
        alertDiv.setAttribute('role', 'alert');
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container') || document.body;
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => alertDiv.remove(), 5000);
    }
    
    setLanguage(lang) {
        this.recognition.language = lang;
    }
}

// Initialize on page load
let voiceManager = null;

document.addEventListener('DOMContentLoaded', () => {
    voiceManager = new VoiceInputManager();
    
    if (voiceManager.supported) {
        console.log('✓ Voice input feature is active');
    } else {
        console.warn('⚠ Voice input not supported in this browser');
    }
});

/**
 * Global function to toggle voice input
 */
function toggleVoiceInput(fieldId = 'description') {
    if (!voiceManager) {
        voiceManager = new VoiceInputManager();
    }
    voiceManager.startListening(fieldId);
}

/**
 * Global function to stop voice input
 */
function stopVoiceInput() {
    if (voiceManager) {
        voiceManager.stopListening();
    }
}
