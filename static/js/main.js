// Main JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // Enable tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Enable popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    });

    // Auto-dismiss alerts after 5 seconds
    var alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Form validation enhancement
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Dynamic filter form submission
    var filterForms = document.querySelectorAll('.filter-form');
    filterForms.forEach(function(form) {
        var selects = form.querySelectorAll('select');
        selects.forEach(function(select) {
            select.addEventListener('change', function() {
                form.submit();
            });
        });

        var inputs = form.querySelectorAll('input[type="text"], input[type="search"]');
        inputs.forEach(function(input) {
            input.addEventListener('keyup', debounce(function() {
                form.submit();
            }, 500));
        });
    });

    // Debounce function for search inputs
    function debounce(func, wait, immediate) {
        var timeout;
        return function() {
            var context = this, args = arguments;
            var later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            var callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    }

    // Toggle advanced filters
    var advancedFilterToggles = document.querySelectorAll('.toggle-advanced-filters');
    advancedFilterToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            var target = document.querySelector(this.getAttribute('data-target'));
            target.classList.toggle('d-none');
            this.querySelector('i').classList.toggle('bi-chevron-down');
            this.querySelector('i').classList.toggle('bi-chevron-up');
        });
    });
});