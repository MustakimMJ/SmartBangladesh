// Smart Bangladesh - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize menu toggles
    initializeMenus();
    initializeModals();
    initializeFormValidation();
});

// Toggle user menu
function initializeMenus() {
    const userMenuBtn = document.querySelector('.user-menu-btn');
    if (userMenuBtn) {
        userMenuBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const dropdown = this.nextElementSibling;
            dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            const userMenu = document.querySelector('.user-menu');
            if (userMenu && !userMenu.contains(e.target)) {
                const dropdown = userMenu.querySelector('.user-dropdown');
                if (dropdown) {
                    dropdown.style.display = 'none';
                }
            }
        });
    }
}

// Initialize modals
function initializeModals() {
    const modals = document.querySelectorAll('.modal');
    
    modals.forEach(modal => {
        const closeBtn = modal.querySelector('.close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                modal.style.display = 'none';
            });
        }
    });

    window.addEventListener('click', function(e) {
        modals.forEach(modal => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    });
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = this.querySelectorAll('input[required], textarea[required]');
            let isValid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('error');
                } else {
                    input.classList.remove('error');
                }
            });

            if (!isValid) {
                e.preventDefault();
                console.log("[v0] Form validation failed");
            }
        });
    });
}

// Open modal function
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
    }
}

// Close modal function
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

// Format date display
function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-BD', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('show');
    }, 100);

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}

// Confirm action
function confirmAction(message) {
    return confirm(message);
}

// Export functions for global use
window.openModal = openModal;
window.closeModal = closeModal;
window.formatDate = formatDate;
window.showToast = showToast;
window.confirmAction = confirmAction;
