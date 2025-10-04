// Edu-Ride Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Add loading states to forms
    var forms = document.querySelectorAll('form');
    if (forms) {
        forms.forEach(function(form) {
            form.addEventListener('submit', function() {
                var submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.innerHTML = '<span class="loading"></span> Processing...';
                    submitBtn.disabled = true;
                }
            });
        });
    }
});

// Utility Functions
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container-fluid') || document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    }
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

// API Functions
async function fetchRides() {
    try {
        const response = await fetch('/api/rides');
        if (!response.ok) throw new Error('Failed to fetch rides');
        return await response.json();
    } catch (error) {
        console.error('Error fetching rides:', error);
        showNotification('Failed to load rides. Please refresh the page.', 'danger');
        return [];
    }
}

async function bookRide(rideId) {
    try {
        const response = await fetch('/api/book_ride', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ride_id: rideId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Ride booked successfully!', 'success');
            // Refresh the page or update the UI
            setTimeout(() => location.reload(), 1000);
        } else {
            showNotification(data.error || 'Failed to book ride', 'danger');
        }
    } catch (error) {
        console.error('Error booking ride:', error);
        showNotification('An error occurred while booking the ride', 'danger');
    }
}

async function startRide(rideId) {
    try {
        const response = await fetch('/api/start_ride', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ride_id: rideId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Ride started successfully!', 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            showNotification(data.error || 'Failed to start ride', 'danger');
        }
    } catch (error) {
        console.error('Error starting ride:', error);
        showNotification('An error occurred while starting the ride', 'danger');
    }
}

async function completeRide(rideId) {
    try {
        const response = await fetch('/api/complete_ride', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ride_id: rideId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Ride completed successfully!', 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            showNotification(data.error || 'Failed to complete ride', 'danger');
        }
    } catch (error) {
        console.error('Error completing ride:', error);
        showNotification('An error occurred while completing the ride', 'danger');
    }
}

// Real-time Updates
function startRealTimeUpdates() {
    // Update rides every 30 seconds
    setInterval(async () => {
        try {
            const rides = await fetchRides();
            updateRidesDisplay(rides);
        } catch (error) {
            console.error('Error updating rides:', error);
        }
    }, 30000);
}

function updateRidesDisplay(rides) {
    const container = document.getElementById('rides-container');
    if (!container) return;

    if (rides.length === 0) {
        container.innerHTML = `
            <div class="col-12">
                <div class="text-center py-4">
                    <i class="fas fa-search text-muted display-4 mb-3"></i>
                    <h5 class="text-muted">No rides available at the moment</h5>
                    <p class="text-muted">Check back later for new ride offers</p>
                </div>
            </div>
        `;
    } else {
        container.innerHTML = rides.map(ride => `
            <div class="col-md-6 mb-3">
                <div class="card border ride-card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <h6 class="card-title mb-0">${ride.pickup_location} → ${ride.dropoff_location}</h6>
                            <span class="badge bg-primary">${formatCurrency(ride.fare)}</span>
                        </div>
                        <p class="card-text text-muted small mb-2">
                            <i class="fas fa-clock me-1"></i>${formatDateTime(ride.pickup_time)}
                        </p>
                        <p class="card-text text-muted small mb-2">
                            <i class="fas fa-user me-1"></i>Driver: ${ride.driver_name}
                        </p>
                        ${ride.is_group_ride ? `
                        <p class="card-text text-muted small mb-3">
                            <i class="fas fa-users me-1"></i>Group Ride: ${ride.current_passengers}/${ride.max_passengers} passengers
                        </p>
                        ` : ''}
                        <button class="btn btn-primary btn-sm" onclick="bookRide(${ride.id})">
                            <i class="fas fa-bookmark me-1"></i>Book Ride
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }
}

// Form Validation
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Add form validation to all forms
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
                showNotification('Please fill in all required fields', 'warning');
            }
        });
    });
});

// Smooth Scrolling
function smoothScrollTo(element) {
    element.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// Add smooth scrolling to anchor links
document.addEventListener('DOMContentLoaded', function() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                smoothScrollTo(target);
            }
        });
    });
});

// Initialize real-time updates on dashboard pages
if (window.location.pathname.includes('dashboard')) {
    document.addEventListener('DOMContentLoaded', function() {
        startRealTimeUpdates();
    });
}
